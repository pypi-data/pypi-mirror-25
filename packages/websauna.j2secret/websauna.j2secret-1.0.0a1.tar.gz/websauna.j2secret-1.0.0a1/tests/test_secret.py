"""Test SecretExtension."""
import pytest

from jinja2 import Environment


@pytest.fixture
def environment() -> Environment:
    """Return an environment with our extension already loaded."""
    return Environment(
        extensions=['websauna.j2secret.SecretExtension']
    )


def test_secret(environment):
    """Test extension tag."""
    template = environment.from_string(r'{% secret() %}')
    result = template.render()
    assert isinstance(result, str)
    assert len(result) == 40
