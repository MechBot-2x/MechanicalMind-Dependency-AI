"""Tests del sistema de plugins/registro (V3)."""

import tempfile
import unittest
from pathlib import Path

from mechanicalmind_ai.core.models import Package
from mechanicalmind_ai.core.plugins import (
    Parser,
    list_parsers,
    register_parser,
    registry,
    unregister_parser,
)


class TestPluginRegistry(unittest.TestCase):

    def test_builtin_parsers_registered(self):
        parsers = list_parsers()
        names = {p.name for p in parsers}
        self.assertIn("python-requirements", names)
        self.assertIn("python-pyproject", names)
        self.assertIn("node-package-json", names)
        self.assertIn("java-maven", names)
        self.assertIn("docker-dockerfile", names)
        self.assertIn("go-mod", names)
        self.assertIn("rust-cargo", names)
        self.assertIn("ruby-gemfile", names)
        self.assertIn("php-composer", names)
        self.assertIn("swift-package", names)

    def test_register_and_unregister_custom(self):
        def fake_parse(path):
            return [Package(name="fake", version="1.0", ecosystem="test", source=str(path))]

        p = Parser(
            name="test-parser",
            ecosystem="test",
            description="test only",
            filename_patterns=("test.file",),
            parse=fake_parse,
        )
        register_parser(p, replace=True)
        self.assertIsNotNone(registry.get("test-parser"))
        unregister_parser("test-parser")
        self.assertIsNone(registry.get("test-parser"))

    def test_register_duplicate_raises(self):
        def fake_parse(path):
            return []

        p = Parser(
            name="dup-test",
            ecosystem="test",
            description="dup",
            filename_patterns=("dup.file",),
            parse=fake_parse,
        )
        register_parser(p, replace=True)
        with self.assertRaises(ValueError):
            register_parser(p, replace=False)
        unregister_parser("dup-test")

    def test_registry_list_sorted(self):
        parsers = list_parsers()
        keys = [(p.ecosystem, p.name) for p in parsers]
        self.assertEqual(keys, sorted(keys))


if __name__ == "__main__":
    unittest.main()
