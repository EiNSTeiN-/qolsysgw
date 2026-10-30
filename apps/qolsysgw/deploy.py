"""Connect an AppDaemon apps directory to its HACS-managed fork installation.

The directories remain real directories so AppDaemon discovers every Python file.
Each source file is linked to HACS's managed copy, so updates do not restore an
unrelated upstream installation. Run before AppDaemon starts.
"""
import argparse
import shutil
from pathlib import Path


def deploy(source, target, backup):
    source = Path(source).resolve()
    target = Path(target).absolute()
    backup = Path(backup).absolute()
    if source == target or source in target.parents or target in source.parents:
        raise ValueError('Source and target must be separate directories')
    if not (source / 'gateway.py').is_file():
        raise ValueError('Source is not a Qolsys Gateway installation')
    if target.exists() and not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(target, backup, symlinks=True)
    target.mkdir(parents=True, exist_ok=True)
    expected = {p.relative_to(source) for p in source.rglob('*.py')}
    for relative in expected:
        original = source / relative
        destination = target / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        if destination.is_symlink():
            if destination.resolve() == original:
                continue
            destination.unlink()
        elif destination.exists():
            destination.unlink()
        destination.symlink_to(original)
    for path in target.rglob('*.py'):
        if path.is_symlink() and path.relative_to(target) not in expected:
            path.unlink()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target', required=True)
    parser.add_argument('--backup', required=True)
    arguments = parser.parse_args()
    deploy(Path(__file__).parent, arguments.target, arguments.backup)
