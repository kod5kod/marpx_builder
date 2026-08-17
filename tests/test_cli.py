import pytest
import sys
from pathlib import Path
from unittest.mock import patch
from marpx_builder.cli import init_scaffold, main

def test_init_scaffold_creates_files(tmp_path: Path):
    target = tmp_path / "my_presentation"
    init_scaffold(str(target))
    
    assert target.exists()
    assert (target / "presentation.md").exists()
    assert (target / "custom.css").exists()
    assert (target / "marpx.yaml").exists()
    assert (target / "assets").is_dir()

def test_init_scaffold_existing_directory_errors(tmp_path: Path):
    target = tmp_path / "my_presentation"
    target.mkdir()
    
    with pytest.raises(SystemExit):
        init_scaffold(str(target))

@patch("marpx_builder.cli.init_scaffold")
def test_main_init_command(mock_init_scaffold):
    with patch.object(sys, "argv", ["marpx-builder", "init", "test_pres"]):
        with pytest.raises(SystemExit) as e:
            main()
        assert e.value.code == 0
        mock_init_scaffold.assert_called_once_with("test_pres")

@patch("marpx_builder.cli.build")
def test_main_build_command(mock_build):
    with patch.object(sys, "argv", ["marpx-builder", "build", "my_pres", "-o", "dist"]):
        main()
        mock_build.assert_called_once_with(
            content_dir="my_pres",
            output_dir="dist",
            theme=None,
            watch=False,
            pdf=False,
            pptx=False
        )

@patch("marpx_builder.cli.build")
def test_main_watch_command(mock_build):
    with patch.object(sys, "argv", ["marpx-builder", "watch", "my_pres", "-o", "dist", "--theme", "einstein"]):
        main()
        mock_build.assert_called_once_with(
            content_dir="my_pres",
            output_dir="dist",
            theme="einstein",
            watch=True,
            pdf=False,
            pptx=False
        )

def test_main_no_args():
    with patch.object(sys, "argv", ["marpx-builder"]):
        with pytest.raises(SystemExit) as e:
            main()
        assert e.value.code == 1
