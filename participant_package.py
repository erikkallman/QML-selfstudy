"""Build the participant ZIP, the exercise notebooks, and their support modules from the main notebook."""
import ast
import builtins
import copy
import hashlib
import io
import json
from pathlib import Path
import textwrap
import zipfile


ROOT = Path(__file__).resolve().parent
INPUT_FILES = (
    "tutorials.py", "workshop.css", "requirements.txt",
    "verify_tutorials.py", "serve.py", "participant_package.py", "PARTICIPANTS.md",
    "figure_style.py", "research_generation.py", "research_generation_figures.py",
    "research_memory.py", "research_memory_figures.py",
)
# tutorials.py loads the text of the research chapters from these files.
CHAPTER_FOLDER = "chapters"
EXERCISES = {
    "exercise_1.py": ("Circuit exercise", "exercise_one", "exercise_one_page", "circuit_functions"),
    "exercise_2.py": ("Training exercise", "exercise_two", "exercise_two_page", "training_functions"),
}
# The exercises import their supplied code from these generated modules.
# Each entry: the tutorials.py cells that hold the functions, then the module docstring.
SUPPORT_MODULES = {
    "exercise_circuits.py": (
        ("circuit_drawing", "circuit_functions", "training_functions"),
        "Supplied code for the two exercises: the circuits, the loss function, and the circuit drawing.\n\n"
        "The exercise notebooks import these functions. You can read and change them.\n"
        "When you save this file, marimo reruns the notebook cells that use a changed function.\n\n"
        "The presenter generates this file from tutorials.py, so the code matches the presentation.",
    ),
    "exercise_layout.py": (
        ("layouts",),
        "Layout helpers for the exercise notebooks: the Lab layout and the code listing of the reference panel.\n\n"
        "The exercise notebooks import these functions. You can read and change them.\n"
        "When you save this file, marimo reruns the notebook cells that use a changed function.\n\n"
        "The presenter generates this file from tutorials.py, so the code matches the presentation.",
    ),
}
TASKS = {
    "exercise_1.py": {
        "function": "encoding_circuit",
        "cell": "edit_encoding",
        "arguments": "qml",
        "brief": r"""# Exercise 1: change the input rotation

## Your task (six minutes)

The notebook already contains the circuit, the measurement, and the plots.
You change one gate: the input rotation in `encoding_circuit`.
That function is in the code cell directly below these instructions.
The *$Z$ output* is the mean value of a $Z$ measurement on the qubit.

1. Click the Run button at the bottom right. The check cell, below the code cell, shows the $Z$ output.
2. Predict how the $Z$ output changes if the input rotation is $R_Y$ instead of $R_X$.
3. In the marked line, replace `qml.RX` with `qml.RY`. Keep `x` and `wires=0` as they are.
4. Click Run again. Read the new value in the check cell, then look at the circuit drawing and the curve below it.
5. Explain why the $Z$ output changed. Hint: $R_X$ and $R_Y$ rotate the qubit about different axes.
6. Change `qml.RY` back to `qml.RX`, and click Run again.

The check cell always uses the same settings: input $x=\pi/3$, angles $\theta=(\pi/2,\pi/3,\pi/4)$, and the $Z$ measurement.
With $R_X$, it shows $-0.5$.
After the check, try other values with the sliders below it.

## Algorithm guide

```text
# Already in the notebook: preparation, fixed gates, measurement, plots.
prepare the qubit in the state |0>
apply the input rotation RX(x)    # YOUR EDIT: change RX to RY below
apply the fixed gates RZ, RY, RZ with the angles theta
measure the mean Z value
compare it with the value before your edit
change RY back to RX
```

## Edit this function
""",
        "comments": [
            "# YOUR EDIT: replace RX with RY. Keep x and wires=0 as they are.",
            "# Run this cell, read the check below, then change RY back to RX.",
        ],
        "checkpoint": '''@app.cell(hide_code=True)
def check_encoding(mo, onp, quantum_model):
    _angles = [onp.pi / 2, onp.pi / 3, onp.pi / 4]
    fixed_output = float(quantum_model(onp.pi / 3, _angles, "Z"))
    if onp.isclose(fixed_output, -0.5):
        check_status = "This is the value with $R_X$. Predict the value with $R_Y$, then edit the marked line."
    elif onp.isclose(fixed_output, 0.25):
        check_status = "This is the value with $R_Y$. Explain why it differs from $-0.5$, then change `qml.RY` back to `qml.RX`."
    else:
        check_status = "This value matches neither $R_X$ ($-0.5$) nor $R_Y$ ($0.25$). Check the edited line: the gate name, the argument `x`, and `wires=0`."
    mo.md(f"## Check\\n\\n$Z$ output at the check settings: `{fixed_output:.6f}`.\\n\\n{check_status}")
    return check_status, fixed_output''',
        "reference": ("trainable_block", "quantum_model"),
        # quantum_model calls encoding_circuit, the edited function, so it stays in the notebook.
        "notebook_functions": ("quantum_model",),
    },
    "exercise_2.py": {
        "function": "fit_regression",
        "cell": "edit_training",
        "arguments": "np, qml, regression_loss",
        "brief": r"""# Exercise 2: freeze and restore learning

## Your task (six minutes)

The notebook already contains the data, the circuit, the loss function, the starting weights, and the plots.
You change one assignment: the weight update in `fit_regression`.
That function is in the code cell directly below these instructions.
Freezing the weights means keeping them at their starting values during training.

1. Click the Run button at the bottom right. The check cell, below the code cell, shows the training loss before the first update and after 100 updates.
2. Predict the loss curve if the weights never change.
3. Replace the marked three-line assignment `weights = optimizer.step(...)` with `weights = weights`.
4. Click Run again. If the edit is right, the check cell reports that the weights keep their starting values and that the loss stays constant.
5. Open "Restore the optimizer assignment" in the check cell. Copy those three lines back in place of `weights = weights`, and click Run. The loss falls again.

Change nothing else in the function. The check cell always uses the learning rate $\eta=0.2$ and 100 updates.
After the check, try other settings with the sliders and the checkbox next to the plots further down.

## Algorithm guide

```text
# Already in the notebook: data, circuit, loss function, starting weights.
set the weights to their starting values
record the loss
repeat for the requested number of updates:
    if updates are enabled:
        compute new weights from the gradient of the loss
        # YOUR EDIT: keep the current weights instead
    record the loss with the current weights
compare the last loss with the first loss
restore the gradient update      # then check that the loss falls again
```

## Edit this function
""",
        "comments": [
            "# YOUR EDIT: replace this whole three-line assignment with:",
            "# weights = weights",
            "# Keep the history.append line below. It records the loss with frozen weights.",
        ],
        "checkpoint": '''@app.cell(hide_code=True)
def check_training(fit_regression, mo, onp):
    _, _, check_weights, check_history = fit_regression(rate=0.2, steps=100, enabled=True)
    if onp.allclose(check_history, check_history[0]) and onp.allclose(check_weights, [0.3, 0.7]):
        check_status = "The weights keep their starting values, so the loss stays constant. Now restore the optimizer assignment, so that the circuit learns again."
    elif check_history[-1] < 1e-8:
        check_status = "The loss falls below $10^{-8}$, so the circuit learns. Predict the loss with frozen weights, then edit the marked assignment."
    else:
        check_status = "The loss neither stays constant nor falls below $10^{-8}$. Check the edited assignment, and undo any other change in the function."
    mo.vstack([
        mo.md(f"## Check\\n\\nTraining loss: `{check_history[0]:.6f}` before the first update, `{check_history[-1]:.6g}` after 100 updates.\\n\\n{check_status}"),
        mo.accordion({"Restore the optimizer assignment": mo.md("```python\\nweights = optimizer.step(\\n    lambda w: regression_loss(w, xs, targets), weights\\n)\\n```")}),
    ])
    return check_history, check_status, check_weights''',
        "reference": ("training_model", "regression_loss"),
        "notebook_functions": (),
    },
}


