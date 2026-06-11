from pathlib import Path

import pytest

from unit_converter.domain.converter import Converter
from unit_converter.infrastructure.config_loader import load_registry

CONFIG_PATH = Path("config/units.json")


@pytest.fixture
def registry():
    return load_registry(CONFIG_PATH)


@pytest.fixture
def converter(registry):
    return Converter(registry)
