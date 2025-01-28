import time
from multiprocessing import Process
from src.custom_queue import CustomQueue


class StreamingJsonParser:
    def __init__(self, temp_state_dict: dict, explanatory_mode: bool):
        self.__queue: CustomQueue = CustomQueue()
        self.__parse_process = None
        self.__buffer: str = ""
        self.__shared_dict = temp_state_dict
        self.__explanatory_mode = explanatory_mode

    def consume(self, chunk: str):
        """Consumes a chunk of JSON data and puts that to queue."""
        self.__queue.put(chunk)
        if self.__parse_process is None:
            self.__start_parse()
        elif not self.__parse_process.is_alive():
            self.__start_parse()

    def get(self):
        """Returns the current state of the parsed JSON object. Cleaned to be valid JSON"""
        temp_state_dict = self.__shared_dict
        temp_state = "{}"
        try:
            temp_state = temp_state_dict["partial_data"]
            if len(temp_state_dict["partial_data"]) > 0 and self.__queue.qsize() > 0:
                if temp_state[-1] == ",":
                    temp_state = temp_state[:-1]
                if temp_state[-1] == "\"" and temp_state[-2] == " " and temp_state[-3] == ",":
                    temp_state = temp_state[:-3]
                if temp_state[-1] == " " and temp_state[-2] == ":":
                    temp_state += "\"\""
                if not temp_state_dict["closed_double_quotes"] and temp_state[-1] != "\"" and  temp_state[-1] != "}":
                    temp_state += "\""
                if temp_state[-1] == "\"" and temp_state[-2] == "{":
                    temp_state = temp_state[:-1]
                for i in range(len(temp_state_dict["object_stack"])-1, -1, -1):
                    if temp_state_dict["object_stack"][i] == "[":
                        temp_state += "]"
                    elif temp_state_dict["object_stack"][i] == "{":
                        temp_state += "}"
        except Exception as e:
            print(e)
        return temp_state

    def is_parsed(self):
        """Returns the state about the progress."""
        if self.__queue.qsize() > 0:
            return False
        return True

    def __start_parse(self):
        """Starts parsing in the separated process."""
        self.__shared_dict["partial_data"] = ""
        self.__shared_dict["object_stack"] = ""
        self.__shared_dict["closed_double_quotes"] = True
        self.__shared_dict["key_mode"] = True
        self.__parse_process = Process(target=self.parse, args=())
        self.__parse_process.start()

    def parse(self):
        """Incrementally parses the buffer to update the partial result."""
        temp_buffer = ""
        while self.__queue.qsize() > 0:
            self.__buffer += self.__queue.get()
            if self.__queue.qsize() == 0:
                self.__shared_dict["partial_data"] += self.__buffer
                return 0
            for char in self.__buffer:
                temp_buffer += char
                if not self.__shared_dict["key_mode"]:
                    self.__shared_dict["partial_data"] += temp_buffer
                    temp_buffer = ""
                if char == ":" and self.__shared_dict["closed_double_quotes"]:
                    if self.__shared_dict["key_mode"]:
                        self.__shared_dict["key_mode"] = not self.__shared_dict["key_mode"]
                        self.__shared_dict["partial_data"] += temp_buffer
                        temp_buffer = ""
                    continue
                if char == "\"":
                    if self.__shared_dict["closed_double_quotes"]:
                        self.__shared_dict["partial_data"] += temp_buffer
                        temp_buffer = ""
                    self.__shared_dict["closed_double_quotes"] = not self.__shared_dict["closed_double_quotes"]
                    continue
                if char == "," and self.__shared_dict["closed_double_quotes"]:
                    self.__shared_dict["partial_data"] += temp_buffer
                    temp_buffer = ""
                    self.__shared_dict["key_mode"] = not self.__shared_dict["key_mode"]
                    continue
                if char == "{":
                    self.__shared_dict["key_mode"] = True
                    self.__shared_dict["object_stack"] += char
                    continue
                if char == "}" or char == "]":
                    self.__shared_dict["object_stack"] += char
                    self.__shared_dict["partial_data"] += temp_buffer
                    temp_buffer += ""
                    self.__shared_dict["object_stack"] = self.__shared_dict["object_stack"][:-2]
                    continue
                if char == "[":
                    self.__shared_dict["object_stack"] += char
                    continue
                if self.__explanatory_mode:
                    time.sleep(0.1)
            self.__buffer = temp_buffer
            temp_buffer = ""















