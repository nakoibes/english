from abc import ABCMeta, abstractmethod
from collections import deque
from typing import List

from adapters import AbstractInputAdapter, AbstractOutputAdapter
from models import WordStatus, WordBelonging, Word
from word_repository import AbstractWordRepository


class AbstractWordService(metaclass=ABCMeta):
    @abstractmethod
    def get_current_words(self) -> List[Word]:
        pass

    @abstractmethod
    def get_previous_words(self) -> List[Word]:
        pass

    @abstractmethod
    def get_pre_previous_words(self) -> List[Word]:
        pass

    @abstractmethod
    def get_reverse_pool_words(self) -> List[Word]:
        pass

    @abstractmethod
    def passage(self, data: List[Word], reverse: bool = False) -> List[Word]:
        pass

    @abstractmethod
    def input(self) -> str:
        pass

    @abstractmethod
    def output(self, string: str) -> None:
        pass

    @abstractmethod
    def put_words(self, words: List[Word]) -> None:
        pass

    @abstractmethod
    def transfer_to_reverse_pool(self, words: List[Word]) -> None:
        pass

    @abstractmethod
    def get_all_words(self) -> List[Word]:
        pass


class WordService(AbstractWordService):
    def __init__(self,
                 repository: AbstractWordRepository,
                 input_adapter: AbstractInputAdapter,
                 output_adapter: AbstractOutputAdapter):
        self.repository = repository
        self.input_adapter = input_adapter
        self.output_adapter = output_adapter

    def get_current_words(self) -> List[Word]:
        return self.repository.get_words_by_status_belonging(WordStatus.FAILED, WordBelonging.CURRENT)

    def get_previous_words(self) -> List[Word]:
        return self.repository.get_words_by_status_belonging(WordStatus.FAILED, WordBelonging.PREVIOUS)

    def get_pre_previous_words(self) -> List[Word]:
        return self.repository.get_words_by_status_belonging(WordStatus.FAILED, WordBelonging.PRE_PREVIOUS)

    def get_reverse_pool_words(self) -> List[Word]:
        return self.repository.get_words_by_status_belonging(WordStatus.FAILED, WordBelonging.REVERSE_POOL)

    def get_all_words(self) -> List[Word]:
        return self.repository.get_words()

    def put_words(self, words: List[Word]) -> None:
        self.repository.put_words(words)

    def passage(self, data: List[Word], reverse: bool = False) -> List[Word]:
        failed = list()
        for word in data:
            if not reverse:
                status = self.word_check(word.word_to_translate, word.translation)
            else:
                status = self.word_check(word.translation, word.word_to_translate)
            if status:
                word.translate()
            else:
                word.fail()
                failed.append(word)
        words = deque(failed)
        while words:
            word = words.popleft()
            if not reverse:
                status = self.word_check(word.word_to_translate, word.translation)
            else:
                status = self.word_check(word.translation, word.word_to_translate)
            if status:
                word.translate()
            else:
                word.fail()
                words.append(word)
        return failed

    def word_check(self, question: str, answer: str) -> bool:
        self.output_adapter.send_output(question)
        input_ = self.input_adapter.get_input()
        while not self.first_validation(input_):
            input_ = self.input_adapter.get_input()
        if input_ == '0':
            self.output_adapter.send_output(f'translation is {answer}')
            self.input_adapter.get_input()
            return False
        else:
            self.output_adapter.send_output(f'translation is {answer}')
            input_ = self.input_adapter.get_input()
            while self.second_validation(input_):
                input_ = self.input_adapter.get_input()
            if input_ == '0':
                self.input_adapter.get_input()
                return False
        return True

    def input(self) -> str:
        return self.input_adapter.get_input()

    def output(self, string: str) -> None:
        self.output_adapter.send_output(string)

    def transfer_to_reverse_pool(self, words: List[Word]) -> None:
        for word in words:
            word.belonging = WordBelonging.REVERSE_POOL

    @staticmethod
    def first_validation(input_):
        return input_ == '0' or input_ == '1' or len(input_) >= 2

    @staticmethod
    def second_validation(input_):
        return input_ == '0' or input_ == '1'