def editable_cell(lines, function, task):
    source = textwrap.dedent(cell_source(lines, function))
    tree = ast.parse(source)
    if task["function"] == "encoding_circuit":
        target = next(n for n in ast.walk(tree) if isinstance(n, ast.Expr)
                      and isinstance(n.value, ast.Call))
    else:
        target = next(n for n in ast.walk(tree) if isinstance(n, ast.Assign)
                      and isinstance(n.value, ast.Call)
                      and isinstance(n.value.func, ast.Attribute)
                      and n.value.func.attr == "step")
    code_lines = source.splitlines()
    indent = " " * target.col_offset
    code_lines[target.lineno - 1:target.lineno - 1] = [indent + line for line in task["comments"]]
    body = textwrap.indent("\n".join(code_lines), "    ")
    return (f"@app.cell\ndef {task['cell']}({task['arguments']}):\n{body}\n"
            f"    return ({task['function']},)")


def cell_source(lines, node):
    start = min([node.lineno] + [d.lineno for d in node.decorator_list])
    return "".join(lines[start - 1:node.end_lineno]).rstrip()


def free_names(statements):
    """Names that the statements read but do not define themselves."""
    loaded, defined = set(), set(dir(builtins))
    for node in (n for statement in statements for n in ast.walk(statement)):
        if isinstance(node, ast.Name):
            (loaded if isinstance(node.ctx, ast.Load) else defined).add(node.id)
        elif isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            defined.add(node.name)
        elif isinstance(node, ast.arg):
            defined.add(node.arg)
    return loaded - defined


