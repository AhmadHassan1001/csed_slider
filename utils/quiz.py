import typing_extensions as typing

class Option(typing.TypedDict):
    index: int
    text: str

class Quiz(typing.TypedDict):
    question: str
    options: list[Option]
    answer_index: int
    explanation: str