#!/usr/bin/env python3
"""
JS/JSX Map Generator — extract structural information from JavaScript source files.

Produces a JSON summary of imports, exports, functions, classes, hooks, PropTypes,
and Stimulus controller metadata. Designed to give an LLM enough context for
specre card generation without reading the full source.

Usage:
  # Single file
  python3 js-map-generator.py app/javascript/crayons/Button/Button.jsx

  # Multiple files
  python3 js-map-generator.py app/javascript/article-form/articleForm.jsx app/javascript/crayons/Button/Button.jsx

  # Directory scan
  python3 js-map-generator.py --dirs app/javascript/crayons app/javascript/article-form

  # Output to file
  python3 js-map-generator.py --out js_map.json --dirs app/javascript/admin
"""

import os
import re
import sys
import json
import argparse


# --- Regex patterns ---

# Import statements
RE_IMPORT_FROM = re.compile(
    r'''^\s*import\s+(.+?)\s+from\s+['"](.+?)['"]'''
)
RE_IMPORT_SIDE_EFFECT = re.compile(
    r'''^\s*import\s+['"](.+?)['"]'''
)

# Export braces
RE_EXPORT_BRACES = re.compile(r'^\s*export\s*\{')
RE_EXPORT_DEFAULT_EXPR = re.compile(r'^\s*export\s+default\s+(\w+)')

# Class declarations
RE_CLASS_DECL = re.compile(
    r'^\s*(?:export\s+(?:default\s+)?)?class\s+(\w+)(?:\s+extends\s+([\w.]+))?'
)

# Function declaration (may have multi-line params — match name only)
RE_FUNC_START = re.compile(
    r'^(\s*)(?:export\s+(?:default\s+)?)?(?:async\s+)?function\s+(\w+)\s*\('
)

# Arrow / function expression (may have multi-line params — match name only)
RE_ARROW_START = re.compile(
    r'^(\s*)(?:export\s+(?:default\s+)?)?(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s+)?\(?'
)

# Class method (match against original indented line)
RE_METHOD = re.compile(
    r'^\s+(?:static\s+)?(?:async\s+)?(?:get\s+|set\s+)?(\w+)\s*\([^)]*\)\s*\{'
)
# Keywords that look like methods but aren't
METHOD_KEYWORD_BLACKLIST = {
    'if', 'else', 'for', 'while', 'switch', 'catch', 'return',
    'throw', 'new', 'delete', 'typeof', 'void', 'yield', 'await',
    'import', 'export', 'from', 'class', 'extends', 'super', 'this',
}
# Static property (match against original indented line)
RE_STATIC_PROP = re.compile(r'^\s+static\s+(\w+)\s*=')

# Hooks (Preact/React)
RE_HOOK = re.compile(r'\b(use[A-Z]\w+)\s*\(')

# PropTypes definition
RE_PROPTYPES_STATIC = re.compile(r'^\s+static\s+propTypes\s*=')
RE_PROPTYPES_EXTERNAL = re.compile(r'^(\w+)\.propTypes\s*=')

# Stimulus static members
RE_STIMULUS_STATIC = re.compile(
    r'^\s+static\s+(targets|values|classes|outlets)\s*='
)

# JSX component usage
RE_JSX_COMPONENT = re.compile(r'<([A-Z]\w+)[\s/>]')

# Constants (SCREAMING_CASE)
RE_CONST_DECL = re.compile(
    r'^\s*(?:export\s+)?(?:const|let|var)\s+([A-Z_][A-Z0-9_]+)\s*='
)


