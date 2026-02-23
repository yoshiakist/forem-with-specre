#!/usr/bin/env python3
"""
domain-discovery.py — 4-stage domain file discovery for specre-generate.

Discovers ALL source files related to a domain via:
  Stage 1: Convention-based glob (Rails layers + JS modules)
  Stage 2: Reference tracing (Ruby class refs + JS imports + ERB<->JS bridges)
  Stage 3: Transitive expansion (iterate Stage 2 until convergence)
  Stage 4: Already-tagged check (@specre marker annotation)

Usage:
    python3 .claude/commands/scripts/domain-discovery.py <domain> [options]

Examples:
    python3 .claude/commands/scripts/domain-discovery.py article
    python3 .claude/commands/scripts/domain-discovery.py article --json
    python3 .claude/commands/scripts/domain-discovery.py github_repo --max-rounds 1
    python3 .claude/commands/scripts/domain-discovery.py comment --untagged-only
    python3 .claude/commands/scripts/domain-discovery.py comment --json --exclude comments_admin comments_moderation comments_scoring
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
import tomllib
from dataclasses import dataclass, field
from fnmatch import fnmatch
from pathlib import Path


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class DiscoveredFile:
    path: str
    stage: int
    discovery_reason: str
    specre_tags: list[str] = field(default_factory=list)


@dataclass
class DiscoveryResult:
    domain: str
    seed_class_names: list[str] = field(default_factory=list)
    files: dict[str, DiscoveredFile] = field(default_factory=dict)

    def stats(self) -> dict:
        s1 = sum(1 for f in self.files.values() if f.stage == 1)
        s2 = sum(1 for f in self.files.values() if f.stage == 2)
        s3 = sum(1 for f in self.files.values() if f.stage == 3)
        tagged = sum(1 for f in self.files.values() if f.specre_tags)
        return {
            "stage1": s1,
            "stage2": s2,
            "stage3": s3,
            "total": len(self.files),
            "untagged": len(self.files) - tagged,
            "tagged": tagged,
        }


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

class Config:
    @staticmethod
    def load_specre_toml(project_root: str) -> dict:
        config_path = os.path.join(project_root, "specre.toml")
        with open(config_path, "rb") as f:
            data = tomllib.load(f)
        return {
            "specre_dir": data["specre_dir"],
            "source_dirs": data["source_dirs"],
            "ext": data.get("ext", ["rb", "erb", "js", "jsx"]),
        }

    @staticmethod
    def load_jsconfig(project_root: str) -> dict[str, str]:
        config_path = os.path.join(project_root, "jsconfig.json")
        if not os.path.isfile(config_path):
            return {}
        with open(config_path, "r") as f:
            data = json.load(f)
        paths = data.get("compilerOptions", {}).get("paths", {})
        aliases: dict[str, str] = {}
        for alias_pattern, targets in paths.items():
            if targets:
                target = targets[0].lstrip("./")
                aliases[alias_pattern] = target
        return aliases


# ---------------------------------------------------------------------------
# Stage 1: Convention-based glob
# ---------------------------------------------------------------------------

# Regex for Ruby class/module declaration
RE_CLASS_DECL = re.compile(r"^\s*(?:class|module)\s+([A-Z]\w*(?:::[A-Z]\w*)*)", re.MULTILINE)

# Framework/stdlib classes to skip in reference tracing
SKIP_CLASSES = frozenset({
    "I18n", "Rails", "ENV", "URI", "JSON", "File",
    "Time", "Date", "DateTime", "String", "Integer",
    "Float", "Array", "Hash", "Set", "Regexp",
    "ActiveRecord", "ActionController", "ActiveSupport",
    "Kernel", "Object", "BasicObject", "Module", "Class",
    "ApplicationRecord", "ApplicationController", "ApplicationJob",
    "ApplicationMailer", "ApplicationHelper", "ApplicationPolicy",
    "ApplicationService", "ApplicationWorker",
    "ActionMailer", "ActionView", "ActiveJob", "ActiveModel",
    "ActiveStorage", "ActionCable", "ActionDispatch",
    "Devise", "Pundit", "Sidekiq", "Dry", "Struct",
    "OpenStruct", "Pathname", "Logger", "IO", "Net",
    "CSV", "YAML", "ERB", "Nokogiri", "Faraday",
    "StandardError", "RuntimeError", "ArgumentError",
    "NotImplementedError", "TypeError",
    "Benchmark", "Mutex", "Thread", "Proc", "Lambda",
    "Enumerator", "Range", "Numeric", "Symbol", "NilClass",
    "TrueClass", "FalseClass", "Comparable", "Enumerable",
})


class ConventionDiscovery:
    """Stage 1: Find domain files by Rails/JS naming conventions."""

    RAILS_LAYERS = [
        "models", "controllers", "services", "workers", "views",
        "helpers", "policies", "decorators", "serializers", "queries",
        "validators", "forms", "mailers", "liquid_tags", "view_objects",
        "uploaders", "refinements", "sanitizers", "errors", "lib",
    ]

    def __init__(
        self,
        project_root: str,
        source_dirs: list[str],
        extensions: list[str],
        exclude_keywords: list[str] | None = None,
    ):
        self.project_root = project_root
        self.source_dirs = source_dirs
        self.extensions = set(extensions)
        # Build exclude variants (substring match) from all exclude keywords
        self.exclude_variants: list[str] = []
        # Build exclude part groups (all-parts-present match) for compound keywords
        self.exclude_part_groups: list[list[str]] = []
        for kw in (exclude_keywords or []):
            variants = self._domain_variants(kw)
            self.exclude_variants.extend(variants)
            # Add joined-lowercase variant for CamelCase directory matching
            # e.g., "comment_subscription" → "commentsubscription" matches JS dir "CommentSubscription"
            if "_" in kw:
                joined = kw.replace("_", "").lower()
                if joined not in self.exclude_variants:
                    self.exclude_variants.append(joined)
                # Multi-part matching: split by "_" and check all parts present in path
                # e.g., "comments_admin" → ["comment", "admin"] both must appear in path
                parts = kw.lower().split("_")
                # Normalize: strip trailing 's' for singular matching
                normalized = []
                for p in parts:
                    singular = p.rstrip("s") if p.endswith("s") and len(p) > 2 else p
                    normalized.append(singular)
                self.exclude_part_groups.append(normalized)

    def _is_excluded(self, fname_lower: str, rel_lower: str) -> bool:
        """Return True if the file matches any exclusion pattern.

        Two matching strategies:
        1. Substring match: any exclude variant appears in filename or path
        2. All-parts match: for compound keywords (e.g., "comments_admin"),
           ALL parts must appear somewhere in the full path
        """
        combined = rel_lower + "/" + fname_lower
        # Strategy 1: substring match
        for ev in self.exclude_variants:
            if ev in fname_lower or ev in rel_lower:
                return True
        # Strategy 2: all-parts match (for compound exclude keywords)
        for parts in self.exclude_part_groups:
            if all(p in combined for p in parts):
                return True
        return False

    def discover(self, domain: str) -> tuple[dict[str, DiscoveredFile], list[str]]:
        results: dict[str, DiscoveredFile] = {}
        seed_classes: list[str] = []
        variants = self._domain_variants(domain)

        self._scan_rails_layers(domain, variants, results, seed_classes)
        self._scan_js_modules(domain, variants, results)
        self._scan_spec_dirs(domain, variants, results)

        return results, seed_classes

    def _scan_rails_layers(
        self,
        domain: str,
        variants: list[str],
        results: dict[str, DiscoveredFile],
        seed_classes: list[str],
    ) -> None:
        app_dir = os.path.join(self.project_root, "app")
        if not os.path.isdir(app_dir):
            return

        for layer in self.RAILS_LAYERS:
            layer_dir = os.path.join(app_dir, layer)
            if not os.path.isdir(layer_dir):
                continue

            for root, dirs, files in os.walk(layer_dir):
                # Check if this directory or any ancestor matches a variant
                rel_root = os.path.relpath(root, self.project_root)
                for fname in files:
                    fpath = os.path.join(rel_root, fname)
                    ext = fname.rsplit(".", 1)[-1] if "." in fname else ""
                    if ext not in self.extensions:
                        continue
                    if fpath in results:
                        continue

                    # Match: filename or directory path contains a variant
                    fname_lower = fname.lower()
                    rel_lower = rel_root.lower()

                    # Skip files matching exclusion keywords
                    if self._is_excluded(fname_lower, rel_lower):
                        continue

                    matched_variant = None
                    for v in variants:
                        if v in fname_lower or v in rel_lower:
                            matched_variant = v
                            break

                    if matched_variant is not None:
                        reason = f"convention: {layer}"
                        results[fpath] = DiscoveredFile(
                            path=fpath, stage=1, discovery_reason=reason
                        )
                        # Extract class names from model files
                        if layer == "models" and ext == "rb":
                            classes = self._extract_class_names(
                                os.path.join(self.project_root, fpath)
                            )
                            seed_classes.extend(classes)

    def _scan_js_modules(
        self, domain: str, variants: list[str], results: dict[str, DiscoveredFile]
    ) -> None:
        # Scan all JS directories: app/javascript/ and app/assets/javascripts/
        js_dirs = [
            os.path.join(self.project_root, "app", "javascript"),
            os.path.join(self.project_root, "app", "assets", "javascripts"),
        ]

        for js_dir in js_dirs:
            if not os.path.isdir(js_dir):
                continue
            # Walk the entire tree and match by file name or directory path
            for root, dirs, files in os.walk(js_dir):
                rel_root = os.path.relpath(root, self.project_root)
                for fname in files:
                    fpath = os.path.join(rel_root, fname)
                    ext = fname.rsplit(".", 1)[-1] if "." in fname else ""
                    if ext not in self.extensions:
                        continue
                    if fpath in results:
                        continue
                    fname_lower = fname.lower()
                    rel_lower = rel_root.lower()

                    if self._is_excluded(fname_lower, rel_lower):
                        continue

                    for v in variants:
                        if v in fname_lower or v in rel_lower:
                            results[fpath] = DiscoveredFile(
                                path=fpath, stage=1,
                                discovery_reason="convention: js_module",
                            )
                            break

    def _scan_spec_dirs(
        self, domain: str, variants: list[str], results: dict[str, DiscoveredFile]
    ) -> None:
        spec_dir = os.path.join(self.project_root, "spec")
        if not os.path.isdir(spec_dir):
            return

        for root, dirs, files in os.walk(spec_dir):
            rel_root = os.path.relpath(root, self.project_root)
            for fname in files:
                fpath = os.path.join(rel_root, fname)
                ext = fname.rsplit(".", 1)[-1] if "." in fname else ""
                if ext not in self.extensions:
                    continue
                if fpath in results:
                    continue

                fname_lower = fname.lower()
                rel_lower = rel_root.lower()

                if self._is_excluded(fname_lower, rel_lower):
                    continue

                for v in variants:
                    if v in fname_lower or v in rel_lower:
                        results[fpath] = DiscoveredFile(
                            path=fpath, stage=1, discovery_reason="convention: spec"
                        )
                        break

    def _add_dir_recursive(
        self, dir_path: str, results: dict[str, DiscoveredFile], reason: str
    ) -> None:
        for root, dirs, files in os.walk(dir_path):
            for fname in files:
                fpath = os.path.relpath(os.path.join(root, fname), self.project_root)
                ext = fname.rsplit(".", 1)[-1] if "." in fname else ""
                if ext not in self.extensions:
                    continue
                if fpath not in results:
                    results[fpath] = DiscoveredFile(
                        path=fpath, stage=1, discovery_reason=reason
                    )

    def _scan_matching_files(
        self,
        dir_path: str,
        variants: list[str],
        results: dict[str, DiscoveredFile],
        reason: str,
        recursive: bool = False,
    ) -> None:
        walker = os.walk(dir_path) if recursive else [(dir_path, [], os.listdir(dir_path))]
        for root, dirs, files in walker:
            for fname in files:
                fpath = os.path.relpath(os.path.join(root, fname), self.project_root)
                ext = fname.rsplit(".", 1)[-1] if "." in fname else ""
                if ext not in self.extensions:
                    continue
                if fpath in results:
                    continue
                fname_lower = fname.lower()
                for v in variants:
                    if v in fname_lower:
                        results[fpath] = DiscoveredFile(
                            path=fpath, stage=1, discovery_reason=reason
                        )
                        break

    @staticmethod
    def _extract_class_names(file_path: str) -> list[str]:
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
        except OSError:
            return []
        names = []
        for m in RE_CLASS_DECL.finditer(content):
            name = m.group(1)
            # Take the top-level name (e.g., "Articles::CachedEntity" → keep full,
            # but also add the leaf: "CachedEntity")
            if name not in SKIP_CLASSES:
                names.append(name)
                if "::" in name:
                    leaf = name.rsplit("::", 1)[-1]
                    if leaf not in SKIP_CLASSES:
                        names.append(leaf)
        return names

    @staticmethod
    def _domain_variants(domain: str) -> list[str]:
        singular = domain.rstrip("s") if domain.endswith("s") and len(domain) > 2 else domain
        plural = domain if domain.endswith("s") else domain + "s"
        camel = ConventionDiscovery._snake_to_camel(domain)
        camel_plural = ConventionDiscovery._snake_to_camel(plural)
        # kebab-case variant (common in JS directory names)
        kebab = domain.replace("_", "-")
        result = list({domain, singular, plural, camel, camel_plural, kebab})
        return [v for v in result if v]

    @staticmethod
    def _snake_to_camel(s: str) -> str:
        parts = s.split("_")
        return parts[0] + "".join(p.capitalize() for p in parts[1:])


# ---------------------------------------------------------------------------
# Stage 2: Reference tracing
# ---------------------------------------------------------------------------

RE_JS_IMPORT = re.compile(
    r"""import\s+(?:.+?\s+from\s+)?['"](.+?)['"]""", re.DOTALL
)
RE_JS_DYNAMIC_IMPORT = re.compile(r"""import\s*\(\s*['"](.+?)['"]\s*\)""")
RE_JS_INCLUDE_TAG = re.compile(r"""javascript_include_tag\s+(.+?)(?:%>|\n)""")
RE_DATA_CONTROLLER = re.compile(r"""data-controller=["']([^"']+)["']""")
RE_FETCH_URL = re.compile(r"""fetch\s*\(\s*['"`](/[\w/.]+)""")


