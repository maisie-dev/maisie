from click.testing import CliRunner
from maisie.cli.models import *
import unittest


class TestModels(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestModels, self).__init__(*args, **kwargs)
        self.runner = CliRunner()

    def asserts_for_correct_invokes(self, result):
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.exception, None)

    def test_upload(self):
        runner = CliRunner()
        result = runner.invoke(
            cli=upload,
            args=[
                "-n",
                "some_name",
                "-f",
                "params.json",
                "-hp",
                "params.json",
                "-p",
                "params.json",
                "-m",
                "params.json",
                "-d",
                "some_data_name",
            ],
        )
        self.asserts_for_correct_invokes(result)

    def test_ls(self):
        runner = CliRunner()
        result = runner.invoke(cli=ls)
        self.asserts_for_correct_invokes(result)

    def test_download(self):
        runner = CliRunner()
        result = runner.invoke(cli=download, args=["-id", "239"])
        self.asserts_for_correct_invokes(result)
        self.assertEqual(result.output, "Model downloaded successfully\n")


if __name__ == "__main__":
    unittest.main()
