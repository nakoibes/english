import json
import logging
from abc import ABCMeta, abstractmethod
from dataclasses import asdict
from typing import List

from models import Word, WordBelonging, WordStatus

logger = logging.getLogger(__name__)


class AbstractWordRepository(metaclass=ABCMeta):
    @abstractmethod
    def get_words_by_status_belonging(self, status: WordStatus, belonging: WordBelonging) -> List[Word]:
        pass

    @abstractmethod
    def get_words(self) -> List[Word]:
        pass

    @abstractmethod
    def put_words(self, data: List[Word]) -> None:
        pass


class JsonWordRepository(AbstractWordRepository):
    def __init__(self, jsonpath: str):
        self.jsonpath = jsonpath

    def get_words_by_status_belonging(self, status: WordStatus, belonging: WordBelonging) -> List[Word]:
        words = self.get_words()
        return [word for word in words if word.belonging == belonging and word.status == status]

    def get_words(self) -> List[Word]:
        with open(self.jsonpath) as f:
            raw_data = json.load(f)
            return [Word(**word) for word in raw_data]

    def put_words(self, data: List[Word]) -> None:
        with open(self.jsonpath, "w") as f:
            data = [asdict(word) for word in data]
            json.dump(data, f, default=str)
