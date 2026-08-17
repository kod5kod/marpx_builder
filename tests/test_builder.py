import pytest
from pathlib import Path
import yaml
from unittest.mock import patch
from marpx_builder.builder import get_bundled_themes, load_config, render_templates, build

def test_get_bundled_themes():
    themes = get_bundled_themes()
    assert isinstance(themes, list)

def test_load_config_missing(tmp_path: Path):
    config = load_config(tmp_path)
    assert config == {}

def test_load_config_exists(tmp_path: Path):
    config_file = tmp_path / "marpx.yaml"
    with open(config_file, "w", encoding="utf-8") as f:
        yaml.dump({"theme": "einstein"}, f)
    config = load_config(tmp_path)
    assert config == {"theme": "einstein"}

def test_render_templates(tmp_path: Path):
    content_dir = tmp_path / "content"
    output_dir = tmp_path / "output"
    content_dir.mkdir()
    
    # Create a template
    md_file = content_dir / "presentation.md"
    with open(md_file, "w", encoding="utf-8") as f:
        f.write("Hello {{ name }}")
        
    render_templates(content_dir, output_dir, {"name": "World"})
    
    out_file = output_dir / "presentation.md"
    assert out_file.exists()
    with open(out_file, "r", encoding="utf-8") as f:
        assert f.read() == "Hello World"

@patch("marpx_builder.builder.subprocess.run")
def test_build(mock_run, tmp_path: Path):
    content_dir = tmp_path / "content"
    output_dir = tmp_path / "output"
    content_dir.mkdir()
    
    build(str(content_dir), str(output_dir))
    
    assert mock_run.called
    args = mock_run.call_args[0][0]
    assert args[0] == "npx"
    assert "--html" in args

@patch("marpx_builder.builder.subprocess.run")
def test_build_pdf(mock_run, tmp_path: Path):
    content_dir = tmp_path / "content"
    output_dir = tmp_path / "output"
    content_dir.mkdir()
    
    build(str(content_dir), str(output_dir), pdf=True)
    
    args = mock_run.call_args[0][0]
    assert "--pdf" in args

@patch("marpx_builder.builder.subprocess.run")
def test_build_watch(mock_run, tmp_path: Path):
    content_dir = tmp_path / "content"
    output_dir = tmp_path / "output"
    content_dir.mkdir()
    
    build(str(content_dir), str(output_dir), watch=True)
    
    args = mock_run.call_args[0][0]
    assert "--watch" in args
