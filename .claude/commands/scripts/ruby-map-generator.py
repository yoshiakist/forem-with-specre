#!/usr/bin/env python3
"""
Ruby Map Generator — extract structural information from Ruby source files.

Produces a JSON summary of classes, modules, methods, callbacks, includes,
response patterns, class references, and authorization calls. Designed to
give an LLM enough context for specre card generation without reading the
full source.

Usage:
  # Single file
  python3 ruby-map-generator.py app/controllers/users_controller.rb

  # Multiple files
  python3 ruby-map-generator.py app/controllers/users_controller.rb app/controllers/articles_controller.rb

  # Directory scan (legacy mode)
  python3 ruby-map-generator.py --dirs app/models app/services app/controllers

  # Output to file
  python3 ruby-map-generator.py --out ruby_logic_map.json app/controllers/users_controller.rb
"""

import os
import re
import sys
import json
import argparse


# --- Regex patterns ---

RE_CLASS = re.compile(
    r'^\s*(class|module)\s+([\w:]+)(?:\s*<\s*([\w:]+))?'
)
RE_INCLUDE = re.compile(
    r'^\s*(?:include|extend|prepend)\s+([\w:]+)'
)
RE_CALLBACK = re.compile(
    r'^\s*(before_action|after_action|around_action|before_filter|after_filter|around_filter'
    r'|before_validation|after_validation|before_save|after_save|before_create|after_create'
    r'|before_update|after_update|before_destroy|after_destroy'
    r'|after_commit|after_rollback'
    r'|skip_before_action|skip_after_action'
    r'|rescue_from'
    r')\s+(.*)',
    re.DOTALL,
)
RE_DEF = re.compile(r'^\s*def\s+(self\.)?([\w!?=]+)(?:\((.*?)\))?')
RE_VISIBILITY = re.compile(r'^\s*(private|protected|public)\s*$')
RE_RETURN = re.compile(r'^\s*return\b\s*(.*)')
RE_YIELD = re.compile(r'^\s*yield\b\s*(.*)')

# Response patterns (controller-specific)
RE_RENDER = re.compile(r'\brender\b[\s(]+(.+)')
RE_REDIRECT = re.compile(r'\bredirect_to\b[\s(]+(.+)')
RE_RESPOND_TO = re.compile(r'\brespond_to\b')
RE_HEAD = re.compile(r'\bhead\b[\s(]+(.+)')

# Authorization patterns
RE_AUTHORIZE = re.compile(r'\b(authorize|skip_authorization|pundit_authorize)\b')

# Class reference patterns (ClassName.method or ClassName::Const)
RE_CLASS_REF = re.compile(r'\b([A-Z][A-Za-z0-9]*(?:::[A-Z][A-Za-z0-9]*)*)\.([\w!?]+)')

# Association macros (model-specific)
RE_ASSOCIATION = re.compile(
    r'^\s*(belongs_to|has_many|has_one|has_and_belongs_to_many)\s+:(\w+)'
)
# Validation macros
RE_VALIDATION = re.compile(
    r'^\s*(validates?|validates_\w+)\s+(.*)'
)
# Scope
RE_SCOPE = re.compile(
    r'^\s*scope\s+:(\w+)'
)
# Delegate
RE_DELEGATE = re.compile(
    r'^\s*delegate\s+(.*?),\s*to:\s*(.+)'
)
# attr_accessor etc
RE_ATTR = re.compile(
    r'^\s*(attr_accessor|attr_reader|attr_writer)\s+(.*)'
)

# Keywords that open an end-requiring block when at statement position
BLOCK_OPENING_KEYWORDS = {
    'def', 'class', 'module', 'if', 'unless', 'case',
    'while', 'until', 'for', 'begin',
}
# 'do' is special — handled separately


