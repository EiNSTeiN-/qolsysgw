"""The active app must keep following files replaced during a HACS update."""
import importlib.util
from pathlib import Path

import pytest

MODULE = Path(__file__).parents[2] / 'apps' / 'qolsysgw' / 'deploy.py'
SPEC = importlib.util.spec_from_file_location('qolsys_deploy', MODULE)
DEPLOY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(DEPLOY)


def test_hacs_update_and_new_modules_reach_active_install(tmp_path):
    source = tmp_path / 'hacs'
    target = tmp_path / 'active'
    backup = tmp_path / 'backup'
    source.mkdir()
    target.mkdir()
    (source / 'gateway.py').write_text('version = 1')
    (target / 'gateway.py').write_text('old installed version')
    DEPLOY.deploy(source, target, backup)
    assert (backup / 'gateway.py').read_text() == 'old installed version'
    assert (target / 'gateway.py').is_symlink()
    (source / 'replacement.py').write_text('version = 2')
    (source / 'replacement.py').replace(source / 'gateway.py')
    assert (target / 'gateway.py').read_text() == 'version = 2'
    (source / 'mqtt').mkdir()
    (source / 'mqtt' / 'new_module.py').write_text('new module')
    DEPLOY.deploy(source, target, backup)
    assert (target / 'mqtt').is_dir() and not (target / 'mqtt').is_symlink()
    assert (target / 'mqtt' / 'new_module.py').read_text() == 'new module'
    assert (backup / 'gateway.py').read_text() == 'old installed version'


def test_rejects_overlapping_installation_paths(tmp_path):
    with pytest.raises(ValueError):
        DEPLOY.deploy(tmp_path, tmp_path / 'nested', tmp_path / 'backup')
