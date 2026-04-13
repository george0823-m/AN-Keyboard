#!/usr/bin/env python3
"""
Standalone .kmn syntax validator (Linux/macOS without Keyman Developer)

Checks the AN keyboard .kmn file for common syntax issues:
- Required header stores
- Group definition
- Rule syntax (key context, > separator, output)
- Balanced quotes
- Valid Unicode codepoint references
- Undefined group references
- Common Keyman pitfalls
"""

import re
import sys
from pathlib import Path

class KMNValidator:
    def __init__(self, filepath):
        self.filepath = Path(filepath)
        self.lines = []
        self.errors = []
        self.warnings = []
        self.info = []
        self.stores = {}
        self.groups = {}
        self.rule_count = 0
        self.has_begin = False

    def load(self):
        if not self.filepath.exists():
            self.errors.append(f"File not found: {self.filepath}")
            return False
        with open(self.filepath, 'r', encoding='utf-8') as f:
            self.lines = f.readlines()
        return True

    def strip_comment(self, line):
        """Remove .kmn comments. 'c' at start of line or 'c' followed by space."""
        # Line starting with 'c '
        s = line.lstrip()
        if s.startswith('c ') or s == 'c\n' or s == 'c':
            return ''
        # Inline comment: ' c ' marks start of comment
        # but we must not split inside string literals
        in_str = False
        str_char = None
        result = []
        i = 0
        while i < len(line):
            ch = line[i]
            if in_str:
                result.append(ch)
                if ch == str_char:
                    in_str = False
                    str_char = None
            else:
                if ch == "'" or ch == '"':
                    in_str = True
                    str_char = ch
                    result.append(ch)
                elif ch == 'c' and i+1 < len(line) and line[i+1] == ' ' and (i == 0 or line[i-1] in ' \t'):
                    # Inline comment starts here
                    break
                else:
                    result.append(ch)
            i += 1
        return ''.join(result)

    def parse_stores(self):
        """Parse store(&NAME) 'value' definitions."""
        store_re = re.compile(r"store\s*\(\s*([&\w]+)\s*\)\s*(.+)$")
        for ln, line in enumerate(self.lines, 1):
            stripped = self.strip_comment(line).strip()
            if not stripped:
                continue
            m = store_re.match(stripped)
            if m:
                name = m.group(1)
                value = m.group(2).strip()
                self.stores[name] = (ln, value)

    def parse_groups(self):
        """Parse group(name) declarations."""
        group_re = re.compile(r"group\s*\(\s*(\w+)\s*\)(.*)$")
        begin_re = re.compile(r"begin\s+(Unicode|ANSI)\s*>\s*use\s*\(\s*(\w+)\s*\)")
        for ln, line in enumerate(self.lines, 1):
            stripped = self.strip_comment(line).strip()
            m = group_re.match(stripped)
            if m:
                self.groups[m.group(1)] = ln
            m2 = begin_re.match(stripped)
            if m2:
                self.has_begin = True
                target_group = m2.group(2)
                if target_group not in self.groups:
                    # Check later — store the begin target
                    self._begin_target = (ln, target_group)

    def validate_required_headers(self):
        required = ['&VERSION', '&NAME', '&KEYBOARDVERSION', '&TARGETS']
        recommended = ['&COPYRIGHT', '&BITMAP', '&LAYOUTFILE', '&VISUALKEYBOARD']
        for req in required:
            if req not in self.stores:
                self.errors.append(f"Missing required store: {req}")
            else:
                self.info.append(f"  ✓ {req} = {self.stores[req][1][:60]}")
        for rec in recommended:
            if rec not in self.stores:
                self.warnings.append(f"Missing recommended store: {rec}")
            else:
                self.info.append(f"  ✓ {rec} = {self.stores[rec][1][:60]}")

    def validate_groups(self):
        if not self.has_begin:
            self.errors.append("Missing 'begin Unicode > use(...)' statement")
        if 'main' not in self.groups:
            self.warnings.append("No 'main' group found (convention)")
        if hasattr(self, '_begin_target'):
            ln, target = self._begin_target
            if target not in self.groups:
                self.errors.append(f"Line {ln}: begin references undefined group '{target}'")

    def validate_rules(self):
        """Check rule syntax: + LHS > RHS"""
        rule_re = re.compile(r"^\s*\+\s*(.+?)\s*>\s*(.+?)$")
        vk_re = re.compile(r"\[\s*([A-Z_ ]+)\s*\]")
        unicode_re = re.compile(r"U\+([0-9A-Fa-f]{4,6})")

        valid_modifiers = {'SHIFT', 'CTRL', 'ALT', 'LCTRL', 'RCTRL', 'LALT', 'RALT', 'CAPS', 'NCAPS'}

        in_group = None
        for ln, line in enumerate(self.lines, 1):
            stripped = self.strip_comment(line).strip()
            if not stripped:
                continue

            # Track group context
            gm = re.match(r"group\s*\(\s*(\w+)\s*\)", stripped)
            if gm:
                in_group = gm.group(1)
                continue

            # Check rule
            if stripped.startswith('+'):
                self.rule_count += 1
                m = rule_re.match(stripped)
                if not m:
                    self.errors.append(f"Line {ln}: malformed rule (no '>' found): {stripped[:60]}")
                    continue

                lhs = m.group(1)
                rhs = m.group(2)

                # Validate VK notation in LHS
                vk_matches = vk_re.findall(lhs)
                for vk_content in vk_matches:
                    parts = vk_content.split()
                    has_key = False
                    for part in parts:
                        if part.startswith('K_'):
                            has_key = True
                        elif part not in valid_modifiers:
                            self.warnings.append(f"Line {ln}: unknown modifier/key '{part}' in [{vk_content}]")
                    if not has_key:
                        self.errors.append(f"Line {ln}: VK notation [{vk_content}] missing K_ key code")

                # Validate Unicode references in RHS
                u_matches = unicode_re.findall(rhs)
                for u in u_matches:
                    cp = int(u, 16)
                    if cp == 0x0008:
                        self.errors.append(f"Line {ln}: Output U+0008 (BACKSPACE) is dangerous — system delete will be broken")
                    if cp > 0x10FFFF:
                        self.errors.append(f"Line {ln}: Invalid Unicode codepoint U+{u}")

                # Quote balance check
                if stripped.count("'") % 2 != 0:
                    # Could be apostrophe inside double-quoted string
                    if stripped.count('"') % 2 == 0 and stripped.count('"') > 0:
                        pass  # OK
                    else:
                        self.warnings.append(f"Line {ln}: unbalanced single quotes")

    def report(self):
        print("=" * 70)
        print(f"  KMN Validator — {self.filepath.name}")
        print("=" * 70)
        print(f"\n📊 Statistics:")
        print(f"  Total lines:     {len(self.lines)}")
        print(f"  Stores defined:  {len(self.stores)}")
        print(f"  Groups defined:  {len(self.groups)}")
        print(f"  Rules defined:   {self.rule_count}")

        if self.info:
            print(f"\n✅ Required & recommended headers:")
            for i in self.info:
                print(i)

        if self.warnings:
            print(f"\n⚠️  Warnings ({len(self.warnings)}):")
            for w in self.warnings:
                print(f"  ⚠ {w}")

        if self.errors:
            print(f"\n❌ Errors ({len(self.errors)}):")
            for e in self.errors:
                print(f"  ✗ {e}")
            return False
        else:
            print(f"\n✅ No errors found!")
            return True

    def run(self):
        if not self.load():
            self.report()
            return False
        self.parse_stores()
        self.parse_groups()
        self.validate_required_headers()
        self.validate_groups()
        self.validate_rules()
        return self.report()


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "an_alphabet_national.kmn"
    v = KMNValidator(target)
    success = v.run()
    sys.exit(0 if success else 1)
