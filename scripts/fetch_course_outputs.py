import os
import shutil
from pathlib import Path

import icsspy
from icsspy.paths import cm_export, slides_qmd

logger = icsspy.initialize_logger()

source_dir = cm_export
destination_dir = slides_qmd
os.makedirs(destination_dir, exist_ok=True)


def fetch_course_outputs(
    source_dir: Path = source_dir, destination_dir: Path = destination_dir
):
    for file_path in source_dir.glob("*"):
        if file_path.is_file():
            if ".pdpp" not in file_path.name:
                if file_path.suffix.lower() == ".png":
                    destination_path = destination_dir / "media" / file_path.name
                    shutil.copy(file_path, destination_path)
                elif file_path.suffix.lower() == ".md":
                    destination_path = destination_dir / file_path.name
                    shutil.copy(file_path, destination_path)
                else:
                    logger.warning(
                        f"File {file_path} not copied. Set destination rule."
                    )

    logger.info(f"Copied files from {source_dir}\nto {destination_dir}.")
