"""Build an installable ZIP and SHA-256 checksum without repository-only files."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import stat
import sys
import tempfile
import zipfile

try:
    from .validate_skill import RUNTIME_DIRS, ValidationError, runtime_files, validate
except ImportError:
    from validate_skill import RUNTIME_DIRS, ValidationError, runtime_files, validate


def build(root: Path, output: Path) -> Path:
    root = root.resolve()
    metadata = validate(root)
    output = output.absolute()
    checksum = output.with_suffix(output.suffix + ".sha256")
    if output.suffix.lower() != ".zip":
        raise ValidationError("Output must be a .zip file")
    if any(output.resolve().is_relative_to(root / directory) for directory in RUNTIME_DIRS):
        raise ValidationError("Output cannot be inside a runtime resource directory")
    if output.is_symlink() or checksum.is_symlink():
        raise ValidationError("Output and checksum cannot be symlinks")
    files = runtime_files(root)
    output.parent.mkdir(parents=True, exist_ok=True)
    # Stable entry order, timestamps, permissions and paths; no host metadata.
    with tempfile.TemporaryDirectory(prefix="skill-package-", dir=output.parent) as temporary:
        archive = Path(temporary) / "package.zip"
        with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as package:
            for path in files:
                relative = path.relative_to(root)
                member = zipfile.ZipInfo(f"{metadata['name']}/{relative.as_posix()}", date_time=(1980, 1, 1, 0, 0, 0))
                member.create_system = 3
                mode = 0o755 if relative.parts[0] == "scripts" and path.suffix == ".sh" else 0o644
                member.external_attr = (stat.S_IFREG | mode) << 16
                member.compress_type = zipfile.ZIP_DEFLATED
                package.writestr(member, path.read_bytes())
        digest = hashlib.sha256(archive.read_bytes()).hexdigest()
        receipt = Path(temporary) / "checksum"
        receipt.write_text(f"{digest}  {output.name}\n", encoding="utf-8", newline="\n")
        archive.replace(output)
        receipt.replace(checksum)
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        output = args.output or args.source / "dist" / "flutter-start.zip"
        print(build(args.source, output))
        print(output.with_suffix(output.suffix + ".sha256"))
    except (ValidationError, OSError, UnicodeError) as error:
        print(f"PACKAGE FAILED: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
