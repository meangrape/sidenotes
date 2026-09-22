#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
"""Build a Markdown file into HTML and PDF with margin notes.

Every option maps onto a pandoc option of the same name. Anything after
`--` is handed to pandoc unchanged, for both outputs.
"""
import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def parse_args(argv: list[str]) -> tuple[argparse.Namespace, list[str]]:
    extra: list[str] = []
    if "--" in argv:
        i = argv.index("--")
        argv, extra = argv[:i], argv[i + 1 :]

    p = argparse.ArgumentParser(
        prog="build.py",
        description=__doc__.split("\n\n")[0],
        epilog="Arguments after `--` are passed to pandoc unchanged.",
    )
    p.add_argument("source", type=Path, help="Markdown file to build")
    p.add_argument("-t", "--to", choices=["html", "pdf", "all"], default="all",
                   help="which output to build (default: all)")
    p.add_argument("-o", "--output-dir", type=Path, default=ROOT / "output",
                   help="directory for the built files (default: output/)")
    p.add_argument("--pandoc", default="pandoc", help="pandoc executable")
    p.add_argument("--pdf-engine", default="lualatex",
                   help="pandoc --pdf-engine (default: lualatex)")
    p.add_argument("--include-in-header", type=Path, default=ROOT / "tex" / "preamble.tex",
                   help="LaTeX preamble, pandoc --include-in-header (default: tex/preamble.tex)")
    p.add_argument("--css", type=Path, default=ROOT / "css" / "style.css",
                   help="stylesheet for the HTML build (default: css/style.css)")
    p.add_argument("--lua-filter", type=Path, default=ROOT / "lua" / "sidenotes.lua",
                   help="pandoc --lua-filter for the HTML build (default: lua/sidenotes.lua)")
    p.add_argument("--csl", type=Path,
                   help="CSL style; overrides the csl metadata field")
    p.add_argument("--bibliography", type=Path,
                   help="BibTeX file; overrides the bibliography metadata field")
    p.add_argument("--papersize",
                   help="letter, a4, legal, ...; overrides the papersize metadata field")
    p.add_argument("--no-citeproc", dest="citeproc", action="store_false",
                   help="do not run pandoc --citeproc")
    p.add_argument("--no-embed-resources", dest="embed", action="store_false",
                   help="link the stylesheet instead of embedding it in the HTML")
    p.add_argument("-M", "--metadata", action="append", default=[], metavar="KEY=VAL",
                   help="pandoc --metadata; may repeat")
    p.add_argument("-V", "--variable", action="append", default=[], metavar="KEY=VAL",
                   help="pandoc --variable; may repeat")
    p.add_argument("--resource-path", action="append", default=[], metavar="DIR",
                   help="extra directory pandoc searches for the bib, csl and images; may repeat")
    p.add_argument("--verbose", action="store_true",
                   help="pandoc --verbose; the PDF build then shows the LaTeX log")
    p.add_argument("-n", "--dry-run", action="store_true",
                   help="print the pandoc commands without running them")
    return p.parse_args(argv), extra


def common_args(a: argparse.Namespace, extra: list[str]) -> list[str]:
    resource_path = [".", str(a.source.resolve().parent), str(ROOT), *a.resource_path]
    args = ["--resource-path", ":".join(resource_path)]
    if a.citeproc:
        args.append("--citeproc")
    if a.csl:
        args += ["--csl", str(a.csl)]
    if a.bibliography:
        args += ["--bibliography", str(a.bibliography)]
    if a.papersize:
        args += ["--metadata", f"papersize={a.papersize}"]
    for kv in a.metadata:
        args += ["--metadata", kv]
    for kv in a.variable:
        args += ["--variable", kv]
    if a.verbose:
        args.append("--verbose")
    return args + extra


def html_command(a: argparse.Namespace, extra: list[str], out: Path) -> list[str]:
    cmd = [a.pandoc, str(a.source), "--standalone",
           "--lua-filter", str(a.lua_filter), "--css", str(a.css)]
    if a.embed:
        cmd.append("--embed-resources")
    return cmd + common_args(a, extra) + ["-o", str(out)]


def pdf_command(a: argparse.Namespace, extra: list[str], out: Path) -> list[str]:
    cmd = [a.pandoc, str(a.source), "--pdf-engine", a.pdf_engine,
           "--include-in-header", str(a.include_in_header)]
    return cmd + common_args(a, extra) + ["-o", str(out)]


def main(argv: list[str]) -> int:
    a, extra = parse_args(argv)
    if not a.source.is_file():
        print(f"build.py: no such file: {a.source}", file=sys.stderr)
        return 2
    if not a.dry_run and shutil.which(a.pandoc) is None:
        print(f"build.py: pandoc not found: {a.pandoc}", file=sys.stderr)
        return 2

    stem = a.source.stem
    jobs: list[list[str]] = []
    if a.to in ("html", "all"):
        jobs.append(html_command(a, extra, a.output_dir / f"{stem}.html"))
    if a.to in ("pdf", "all"):
        jobs.append(pdf_command(a, extra, a.output_dir / f"{stem}.pdf"))

    if not a.dry_run:
        a.output_dir.mkdir(parents=True, exist_ok=True)
    status = 0
    for cmd in jobs:
        if a.dry_run or a.verbose:
            print(subprocess.list2cmdline(cmd))
        if a.dry_run:
            continue
        rc = subprocess.run(cmd).returncode
        if rc != 0:
            print(f"build.py: pandoc exited {rc} for {cmd[-1]}", file=sys.stderr)
            status = rc
        else:
            print(f"wrote {cmd[-1]}")
    return status


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
