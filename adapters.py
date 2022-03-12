from abc import ABCMeta, abstractmethod

from typing import Callable


class AbstractInputAdapter(metaclass=ABCMeta):
    @abstractmethod
    def get_input(self) -> str:
        pass


class AbstractOutputAdapter(metaclass=ABCMeta):
    @abstractmethod
    def send_output(self, output: str) -> None:
        pass


class InputAdapter(AbstractInputAdapter):
    def __init__(self, input_: Callable[[], str]):
        self.input_ = input_

    def get_input(self) -> str:
        return self.input_()


class OutputAdapter(AbstractOutputAdapter):
    def __init__(self, output: Callable[[str], None]):
        self.output = output

    def send_output(self, output: str) -> None:
        self.output(output)