def supplied_functions(cells):
    """Every function in the support-module cells, by name, with its cell."""
    return {f.name: (cell, f) for _, (cell_names, _) in SUPPORT_MODULES.items()
            for cell in cell_names for f in cells[cell].body if isinstance(f, ast.FunctionDef)}


def standalone_exercise(source, filename):
    """Return the exercise notebook and the supplied functions it needs from each support module."""
    title, lesson, page, functions = EXERCISES[filename]
    task = TASKS[filename]
    tree = ast.parse(source)
    cells = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
    editable = next(n for n in cells[functions].body
                    if isinstance(n, ast.FunctionDef) and n.name == task["function"])
    lines = source.splitlines(keepends=True)
    first_import = next(n.lineno for n in tree.body if isinstance(n, ast.Import))
    header = "".join(lines[:first_import - 1])
    # marimo reruns the cells that use a function from a support module when that module changes.
    assert header.count("\n# ///\n") == 1, "expected one closing line of the script header"
    header = header.replace("\n# ///\n", '\n#\n# [tool.marimo.runtime]\n# auto_reload = "autorun"\n# ///\n')
    sections = [
        header.rstrip(), "import marimo",
        '__generated_with = "0.25.2"',
        f"app = marimo.App(width='full', app_title={title!r}, css_file='workshop.css')",
        "@app.cell(hide_code=True)\ndef task_instructions(mo):\n"
        "    mo.md(r\"\"\"\n"
        + textwrap.indent(textwrap.dedent(task["brief"]).strip(), "    ")
        + "\n    \"\"\")\n    return",
        editable_cell(lines, editable, task),
        task["checkpoint"],
        "@app.cell(hide_code=True)\n"
        f"def show_experiment({page}):\n    {page}\n    return",
    ]
    # Notebook cells: imports, the functions that call the edited function, controls, and the lab.
    copied = {}
    for name in ["imports", functions, "exercise_controls", lesson]:
        node = copy.deepcopy(cells[name])
        if name == functions:
            node.body = [n for n in node.body if isinstance(n, ast.FunctionDef)
                         and n.name in task["notebook_functions"]]
            if not node.body:
                continue
            node.body.append(ast.Return(value=ast.Tuple(
                elts=[ast.Name(id=n.name, ctx=ast.Load()) for n in node.body], ctx=ast.Load())))
            node.args.args = [ast.arg(arg=n) for n in sorted(free_names(node.body))]
        if name == lesson:
            # Reuse the presentation's live lab without repeating its tutorial below the task.
            node.body = [n for n in node.body if not (isinstance(n, ast.Assign)
                         and any(isinstance(t, ast.Name) and t.id == "_story" for t in n.targets))]
            for statement in node.body:
                if (isinstance(statement, ast.Assign)
                        and any(isinstance(t, ast.Name) and t.id == page for t in statement.targets)):
                    statement.value = ast.Name(id="_lab", ctx=ast.Load())
            # Without the tutorial and the tabs, keep only the inputs the lab still uses.
            used = {n.id for n in ast.walk(node) if isinstance(n, ast.Name)}
            node.args.args = [a for a in node.args.args if a.arg in used]
        node.decorator_list = [ast.Call(
            func=ast.Attribute(value=ast.Name(id="app", ctx=ast.Load()), attr="cell", ctx=ast.Load()),
            args=[], keywords=[ast.keyword(arg="hide_code", value=ast.Constant(True))],
        )]
        copied[name] = node
    references = ", ".join(task["reference"])
    reference_label = ("Code of the circuit and the loss function" if filename == "exercise_2.py"
                       else "Code of the fixed gates and the measurement")
    reference_cell = (
        "@app.cell(hide_code=True)\n"
        f"def supplied_reference(mo, source_of, {references}):\n"
        f"    mo.accordion({{{reference_label!r}: "
        f"mo.md('```python\\n' + source_of({references}) + '\\n```')}})\n"
        "    return"
    )
    # The controls cell defines the sliders of both exercises; keep the ones this exercise uses.
    others = [node for name, node in copied.items() if name not in ("imports", "exercise_controls")]
    others += [ast.parse(section) for section in sections + [reference_cell]]
    wanted = {n.id for tree in others for n in ast.walk(tree) if isinstance(n, ast.Name)}
    controls = copied["exercise_controls"]
    controls.body = [s for s in controls.body if not (isinstance(s, ast.Assign) and all(
        isinstance(t, ast.Name) and t.id not in wanted for t in s.targets))]
    for statement in controls.body:
        if isinstance(statement, ast.Return):
            statement.value.elts = [e for e in statement.value.elts if e.id in wanted]
    trees = [node for name, node in copied.items() if name != "imports"]
    trees += [ast.parse(section) for section in sections + [reference_cell]]
    used = {n.id for tree in trees for n in ast.walk(tree) if isinstance(n, ast.Name)}
    # Supplied functions the notebook uses, plus the supplied functions those call.
    supplied = supplied_functions(cells)
    kept_here = set(task["notebook_functions"]) | {task["function"]}
    needed = {name for name in used if name in supplied and name not in kept_here}
    while True:
        more = {n for name in needed for n in free_names([supplied[name][1]])
                if n in supplied and n not in kept_here} - needed
        if not more:
            break
        needed |= more
    by_module = {module: sorted(n for n in needed if supplied[n][0] in cell_names)
                 for module, (cell_names, _) in SUPPORT_MODULES.items()}
    # The imports cell: standard imports the notebook uses, then the support modules.
    kept = []
    for statement in copied["imports"].body:
        if isinstance(statement, (ast.Import, ast.ImportFrom)):
            statement.names = [a for a in statement.names if (a.asname or a.name.split(".")[0]) in used]
            if not statement.names:
                continue
        if isinstance(statement, ast.Return):
            continue
        kept.append(statement)
    imported = [a.asname or a.name.split(".")[0] for s in kept
                if isinstance(s, (ast.Import, ast.ImportFrom)) for a in s.names]
    for module, function_names in by_module.items():
        if function_names:
            kept.append(ast.ImportFrom(module=Path(module).stem, level=0,
                                       names=[ast.alias(name=n) for n in function_names]))
            imported += function_names
    kept.append(ast.Return(value=ast.Tuple(
        elts=[ast.Name(id=n, ctx=ast.Load()) for n in sorted(imported)], ctx=ast.Load())))
    copied["imports"].body = kept
    for node in copied.values():
        ast.fix_missing_locations(node)
        sections.append(ast.unparse(node))
    sections.append(reference_cell)
    sections.append('if __name__ == "__main__":\n    app.run()')
    result = "\n\n\n".join(sections) + "\n"
    compile(result, filename, "exec")
    return result.encode(), by_module


