import os
import time
import json
from multiprocessing import Manager
from src.streaming_json_parser import StreamingJsonParser


def string_to_bool(s: str) -> bool:
    # Convert to lowercase and check for truthy values
    truthy_values = {"true", "yes", "1", "on"}
    falsy_values = {"false", "no", "0", "off"}

    if s.lower() in truthy_values:
        return True
    elif s.lower() in falsy_values:
        return False
    else:
        raise ValueError(f"Cannot convert '{s}' to a boolean.")


def clean_json_from_escape_chars(json_string: str) -> str:
    # Decode JSON to Python object
    json_obj = json.loads(json_string)

    # Re-encode JSON to a string without escape characters
    clean_json_string = json.dumps(json_obj, ensure_ascii=False)

    return clean_json_string


def load_file_to_string(file_path: str) -> str:
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None


if __name__ == "__main__":
    if "EXPLANATORY_MODE" in os.environ:
        EXPLANATORY_MODE = string_to_bool(os.getenv("EXPLANATORY_MODE"))
    else:
        EXPLANATORY_MODE = False
    print(EXPLANATORY_MODE)

    manager = Manager()
    temp_state_dict = manager.dict()
    parser = StreamingJsonParser(temp_state_dict, EXPLANATORY_MODE)

    json_data_from_file = load_file_to_string("example_data.json")
    json_string = clean_json_from_escape_chars(json_data_from_file)

    # Simulate streaming
    chunk_size = 50
    for i in range(0, len(json_string), chunk_size):
        parser.consume(json_string[i:i + chunk_size])

    while not parser.is_parsed():
        print(parser.get())
        if EXPLANATORY_MODE:
            time.sleep(0.05)

    print(parser.get())

