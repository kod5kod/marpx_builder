<p align="center">
  <img src="assets/logo.jpg" alt="MarpX Builder Logo" width="300"/>
</p>

# MarpX Builder

A Python CLI tool and library for compiling [Marp](https://marp.app/) presentations using the [MarpX](https://github.com/cunhapaulo/MarpX) theme suite.

## Overview

**The core philosophy behind MarpX Builder is simple:** For every project, library, framework, research paper, or repository you build, you should be able to instantly scaffold and write a beautiful presentation using a single, shared Python library.

MarpX Builder acts as an enhanced wrapper around the official Marp CLI. It brings powerful features to your Markdown-driven presentations, including Jinja2 templating, project scaffolding, Python API access, and automatic injection of the highly-polished MarpX theme suite.

## Features

- **Project Scaffolding:** Instantly initialize a new presentation directory with a boilerplate Markdown file, custom CSS stylesheet, assets folder, and configuration file.
- **Jinja2 Templating:** Dynamically inject variables into your Markdown slides at build time using a `marpx.yaml` configuration file and Jinja2 syntax.
- **Multiple Export Formats:** Build presentations into static HTML, or export directly to PDF and PPTX.
- **Watch Mode:** Automatically rebuild your HTML presentation upon file changes for a seamless, hot-reloading authoring experience.
- **Bundled Themes:** Access canonical MarpX themes out-of-the-box, such as `marpx`, `einstein`, `gödel`, `newton`, and `socrates`.
- **Python API:** Programmatically compile and export presentations directly from your own Python scripts.

## Use Cases

- **Universal Project Presentations:** Seamlessly document and present any framework, repository, or library by scaffolding a presentation right alongside your codebase.
- **Research Papers & Technical Talks:** Leverage beautifully designed, typography-focused MarpX themes tailored for technical content, math, and code.
- **Automated Reporting:** Generate dynamic, data-driven slide decks (e.g., weekly metrics) by passing data into Jinja2 templates via `marpx.yaml`.
- **Standardized Workflows:** Ensure your team uses consistent styling and layouts by quickly scaffolding new presentations with pre-configured themes and custom CSS.
- **Data Pipeline Integration:** Automatically generate and distribute PDF/PPTX presentation reports at the end of a Python-based data analysis pipeline.

## Installation

Install the package directly using pip. 
*(Note: Requires Node.js to be installed on your system, as it uses `npx` under the hood to invoke the Marp CLI).*

```bash
pip install -e .
```

## CLI Usage

### 1. Initialize a new presentation
Instantly scaffold a new directory with a boilerplate presentation, custom CSS, and assets folder:

```bash
marpx-builder init my_presentation
```

### 2. Configuration & Jinja2 (Optional)
You can place a `marpx.yaml` file in your content directory to set default variables and define the theme:

```yaml
theme: gödel
context:
  subtitle: "Dynamic subtitle here"
```

These `context` variables are parsed using **Jinja2** at build time. In your `presentation.md`, you can render them simply: `{{ subtitle }}`.

### 3. Build the presentation
Run the builder, pointing it to your content directory and specifying an output directory.

**Build to HTML:**
```bash
marpx-builder build my_presentation/ -o dist/
```

**Build to PDF / PPTX:**
*(Requires Google Chrome or Microsoft Edge installed)*
```bash
marpx-builder build my_presentation/ -o dist/ --pdf
marpx-builder build my_presentation/ -o dist/ --pptx
```

**Watch Mode:**
Automatically rebuild HTML whenever a file in your content directory changes:
*(Note: Jinja2 variables are not evaluated in watch mode to allow native hot-reloading).*
```bash
marpx-builder watch my_presentation/ -o dist/
```

## Python API Usage

You can seamlessly generate presentations programmatically from within Python applications:

```python
from marpx_builder import build

build(
    content_dir="my_presentation",
    output_dir="dist",
    theme="einstein",
    pdf=True
)
```

## Available Themes

You can specify the theme using the `--theme` flag or in your `marpx.yaml`. Bundled themes include:
- `marpx`
- `gödel`
- `einstein`
- `socrates`
- `newton`
- *...and all other canonical MarpX themes.*

## References & Acknowledgements

This project builds upon the incredible work of several open-source tools:
- **[Marp Ecosystem & CLI](https://marp.app/)**: The core engine that powers the Markdown-to-presentation conversion.
- **[MarpX Themes](https://github.com/cunhapaulo/MarpX)**: The beautiful, typography-focused theme suite bundled into this builder.
- **[Jinja2](https://jinja.palletsprojects.com/)**: The templating engine used for dynamic slide generation.
