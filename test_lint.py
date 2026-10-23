import json
import tempfile
import unittest
from pathlib import Path

from lint import lint


def make(files):
    root = Path(tempfile.mkdtemp())
    for path, text in files.items():
        p = root / path
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)
    return root


class LintTest(unittest.TestCase):
    def test_clean_tree(self):
        root = make({"skills/a/SKILL.md": "# a", "docs/x.md": "use [[skill:a]]"})
        self.assertEqual(lint(root), [])

    def test_missing_skill(self):
        root = make({"skills/a/SKILL.md": "# a", "docs/x.md": "use [[skill:b]]"})
        self.assertEqual(lint(root), ["docs/x.md:1: unknown skill 'b'"])

    def test_alias_resolves(self):
        root = make({"skills/a/SKILL.md": "# a", "docs/x.md": "[[skill:old]]",
                     "registry.json": json.dumps({"aliases": {"old": "a"}})})
        self.assertEqual(lint(root), [])

    def test_alias_cycle_is_reported(self):
        root = make({"skills/a/SKILL.md": "# a",
                     "registry.json": json.dumps({"aliases": {"x": "y", "y": "x"}})})
        self.assertEqual(len(lint(root)), 2)

    def test_alias_shadowing_skill(self):
        root = make({"skills/a/SKILL.md": "# a",
                     "registry.json": json.dumps({"aliases": {"a": "a"}})})
        self.assertIn("shadows", lint(root)[0])

    def test_example(self):
        problems = lint(Path(__file__).parent / "example")
        self.assertEqual(len(problems), 2)


if __name__ == "__main__":
    unittest.main()
