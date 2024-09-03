import json
import re
import warnings
from typing import List, Optional, Tuple

import pandas
from bs4 import BeautifulSoup, MarkupResemblesLocatorWarning

warnings.filterwarnings("ignore", category=MarkupResemblesLocatorWarning)


def write_text(
    file_path: str, title_list: List[str], description_list: Optional[List[str]] = None
) -> None:
    with open(file_path, "w") as f:
        if description_list is None:
            for item in title_list:
                f.write(f"{item}\n")


def remove_text_in_brackets(input_string: str) -> str:
    bracket_pattern = r"\(.*?\)"
    result = re.sub(bracket_pattern, "", input_string)
    return result


def process_urls(text: str) -> Tuple[str, List[str]]:
    url_pattern = re.compile(r"https?://\S+|www\.\S+")
    urls = url_pattern.findall(text)
    cleaned_text = url_pattern.sub("", text)
    return cleaned_text, urls


def remove_substrings(text: str, substrings_to_remove: List[str]) -> str:
    for substr in substrings_to_remove:
        text = text.replace(substr, "")
    return text.strip()


def merge_title_and_description_strings(
    df: "pandas.DataFrame",
    title_col: str = "snippet.title",
    description_col: str = "snippet.description",
) -> List[str]:
    docs: List[str] = []
    titles = df[title_col].tolist()
    descriptions = df[description_col].tolist()

    for t, d in zip(titles, descriptions):
        if isinstance(d, str):
            # If an identical title string is duplicated in the description, remove it
            d = d.replace(t, "").strip()
            # and then merge them. Will not catch fuzzier matches, obviously.
            text = ". ".join([t.strip(), d.replace("\n", "").strip()])
        else:
            text = t.strip()
        docs.append(text.strip())
    return docs


def clean_html(text: str) -> str:
    soup = BeautifulSoup(text, "html.parser")
    return soup.get_text()


def parse_nested_json(text: str) -> str:
    """Identify and parse JSON-like structures within text."""
    try:
        # Attempt to find and parse JSON-like structures
        start_idx = text.find("{")
        if start_idx != -1:
            json_str = text[start_idx:]
            parsed_json = json.loads(json_str)
            # Extract the meaningful content from the parsed JSON
            text = text[:start_idx] + json.dumps(parsed_json, indent=2)
    except json.JSONDecodeError:
        # If parsing fails, return the original text
        pass
    return text


def clean_comment_text(text: str) -> str:
    """Clean the comment text by removing HTML and parsing nested JSON."""
    if isinstance(text, str):
        text = clean_html(text)
        text = parse_nested_json(text)
        return text
    return ""  # Return an empty string if the text is not a valid string
