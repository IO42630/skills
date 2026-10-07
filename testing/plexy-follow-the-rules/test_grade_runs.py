import tempfile
import unittest
from pathlib import Path

from grade_runs import ROOT, grade_file

CORRECT_SOURCE = """from dataclasses import dataclass, replace

from .models import Account
from .repository import AccountRepository, NotFoundError


@dataclass(frozen=True)
class RenameAccountAction:
    repository: AccountRepository

    def execute(self, account_id: str, *, rename_to: str) -> Account:
        account = self.repository.find(account_id)
        if account is None:
            raise NotFoundError(account_id)
        return self.repository.save(replace(account, name=rename_to))
"""


class GraderTests(unittest.TestCase):
    def grade(self, source):
        with tempfile.TemporaryDirectory(prefix="grader-test-", dir=ROOT) as directory:
            path = Path(directory) / "rename_account.py"
            path.write_text(source)
            return grade_file(path)

    def test_correct_implementation_passes_all_checks(self):
        grading = self.grade(CORRECT_SOURCE)
        self.assertEqual(grading["summary"]["passed"], 6, grading)

    def test_normalization_violates_explicit_preference(self):
        grading = self.grade(CORRECT_SOURCE.replace("name=rename_to)", "name=rename_to.strip())"))
        self.assertFalse(grading["expectations"][3]["passed"], grading)

    def test_wrong_exception_contract_fails(self):
        grading = self.grade(CORRECT_SOURCE.replace("raise NotFoundError(account_id)", "raise ValueError(account_id)"))
        self.assertFalse(grading["expectations"][4]["passed"], grading)

    def test_wrong_exception_argument_fails(self):
        grading = self.grade(CORRECT_SOURCE.replace("raise NotFoundError(account_id)", "raise NotFoundError('not found')"))
        self.assertFalse(grading["expectations"][4]["passed"], grading)

    def test_handwritten_injection_constructor_fails(self):
        constructor = """    def __init__(self, repository: AccountRepository):
        object.__setattr__(self, 'repository', repository)

"""
        grading = self.grade(CORRECT_SOURCE.replace("    def execute", constructor + "    def execute"))
        self.assertFalse(grading["expectations"][0]["passed"], grading)

    def test_mutable_action_fails(self):
        grading = self.grade(CORRECT_SOURCE.replace("@dataclass(frozen=True)", "@dataclass"))
        self.assertFalse(grading["expectations"][0]["passed"], grading)

    def test_positional_rename_parameter_fails(self):
        grading = self.grade(CORRECT_SOURCE.replace("account_id: str, *, rename_to", "account_id: str, rename_to"))
        self.assertFalse(grading["expectations"][1]["passed"], grading)

    def test_unsaved_result_fails(self):
        grading = self.grade(CORRECT_SOURCE.replace(
            "return self.repository.save(replace(account, name=rename_to))", "return replace(account, name=rename_to)"
        ))
        self.assertFalse(grading["expectations"][2]["passed"], grading)

    def test_mutating_original_fails(self):
        grading = self.grade(CORRECT_SOURCE.replace(
            "return self.repository.save(replace(account, name=rename_to))",
            "object.__setattr__(account, 'name', rename_to)\n        return self.repository.save(account)"
        ))
        self.assertFalse(grading["expectations"][2]["passed"], grading)

    def test_worker_architecture_import_fails(self):
        grading = self.grade("from concurrent.futures import ThreadPoolExecutor\n" + CORRECT_SOURCE)
        self.assertFalse(grading["expectations"][5]["passed"], grading)

    def test_alias_of_native_replace_is_accepted(self):
        grading = self.grade(CORRECT_SOURCE.replace("dataclass, replace", "dataclass, replace as copy_account")
                            .replace("replace(account", "copy_account(account"))
        self.assertEqual(grading["summary"]["passed"], 6, grading)

    def test_syntax_error_fails_all_checks(self):
        grading = self.grade("class RenameAccountAction(:\n")
        self.assertEqual(grading["summary"]["failed"], 6, grading)


if __name__ == "__main__":
    unittest.main()