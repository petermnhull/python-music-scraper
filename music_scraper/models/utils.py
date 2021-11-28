import re


def normalise_string(input_string: str) -> str:
    output_string = re.sub(r"\W+", "", input_string)
    output_string = output_string.lower()
    return output_string
