from random import shuffle
from typing import List

from models import Word
from service import AbstractWordService


class Lesson:
    def __init__(self,
                 service: AbstractWordService,
                 reverse_pool_number: int = 50,
                 main_size: int = 50
                 ):
        self.service = service
        self.reverse_pool_number = reverse_pool_number
        self.demarcation = '--------------------------'
        self.main_size = main_size

    def start_lesson(self):
        current_failed = self.process_current()
        pre_previous_failed = self.process_pre_precious()
        previous = self.service.get_previous_words()
        current_reverse_failed = self.process_current_reverse()
        current_swap_failed = self.process_reverse_pool()
        result = current_failed + previous + pre_previous_failed + current_reverse_failed + current_swap_failed
        self.process_result(result)

    def process_current(self) -> List[Word]:
        current = self.service.get_current_words()
        shuffle(current)
        current_failed = self.service.passage(current)
        self.service.output(self.demarcation)
        return current_failed

    def process_pre_precious(self) -> List[Word]:
        pre_previous = self.service.get_pre_previous_words()
        pre_previous_failed = self.service.passage(pre_previous)
        self.service.output(self.demarcation)
        return pre_previous_failed

    def process_current_reverse(self) -> List[Word]:
        current_reverse = self.service.get_current_words()
        shuffle(current_reverse)
        current_reverse_failed = self.service.passage(current_reverse, True)
        self.service.transfer_to_reverse_pool(current_reverse_failed)
        self.service.output(self.demarcation)
        return current_reverse_failed

    def process_reverse_pool(self) -> List[Word]:
        reverse_pool = self.service.get_reverse_pool_words()
        reverse_pool_failed = list()
        if len(reverse_pool) > self.reverse_pool_number:
            self.service.output('REVERSE POOL')
            shuffle(reverse_pool)
            reverse_pool_failed = self.service.passage(reverse_pool, True)
        return reverse_pool_failed

    def process_result(self, result: List[Word]) -> None:
        for word in result:
            word.next_belonging()
        self.service.put_words(result)
        self.service.output('---------END---------')

    def enter_new(self) -> None:
        current_size = len(self.service.get_current_words())
        additional_words = list()
        for _ in range(self.main_size - current_size):
            self.service.output(self.demarcation)
            term = self.service.input()
            translation = self.service.input()
            word = Word(term, translation)
            word.assign()
            additional_words.append(word)
        words = self.service.get_all_words()
        self.service.put_words(words + additional_words)
