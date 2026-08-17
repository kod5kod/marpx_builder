import shutil
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

import yaml
from jinja2 import Environment, FileSystemLoader


def get_bundled_themes():
    """Returns a list of valid CSS files from the bundled MarpX themes."""
    marpx_dir = Path(__file__).parent / "themes" / "marpx"
    themes = []
    if marpx_dir.exists():
        for file in marpx_dir.iterdir():
            # Skip partials (starting with '_') and directories
            if file.is_file() and file.name.endswith(".css") and not file.name.startswith("_"):
                themes.append(str(file))
    return themes

def load_config(content_dir: Path):
    """Loads configuration from marpx.yaml if it exists."""
    config_path = content_dir / "marpx.yaml"
    if config_path.exists():
        with open(config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    return {}

def render_templates(content_dir: Path, output_dir: Path, context: dict):
    """Renders all markdown files using Jinja2 into the output directory."""
    env = Environment(loader=FileSystemLoader(str(content_dir)))

    # Copy all files first (assets, css, etc.)
    shutil.copytree(str(content_dir), str(output_dir), dirs_exist_ok=True)

    # Then overwrite markdown files with rendered templates
    for file in output_dir.rglob("*.md"):
        rel_path = file.relative_to(output_dir)
        try:
            template = env.get_template(str(rel_path))
            rendered = template.render(**context)
            with open(file, "w", encoding="utf-8") as f:
                f.write(rendered)
        except Exception as e:
            print(f"[marpx-builder] Warning: Failed to render {rel_path} with Jinja2: {e}")

def build(content_dir: str, output_dir: str, theme: str = None, watch: bool = False, pdf: bool = False, pptx: bool = False):
    """Executes the Marp CLI via npx, applying Jinja2 templating."""
    content_path = Path(content_dir).resolve()
    final_output_path = Path(output_dir).resolve()

    # Ensure output directory exists
    final_output_path.mkdir(parents=True, exist_ok=True)

    # Load optional config
    config = load_config(content_path)
    context = config.get("context", {})
    theme = theme or config.get("theme")

    with TemporaryDirectory() as temp_dir:
        temp_content_path = Path(temp_dir) / "content"

        # In watch mode, we skip Jinja2 to allow Marp's native hot-reloading on raw files
        if watch:
            print("[marpx-builder] Note: Watch mode enabled. Jinja2 templating is disabled.")
            active_content_path = content_path
        else:
            # Render Jinja2 templates into a temp directory
            render_templates(content_path, temp_content_path, context)
            active_content_path = temp_content_path

        # Base command: npx --yes @marp-team/marp-cli@latest
        cmd = ["npx", "--yes", "@marp-team/marp-cli@latest"]

        if watch:
            cmd.append("--watch")

        if pptx:
            cmd.extend(["--pptx", "--allow-local-files"])
        elif pdf:
            cmd.extend(["--pdf", "--allow-local-files"])
        else:
            cmd.append("--html")

        # Inputs and Outputs
        cmd.extend(["-I", str(active_content_path)])
        cmd.extend(["-o", str(final_output_path)])

        # Specify the selected theme
        if theme:
            cmd.extend(["--theme", theme])

        # Gather themes to inject
        theme_sets = get_bundled_themes()

        # Automatically detect custom.css in the content directory
        custom_css_path = active_content_path / "custom.css"
        if custom_css_path.exists():
            theme_sets.append(str(custom_css_path))
            print("[marpx-builder] Found and injected custom CSS.")

        for ts in theme_sets:
            cmd.extend(["--theme-set", ts])

        print("[marpx-builder] Running Marp build...")

        try:
            # Run the command and stream output to the console
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            print(f"[marpx-builder] Error executing Marp CLI: {e}", file=sys.stderr)
            sys.exit(e.returncode)
        except FileNotFoundError:
            print("[marpx-builder] Error: 'npx' command not found. Please ensure Node.js is installed.", file=sys.stderr)
            sys.exit(1)
