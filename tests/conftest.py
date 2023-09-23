"""
This module is used to provide configuration, fixtures, and plugins for pytest.

It may be also used for extending doctest's context:
1. https://docs.python.org/3/library/doctest.html
2. https://docs.pytest.org/en/latest/doctest.html
"""

import random
from typing import cast

import pytest

pytest_plugins = [
    # Should be the first custom one:
    'plugins.django_settings',
    # TODO: add your own plugins here!
    'plugins.custom_types',
    'plugins.common',
    'plugins.identity.registration_data',
    'plugins.identity.created_user',
    'plugins.identity.external_api',
    'plugins.pictures.favourite_picture',
]


def pytest_configure(config: pytest.Config) -> None:
    """Configuring seed based on the command line option.

    Options:
        default: use default random seed
        last: use the last used random seed
    """
    seed_value = config.getoption('randomly_seed')
    default_seed = random.Random().getrandbits(32)

    if seed_value == 'last':
        seed = cast(pytest.Cache, config.cache).get(
            'randomly_seed',
            default_seed,
        )
    elif seed_value == 'default':
        seed = default_seed
    else:
        seed = seed_value

    cast(pytest.Cache, config.cache).set('randomly_seed', seed)
    config.option.randomly_seed = seed