class RubyMapGenerator:
    def __init__(self, root_dir='.'):
        self.root_dir = root_dir

    @staticmethod
    def _strip_strings_and_comments(code):
        """Remove string literals and comments to avoid false keyword matches."""
        # Remove single-line comments
        code = re.sub(r'#.*$', '', code)
        # Remove double-quoted strings (non-greedy)
        code = re.sub(r'"(?:[^"\\]|\\.)*"', '""', code)
        # Remove single-quoted strings (non-greedy)
        code = re.sub(r"'(?:[^'\\]|\\.)*'", "''", code)
        # Remove regex literals
        code = re.sub(r'/(?:[^/\\]|\\.)*/', '//', code)
        return code

    @staticmethod
    def _tokenize_statements(line):
        """Split a line into semicolon-separated statements."""
        clean = RubyMapGenerator._strip_strings_and_comments(line)
        # Split by semicolons
        parts = clean.split(';')
        return [p.strip() for p in parts if p.strip()]

    @staticmethod
    def _count_depth_change(line):
        """Estimate net depth change for a line of Ruby code.

        Uses statement-level tokenization to handle `def foo; end` correctly.
        Handles assignment-if (`x = if cond`) as a block opener.
        """
        statements = RubyMapGenerator._tokenize_statements(line)
        delta = 0

        for stmt in statements:
            words = re.findall(r'\b\w+\b', stmt)
            if not words:
                continue

            first_word = words[0]

            # Block-opening keywords at statement position (first word)
            if first_word in BLOCK_OPENING_KEYWORDS:
                delta += 1
            else:
                # Check for assignment-position block openers: `x = if ...`, `x = case ...`
                # These are block openers even though they're not the first word.
                assign_block = re.search(
                    r'=\s*\b(if|unless|case|begin|while|until)\b', stmt
                )
                if assign_block:
                    delta += 1

            # 'do' keyword (block opener)
            if 'do' in words:
                if re.search(r'\bdo\b(?:\s*\||\s*$)', stmt):
                    delta += 1

            # 'end' keyword — can appear anywhere in the statement
            # Count all standalone 'end' tokens
            for end_match in re.finditer(r'\bend\b', stmt):
                # Verify it's standalone (not part of send, __END__, .end, etc.)
                pos = end_match.start()
                # Check character before
                if pos > 0 and (stmt[pos - 1].isalnum() or stmt[pos - 1] in ('_', '.')):
                    continue
                # Check character after
                end_pos = end_match.end()
                if end_pos < len(stmt) and (stmt[end_pos].isalnum() or stmt[end_pos] == '_'):
                    continue
                delta -= 1

        return delta

    # Classes to skip when detecting class references
    SKIP_CLASSES = frozenset({
        'I18n', 'Rails', 'ENV', 'URI', 'JSON', 'File',
        'Time', 'Date', 'DateTime', 'String', 'Integer',
        'Float', 'Array', 'Hash', 'Set', 'Regexp',
        'ActiveRecord', 'ActionController', 'ActiveSupport',
        'Kernel', 'Object', 'BasicObject', 'Module', 'Class',
    })

    def _extract_line_info(self, stripped, lineno, method_info):
        """Extract return/response/auth/class_ref info from a single line."""
        # Return / yield
        ret_match = RE_RETURN.search(stripped)
        if ret_match:
            val = ret_match.group(1).strip()
            if val:
                method_info["returns"].append(f"L{lineno}: return {val}")
            else:
                method_info["returns"].append(f"L{lineno}: return")

        # Response patterns
        resp = self._extract_response_info(stripped)
        if resp:
            method_info["responses"].append(f"L{lineno}: {resp}")

        # Authorization
        auth_match = RE_AUTHORIZE.search(stripped)
        if auth_match:
            method_info["auth"].append(f"L{lineno}: {stripped}")

        # Class references (dependencies)
        for ref_match in RE_CLASS_REF.finditer(stripped):
            cls = ref_match.group(1)
            method = ref_match.group(2)
            if cls not in self.SKIP_CLASSES:
                ref_str = f"{cls}.{method}"
                if ref_str not in method_info["class_refs"]:
                    method_info["class_refs"].append(ref_str)

    @staticmethod
    def _cleanup_method(method_info):
        """Remove empty optional lists from method info."""
        for key in ("responses", "returns", "class_refs", "auth"):
            if not method_info.get(key):
                method_info.pop(key, None)

    def _extract_response_info(self, stripped):
        """Extract response pattern from a stripped line."""
        m = RE_RENDER.search(stripped)
        if m:
            return f"render {m.group(1).rstrip(',).').strip()}"
        m = RE_REDIRECT.search(stripped)
        if m:
            return f"redirect_to {m.group(1).rstrip(',).').strip()}"
        m = RE_HEAD.search(stripped)
        if m:
            return f"head {m.group(1).rstrip(',).').strip()}"
        return None

    def extract_essence(self, file_path):
        """Extract structural information from a single Ruby file."""
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()

        result = {
            "classes": [],
        }

        current_class = None
        current_class_info = None
        visibility = "public"
        class_depth = 0
        in_method = False
        method_depth = 0
        current_method = None

        for i, line in enumerate(lines):
            stripped = line.strip()
            lineno = i + 1

            # Skip empty lines and pure comments for structural parsing
            if not stripped or stripped.startswith('#'):
                continue

            # --- Class / Module detection ---
            class_match = RE_CLASS.match(line)
            if class_match:
                kind = class_match.group(1)  # class or module
                name = class_match.group(2)
                parent = class_match.group(3)  # may be None
                current_class = name
                visibility = "public"
                current_class_info = {
                    "kind": kind,
                    "name": name,
                    "line": lineno,
                    "includes": [],
                    "callbacks": [],
                    "associations": [],
                    "validations": [],
                    "scopes": [],
                    "delegates": [],
                    "attrs": [],
                    "methods": [],
                }
                if parent:
                    current_class_info["parent"] = parent
                result["classes"].append(current_class_info)
                continue

            if current_class_info is None:
                continue

            # --- Include / Extend / Prepend ---
            inc_match = RE_INCLUDE.match(line)
            if inc_match:
                current_class_info["includes"].append(inc_match.group(1))
                continue

            # --- Callbacks ---
            cb_match = RE_CALLBACK.match(line)
            if cb_match:
                cb_type = cb_match.group(1)
                cb_detail = cb_match.group(2).strip().rstrip('\\').strip()
                # Handle multi-line callbacks: accumulate continuation lines
                j = i + 1
                while j < len(lines) and lines[j].strip().startswith(('only:', 'except:', 'if:', 'unless:')):
                    cb_detail += ' ' + lines[j].strip()
                    j += 1
                current_class_info["callbacks"].append(f"{cb_type} {cb_detail}")
                continue

            # --- Associations (model) ---
            assoc_match = RE_ASSOCIATION.match(line)
            if assoc_match:
                current_class_info["associations"].append(
                    f"{assoc_match.group(1)} :{assoc_match.group(2)}"
                )
                continue

            # --- Validations (model) ---
            val_match = RE_VALIDATION.match(line)
            if val_match:
                val_text = f"{val_match.group(1)} {val_match.group(2).strip()}"
                # Truncate long validation lines
                if len(val_text) > 120:
                    val_text = val_text[:117] + "..."
                current_class_info["validations"].append(val_text)
                continue

            # --- Scopes ---
            scope_match = RE_SCOPE.match(line)
            if scope_match:
                current_class_info["scopes"].append(scope_match.group(1))
                continue

            # --- Delegates ---
            del_match = RE_DELEGATE.match(line)
            if del_match:
                current_class_info["delegates"].append(stripped)
                continue

            # --- Attr accessors ---
            attr_match = RE_ATTR.match(line)
            if attr_match:
                current_class_info["attrs"].append(stripped)
                continue

            # --- Visibility ---
            vis_match = RE_VISIBILITY.match(line)
            if vis_match:
                visibility = vis_match.group(1)
                continue

            # --- Method definition ---
            def_match = RE_DEF.match(line)
            if def_match:
                is_class_method = bool(def_match.group(1))
                method_name = def_match.group(2)
                params = def_match.group(3) or ""
                if is_class_method:
                    method_name = f"self.{method_name}"

                current_method = {
                    "name": method_name,
                    "line": lineno,
                    "visibility": visibility,
                    "responses": [],
                    "returns": [],
                    "class_refs": [],
                    "auth": [],
                }
                if params:
                    current_method["params"] = params

                current_class_info["methods"].append(current_method)

                # Check for single-line method: `def foo; bar; end`
                # Net depth of the def line itself should be 0 (def +1, end -1)
                def_line_depth = self._count_depth_change(stripped)
                if def_line_depth == 0:
                    # Single-line method — no body to scan
                    # Still extract info from the line itself
                    self._extract_line_info(stripped, lineno, current_method)
                    self._cleanup_method(current_method)
                    current_method = None
                    continue

                # Multi-line method — scan body
                method_depth = def_line_depth  # normally 1
                j = i + 1
                while j < len(lines) and method_depth > 0:
                    mline = lines[j]
                    mstripped = mline.strip()
                    mlineno = j + 1

                    if mstripped and not mstripped.startswith('#'):
                        # Depth tracking
                        method_depth += self._count_depth_change(mstripped)
                        if method_depth <= 0:
                            break

                        self._extract_line_info(mstripped, mlineno, current_method)

                    j += 1

                # Deduplicate
                current_method["returns"] = list(dict.fromkeys(current_method["returns"]))
                current_method["responses"] = list(dict.fromkeys(current_method["responses"]))

                self._cleanup_method(current_method)
                current_method = None
                continue

        # Clean up empty lists in class info
        for cls_info in result["classes"]:
            for key in ("includes", "callbacks", "associations", "validations",
                        "scopes", "delegates", "attrs"):
                if not cls_info[key]:
                    del cls_info[key]

        return result

    def run_files(self, file_paths):
        """Extract essence from a list of specific file paths."""
        data_map = {}
        for fp in file_paths:
            if fp.endswith('.rb') and os.path.isfile(fp):
                rel_p = os.path.relpath(fp, self.root_dir)
                essence = self.extract_essence(fp)
                if essence["classes"]:
                    data_map[rel_p] = essence
        return data_map

    def run_dirs(self, target_dirs):
        """Extract essence from all .rb files in given directories."""
        data_map = {}
        for d in target_dirs:
            full_path = os.path.join(self.root_dir, d)
            if not os.path.exists(full_path):
                continue
            for root, _, files in os.walk(full_path):
                for file in files:
                    if file.endswith('.rb'):
                        p = os.path.join(root, file)
                        rel_p = os.path.relpath(p, self.root_dir)
                        essence = self.extract_essence(p)
                        if essence["classes"]:
                            data_map[rel_p] = essence
        return data_map


