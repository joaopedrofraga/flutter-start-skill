"""Behavioral tests for metadata validation and distributable archives."""

from __future__ import annotations

import hashlib
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile

from tools.package_skill import build
from tools.validate_skill import ValidationError, validate


class DistributionTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="flutter-start-test-")
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.root = self.base / "repository with spaces café"
        self.root.mkdir()
        self.write("SKILL.md", "---\nname: flutter-start\ndescription: Create a Flutter foundation ready for development.\n---\n\n# Instructions\n\nRead [the foundation](references/base.md).\n")
        self.write("references/base.md", "# Foundation\n\nContent containing an accented word: café.\n")
        self.write("agents/openai.yaml", 'interface:\n  display_name: "Start Flutter"\n  short_description: "Create a Flutter foundation ready for development"\n  default_prompt: "Use $flutter-start to start my app."\n')

    def write(self, name, content):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def append(self, name, content):
        path = self.root / name
        self.write(name, path.read_text(encoding="utf-8") + content)

    def test_accepts_utf8_and_directory_with_spaces(self):
        self.assertEqual(validate(self.root)["name"], "flutter-start")

    def test_rejects_empty_or_invalid_metadata(self):
        for frontmatter in ("name: ''\ndescription: Ready", "name: Flutter Start\ndescription: Ready", "name: flutter-start\ndescription: ''", "- not-a-mapping"):
            with self.subTest(frontmatter=frontmatter):
                self.write("SKILL.md", f"---\n{frontmatter}\n---\nInstructions\n")
                with self.assertRaises(ValidationError):
                    validate(self.root)

    def test_rejects_duplicate_yaml_keys(self):
        self.write("SKILL.md", "---\nname: flutter-start\nname: unexpected\ndescription: Ready\n---\nInstructions\n")
        with self.assertRaises(ValidationError):
            validate(self.root)

    def test_rejects_broken_runtime_link(self):
        self.append("references/base.md", "\n[Missing](missing.md)\n")
        with self.assertRaises(ValidationError):
            validate(self.root)

    def test_rejects_encoded_path_escape(self):
        (self.base / "outside.md").write_text("Outside", encoding="utf-8")
        self.append("SKILL.md", "\n[Outside](%2e%2e/outside.md)\n")
        with self.assertRaises(ValidationError):
            validate(self.root)

    def test_rejects_link_to_maintenance_file_not_packaged(self):
        self.write("README.md", "# Repository documentation\n")
        self.append("SKILL.md", "\n[Readme](README.md)\n")
        with self.assertRaises(ValidationError):
            validate(self.root)

    def test_rejects_broken_repository_documentation_link(self):
        self.write("README.md", "# Readme\n\n[Missing](missing.md)\n")
        with self.assertRaises(ValidationError):
            validate(self.root)

    def test_code_examples_are_not_mistaken_for_links(self):
        self.append("references/base.md", "\n```markdown\n[Example](not-a-real-file.md)\n[TODO: an example]\n```\n")
        self.assertEqual(validate(self.root)["name"], "flutter-start")

    def test_rejects_wrong_invocation_and_wrong_boolean(self):
        original = (self.root / "agents/openai.yaml").read_text(encoding="utf-8")
        for content in (original.replace("$flutter-start", "$another-skill"), original + 'policy:\n  allow_implicit_invocation: "false"\n'):
            with self.subTest(content=content):
                self.write("agents/openai.yaml", content)
                with self.assertRaises(ValidationError):
                    validate(self.root)

    def test_rejects_missing_icon(self):
        self.append("agents/openai.yaml", '  icon_small: "./assets/missing.svg"\n')
        with self.assertRaises(ValidationError):
            validate(self.root)

    def test_rejects_absolute_icon_even_if_the_file_exists(self):
        asset = self.write("assets/icon.svg", '<svg xmlns="http://www.w3.org/2000/svg"/>\n')
        self.append("agents/openai.yaml", f'  icon_small: "{asset.as_posix()}"\n')
        with self.assertRaises(ValidationError):
            validate(self.root)

    def test_rejects_machine_specific_runtime_path(self):
        self.append("references/base.md", "\nUse Z:/Users/Example/private/project.\n")
        with self.assertRaises(ValidationError):
            validate(self.root)

    def test_archive_roundtrip_excludes_repository_files_and_verifies_checksum(self):
        self.write("README.md", "# Maintenance readme\n")
        self.write("tools/private.py", "# Must not be installed\n")
        self.write(".git/config", "# Must not be distributed\n")
        self.write(".env", "EXAMPLE=not-a-secret\n")
        output = build(self.root, self.base / "output" / "flutter-start.zip")
        receipt = output.with_suffix(".zip.sha256").read_text(encoding="utf-8")
        self.assertEqual(receipt.split()[0], hashlib.sha256(output.read_bytes()).hexdigest())
        with zipfile.ZipFile(output) as package:
            names = package.namelist()
            self.assertEqual(set(names), {"flutter-start/SKILL.md", "flutter-start/agents/openai.yaml", "flutter-start/references/base.md"})
            self.assertTrue(all(not name.startswith("/") and ".." not in Path(name).parts for name in names))
            extracted = self.base / "extracted"
            package.extractall(extracted)
        self.assertEqual(validate(extracted / "flutter-start")["name"], "flutter-start")

    def test_package_is_repeatable_and_preserves_license(self):
        self.write("LICENSE", "License fixture, not a license grant.\n")
        first = build(self.root, self.base / "one.zip")
        second = build(self.root, self.base / "two.zip")
        self.assertEqual(first.read_bytes(), second.read_bytes())
        with zipfile.ZipFile(first) as package:
            self.assertIn("flutter-start/LICENSE", package.namelist())

    def test_invalid_source_does_not_replace_existing_archive(self):
        output = self.base / "existing.zip"
        output.write_bytes(b"existing archive")
        self.append("SKILL.md", "\n[Broken](missing.md)\n")
        with self.assertRaises(ValidationError):
            build(self.root, output)
        self.assertEqual(output.read_bytes(), b"existing archive")

    def test_package_cannot_write_into_runtime_resources(self):
        with self.assertRaises(ValidationError):
            build(self.root, self.root / "references" / "archive.zip")

    def test_external_symlink_is_rejected(self):
        outside = self.base / "outside.md"
        outside.write_text("Do not package", encoding="utf-8")
        link = self.root / "references" / "external.md"
        try:
            link.symlink_to(outside)
        except OSError:
            self.skipTest("Symlink creation is unavailable on this host")
        with self.assertRaises(ValidationError):
            build(self.root, self.base / "symlink.zip")

    def test_invalid_skill_cli_exits_nonzero(self):
        self.append("SKILL.md", "\n[Broken](missing.md)\n")
        script = Path(__file__).resolve().parents[1] / "tools" / "validate_skill.py"
        result = subprocess.run([sys.executable, str(script), str(self.root)], capture_output=True, text=True, encoding="utf-8")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("INVALID:", result.stderr)


if __name__ == "__main__":
    unittest.main()
