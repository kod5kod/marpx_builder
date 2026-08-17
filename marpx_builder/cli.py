import argparse
import sys
from pathlib import Path

from marpx_builder.builder import build


def init_scaffold(directory: str):
    """Scaffolds a basic Marp presentation directory."""
    target = Path(directory)
    if target.exists():
        print(f"Error: Directory '{target}' already exists.")
        sys.exit(1)

    target.mkdir(parents=True)
    (target / "assets").mkdir()

    # Create default presentation.md
    with open(target / "presentation.md", "w", encoding="utf-8") as f:
        f.write("""---
title: My MarpX Presentation
author: Author Name
description: Created with marpx-builder
marp: true
theme: einstein
paginate: true
---

<!-- Import custom overrides -->
<style>
  @import url('custom.css');
</style>

<!-- _class: title -->

# Welcome to MarpX
## {{ subtitle }}

---

<!-- _class: chapter -->

# Introduction

---

## Slide 1

This is a templated slide. You can put assets in the `assets/` folder.
""")

    # Create default custom.css
    with open(target / "custom.css", "w", encoding="utf-8") as f:
        f.write("""/* @theme custom */
/*
 * Custom Marp Theme Overrides
 */

:root {
  /* Override MarpX variables here */
}
""")

    # Create default config
    with open(target / "marpx.yaml", "w", encoding="utf-8") as f:
        f.write("""# Default configuration for marpx-builder
theme: einstein
context:
  subtitle: "Built with Python"
""")

    print(f"Successfully initialized presentation in '{target}'.")
    print(f"Run `marpx-builder build {target} -o dist/` to compile it.")

def main():
    parser = argparse.ArgumentParser(description="MarpX Builder: Compile Marp presentations with MarpX themes.")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Init command
    parser_init = subparsers.add_parser("init", help="Scaffold a new presentation directory")
    parser_init.add_argument("directory", help="Name of the directory to create")

    # Common arguments for both build and watch
    def add_common_args(subparser):
        subparser.add_argument("content_dir", help="Directory containing Markdown content files")
        subparser.add_argument("-o", "--output", dest="output_dir", required=True, help="Output directory for compiled files")
        subparser.add_argument("--theme", help="Specific theme to apply (e.g., 'gödel', 'einstein')")

    # Build command
    parser_build = subparsers.add_parser("build", help="Build the presentations once")
    add_common_args(parser_build)
    parser_build.add_argument("--pdf", action="store_true", help="Build as PDF instead of HTML")
    parser_build.add_argument("--pptx", action="store_true", help="Build as PPTX instead of HTML")

    # Watch command
    parser_watch = subparsers.add_parser("watch", help="Watch the content directory and rebuild on changes")
    add_common_args(parser_watch)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "init":
        init_scaffold(args.directory)
        sys.exit(0)

    watch_mode = args.command == "watch"
    pdf_mode = getattr(args, "pdf", False)
    pptx_mode = getattr(args, "pptx", False)

    build(
        content_dir=args.content_dir,
        output_dir=args.output_dir,
        theme=args.theme,
        watch=watch_mode,
        pdf=pdf_mode,
        pptx=pptx_mode
    )

if __name__ == "__main__":
    main()