def main():
    parser = argparse.ArgumentParser(
        description='Extract structural information from Ruby source files.'
    )
    parser.add_argument(
        'files', nargs='*',
        help='Ruby source file paths to analyze'
    )
    parser.add_argument(
        '--dirs', nargs='*',
        help='Directories to scan recursively for .rb files'
    )
    parser.add_argument(
        '--out', '-o',
        help='Output file path (default: stdout)'
    )
    parser.add_argument(
        '--root', default='.',
        help='Project root directory (default: current directory)'
    )
    parser.add_argument(
        '--pretty', action='store_true',
        help='Pretty-print JSON with indentation (default: compact for LLM consumption)'
    )

    args = parser.parse_args()

    generator = RubyMapGenerator(args.root)

    if args.files:
        mapping = generator.run_files(args.files)
    elif args.dirs:
        mapping = generator.run_dirs(args.dirs)
    else:
        # Default: scan common Rails directories
        mapping = generator.run_dirs([
            'app/models', 'app/services', 'app/controllers'
        ])

    if args.pretty:
        output = json.dumps(mapping, indent=2, ensure_ascii=False)
    else:
        output = json.dumps(mapping, separators=(',', ':'), ensure_ascii=False)

    if args.out:
        with open(args.out, 'w') as f:
            f.write(output)
        print(f"Map generated: {args.out}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
