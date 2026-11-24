"""Validate this skill's metadata, portable resources and local Markdown links."""

from __future__ import annotations

import argparse
from pathlib import Path, PurePosixPath
import re
import sys
from urllib.parse import unquote, urlsplit

import yaml


RUNTIME_DIRS = ("agents", "references", "scripts", "assets")
PERSONAL_PATH = re.compile(r"[A-Za-z]:[/\\]Users[/\\][^/\\\s]+|/(?:home|Users)/[^/\s]+/")


class ValidationError(ValueError):
    """An invalid skill or distribution input."""


class UniqueLoader(yaml.SafeLoader):
    """Reject duplicate keys instead of silently replacing earlier metadata."""


def _unique_mapping(loader, node, deep=False):
    mapping = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        try:
            if key in mapping:
                raise ValidationError(f"Duplicate YAML key: {key}")
            mapping[key] = loader.construct_object(value_node, deep=deep)
        except TypeError as error:
            raise ValidationError("YAML keys must be scalar values") from error
    return mapping


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _unique_mapping)


def read_yaml(text: str):
    try:
        return yaml.load(text, Loader=UniqueLoader)
    except yaml.YAMLError as error:
        raise ValidationError(f"Invalid YAML: {error}") from error


def runtime_files(root: Path) -> list[Path]:
    """Return only installable files, never repository maintenance artifacts."""
    root = root.resolve()
    files = [root / "SKILL.md"]
    if (root / "LICENSE").exists():
        files.append(root / "LICENSE")
    for name in RUNTIME_DIRS:
        directory = root / name
        if directory.is_symlink():
            raise ValidationError(f"Symlinked resource directory: {name}")
        if directory.exists():
            if not directory.is_dir():
                raise ValidationError(f"Resource directory is not a directory: {name}")
            for path in directory.rglob("*"):
                if path.is_symlink() or not path.resolve().is_relative_to(root):
                    raise ValidationError(f"Resource escapes package or uses symlink: {path.name}")
                if path.is_file():
                    files.append(path)
    for path in files:
        if path.is_symlink() or not path.is_file():
            raise ValidationError(f"Missing or symlinked runtime file: {path.name}")
    return sorted(files)


def _without_fences(text: str) -> str:
    lines = []
    fence = None
    for line in text.splitlines():
        match = re.match(r"^\s*(`{3,}|~{3,})(.*)$", line)
        if match:
            marker, rest = match.groups()
            if fence is None:
                fence = marker
            elif marker[0] == fence[0] and len(marker) >= len(fence) and not rest.strip():
                fence = None
            continue
        if fence is None:
            lines.append(line)
    if fence is not None:
        raise ValidationError("Unclosed Markdown code fence")
    return "\n".join(lines)


def check_links(path: Path, root: Path, allowed: set[Path] | None = None):
    for match in re.finditer(r"!?\[[^\]\n]*\]\(([^)\n]+)\)", _without_fences(path.read_text(encoding="utf-8"))):
        target = match.group(1).strip()
        if target.startswith("<") and target.endswith(">"):
            target = target[1:-1]
        parsed = urlsplit(target)
        if parsed.scheme in {"https", "http", "mailto"}:
            continue
        if parsed.scheme or target.startswith(("/", "\\")):
            raise ValidationError(f"Nonportable link in {path.name}: {target}")
        if not parsed.path:
            continue
        destination = (path.parent / unquote(parsed.path)).resolve()
        if not destination.is_relative_to(root) or not destination.is_file():
            raise ValidationError(f"Broken or escaping link in {path.name}: {target}")
        if allowed is not None and destination not in allowed:
            raise ValidationError(f"Link target is not included in distribution: {target}")


def validate(root: Path) -> dict:
    root = root.resolve()
    files = runtime_files(root)
    content = (root / "SKILL.md").read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---(?:\n|$)", content, re.DOTALL)
    if match is None:
        raise ValidationError("SKILL.md needs YAML frontmatter")
    metadata = read_yaml(match.group(1))
    if not isinstance(metadata, dict):
        raise ValidationError("Frontmatter must be a mapping")
    allowed_keys = {"name", "description", "license", "allowed-tools", "metadata"}
    if set(metadata) - allowed_keys:
        raise ValidationError("Unsupported frontmatter field")
    name, description = metadata.get("name"), metadata.get("description")
    if not isinstance(name, str) or len(name) > 64 or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        raise ValidationError("Skill name must use lowercase words separated by hyphens, up to 64 characters")
    if not isinstance(description, str) or not description.strip() or len(description) > 1024 or "<" in description or ">" in description:
        raise ValidationError("Description must be nonempty plain text, up to 1024 characters")
    if not content[match.end():].strip():
        raise ValidationError("Skill instructions are empty")
    interface_file = root / "agents" / "openai.yaml"
    if interface_file not in files:
        raise ValidationError("Missing agents/openai.yaml")
    interface_document = read_yaml(interface_file.read_text(encoding="utf-8"))
    if not isinstance(interface_document, dict):
        raise ValidationError("UI metadata must be a mapping")
    interface = interface_document.get("interface", {})
    if not isinstance(interface, dict):
        raise ValidationError("Interface must be a mapping")
    for field in ("display_name", "short_description", "default_prompt"):
        if not isinstance(interface.get(field), str) or not interface[field].strip():
            raise ValidationError(f"Missing UI field: {field}")
    if not 25 <= len(interface["short_description"]) <= 64:
        raise ValidationError("UI short_description must contain 25–64 characters")
    if f"${name}" not in interface["default_prompt"]:
        raise ValidationError("UI default_prompt must invoke this skill")
    policy = interface_document.get("policy", {})
    if not isinstance(policy, dict) or ("allow_implicit_invocation" in policy and type(policy["allow_implicit_invocation"]) is not bool):
        raise ValidationError("allow_implicit_invocation must be a boolean")
    allowed_files = set(files)
    for path in files:
        if path.suffix in {".md", ".yaml", ".yml", ".py"}:
            text = path.read_text(encoding="utf-8")
            if PERSONAL_PATH.search(text):
                raise ValidationError(f"Personal machine path in runtime file: {path.name}")
        if path.suffix == ".md":
            visible = _without_fences(path.read_text(encoding="utf-8"))
            if re.search(r"(?m)^\s*\[TODO:[^\n]*\]\s*$", visible):
                raise ValidationError(f"Unfinished instruction in {path.name}")
            check_links(path, root, allowed_files)
    for field in ("icon_small", "icon_large"):
        if field in interface:
            value = interface[field]
            if not isinstance(value, str):
                raise ValidationError(f"Icon path must be a string: {field}")
            if "\\" in value or urlsplit(value).scheme or PurePosixPath(value).is_absolute() or ".." in PurePosixPath(value).parts:
                raise ValidationError(f"Icon must use a relative portable path: {value}")
            if (root / value).resolve() not in allowed_files:
                raise ValidationError(f"Icon is not included in distribution: {value}")
    readme = root / "README.md"
    if readme.is_file():
        check_links(readme, root)
    return metadata


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    try:
        metadata = validate(args.path)
    except (ValidationError, OSError, UnicodeError) as error:
        print(f"INVALID: {error}", file=sys.stderr)
        return 1
    print(f"VALID: {metadata['name']} — metadata, resources and local links")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
