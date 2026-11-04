"""Layout helpers for the exercise notebooks: the Lab layout and the code listing of the reference panel.

The exercise notebooks import these functions. You can read and change them.
When you save this file, marimo reruns the notebook cells that use a changed function.

The presenter generates this file from tutorials.py, so the code matches the presentation.
"""
import inspect
import textwrap
import marimo as mo


def source_of(*functions):
    return "\n\n".join(textwrap.dedent(inspect.getsource(getattr(f, "func", f))).strip() for f in functions)


def input_output(controls, output):
    inputs = mo.vstack(controls, align="stretch", gap=1.5)
    return mo.Html(f'<div class="experiment-layout"><div class="experiment-inputs" role="group" aria-label="Inputs">{inputs}</div>'
                   f'<div class="experiment-output" role="group" aria-label="Output">{mo.as_html(output)}</div></div>')
