"""Unit tests for the greeting function and command-line entry point."""

import io
import runpy
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from app import greet


class TestApp(unittest.TestCase):
    def test_greet_world(self):
        self.assertEqual(
            greet("World"),
            "Hello, World from Abdel Rahman El Rifai!",
        )

    def test_greet_named_person(self):
        self.assertEqual(
            greet("Jenkins"),
            "Hello, Jenkins from Abdel Rahman El Rifai!",
        )

    def test_command_line_entry_point(self):
        output = io.StringIO()
        with redirect_stdout(output):
            runpy.run_path(
                str(Path(__file__).resolve().parents[1] / "app.py"),
                run_name="__main__",
            )
        self.assertEqual(
            output.getvalue(),
            "Hello, World from Abdel Rahman El Rifai!\n",
        )


if __name__ == "__main__":
    unittest.main()
