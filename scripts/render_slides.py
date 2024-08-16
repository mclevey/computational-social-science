import glob
import logging
import os
import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from icsspy.paths import slides_html, slides_qmd

slides = slides_qmd

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def list_qmd_files(directory):
    qmd_files = glob.glob(f"{directory}/*.qmd")
    qmd_files = [Path(file) for file in qmd_files]
    return qmd_files


def move_files_with_extension(source_dir, target_dir, file_extension):
    source_dir, target_dir = Path(source_dir), Path(target_dir).resolve()
    target_dir.mkdir(parents=True, exist_ok=True)
    for file_path in source_dir.glob(f"*{file_extension}"):
        if file_path.is_file():
            target_path = target_dir / file_path.name
            shutil.move(str(file_path), str(target_path))


def render_qmd_file(qmd_deck):
    command = f"quarto render {qmd_deck} --output-dir ../docs/"
    try:
        subprocess.run(command, capture_output=True, text=True, shell=True, check=True)
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")


def main():
    qmd_slide_decks = list_qmd_files(slides)
    os.chdir(slides.resolve())
    with ThreadPoolExecutor() as executor:
        executor.map(render_qmd_file, qmd_slide_decks)
    move_files_with_extension(slides, slides_html, ".html")


if __name__ == "__main__":
    main()
