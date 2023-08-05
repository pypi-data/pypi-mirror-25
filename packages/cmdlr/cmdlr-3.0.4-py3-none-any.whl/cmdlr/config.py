"""Cmdlr config system."""

import os

from . import yamla
from . import schema


_default_config = {
        'dirs': ['~/comics'],
        'disabled_analyzers': [],
        'extra_analyzer_dir': None,
        'max_concurrent': 10,
        'max_retry': 4,
        'proxy': None,
        }

_config_filepath = os.path.join(
        os.getenv(
            'XDG_CONFIG_HOME',
            os.path.join(os.path.expanduser('~'), '.config'),
            ),
        'cmdlr',
        'config.yaml',
        )

_config = None


def _normalize_path(path):
    return os.path.expanduser(path)


def _create_default(filepath):
    """Create default config on `filepath` location."""
    yamla.to_file(filepath, _default_config)


def _init():
    if not os.path.exists(_config_filepath):
        _create_default(_config_filepath)

    global _config
    _config = schema.config(yamla.from_file(_config_filepath))


def get_incoming_dir():
    """Get incoming dir."""
    return _normalize_path(_config['dirs'][0])


def get_all_dirs():
    """Get all dirs."""
    return list(map(_normalize_path, _config['dirs']))


def get_extra_analyzer_dir():
    """Get extra analyzer dir."""
    extra_analyzer_dir = _config['extra_analyzer_dir']
    if extra_analyzer_dir:
        return _normalize_path(extra_analyzer_dir)


def get_disabled_analyzers():
    """Get disabled analyzers."""
    return _config['disabled_analyzers']


def get_max_concurrent():
    """Get max concurrent number."""
    return _config['max_concurrent']


def get_max_retry():
    """Get max retry number."""
    return _config['max_retry']


def get_proxy():
    """Get extra analyzer dir."""
    return _config['proxy']


def get_customization(analyzer_name):
    """Get user setting for an analyzer."""
    return _config.get('customization', {}).get(analyzer_name, {})


_init()
