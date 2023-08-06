"""Websauna Jinja2 extension to generate secrets."""
import binascii
import os

from jinja2 import nodes
from jinja2.ext import Extension
from jinja2.parser import Parser


# __all__ = ['SecretExtension']


def secret() -> str:
    """Generate a random seed

    :returns: Random seed to be used in Websauna projects.
    """
    return binascii.hexlify(os.urandom(20)).decode('utf-8')


class SecretExtension(Extension):
    """Jinja 2 Extension to generate a random seed for projects."""

    tags = set(['secret'])

    def _secret(self, *args) -> str:
        """Return a secret.

        :returns: Random seed to be used in Websauna projects.
        """
        return secret()

    def parse(self, parser: Parser) -> nodes:
        """Parse the current expression and return a node with the secret.

        :returns: A node.
        """
        lineno = next(parser.stream).lineno
        node = parser.parse_expression()
        call_method = self.call_method('_secret', [node], lineno=lineno)
        return nodes.Output([call_method], lineno=lineno)
