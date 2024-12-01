import inspect
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()


def _get_input(nth_frame):
    frame = inspect.stack()[nth_frame]
    module = inspect.getmodule(frame[0])
    input_path = Path(module.__file__).parent / "input.txt"
    if input_path.exists():
        with open(input_path, "r") as f:
            return f.read()
    else:
        day = module.__package__.split(".")[-1][3:]
        url = f"https://adventofcode.com/2024/day/{day}/input"
        cookies = {"session": os.environ.get("AOC_SESSION")}
        res = requests.get(url, cookies=cookies)
        res.raise_for_status()
        data = res.text
        with open(input_path, "w") as f:
            f.write(data)
        return data


def get_input(strip=True):
    content = _get_input(2)
    return content.strip() if strip else content


def get_input_lines(strip=True):
    lines = _get_input(2).splitlines()
    return [l.strip() for l in lines] if strip else lines
