# QML workshop code

## What is in this folder

- `exercise_1.py`: the circuit exercise. You change one gate.
- `exercise_2.py`: the training exercise. You change one line of the training loop.
- `tutorials.py`: the tutorial, the full presentation. It has seven chapters:
  Start, Circuit, Training, Models, Quantum memory, Structured generation, and
  Outlook.
- `exercise_circuits.py` and `exercise_layout.py`: the supplied code that the
  exercises import. `exercise_circuits.py` holds the circuits, the loss
  function, and the circuit drawing. `exercise_layout.py` holds the layout of
  the Lab. The exercises do not need changes to them, but you can read and
  change them.
- `workshop.css`: the styles of the exercises and of `tutorials.py`.
- `research_memory.py` and `research_generation.py`: the code of the two
  research chapters. `research_memory_figures.py`,
  `research_generation_figures.py`, and `figure_style.py` draw their figures.
  The chapters show parts of this code; you can read all of it.
- `chapters/`: the text of the two research chapters, one Markdown file per
  section or step, in reading order.
- `participant_package.py`: a file that `tutorials.py` needs.
- Keep all these files in the same folder.
- `serve.py`: starts the tutorial in your browser. See "Open the tutorial".
- `requirements.txt`: the package list for the tutorial and for the fallback
  setup at the end of this file.
- `verify_tutorials.py`: only for the fallback setup.
- `manifest.json`: a SHA-256 hash of every file, to check that everyone has the same version.

## How an exercise notebook works

Both exercise notebooks have the same layout, from top to bottom:

1. The task: the goal, numbered steps, and a short pseudocode outline.
2. One code cell with the function you edit. Comments marked `YOUR EDIT` show the line to change.
3. A check cell. It runs the code at fixed settings and reports whether your edit has the expected effect.
4. Plots with sliders, to try other settings.
5. At the end, a collapsed panel with the rest of the circuit code, for reference.

The notebook contains only what you read and edit. It imports the rest of the
supplied code from `exercise_circuits.py` and `exercise_layout.py`.

Both notebooks start with working code. In each exercise, you predict the
effect of one edit, make the edit, run the code, explain the result, and then
undo the edit.

The presenter also runs both exercises on screen. If your setup does not work,
follow along there and make the predictions with everyone else.

## Before the session (about 10 minutes, needs internet)

Do these steps before you arrive. The first run downloads about 450 MB of
packages, and the venue network is shared.

1. Install uv. uv is a tool that installs Python packages, and Python itself if needed.

   macOS and Linux:

   ```sh
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

   Windows, in PowerShell:

   ```sh
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

   Then open a new terminal window, so that it finds the `uv` and `uvx` commands.

2. Download this folder as a ZIP file and extract it. On the GitHub page,
   click Code, then Download ZIP. You do not need a GitHub account.

3. Open a terminal in the extracted folder and run:

   ```sh
   uvx marimo edit --sandbox exercise_1.py
   ```

   The first time, this takes a few minutes. uv reads the package list at the
   top of `exercise_1.py`, downloads those packages, and Python 3.12 if your
   computer does not have it, and installs them in a separate environment.
   You do not create or activate an environment yourself.
   When the exercise opens in your browser, your setup works.
   Stop it with Ctrl-C in the terminal.

4. Start the tutorial once, as described in "Open the tutorial" below. This
   installs its packages now, not on the venue network. When the page opens,
   stop it with Ctrl-C.

## During the exercises

Open the first exercise:

```sh
uvx marimo edit --sandbox exercise_1.py
```

In the `edit_encoding` cell, you change `qml.RX` to `qml.RY`.
The notebook lists each step.

Open the second exercise:

```sh
uvx marimo edit --sandbox exercise_2.py
```

In the `edit_training` cell, you replace the weight update in `fit_regression`
with `weights = weights`. The notebook lists each step.

Click the Run button at the bottom right when a notebook opens, and again
after every edit. It runs every cell that your edit affects, including the
check cell and the plots.

You can also change a function in `exercise_circuits.py` or
`exercise_layout.py` in a text editor. When you save the file, marimo reruns
the cells of the open exercise that use the changed function. You do not
click Run for this.

To start over, download the changed files again, or keep unedited copies
before you begin. Keep each exercise file in this folder: it imports
`exercise_circuits.py` and `exercise_layout.py`, and it uses `workshop.css`.

## Open the tutorial

Open a terminal in this folder and run:

```sh
uv run --no-project --python 3.12 --with-requirements requirements.txt serve.py
```

Then open http://localhost:8796 in your browser. Keep the terminal open while
you use the tutorial. Ctrl-C in the terminal stops it. If another program
uses port 8796, add `--port 8797` to the command and open
http://localhost:8797.

Go through the chapters in order, starting with Start. Most chapters have two
tabs: Tutorial, with the explanations and the code, and Lab, with the sliders,
circuits, and plots. You can move the sliders, but you cannot edit the code on
this page. To change code, use the exercises.

## If uv does not work for you

Use a virtual environment instead. With Python 3.12 installed, run these
commands in the extracted folder:

```sh
python3.12 -m venv .venv
```

Activate the environment:

- macOS and Linux: `source .venv/bin/activate`
- Windows PowerShell: `.venv\Scripts\Activate.ps1`

Install the packages and check the setup:

```sh
python -m pip install -r requirements.txt
python verify_tutorials.py
```

Then open each exercise with `python -m marimo edit exercise_1.py --no-sandbox`,
and the same for `exercise_2.py`. Start the tutorial with `python serve.py`.
