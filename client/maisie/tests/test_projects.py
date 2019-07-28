from click.testing import CliRunner
from maisie.cli.projects import *
import unittest


class TestProjects(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestProjects, self).__init__(*args, **kwargs)
        self.runner = CliRunner()

    def asserts_for_correct_invokes(self, result):
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.exception, None)

    def test_add(self):
        result = self.runner.invoke(
            cli=add,
            args=[
                "-n",
                "some_name",
                "-d",
                "some_description",
                "-git",
                "https://github.com/maisie-dev/maisie",
            ],
        )
        self.asserts_for_correct_invokes(result)

    def test_rm(self):
        pass

    def test_ls(self):
        result = self.runner.invoke(cli=ls)
        self.asserts_for_correct_invokes(result)


if __name__ == "__main__":
    unittest.main()
