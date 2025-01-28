# deepjudge_streaming_parser

This project demonstrates the streaming parser.

---

## Task description
````
Develop a Streaming JSON Parser

Objective:
You are required to implement a streaming JSON parser that processes JSON data incrementally in Python.
This parser should be capable of handling JSON objects consisting solely of strings and dictionaries.
The primary motivation for this task is to simulate partial responses as would be encountered in the streaming output of a large language model (LLM).
Even if the input JSON data is incomplete, the parser should be able to return the current state of the parsed JSON object at any given point in time.
This should include partial string-values and dictionaries, but not the keys themselves, i.e. `{"test": "hello", "worl` is a partial representation of `{"test": "hello"}`, but not `{"test": "hello", "worl": ""}`. 
Only once the value type of the key is determined should the parser return the key-value pair. 
String values on the other hand can be partially returned: `{"test": "hello", "country": "Switzerl` is a partial representation of `{"test": "hello", "country": "Switzerl"}`.

The parser should be efficient in terms of algorithmic complexity.

Create a class named `StreamingJsonParser`.
Implement the following methods within this class:

- `__init__()`: Initializes the parser.
- `consume(buffer: str)`: Consumes a chunk of JSON data.
- `get()`: Returns the current state of the parsed JSON object.

Examples:

```py
def test_streaming_json_parser():
 parser = StreamingJsonParser()
 parser.consume('{"foo": "bar"}’)
 assert parser.get() == {"foo": "bar"}

def test_chunked_streaming_json_parser():
 parser = StreamingJsonParser()
 parser.consume('{"foo":’)
 parser.consume('"bar’)
 assert parser.get() == {"foo": "bar"}

def test_partial_streaming_json_parser():
 parser = StreamingJsonParser()
 parser.consume('{"foo": "bar’)
 assert parser.get() == {"foo": "bar"}
```
````

---

## Requirements

- Python 3.10
- time
- json
- multiprocessing

## How to run

```bash

python3 main.py

```

* For explanatory mode:
```bash

export EXPLANATORY_MODE=1

```