class JSMapGenerator:
    def __init__(self, root_dir='.'):
        self.root_dir = root_dir

    @staticmethod
    def _strip_strings_and_comments(code):
        """Remove string literals and comments to avoid false matches."""
        code = re.sub(r'(?<![:\w])//.*$', '', code)
        code = re.sub(r'`(?:[^`\\]|\\.)*`', '``', code)
        code = re.sub(r'"(?:[^"\\]|\\.)*"', '""', code)
        code = re.sub(r"'(?:[^'\\]|\\.)*'", "''", code)
        return code

    @staticmethod
    def _count_braces(line):
        """Count net brace depth change for a line."""
        clean = JSMapGenerator._strip_strings_and_comments(line)
        return clean.count('{') - clean.count('}')

    @staticmethod
    def _get_indent(line):
        """Get the indentation level (number of leading spaces)."""
        return len(line) - len(line.lstrip())

    def _collect_params(self, lines, start_idx):
        """Collect function parameters that may span multiple lines.

        Returns (params_string, end_line_idx).
        """
        line = lines[start_idx]
        paren_start = line.index('(')
        text = line[paren_start:]

        depth = text.count('(') - text.count(')')
        j = start_idx

        while depth > 0 and j < len(lines) - 1:
            j += 1
            text += ' ' + lines[j].strip()
            depth += lines[j].count('(') - lines[j].count(')')

        # Extract content between outermost parens
        m = re.search(r'\((.+?)\)', text, re.DOTALL)
        if m:
            params = m.group(1).strip()
            # Simplify destructured params: { a, b, c } → {a, b, c}
            params = re.sub(r'\s+', ' ', params)
            if len(params) > 80:
                params = params[:77] + '...'
            return params, j
        return None, j

    def _skip_block(self, lines, start_idx):
        """Skip past a brace-delimited block. Returns the line after closing brace."""
        depth = self._count_braces(lines[start_idx])
        j = start_idx + 1
        while j < len(lines) and depth > 0:
            depth += self._count_braces(lines[j])
            j += 1
        return j

    def extract_essence(self, file_path):
        """Extract structural information from a single JS/JSX file."""
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()

        result = {
            "imports": [],
            "exports": [],
            "functions": [],
            "classes": [],
            "constants": [],
        }

        i = 0
        in_multiline_import = False
        import_buffer = ""
        # Track brace depth to distinguish top-level vs nested declarations
        top_depth = 0

        while i < len(lines):
            line = lines[i]
            stripped = line.strip()
            lineno = i + 1

            # Skip empty lines and comments
            if not stripped or stripped.startswith('//') or stripped.startswith('/*') or stripped.startswith('*'):
                i += 1
                continue

            # --- Multi-line import handling ---
            if in_multiline_import:
                import_buffer += ' ' + stripped
                if "'" in stripped or '"' in stripped:
                    m = RE_IMPORT_FROM.match(import_buffer)
                    if m:
                        result["imports"].append({
                            "specifiers": m.group(1).strip(),
                            "source": m.group(2),
                        })
                    in_multiline_import = False
                    import_buffer = ""
                i += 1
                continue

            # --- Import statements ---
            if stripped.startswith('import ') and top_depth == 0:
                m = RE_IMPORT_FROM.match(stripped)
                if m:
                    result["imports"].append({
                        "specifiers": m.group(1).strip(),
                        "source": m.group(2),
                    })
                    i += 1
                    continue
                m = RE_IMPORT_SIDE_EFFECT.match(stripped)
                if m:
                    result["imports"].append({
                        "source": m.group(1),
                        "side_effect": True,
                    })
                    i += 1
                    continue
                if 'from' not in stripped:
                    in_multiline_import = True
                    import_buffer = stripped
                    i += 1
                    continue

            # --- Class declarations (top-level only) ---
            m = RE_CLASS_DECL.match(stripped)
            if m and top_depth == 0:
                class_info = self._parse_class(lines, i, m)
                result["classes"].append(class_info)

                if 'export' in stripped:
                    exp = {"name": class_info["name"], "kind": "class"}
                    if 'default' in stripped:
                        exp["default"] = True
                    result["exports"].append(exp)

                # Skip past the class body
                i = self._skip_block(lines, i)
                continue

            # --- Function declarations (top-level only) ---
            m = RE_FUNC_START.match(line)
            if m and top_depth == 0:
                indent_level = len(m.group(1))
                func_name = m.group(2)
                is_async = 'async ' in stripped
                is_export = 'export ' in stripped
                is_default = 'default ' in stripped

                params, params_end = self._collect_params(lines, i)

                func_info = {
                    "name": func_name,
                    "line": lineno,
                }
                if params:
                    func_info["params"] = params
                if is_async:
                    func_info["async"] = True

                # Scan body for hooks and JSX
                self._scan_function_body(lines, i, func_info)
                result["functions"].append(func_info)

                if is_export:
                    exp = {"name": func_name, "kind": "function"}
                    if is_default:
                        exp["default"] = True
                    result["exports"].append(exp)

                # Skip past the function body
                i = self._skip_block(lines, i)
                continue

            # --- Arrow functions / function expressions (top-level only) ---
            m = RE_ARROW_START.match(line)
            if m and top_depth == 0:
                func_name = m.group(2)
                # Verify it's actually a function (has => or function keyword)
                rest_of_line = stripped[stripped.index(func_name) + len(func_name):]
                if '=>' in rest_of_line or 'function' in rest_of_line or '(' in rest_of_line:
                    is_async = 'async ' in stripped
                    is_export = 'export ' in stripped
                    is_default = 'default ' in stripped
                    is_arrow = '=>' in stripped or (i + 1 < len(lines) and '=>' in lines[i + 1])

                    params = None
                    if '(' in rest_of_line:
                        try:
                            params, _ = self._collect_params(lines, i)
                        except ValueError:
                            pass

                    func_info = {
                        "name": func_name,
                        "line": lineno,
                    }
                    if is_arrow:
                        func_info["kind"] = "arrow"
                    if params:
                        func_info["params"] = params
                    if is_async:
                        func_info["async"] = True

                    self._scan_function_body(lines, i, func_info)
                    result["functions"].append(func_info)

                    if is_export:
                        exp = {"name": func_name, "kind": "function"}
                        if is_default:
                            exp["default"] = True
                        result["exports"].append(exp)

                    # Skip past the function body
                    i = self._skip_block(lines, i)
                    continue

            # --- Top-level constants (SCREAMING_CASE) ---
            m = RE_CONST_DECL.match(stripped)
            if m and top_depth == 0:
                result["constants"].append({"name": m.group(1), "line": lineno})
                if 'export ' in stripped:
                    name = m.group(1)
                    if not any(e.get("name") == name for e in result["exports"]):
                        result["exports"].append({"name": name, "kind": "const"})
                # Skip past any block assignment
                brace_change = self._count_braces(stripped)
                if brace_change > 0:
                    i = self._skip_block(lines, i)
                    continue
                i += 1
                continue

            # --- External PropTypes assignment ---
            m = RE_PROPTYPES_EXTERNAL.match(stripped)
            if m and top_depth == 0:
                comp_name = m.group(1)
                props = self._parse_proptypes_block(lines, i)
                for fn in result["functions"]:
                    if fn["name"] == comp_name:
                        fn["propTypes"] = props
                        break
                else:
                    for cls in result["classes"]:
                        if cls["name"] == comp_name:
                            cls["propTypes"] = props
                            break
                i = self._skip_block(lines, i)
                continue

            # --- defaultProps assignment ---
            dp_match = re.match(r'^(\w+)\.defaultProps\s*=', stripped)
            if dp_match and top_depth == 0:
                comp_name = dp_match.group(1)
                defaults = self._parse_simple_keys_block(lines, i)
                for fn in result["functions"]:
                    if fn["name"] == comp_name:
                        fn["defaultProps"] = defaults
                        break
                else:
                    for cls in result["classes"]:
                        if cls["name"] == comp_name:
                            cls["defaultProps"] = defaults
                            break
                i = self._skip_block(lines, i)
                continue

            # --- Export { ... } ---
            if RE_EXPORT_BRACES.match(stripped) and top_depth == 0:
                export_text = stripped
                j = i
                while '}' not in export_text and j < len(lines) - 1:
                    j += 1
                    export_text += ' ' + lines[j].strip()
                inner = export_text.split('{')[1].split('}')[0]
                names = re.findall(r'\b(\w+)\b', inner)
                for name in names:
                    if name not in ('as', 'default'):
                        result["exports"].append({"name": name, "kind": "named"})
                i = j + 1
                continue

            # --- export default expression ---
            m = RE_EXPORT_DEFAULT_EXPR.match(stripped)
            if m and m.group(1) not in ('function', 'class', 'async') and top_depth == 0:
                result["exports"].append({"name": m.group(1), "kind": "default", "default": True})
                i += 1
                continue

            # Track top-level brace depth for other lines
            top_depth += self._count_braces(stripped)
            if top_depth < 0:
                top_depth = 0
            i += 1

        # Clean up empty lists
        for key in list(result.keys()):
            if not result[key]:
                del result[key]

        return result

    def _parse_class(self, lines, start_idx, class_match):
        """Parse a class declaration and its body."""
        stripped = lines[start_idx].strip()
        lineno = start_idx + 1
        class_info = {
            "name": class_match.group(1),
            "line": lineno,
            "methods": [],
        }
        if class_match.group(2):
            class_info["extends"] = class_match.group(2)

        depth = self._count_braces(stripped)
        if depth <= 0:
            return class_info

        j = start_idx + 1
        while j < len(lines) and depth > 0:
            raw_line = lines[j]       # original line (with indentation)
            mline = raw_line.strip()  # stripped for content checks
            mlineno = j + 1

            if not mline or mline.startswith('//') or mline.startswith('*'):
                j += 1
                continue

            # Only parse class-level members (depth == 1)
            if depth == 1:
                # Static propTypes
                if RE_PROPTYPES_STATIC.match(raw_line):
                    class_info["propTypes"] = self._parse_proptypes_block(lines, j)

                # Stimulus static members
                stim_match = RE_STIMULUS_STATIC.match(raw_line)
                if stim_match:
                    member_name = stim_match.group(1)
                    values = self._parse_static_member(lines, j)
                    if "stimulus" not in class_info:
                        class_info["stimulus"] = {}
                    class_info["stimulus"][member_name] = values

                # Static properties (non-special)
                static_match = RE_STATIC_PROP.match(raw_line)
                if static_match and not RE_STIMULUS_STATIC.match(raw_line) and not RE_PROPTYPES_STATIC.match(raw_line):
                    prop_name = static_match.group(1)
                    if prop_name not in ('propTypes', 'defaultProps'):
                        if "static_props" not in class_info:
                            class_info["static_props"] = []
                        class_info["static_props"].append(prop_name)

                # Methods (use raw_line for indentation-aware matching)
                method_match = RE_METHOD.match(raw_line)
                if method_match:
                    method_name = method_match.group(1)
                    if method_name in METHOD_KEYWORD_BLACKLIST:
                        pass  # skip keywords
                    elif method_name == 'constructor':
                        ctor_match = re.search(r'constructor\s*\(([^)]*)\)', mline)
                        if ctor_match and ctor_match.group(1).strip():
                            class_info["constructor_params"] = ctor_match.group(1).strip()
                    else:
                        method_info = {"name": method_name, "line": mlineno}
                        if 'static ' in mline:
                            method_info["static"] = True
                        if 'async ' in mline:
                            method_info["async"] = True
                        class_info["methods"].append(method_info)

            depth += self._count_braces(mline)
            j += 1

        if not class_info["methods"]:
            del class_info["methods"]

        return class_info

    def _scan_function_body(self, lines, start_idx, func_info):
        """Scan a function body for hooks and JSX usage."""
        stripped = lines[start_idx].strip()
        depth = self._count_braces(stripped)

        if depth <= 0:
            return

        j = start_idx + 1
        hooks = set()
        jsx_components = set()

        while j < len(lines) and depth > 0:
            mline = lines[j].strip()
            if mline and not mline.startswith('//'):
                for hook_match in RE_HOOK.finditer(mline):
                    hooks.add(hook_match.group(1))
                for jsx_match in RE_JSX_COMPONENT.finditer(mline):
                    comp = jsx_match.group(1)
                    if comp not in ('React', 'Fragment', 'Suspense', 'Profiler'):
                        jsx_components.add(comp)
                depth += self._count_braces(mline)
            j += 1

        if hooks:
            func_info["hooks"] = sorted(hooks)
        if jsx_components:
            func_info["jsx_components"] = sorted(jsx_components)

    def _parse_proptypes_block(self, lines, start_idx):
        """Parse a PropTypes definition block and extract prop names with types."""
        props = []
        depth = 0
        j = start_idx

        # Find the opening brace
        while j < len(lines):
            depth += self._count_braces(lines[j])
            if depth > 0:
                break
            j += 1

        inner_depth = depth
        j += 1

        while j < len(lines) and inner_depth > 0:
            line = lines[j].strip()
            brace_change = self._count_braces(line)

            # Only parse top-level props (just inside the outer braces)
            if inner_depth == 1 and ':' in line and not line.startswith('//'):
                m = re.match(r'^(\w+)\s*:\s*(.+)', line)
                if m:
                    prop_name = m.group(1)
                    prop_type = m.group(2).strip().rstrip(',')
                    prop_type = self._simplify_proptype(prop_type)
                    props.append(f"{prop_name}: {prop_type}")

            inner_depth += brace_change
            j += 1

        return props

    def _parse_simple_keys_block(self, lines, start_idx):
        """Parse a block and extract top-level key names (for defaultProps etc.)."""
        keys = []
        depth = 0
        j = start_idx

        while j < len(lines):
            depth += self._count_braces(lines[j])
            if depth > 0:
                break
            j += 1

        inner_depth = depth
        j += 1

        while j < len(lines) and inner_depth > 0:
            line = lines[j].strip()
            brace_change = self._count_braces(line)

            if inner_depth == 1 and ':' in line and not line.startswith('//'):
                m = re.match(r'^(\w+)\s*:', line)
                if m:
                    keys.append(m.group(1))

            inner_depth += brace_change
            j += 1

        return keys

    @staticmethod
    def _simplify_proptype(type_str):
        """Simplify PropTypes expression to a concise type description."""
        type_str = type_str.replace('PropTypes.', '')
        if len(type_str) > 60:
            type_str = type_str[:57] + '...'
        return type_str

    def _parse_static_member(self, lines, start_idx):
        """Parse a Stimulus static member (targets, values, classes)."""
        line = lines[start_idx].strip()
        members = []

        if '[' in line:
            text = line
            j = start_idx
            while ']' not in text and j < len(lines) - 1:
                j += 1
                text += ' ' + lines[j].strip()
            return re.findall(r"'(\w+)'", text)

        if '{' in line:
            depth = self._count_braces(line)
            j = start_idx + 1
            while j < len(lines) and depth > 0:
                mline = lines[j].strip()
                if ':' in mline and depth == 1:
                    m = re.match(r'(\w+)\s*:\s*(\w+)', mline)
                    if m:
                        members.append(f"{m.group(1)}: {m.group(2)}")
                depth += self._count_braces(mline)
                j += 1
            return members

        return members

    def run_files(self, file_paths):
        """Extract essence from a list of specific file paths."""
        data_map = {}
        for fp in file_paths:
            if fp.endswith(('.js', '.jsx')) and os.path.isfile(fp):
                rel_p = os.path.relpath(fp, self.root_dir)
                essence = self.extract_essence(fp)
                if essence:
                    data_map[rel_p] = essence
        return data_map

    def run_dirs(self, target_dirs):
        """Extract essence from all .js/.jsx files in given directories."""
        data_map = {}
        for d in target_dirs:
            full_path = os.path.join(self.root_dir, d)
            if not os.path.exists(full_path):
                continue
            for root, _, files in os.walk(full_path):
                for file in files:
                    if file.endswith(('.js', '.jsx')):
                        if '/__tests__/' in os.path.join(root, file):
                            continue
                        p = os.path.join(root, file)
                        rel_p = os.path.relpath(p, self.root_dir)
                        essence = self.extract_essence(p)
                        if essence:
                            data_map[rel_p] = essence
        return data_map


def main():
    parser = argparse.ArgumentParser(
        description='Extract structural information from JavaScript/JSX source files.'
    )
    parser.add_argument(
        'files', nargs='*',
        help='JS/JSX source file paths to analyze'
    )
    parser.add_argument(
        '--dirs', nargs='*',
        help='Directories to scan recursively for .js/.jsx files'
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

    generator = JSMapGenerator(args.root)

    if args.files:
        mapping = generator.run_files(args.files)
    elif args.dirs:
        mapping = generator.run_dirs(args.dirs)
    else:
        mapping = generator.run_dirs(['app/javascript'])

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
