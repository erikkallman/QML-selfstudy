"""Serve a marimo snapshot, publishing source changes at most once per interval."""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time


SOURCE = Path(__file__).resolve().parent
# The research chapters import these modules; tutorials.py also loads its chapter text from chapters/.
MODULES = [
    "figure_style.py", "research_generation.py", "research_generation_figures.py",
    "research_memory.py", "research_memory_figures.py",
]


def read_bundle(source, notebook):
    names = [notebook, "workshop.css", *MODULES]
    if notebook == "tutorials.py":
        names.extend([
            "participant_package.py", "PARTICIPANTS.md", "requirements.txt",
            "verify_tutorials.py", "serve.py",
        ])
        names.extend(sorted(path.relative_to(source).as_posix() for path in (source / "chapters").rglob("*.md")))
    if notebook == "workshop.py":
        names.append("layouts/workshop.slides.json")
    bundle = {name: (source / name).read_bytes() for name in names}
    for name, content in bundle.items():
        if name.endswith(".py"):
            compile(content, name, "exec")
        elif name.endswith(".json"):
            json.loads(content)
    return bundle


def fingerprint(bundle):
    digest = hashlib.sha256()
    for name, content in sorted(bundle.items()):
        digest.update(name.encode())
        digest.update(len(content).to_bytes(8, "big"))
        digest.update(content)
    return digest.hexdigest()


def publish(bundle, destination, notebook):
    revision = fingerprint(bundle)
    # Publish dependencies first; the notebook replacement triggers one reload.
    for name in [n for n in bundle if n != notebook] + [notebook]:
        path = destination / name
        path.parent.mkdir(parents=True, exist_ok=True)
        content = bundle[name]
        if name == notebook:
            content += f"\n# Preview revision: {revision}\n".encode()
        temporary = path.with_suffix(path.suffix + ".pending")
        temporary.write_bytes(content)
        temporary.replace(path)
    return revision


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--notebook", choices=["tutorials.py", "workshop.py"], default="tutorials.py")
    parser.add_argument("--port", type=int, default=8796)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--interval", type=float, default=60, help="Seconds between source checks (default: 60)")
    args = parser.parse_args()
    if not math.isfinite(args.interval) or args.interval < 1:
        parser.error("--interval must be at least one second")
    if not 1 <= args.port <= 65535:
        parser.error("--port must be between 1 and 65535")

    with tempfile.TemporaryDirectory(prefix="qml-dojo-preview-") as directory:
        destination = Path(directory)
        revision = publish(read_bundle(SOURCE, args.notebook), destination, args.notebook)
        command = [
            sys.executable, "-m", "marimo", "run", str(destination / args.notebook),
            "--headless", "--no-sandbox", "--include-code", "--watch",
            "--host", args.host, "--port", str(args.port),
        ]
        if args.host not in ("127.0.0.1", "localhost", "::1"):
            command.append("--token")
        environment = dict(os.environ, MPLBACKEND="Agg", PYTHONDONTWRITEBYTECODE="1")
        print(f"Checking for source changes every {args.interval:g}s. Ctrl-C stops the server.", flush=True)
        process = subprocess.Popen(command, cwd=destination, env=environment)
        try:
            while process.poll() is None:
                deadline = time.monotonic() + args.interval
                while process.poll() is None and time.monotonic() < deadline:
                    time.sleep(min(0.5, max(0, deadline - time.monotonic())))
                if process.poll() is not None:
                    break
                try:
                    bundle = read_bundle(SOURCE, args.notebook)
                except (OSError, SyntaxError, ValueError) as error:
                    print(f"Keeping the previous version: {error}", flush=True)
                    continue
                if fingerprint(bundle) != revision:
                    revision = publish(bundle, destination, args.notebook)
                    print(f"Published source changes ({revision[:10]}). Browser refresh follows.", flush=True)
        except KeyboardInterrupt:
            pass
        finally:
            if process.poll() is None:
                process.terminate()
                try:
                    process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait()
        return process.returncode if process.returncode and process.returncode > 0 else 0


if __name__ == "__main__":
    raise SystemExit(main())