class ReferenceTracer:
    """Stage 2: Find cross-domain references via class names, imports, and bridges."""

    def __init__(
        self,
        project_root: str,
        source_dirs: list[str],
        extensions: set[str],
        jsconfig_aliases: dict[str, str],
    ):
        self.project_root = project_root
        self.source_dirs = source_dirs
        self.extensions = extensions
        self.jsconfig_aliases = jsconfig_aliases

    def trace(
        self,
        seed_class_names: list[str],
        seed_files: dict[str, DiscoveredFile],
        all_discovered: dict[str, DiscoveredFile],
        *,
        forward_only: bool = False,
    ) -> dict[str, DiscoveredFile]:
        """Trace references from seed files to discover new files.

        Args:
            forward_only: If True, only trace forward (imports FROM seed files,
                ERB→JS bridges). Disables reverse import tracing, fetch→controller
                bridges, and Ruby class name grep. Used in Stage 3 to prevent
                shared infrastructure from pulling in unrelated domains.
        """
        new_files: dict[str, DiscoveredFile] = {}

        # 2a. Ruby class name grep (Stage 2 only)
        if seed_class_names and not forward_only:
            self._trace_ruby_refs(seed_class_names, all_discovered, new_files)

        # 2b. JS import tracing
        self._trace_js_imports(
            seed_files, all_discovered, new_files,
            forward_only=forward_only,
        )

        # 2c. ERB -> JS bridge tracing (forward direction only in Stage 3)
        self._trace_erb_js_bridges(
            seed_files, all_discovered, new_files,
            forward_only=forward_only,
        )

        return new_files

    def _trace_ruby_refs(
        self,
        class_names: list[str],
        already: dict[str, DiscoveredFile],
        new: dict[str, DiscoveredFile],
    ) -> None:
        # Separate short names (≤3 chars) that need stricter matching
        short_names = [cn for cn in class_names if len(cn.split("::")[-1]) <= 3]
        long_names = [cn for cn in class_names if len(cn.split("::")[-1]) > 3]

        long_pattern = None
        if long_names:
            escaped = "|".join(re.escape(cn) for cn in long_names)
            long_pattern = re.compile(r"\b(" + escaped + r")\b")

        short_patterns: list[tuple[str, re.Pattern]] = []
        for cn in short_names:
            leaf = cn.split("::")[-1]
            # Require context: ClassName. or ClassName:: or :class_name or _class_name
            pat = re.compile(
                r"(?:\b" + re.escape(cn) + r"(?:\.|::))"
                r"|(?::" + re.escape(leaf.lower()) + r"\b)"
            )
            short_patterns.append((cn, pat))

        for source_dir in self.source_dirs:
            sd_path = os.path.join(self.project_root, source_dir)
            if not os.path.isdir(sd_path):
                continue
            for root, dirs, files in os.walk(sd_path):
                for fname in files:
                    ext = fname.rsplit(".", 1)[-1] if "." in fname else ""
                    if ext not in ("rb", "erb"):
                        continue
                    fpath = os.path.relpath(
                        os.path.join(root, fname), self.project_root
                    )
                    if fpath in already or fpath in new:
                        continue

                    full = os.path.join(self.project_root, fpath)
                    try:
                        with open(full, "r", encoding="utf-8", errors="ignore") as f:
                            content = f.read()
                    except OSError:
                        continue

                    matched_name = None
                    if long_pattern:
                        m = long_pattern.search(content)
                        if m:
                            matched_name = m.group(1)

                    if matched_name is None:
                        for cn, pat in short_patterns:
                            if pat.search(content):
                                matched_name = cn
                                break

                    if matched_name:
                        new[fpath] = DiscoveredFile(
                            path=fpath, stage=2,
                            discovery_reason=f"ref: {matched_name}",
                        )

    def _trace_js_imports(
        self,
        seed_files: dict[str, DiscoveredFile],
        already: dict[str, DiscoveredFile],
        new: dict[str, DiscoveredFile],
        *,
        forward_only: bool = False,
    ) -> None:
        seed_js = {
            p: df for p, df in seed_files.items() if p.endswith((".js", ".jsx"))
        }
        if not seed_js:
            return

        # Forward: resolve imports FROM seed files
        for path in seed_js:
            imports = self._extract_js_imports(path)
            for imp_source in imports:
                resolved = self._resolve_js_import(imp_source, path)
                if not resolved or resolved in already or resolved in new:
                    continue
                # Only include files with tracked extensions
                r_ext = resolved.rsplit(".", 1)[-1] if "." in resolved else ""
                if r_ext not in self.extensions:
                    continue
                new[resolved] = DiscoveredFile(
                    path=resolved, stage=2,
                    discovery_reason=f"import: from {path}",
                )

        if forward_only:
            return

        # Reverse: find JS files that import FROM seed file paths
        seed_js_ids = self._build_js_module_ids(seed_js.keys())
        if not seed_js_ids:
            return

        js_root = os.path.join(self.project_root, "app", "javascript")
        if not os.path.isdir(js_root):
            return

        for root, dirs, files in os.walk(js_root):
            # Skip test/story dirs
            dirs[:] = [
                d for d in dirs
                if d not in ("__tests__", "__stories__", "__mocks__", "node_modules")
            ]
            for fname in files:
                if not fname.endswith((".js", ".jsx")):
                    continue
                fpath = os.path.relpath(
                    os.path.join(root, fname), self.project_root
                )
                if fpath in already or fpath in new:
                    continue
                imports = self._extract_js_imports(fpath)
                for imp in imports:
                    resolved = self._resolve_js_import(imp, fpath)
                    if resolved and resolved in seed_js_ids:
                        new[fpath] = DiscoveredFile(
                            path=fpath, stage=2,
                            discovery_reason=f"imports: {resolved}",
                        )
                        break

    def _trace_erb_js_bridges(
        self,
        seed_files: dict[str, DiscoveredFile],
        already: dict[str, DiscoveredFile],
        new: dict[str, DiscoveredFile],
        *,
        forward_only: bool = False,
    ) -> None:
        erb_files = {p: df for p, df in seed_files.items() if p.endswith(".erb")}
        js_files = {
            p: df for p, df in seed_files.items() if p.endswith((".js", ".jsx"))
        }

        # ERB → JS: javascript_include_tag and data-controller
        for erb_path in erb_files:
            full = os.path.join(self.project_root, erb_path)
            try:
                with open(full, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
            except OSError:
                continue

            # javascript_include_tag
            for m in RE_JS_INCLUDE_TAG.finditer(content):
                tag_args = m.group(1)
                pack_names = re.findall(r"""['"]([^'"]+)['"]""", tag_args)
                for pack in pack_names:
                    for ext in (".jsx", ".js"):
                        candidate = f"app/javascript/packs/{pack}{ext}"
                        if os.path.isfile(
                            os.path.join(self.project_root, candidate)
                        ):
                            if candidate not in already and candidate not in new:
                                new[candidate] = DiscoveredFile(
                                    path=candidate, stage=2,
                                    discovery_reason=f"erb_bridge: javascript_include_tag in {erb_path}",
                                )
                            break

            # data-controller
            for m in RE_DATA_CONTROLLER.finditer(content):
                ctrl_names = m.group(1).split()
                for ctrl_name in ctrl_names:
                    file_name = ctrl_name.replace("-", "_") + "_controller.js"
                    for candidate in [
                        f"app/javascript/controllers/{file_name}",
                        f"app/javascript/admin/controllers/{file_name}",
                    ]:
                        if os.path.isfile(
                            os.path.join(self.project_root, candidate)
                        ):
                            if candidate not in already and candidate not in new:
                                new[candidate] = DiscoveredFile(
                                    path=candidate, stage=2,
                                    discovery_reason=(
                                        f"erb_bridge: data-controller='{ctrl_name}'"
                                        f" in {erb_path}"
                                    ),
                                )
                            break

        if forward_only:
            return

        # JS → Ruby: fetch() URL → controller
        for js_path in js_files:
            full = os.path.join(self.project_root, js_path)
            try:
                with open(full, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
            except OSError:
                continue

            for m in RE_FETCH_URL.finditer(content):
                url_path = m.group(1)
                segments = url_path.strip("/").split("/")
                if not segments:
                    continue
                # Try direct resource mapping
                resource = segments[0]
                # Handle API namespace: /api/v1/articles -> api/v1/articles
                if resource == "api" and len(segments) >= 3:
                    ctrl = f"app/controllers/api/{segments[1]}/{segments[2]}_controller.rb"
                else:
                    ctrl = f"app/controllers/{resource}_controller.rb"

                if os.path.isfile(os.path.join(self.project_root, ctrl)):
                    if ctrl not in already and ctrl not in new:
                        new[ctrl] = DiscoveredFile(
                            path=ctrl, stage=2,
                            discovery_reason=f"fetch_bridge: fetch('{url_path}') in {js_path}",
                        )

    def _extract_js_imports(self, rel_path: str) -> list[str]:
        full = os.path.join(self.project_root, rel_path)
        try:
            with open(full, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
        except OSError:
            return []
        sources: list[str] = []
        for m in RE_JS_IMPORT.finditer(content):
            sources.append(m.group(1))
        for m in RE_JS_DYNAMIC_IMPORT.finditer(content):
            sources.append(m.group(1))
        return sources

    def _resolve_js_import(self, import_source: str, from_file: str) -> str | None:
        # Skip node_modules (no ./ or / prefix, and not an alias)
        if not import_source.startswith((".", "/", "@")):
            return None

        # Handle aliases from jsconfig.json
        for alias_pattern, alias_target in self.jsconfig_aliases.items():
            alias_prefix = alias_pattern.rstrip("*").rstrip("/")
            if import_source.startswith(alias_prefix):
                remainder = import_source[len(alias_prefix):].lstrip("/")
                target_base = alias_target.rstrip("*").rstrip("/")
                return self._find_js_file(os.path.join(target_base, remainder))

        # Handle relative imports
        if import_source.startswith("."):
            from_dir = os.path.dirname(from_file)
            resolved = os.path.normpath(os.path.join(from_dir, import_source))
            return self._find_js_file(resolved)

        return None

    def _find_js_file(self, base_path: str) -> str | None:
        for ext in ("", ".js", ".jsx"):
            candidate = base_path + ext
            if os.path.isfile(os.path.join(self.project_root, candidate)):
                return candidate
        for ext in (".js", ".jsx"):
            candidate = os.path.join(base_path, "index" + ext)
            if os.path.isfile(os.path.join(self.project_root, candidate)):
                return candidate
        return None

    def _build_js_module_ids(self, paths: object) -> set[str]:
        """Build a set of module identifiers for reverse-import matching."""
        ids: set[str] = set()
        for p in paths:
            ids.add(p)
            # Also add without extension for matching
            if p.endswith((".js", ".jsx")):
                ids.add(p.rsplit(".", 1)[0])
            # Add index-style: dir/index.js -> dir
            if os.path.basename(p).startswith("index."):
                ids.add(os.path.dirname(p))
        return ids


# ---------------------------------------------------------------------------
# Stage 3: Transitive expansion
# ---------------------------------------------------------------------------

class TransitiveExpander:
    """Stage 3: Iterate reference tracing until convergence or max rounds."""

    def __init__(self, tracer: ReferenceTracer, max_rounds: int = 3):
        self.tracer = tracer
        self.max_rounds = max_rounds

    def expand(self, result: DiscoveryResult) -> int:
        """Expand result in-place. Returns number of rounds executed.

        Only JS import tracing and ERB bridge tracing are repeated.
        Ruby class name grep is NOT expanded — adding class names from
        transitively discovered files causes runaway explosion (e.g.,
        a file referencing Article also references User, Notification,
        etc., pulling in the entire codebase).
        """
        rounds = 0
        prev_new_files = {
            p: df for p, df in result.files.items() if df.stage == 2
        }

        for round_num in range(1, self.max_rounds + 1):
            if not prev_new_files:
                break

            # Forward-only: resolve imports FROM newly discovered files
            # and ERB→JS bridges. No reverse imports, no fetch→controller,
            # no Ruby class grep. This prevents shared infrastructure
            # (crayons, utilities) from pulling in unrelated domains.
            new_files = self.tracer.trace(
                seed_class_names=[],
                seed_files=prev_new_files,
                all_discovered=result.files,
                forward_only=True,
            )

            if not new_files:
                break

            for path, df in new_files.items():
                df.stage = 3
                df.discovery_reason = (
                    f"transitive(r{round_num}): {df.discovery_reason}"
                )
                result.files[path] = df

            rounds = round_num
            prev_new_files = new_files

        return rounds


# ---------------------------------------------------------------------------
# Stage 4: Tag checker
# ---------------------------------------------------------------------------

RE_SPECRE_TAG = re.compile(r"@specre\s+([0-9A-Z]{26})")


class TagChecker:
    """Stage 4: Check @specre markers in discovered files."""

    @staticmethod
    def check(project_root: str, files: dict[str, DiscoveredFile]) -> None:
        for path, df in files.items():
            full = os.path.join(project_root, path)
            if not os.path.isfile(full):
                continue
            try:
                with open(full, "r", encoding="utf-8", errors="ignore") as f:
                    for _ in range(5):
                        line = f.readline()
                        if not line:
                            break
                        m = RE_SPECRE_TAG.search(line)
                        if m:
                            df.specre_tags.append(m.group(1))
            except OSError:
                continue


# ---------------------------------------------------------------------------
# Output formatting
# ---------------------------------------------------------------------------

class OutputFormatter:
    @staticmethod
    def format_text(result: DiscoveryResult, untagged_only: bool = False, exclude_keywords: list[str] | None = None) -> str:
        s = result.stats()
        lines = [
            f"Domain discovery: {result.domain}",
        ]
        if exclude_keywords:
            lines.append(f"Excluded keywords: {', '.join(exclude_keywords)}")
        lines.extend([
            f"Seed class names: {', '.join(sorted(set(result.seed_class_names)))}",
            "",
            f"Stage 1 — Convention-based glob: {s['stage1']} files",
            f"Stage 2 — Reference tracing: {s['stage2']} files",
            f"Stage 3 — Transitive expansion: {s['stage3']} files",
            f"Total: {s['total']} files ({s['untagged']} untagged, {s['tagged']} tagged)",
            "",
        ])

        # Group by stage, sorted by path
        untagged = {
            p: df for p, df in result.files.items() if not df.specre_tags
        }
        tagged = {
            p: df for p, df in result.files.items() if df.specre_tags
        }

        lines.append(f"--- Untagged files ({len(untagged)}) ---")
        for path in sorted(untagged):
            df = untagged[path]
            lines.append(f"[Stage {df.stage}] {path}  ({df.discovery_reason})")

        if not untagged_only:
            lines.append("")
            lines.append(f"--- Already tagged files ({len(tagged)}) ---")
            for path in sorted(tagged):
                df = tagged[path]
                ulids = ", ".join(df.specre_tags)
                lines.append(
                    f"[Stage {df.stage}] {path}  [{ulids}] ({df.discovery_reason})"
                )

        return "\n".join(lines)

    @staticmethod
    def format_json(result: DiscoveryResult, exclude_keywords: list[str] | None = None) -> str:
        data = {
            "domain": result.domain,
        }
        if exclude_keywords:
            data["exclude_keywords"] = exclude_keywords
        data.update({
            "seed_class_names": sorted(set(result.seed_class_names)),
            "stats": result.stats(),
            "files": {
                path: {
                    "stage": df.stage,
                    "reason": df.discovery_reason,
                    "specre_tags": df.specre_tags,
                }
                for path, df in sorted(result.files.items())
            },
        })
        return json.dumps(data, indent=2, ensure_ascii=False)

    @staticmethod
    def suggest_subdomains(result: DiscoveryResult) -> list[dict]:
        """Suggest sub-domain splits based on seed class names.

        Groups satellite models (CompoundName with domain prefix) into
        potential sub-domains separate from the core domain entity.
        """
        domain = result.domain
        variants = ConventionDiscovery._domain_variants(domain)
        # Case-insensitive set for core entity detection
        core_names = {v.lower() for v in variants}

        satellite_classes: dict[str, list[str]] = {}  # snake_name -> [classes]

        for cn in sorted(set(result.seed_class_names)):
            # Skip framework/search/error/infrastructure classes
            if any(kw in cn for kw in (
                "Searchable", "Algolia", "Error", "LiquidTag",
                "Query", "Segmented",
            )):
                continue
            leaf = cn.rsplit("::", 1)[-1] if "::" in cn else cn
            # Core entity check (case-insensitive)
            if leaf.lower() in core_names:
                continue
            # Convert CamelCase to snake_case for sub-domain name
            snake = re.sub(r"(?<=[a-z0-9])([A-Z])", r"_\1", leaf).lower()
            satellite_classes.setdefault(snake, []).append(cn)

        # Deduplicate singular/plural (e.g., "setting" and "settings")
        to_remove: list[str] = []
        for name in list(satellite_classes):
            plural = name + "s"
            if plural in satellite_classes:
                satellite_classes[plural].extend(satellite_classes[name])
                to_remove.append(name)
        for name in to_remove:
            del satellite_classes[name]

        # Count files per satellite by matching snake name in file paths
        suggestions: list[dict] = []
        for snake_name, classes in sorted(satellite_classes.items()):
            file_count = sum(
                1 for p in result.files
                if snake_name in p.lower()
            )
            if file_count >= 5:  # skip tiny satellites
                suggestions.append({
                    "subdomain": snake_name,
                    "model_classes": sorted(set(classes)),
                    "estimated_files": file_count,
                })

        return suggestions

    @staticmethod
    def split_and_save(result: DiscoveryResult) -> list[str]:
        """Split files into multiple parts and save to /tmp/.

        Splitting rule (each chunk targets ~100 files):
          ≤100 files  → no split (caller should not invoke this)
          101-199     → 2 parts
          200-299     → 3 parts
          300-399     → 4 parts  ...etc.
        """
        file_count = len(result.files)
        num_parts = max(2, math.ceil(file_count / 100))

        files_list = sorted(result.files.items())
        chunk_size = math.ceil(len(files_list) / num_parts)

        meta = {
            "domain": result.domain,
            "seed_class_names": sorted(set(result.seed_class_names)),
            "stats": result.stats(),
        }

        saved_paths: list[str] = []
        for i in range(num_parts):
            chunk = files_list[i * chunk_size : (i + 1) * chunk_size]
            part_data = {
                **meta,
                "part": i + 1,
                "total_parts": num_parts,
                "files": {
                    path: {
                        "stage": df.stage,
                        "reason": df.discovery_reason,
                        "specre_tags": df.specre_tags,
                    }
                    for path, df in chunk
                },
            }
            tmp_path = f"/tmp/specre-discovery-{result.domain}-part{i + 1}.json"
            with open(tmp_path, "w", encoding="utf-8") as f:
                json.dump(part_data, f, indent=2, ensure_ascii=False)
            saved_paths.append(tmp_path)

        return saved_paths


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Discover all source files related to a domain via convention, "
            "reference tracing, and transitive expansion."
        )
    )
    parser.add_argument("domain", help="Domain keyword (e.g., article, comment, github_repo)")
    parser.add_argument(
        "--json", action="store_true", dest="json_output",
        help="Output as JSON (default: human-readable text)",
    )
    parser.add_argument("--root", default=".", help="Project root directory")
    parser.add_argument(
        "--max-rounds", type=int, default=3,
        help="Maximum transitive expansion rounds (default: 3)",
    )
    parser.add_argument(
        "--untagged-only", action="store_true",
        help="Only output untagged files",
    )
    parser.add_argument(
        "--exclude", nargs="+", default=[], metavar="KEYWORD",
        help="Exclude files matching these sub-domain keywords (e.g., --exclude comments_admin comments_scoring)",
    )
    args = parser.parse_args()

    project_root = os.path.abspath(args.root)

    # Load config
    try:
        config = Config.load_specre_toml(project_root)
    except (FileNotFoundError, KeyError) as e:
        print(f"Error loading specre.toml: {e}", file=sys.stderr)
        sys.exit(1)

    jsconfig_aliases = Config.load_jsconfig(project_root)

    # Initialize result
    result = DiscoveryResult(domain=args.domain)

    # Build exclude variants for post-filtering Stage 2/3 results
    exclude_variants: list[str] = []
    exclude_part_groups: list[list[str]] = []
    for kw in args.exclude:
        exclude_variants.extend(ConventionDiscovery._domain_variants(kw))
        if "_" in kw:
            joined = kw.replace("_", "").lower()
            if joined not in exclude_variants:
                exclude_variants.append(joined)
            parts = kw.lower().split("_")
            normalized = []
            for p in parts:
                singular = p.rstrip("s") if p.endswith("s") and len(p) > 2 else p
                normalized.append(singular)
            exclude_part_groups.append(normalized)

    def _matches_exclude(file_path: str) -> bool:
        """Check if a file path matches any exclusion pattern."""
        path_lower = file_path.lower()
        # Strategy 1: substring match
        if any(ev in path_lower for ev in exclude_variants):
            return True
        # Strategy 2: all-parts match
        for parts in exclude_part_groups:
            if all(p in path_lower for p in parts):
                return True
        return False

    # Stage 1: Convention-based glob
    convention = ConventionDiscovery(
        project_root, config["source_dirs"], config["ext"],
        exclude_keywords=args.exclude,
    )
    stage1_files, seed_classes = convention.discover(args.domain)
    result.files.update(stage1_files)
    result.seed_class_names = seed_classes

    # Stage 2: Reference tracing
    tracer = ReferenceTracer(
        project_root, config["source_dirs"], set(config["ext"]), jsconfig_aliases
    )
    stage2_files = tracer.trace(
        seed_class_names=result.seed_class_names,
        seed_files=stage1_files,
        all_discovered=result.files,
    )
    # Filter out excluded files from Stage 2
    if exclude_variants:
        stage2_files = {p: df for p, df in stage2_files.items() if not _matches_exclude(p)}
    result.files.update(stage2_files)

    # Stage 3: Transitive expansion
    if args.max_rounds > 0:
        expander = TransitiveExpander(tracer, args.max_rounds)
        expander.expand(result)
        # Filter out excluded files from Stage 3
        if exclude_variants:
            to_remove = [p for p in result.files if result.files[p].stage == 3 and _matches_exclude(p)]
            for p in to_remove:
                del result.files[p]

    # Stage 4: Tag check
    TagChecker.check(project_root, result.files)

    # Output — split to disk if file count exceeds 100
    file_count = len(result.files)
    if args.exclude:
        exclude_note = f"Excluded keywords: {', '.join(args.exclude)}"
    else:
        exclude_note = None

    if file_count > 100:
        saved_paths = OutputFormatter.split_and_save(result)
        s = result.stats()
        print(f"Domain discovery: {result.domain}")
        if exclude_note:
            print(exclude_note)
        print(f"Seed class names: {', '.join(sorted(set(result.seed_class_names)))}")
        print(f"Total: {s['total']} files "
              f"({s['untagged']} untagged, {s['tagged']} tagged)")
        print(f"\nOutput split into {len(saved_paths)} parts (>{100} files):")
        for p in saved_paths:
            print(f"  {p}")

        # Suggest sub-domain split for very large domains
        if file_count > 300:
            suggestions = OutputFormatter.suggest_subdomains(result)
            print(f"\n⚠ LARGE DOMAIN ({file_count} files > 300 threshold)")
            print("Recommendation: Do NOT process individual files directly.")
            print("Instead, split into sub-domains and process each separately.")
            print(f"\nCore domain '{result.domain}' should retain base CRUD "
                  f"behaviors for the primary entity.")
            if suggestions:
                print(f"\nSuggested sub-domains (based on satellite models):")
                for sg in suggestions:
                    classes = ", ".join(sg["model_classes"])
                    print(f"  {sg['subdomain']}: ~{sg['estimated_files']} files "
                          f"({classes})")
            print(f"\nRun each sub-domain independently:")
            print(f"  /specre-generate {result.domain}")
            if suggestions:
                for sg in suggestions:
                    print(f"  /specre-generate {sg['subdomain']}")
    elif args.json_output:
        print(OutputFormatter.format_json(result, exclude_keywords=args.exclude))
    else:
        print(OutputFormatter.format_text(result, args.untagged_only, exclude_keywords=args.exclude))


if __name__ == "__main__":
    main()
