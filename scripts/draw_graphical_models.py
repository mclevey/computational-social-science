import logging
import subprocess
from pathlib import Path

from icsspy.utils import get_fpaths_and_fnames


def draw_graphical_model(gv, output_dir, pdf=True, png=True, dpi=300):
    gv_path = Path(gv)
    output_dir_path = Path(output_dir)
    output_dir_path.mkdir(parents=True, exist_ok=True)
    base_name = gv_path.stem

    if pdf:
        pdf_output_path = output_dir_path / f"{base_name}.pdf"
        pdf_command = ["dot", "-Tpdf", str(gv_path), "-o", str(pdf_output_path)]
        subprocess.run(pdf_command, check=True)
        logging.info(f"Generated PDF: {pdf_output_path}")

    if png:
        png_output_path = output_dir_path / f"{base_name}.png"
        png_command = [
            "dot",
            "-Tpng:cairo:cairo",
            f"-Gdpi={dpi}",
            str(gv_path),
            "-o",
            str(png_output_path),
        ]
        subprocess.run(png_command, check=True)
        logging.info(f"Generated PNG: {png_output_path}")


def draw_models(model_dir="../graphical_models/"):
    fpaths_fnames = get_fpaths_and_fnames(model_dir, ftype="gv")
    for fpath, fname in fpaths_fnames:
        draw_graphical_model(fpath, model_dir)


if __name__ == "__main__":
    draw_models()
