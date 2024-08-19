import ast
import glob
import json
import logging
import os
import subprocess
from pathlib import Path
from typing import Any, List, Optional, Tuple

import numpy as np
import pandas as pd
from dotenv import load_dotenv
from rich.logging import RichHandler
import yaml

from .paths import root


def set_torch_device():
    import torch

    if torch.cuda.is_available() and torch.cuda.device_count() > 0:
        device = torch.device("cuda")
        device_properties: Any = torch.cuda.get_device_properties(device)
        vram = device_properties.total_memory // (1024**2)
        logging.info(
            f"Set device to {device} with {vram}MB (~ {np.round(vram/1024)}GB) of VRAM"
        )
    elif (
        hasattr(torch.backends, "mps")
        and torch.backends.mps.is_available()
        and torch.backends.mps.is_built()
    ):
        device = torch.device("mps")
        logging.info(f"Set device to {device}")
    else:
        device = torch.device("cpu")
        logging.info(f"Set device to {device}")
    return device


def load_api_key(key: str, env_path: Path = Path.cwd()) -> Optional[str]:
    """
    Assumes you have a .env file in the root directory.
    Should be added to .gitignore, of course.
    """
    load_dotenv(env_path / ".env")
    api_key = os.getenv(key)
    return api_key


def load_api_key_list(
    key_names: List[str], env_path: Path = root
) -> List[Optional[str]]:
    """
    Assumes you have a .env file in the root directory with the api keys on new lines.
    Should be added to .gitignore, of course.
    """
    load_dotenv(env_path / ".env")
    keys: List[Optional[str]] = []
    for key in key_names:
        api_key = os.getenv(key)
        keys.append(api_key)
    return keys


def initialize_logger(logging_level: str = "INFO") -> logging.Logger:
    logging.basicConfig(
        level=getattr(logging, logging_level),
        format="%(asctime)s\n%(message)s",
        handlers=[RichHandler()],
    )
    logger = logging.getLogger("rich")
    return logger


def save_json(data: Any, file_path: str) -> None:
    try:
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        logging.error(f"An error occurred while saving data to {file_path}: {e}")


def get_fpaths_and_fnames(dir: str, ftype: str = "json") -> List[Tuple[Path, str]]:
    directory = Path(dir)
    files = glob.glob(str(directory / f"*.{ftype}"))
    fpaths_fnames = [(Path(file), Path(file).stem) for file in files]
    return fpaths_fnames


def strings_to_lists(series: Any) -> Any:
    return series.apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)


def lists_to_strings(series: Any, sep: str = ", ") -> Any:
    """
    If the lists data you want as a string is stored as a string
    You need to convert it to lists first, then back to the string you want... :/
    """
    series = strings_to_lists(series)
    return series.apply(lambda x: sep.join(x) if isinstance(x, list) else x)


def run_in_conda(script: str, conda_env_name: str = "gt") -> None:
    conda_script = script

    command = (
        "source $(conda info --base)/etc/profile.d/conda.sh && "
        f"conda activate {conda_env_name} && "
        f"python {conda_script} && "
        "conda deactivate"
    )

    logging.info(f"Executing command: {command}")

    try:
        process = subprocess.run(
            command,
            shell=True,
            executable="/bin/bash",
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        logging.info(
            f"Successfully executed '{conda_script}' in conda env '{conda_env_name}'\n"
            f"Output:\n{process.stdout.decode()}"
        )
    except subprocess.CalledProcessError as e:
        logging.error(
            f"Failed to execute '{conda_script}' in conda env '{conda_env_name}'\n"
            f"Error:\n{e.stderr.decode()}"
        )


def markdown_table(df: pd.DataFrame, filepath: str = None) -> str:
    """
    Convert a pandas DataFrame to a markdown table.

    Parameters:
    df (pd.DataFrame): The DataFrame to convert to markdown.
    filepath (str, optional): The path where the markdown file should be saved.
    Defaults to None.

    Returns:
    str: The markdown formatted table as a string.
    """
    md = df.to_markdown(index=False)
    if filepath is not None:
        with open(filepath, "w") as file:
            file.write(md)
    return md


def estimate_meters_from_rssi(df, rssi_col, A=-40, n=2):
    """
    A = -40  # RSSI value at 1 meter distance
    n = 2    # Path-loss exponent
    """
    estimated_meters = 10 ** ((A - df[rssi_col]) / (10 * n))
    return estimated_meters


def update_quarto_variables(new_key, new_value, path="_variables.yml"):
    with open(path, 'r') as file:
        quarto_variables = yaml.safe_load(file)

    # add a new key-value pair or update an existing key
    quarto_variables[new_key] = new_value 
    
    with open(path, 'w') as file:
        yaml.dump(quarto_variables, file, default_flow_style=False)