def support_module(source, module, function_names):
    """Copy the named functions' source text from tutorials.py, with the imports they use."""
    tree = ast.parse(source)
    cells = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
    lines = source.splitlines(keepends=True)
    cell_names, docstring = SUPPORT_MODULES[module]
    functions = [f for cell in cell_names for f in cells[cell].body
                 if isinstance(f, ast.FunctionDef) and f.name in function_names]
    used = free_names(functions)
    imports = []
    for statement in cells["imports"].body:
        if isinstance(statement, (ast.Import, ast.ImportFrom)):
            names = [a for a in statement.names if (a.asname or a.name.split(".")[0]) in used]
            if names:
                statement = copy.deepcopy(statement)
                statement.names = names
                imports.append(ast.unparse(statement))
    bodies = [textwrap.dedent(cell_source(lines, f)) for f in functions]
    result = ('"""' + docstring + '\n"""\n' + "\n".join(imports) + "\n\n\n"
              + "\n\n\n".join(bodies) + "\n")
    compile(result, module, "exec")
    return result.encode()


def build_files(root=ROOT):
    root = Path(root)
    files = {name: (root / name).read_bytes() for name in INPUT_FILES}
    for path in sorted((root / CHAPTER_FOLDER).rglob("*.md")):
        files[path.relative_to(root).as_posix()] = path.read_bytes()
    files["README.md"] = files["PARTICIPANTS.md"]
    for name, content in files.items():
        if name.endswith(".py"):
            compile(content, name, "exec")
    source = files["tutorials.py"].decode()
    needed = {module: set() for module in SUPPORT_MODULES}
    for filename in EXERCISES:
        files[filename], by_module = standalone_exercise(source, filename)
        for module, function_names in by_module.items():
            needed[module] |= set(function_names)
    for module, function_names in needed.items():
        files[module] = support_module(source, module, function_names)
    manifest = {
        "format": 1,
        "main_notebook": "tutorials.py",
        "exercises": list(EXERCISES),
        "sha256": {name: hashlib.sha256(content).hexdigest() for name, content in sorted(files.items())},
    }
    files["manifest.json"] = (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode()
    return files


def build_archive(root=ROOT):
    output = io.BytesIO()
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, content in sorted(build_files(root).items()):
            member = zipfile.ZipInfo("qml-dojo-participants/" + name, date_time=(2026, 1, 1, 0, 0, 0))
            member.compress_type = zipfile.ZIP_DEFLATED
            member.external_attr = 0o100644 << 16
            archive.writestr(member, content)
    return output.getvalue()


if __name__ == "__main__":
    destination = ROOT / "participants.zip"
    destination.write_bytes(build_archive())
    print(f"Wrote {destination.name} ({destination.stat().st_size:,} bytes)")
    directory = ROOT.parent / "participants"
    directory.mkdir(exist_ok=True)
    files = build_files()
    # Chapter files can be renamed or removed; drop the ones the build no longer contains.
    for path in (directory / CHAPTER_FOLDER).rglob("*.md"):
        if path.relative_to(directory).as_posix() not in files:
            path.unlink()
    for name, content in files.items():
        (directory / name).parent.mkdir(parents=True, exist_ok=True)
        (directory / name).write_bytes(content)
    print(f"GitHub-ready files: {directory}")
