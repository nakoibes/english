from abc import ABCMeta, abstractmethod
from collections import deque
from random import shuffle
from typing import List, Callable


class Pair:
    def __init__(self, word1, word2):
        self.word1 = word1
        self.word2 = word2


class AbstractRepository(metaclass=ABCMeta):
    @abstractmethod
    def get_current(self) -> List[Pair]:
        pass

    @abstractmethod
    def get_current_swap(self) -> List[Pair]:
        pass

    @abstractmethod
    def get_previous(self) -> List[Pair]:
        pass

    @abstractmethod
    def get_pre_previous(self) -> List[Pair]:
        pass

    @abstractmethod
    def put_current(self, data: List[Pair], method: str = 'w') -> None:
        pass

    @abstractmethod
    def put_current_swap(self, data: List[Pair], method: str = 'w') -> None:
        pass

    @abstractmethod
    def put_previous(self, data: List[Pair], method: str = 'w') -> None:
        pass

    @abstractmethod
    def put_pre_previous(self, data: List[Pair], method: str = 'w') -> None:
        pass


class AbstractInputAdapter(metaclass=ABCMeta):
    @abstractmethod
    def get_input(self) -> str:
        pass


class AbstractOutputAdapter(metaclass=ABCMeta):
    @abstractmethod
    def send_output(self, output: str) -> None:
        pass


class Lesson:
    def __init__(self, repository: AbstractRepository,
                 input_adapter: AbstractInputAdapter,
                 output_adapter: AbstractOutputAdapter,
                 swap_number: int = 50):
        self.repository = repository
        self.input_adapter = input_adapter
        self.output_adapter = output_adapter
        self.swap_number = swap_number

    def start_lesson(self):
        current = self.repository.get_current()
        shuffle(current)
        current = self.passage(current)
        self.output_adapter.send_output('--------------------------')
        pre_previous = self.repository.get_pre_previous()
        pre_previous = self.passage(pre_previous)
        self.output_adapter.send_output('--------------------------')
        previous = self.repository.get_previous()
        side_current = self.repository.get_current()
        self.repository.put_pre_previous(previous)
        self.repository.put_previous(current)
        self.repository.put_current(pre_previous)
        current = side_current.copy()
        shuffle(current)
        self.passage(current, 'reverse')
        self.output_adapter.send_output('--------------------------')
        current_swap = self.repository.get_current_swap()
        if len(current_swap) > self.swap_number:
            self.output_adapter.send_output('REVERSE')
            shuffle(current_swap)
            self.passage(current_swap, 'reverse')
            self.repository.put_current_swap(current_swap)
        self.repository.put_current_swap(current_swap, 'a')
        self.output_adapter.send_output('---------END---------')

    def passage(self, data: List[Pair], flag: str = 'forward') -> List[Pair]:
        result = list()
        for pair in data:
            if flag == 'forward':
                status = self.word_check(pair.word1, pair.word2)
            else:
                status = self.word_check(pair.word2, pair.word1)
            if not status:
                result.append(pair)
        words = deque(result)
        while words:
            word1, word2 = words.popleft()
            if flag == 'forward':
                status = self.word_check(word1, word2)
            else:
                status = self.word_check(word2, word1)
            if not status:
                words.append(Pair(word1, word2))
        return result

    def word_check(self, question: str, answer: str):
        print(question)
        input_ = self.input_adapter.get_input()
        while not self.first_validation(input_):
            input_ = input()
        if input_ == '0':
            print(f'translation is {answer}')
            self.input_adapter.get_input()
            return False
        else:
            print(f'translation is {answer}')
            input_ = self.input_adapter.get_input()
            while self.second_validation(input_):
                input_ = self.input_adapter.get_input()
            if input_ == '0':
                self.input_adapter.get_input()
                return False
        return True

    @staticmethod
    def first_validation(input_):
        return input_ == '0' or input_ == '1' or len(input_) >= 2

    @staticmethod
    def second_validation(input_):
        return input_ == '0' or input_ == '1'


class FileRepository(AbstractRepository):
    def __init__(self, current: str, current_swap: str, previous: str, pre_previous: str):
        self.current = current
        self.current_swap = current_swap
        self.previous = previous
        self.pre_previous = pre_previous

    def get_current(self):
        return self._get_data(self.current)

    def get_current_swap(self):
        return self._get_data(self.current_swap)

    def get_previous(self):
        return self._get_data(self.previous)

    def get_pre_previous(self):
        return self._get_data(self.pre_previous)

    def put_current(self, data: List[Pair], method: str = 'w'):
        self._put_data(self.current, method, data)

    def put_current_swap(self, data: List[Pair], method: str = 'w'):
        pass

    def put_previous(self, data: List[Pair], method: str = 'w'):
        pass

    def put_pre_previous(self, data: List[Pair], method: str = 'w'):
        pass

    def _get_data(self, filename) -> List[Pair]:
        data = list()
        with open(filename) as f:
            number_of_strings = self.count_number_of_pairs(filename)
            for _ in range(number_of_strings):
                word_one = f.readline().strip()
                word_two = f.readline().strip()
                data.append(Pair(word_one, word_two))
        return data

    @staticmethod
    def _put_data(filename: str, method: str, data: List[Pair]) -> None:
        with open(filename, method) as f:
            for pair in data:
                f.write(pair.word1 + '\n')
                f.write(pair.word2 + '\n')

    @staticmethod
    def count_number_of_pairs(filename: str):
        counter = 0
        with open(filename) as f:
            for _ in f:
                counter += 1

        return counter // 2


class KeyboardAdapter(AbstractInputAdapter):
    def __init__(self, input_: Callable):
        self.input_ = input_

    def get_input(self):
        return self.input_()


class PrintAdapter(AbstractOutputAdapter):
    def send_output(self, output: str):
        print(output)
