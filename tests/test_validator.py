import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from validator import validate


class ValidatorTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.path = Path(directory.name) / "types.xml"

    def check(self, xml):
        self.path.write_text(xml, encoding="utf-8-sig")
        return validate(self.path)

    def test_valid_and_partial_entries(self):
        self.assertEqual(self.check(
            '<types><type name="ItemA"><nominal>10</nominal><min>5</min>'
            '<quantmin>-1</quantmin><quantmax>-1</quantmax></type>'
            '<type name="ItemB"><lifetime>300</lifetime></type></types>'
        ), ([], []))

    def test_malformed_xml_wrong_root_and_doctype(self):
        for xml in ("<types>", "<events/>", '<!DOCTYPE types SYSTEM "local.dtd"><types/>'):
            with self.subTest(xml=xml):
                self.assertTrue(self.check(xml)[0])

    def test_missing_file(self):
        self.assertTrue(validate(self.path)[0])

    def test_duplicates_and_invalid_values(self):
        errors, warnings = self.check(
            '<types><type name="X"><quantmin>101</quantmin><cost>bad</cost>'
            '<min>10</min><nominal>1</nominal></type><type name="X"/>'
            '<type/><type name="Y"><quantmin>20</quantmin><quantmax>10</quantmax>'
            '<restock>-5</restock><cost>1</cost><cost>2</cost></type></types>'
        )
        self.assertEqual(len(errors), 7)
        self.assertEqual(len(warnings), 1)

    def test_cli_exit_code_and_read_only_behavior(self):
        xml = '<types><type name="A"><nominal>0</nominal><min>2</min></type></types>'
        self.path.write_text(xml, encoding="utf-8")
        cli = Path(__file__).resolve().parents[1] / "validator.py"
        result = subprocess.run([sys.executable, cli, self.path], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertIn("WARNING", result.stderr)
        self.assertEqual(self.path.read_text(), xml)
        self.path.write_text("<types>", encoding="utf-8")
        result = subprocess.run([sys.executable, cli, self.path], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn("ERROR", result.stderr)
