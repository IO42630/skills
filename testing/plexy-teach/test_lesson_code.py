import ast
import unittest
from html.parser import HTMLParser

from grade_runs import CONFIGS, EVAL_DIR, ROOT, RUNS


class CodeParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.in_pre = False
        self.parts = []
        self.blocks = []

    def handle_starttag(self, tag, attrs):
        if tag == "pre":
            self.in_pre = True
            self.parts = []
        if self.in_pre and tag == "span" and "code-line" in dict(attrs).get("class", "").split():
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag == "pre":
            self.blocks.append("".join(self.parts))
            self.in_pre = False

    def handle_data(self, data):
        if self.in_pre:
            self.parts.append(data)


def lesson_function(html):
    parser = CodeParser()
    parser.feed(html)
    candidates = []
    for block in parser.blocks:
        if not block.lstrip().startswith("def "):
            continue
        try:
            definitions = ast.parse(block).body
        except SyntaxError:
            continue
        for definition in definitions:
            if isinstance(definition, ast.FunctionDef) and any(
                isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == definition.name
                for node in ast.walk(definition)
            ):
                candidates.append(definition)
    if len(candidates) != 1:
        raise ValueError("Expected exactly one displayed recursive function.")
    function = candidates[0]
    allowed = (
        ast.FunctionDef, ast.arguments, ast.arg, ast.Assign, ast.AugAssign,
        ast.For, ast.If, ast.Return, ast.Name, ast.Constant, ast.Call,
        ast.Load, ast.Store, ast.Add, ast.UnaryOp, ast.Not,
    )
    for node in ast.walk(function):
        if not isinstance(node, allowed):
            raise ValueError(f"Unexpected operation in the teaching function: {type(node).__name__}")
        if isinstance(node, ast.Call) and (not isinstance(node.func, ast.Name) or node.func.id not in [function.name, "isinstance"]):
            raise ValueError("Only recursion and the list type check may be called.")
    module = ast.Module(body=[function], type_ignores=[])
    namespace = {"__builtins__": {"isinstance": isinstance, "list": list}}
    exec(compile(module, "<displayed lesson function>", "exec"), namespace)
    return namespace[function.name]


class LessonCodeTests(unittest.TestCase):
    def test_flat_intro_does_not_replace_recursive_function(self):
        html = """<pre>def flat_total(items):
    total = 0
    for item in items:
        total += item
    return total</pre>
<pre>def exercise(items):
    total += ???</pre>
<pre>def nested_total(items):
    total = 0
    for item in items:
        if isinstance(item, list):
            total += nested_total(item)
        else:
            total += item
    return total</pre>"""
        self.assertEqual(9, lesson_function(html)([2, [3, 4]]))

    def test_nonrecursive_function_is_not_accepted(self):
        with self.assertRaisesRegex(ValueError, "exactly one displayed recursive function"):
            lesson_function("<pre>def flat_total(items):\n    return 0</pre>")

    def test_incomplete_recursive_function_is_not_accepted(self):
        with self.assertRaisesRegex(ValueError, "exactly one displayed recursive function"):
            lesson_function("<pre>def nested_total(items):\n    return nested_total(???)</pre>")

    def test_multiple_recursive_functions_are_not_silently_selected(self):
        html = "<pre>def total(items):\n    return total(items)</pre>" * 2
        with self.assertRaisesRegex(ValueError, "exactly one displayed recursive function"):
            lesson_function(html)

    def test_all_six_displayed_functions(self):
        cases = [
            ([], 0),
            ([2, [3, 4]], 9),
            ([1, [2, [3]], 4], 10),
            ([1, [2, []], 3], 6),
            ([2, [3, [4], 1], 5], 15),
            ([2, [3, [4]], 5], 14),
            ([[], [[]]], 0),
            ([-2, [5]], 3),
            ([1, [2, [], [3]], 4], 10),
        ]
        for iteration_number in [2, 3, 4]:
            eval_dir = ROOT / f"iteration-{iteration_number}" / EVAL_DIR.name
            for config in CONFIGS:
                for number in RUNS:
                    path = eval_dir / config / f"run-{number}/outputs/lesson.html"
                    function = lesson_function(path.read_text())
                    for items, expected in cases:
                        with self.subTest(iteration=iteration_number, configuration=config, run=number, items=items):
                            self.assertEqual(expected, function(items))


if __name__ == "__main__":
    unittest.main()