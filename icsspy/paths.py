from pathlib import Path

import pandas as pd
import pyprojroot

root: Path = pyprojroot.find_root(pyprojroot.has_dir(".git"))

data: Path = root / "icsspy/data"
enron: Path = root / "icsspy/data/enron"
slides_qmd: Path = root / "slides"
slides_html: Path = root / "docs"
course_materials: Path = root / "notebooks"
day1: Path = root / "notebooks/1-introduction"
day2: Path = root / "notebooks/2-obtaining-data"
day3: Path = root / "notebooks/3-computational-text-analysis"
day4: Path = root / "notebooks/4-computational-network-analysis"
day5: Path = root / "notebooks/5-simulation-abms"
day6: Path = root / "notebooks/6-project"
cm_export: Path = root / "notebooks/_export_"


def load_data(file: str) -> pd.DataFrame:
    return pd.read_csv(data / f"{file}.csv")
