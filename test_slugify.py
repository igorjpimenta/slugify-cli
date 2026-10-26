"""Tests for slugify.py — stdlib only (unittest + subprocess).

Covers: case folding, accents/unicode, emoji, punctuation-only,
empty result, very long input, stdin vs args, exit codes.
Run: python3 -m unittest test_slugify -v
"""
import subprocess
import sys
import unittest

from slugify import slugify


def run_cli(args=None, stdin_data=None):
    cmd = [sys.executable, "slugify.py"] + (args or [])
    return subprocess.run(
        cmd, input=stdin_data, capture_output=True, text=True
    )


class TestSlugifyUnit(unittest.TestCase):
    def test_case_folding_and_join(self):
        self.assertEqual(slugify("Hello World"), "hello-world")

    def test_accents_french(self):
        self.assertEqual(
            slugify("Café au lait — crème brûlée"),
            "cafe-au-lait-creme-brulee",
        )

    def test_accents_german(self):
        self.assertEqual(
            slugify("Über API Gateway 2024"), "uber-api-gateway-2024"
        )

    def test_accents_portuguese_spanish(self):
        self.assertEqual(slugify("São Paulo"), "sao-paulo")
        self.assertEqual(slugify("niño año"), "nino-ano")

    def test_repeated_separators_collapse(self):
        self.assertEqual(slugify("  Hello---World!!  "), "hello-world")
        self.assertEqual(slugify("a___b   c---d"), "a-b-c-d")

    def test_underscore_and_trim(self):
        self.assertEqual(slugify("foo_bar"), "foo-bar")
        self.assertEqual(slugify("---hello---"), "hello")

    def test_numbers_kept(self):
        self.assertEqual(slugify("Version 2.0"), "version-2-0")

    def test_emoji_stripped_mid_string(self):
        self.assertEqual(slugify("Hello 🌍 World"), "hello-world")

    def test_emoji_only_is_empty(self):
        self.assertEqual(slugify("🌍🎉"), "")

    def test_punctuation_only_is_empty(self):
        self.assertEqual(slugify("!!!"), "")

    def test_empty_and_whitespace_is_empty(self):
        self.assertEqual(slugify(""), "")
        self.assertEqual(slugify("   "), "")

    def test_cjk_runs_collapse(self):
        # non-latin letters without ascii decomposition become separators
        self.assertEqual(slugify("hello中文world"), "hello-world")

    def test_very_long_input(self):
        long_in = "A " * 10000  # 20000 chars
        out = slugify(long_in)
        self.assertEqual(len(out), 19999)
        self.assertTrue(out.startswith("a-a-a-"))
        self.assertNotIn(" ", out)
        self.assertNotIn("--", out)


class TestSlugifyCLI(unittest.TestCase):
    def test_args_joined(self):
        p = run_cli(["Hello", "World"])
        self.assertEqual((p.returncode, p.stdout.strip()), (0, "hello-world"))

    def test_stdin(self):
        p = run_cli(stdin_data="Hello via stdin\n")
        self.assertEqual((p.returncode, p.stdout.strip()), (0, "hello-via-stdin"))

    def test_args_win_over_stdin(self):
        p = run_cli(["From Args"], stdin_data="from stdin")
        self.assertEqual((p.returncode, p.stdout.strip()), (0, "from-args"))

    def test_punctuation_only_exit2(self):
        p = run_cli(stdin_data="!!!\n")
        self.assertEqual(p.returncode, 2)
        self.assertEqual(p.stdout.strip(), "")
        self.assertIn("empty slug", p.stderr)

    def test_emoji_only_exit2(self):
        p = run_cli(stdin_data="🌍🎉\n")
        self.assertEqual(p.returncode, 2)
        self.assertIn("empty slug", p.stderr)

    def test_empty_stdin_exit2(self):
        p = run_cli(stdin_data="")
        self.assertEqual(p.returncode, 2)
        self.assertIn("empty slug", p.stderr)

    def test_wrapper_executable(self):
        p = subprocess.run(
            ["./slugify", "Hello World"],
            capture_output=True, text=True,
        )
        self.assertEqual((p.returncode, p.stdout.strip()), (0, "hello-world"))


if __name__ == "__main__":
    unittest.main()
