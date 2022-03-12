from dataclasses import field, dataclass, asdict
import datetime
from enum import Enum, auto
from uuid import uuid4
import logging
import logging.config
from typing import Optional


class WordStatus(Enum):
    UNASSIGNED = 'unassigned'
    ASSIGNED = 'assigned'
    FAILED = 'failed'
    TRANSLATED = 'translated'
    ARCHIEVED = 'achieved'

    def __repr__(self):
        return self.value

    def __str__(self):
        return self.value


class WordBelonging(Enum):
    CURRENT = 'current'
    PREVIOUS = 'previous'
    PRE_PREVIOUS = 'pre_previous'
    REVERSE_POOL = 'reverse_pool'

    def __repr__(self):
        return self.value

    def __str__(self):
        return self.value


@dataclass
class WordMetadata:
    id: str = field(default_factory=uuid4)
    created_at: datetime.datetime = field(default_factory=datetime.datetime.now)
    modified_on: Optional[datetime.datetime] = field(default=None)

    def modify(self):
        self.modified_on = datetime.datetime.now()


class WordStateMachine:
    allowed_transformations = {WordStatus.UNASSIGNED: [WordStatus.ASSIGNED],
                               WordStatus.ASSIGNED: [WordStatus.FAILED, WordStatus.TRANSLATED],
                               WordStatus.FAILED: [WordStatus.ASSIGNED],
                               WordStatus.TRANSLATED: [WordStatus.ARCHIEVED]
                               }

    def __get__(self, instance, owner):
        return self.allowed_transformations.get(instance.status, list())


class WordBelongingMachine:
    allowed_transformations = {WordBelonging.CURRENT: [WordBelonging.PREVIOUS],
                               WordBelonging.PREVIOUS: [WordBelonging.PRE_PREVIOUS],
                               WordBelonging.PRE_PREVIOUS: [WordBelonging.CURRENT]
                               }

    def __get__(self, instance, owner):
        return self.allowed_transformations.get(instance.status, list())


@dataclass
class Word:
    word_to_translate: str
    translation: str
    metadata: WordMetadata = field(default_factory=WordMetadata)
    status: WordStatus = field(default=WordStatus.UNASSIGNED)
    belonging: WordBelonging = field(default=WordBelonging.CURRENT)
    _next_statuses = WordStateMachine()
    _next_belonging = {WordBelonging.CURRENT: WordBelonging.PREVIOUS,
                       WordBelonging.PREVIOUS: WordBelonging.PRE_PREVIOUS,
                       WordBelonging.PRE_PREVIOUS: WordBelonging.CURRENT,
                       WordBelonging.REVERSE_POOL: WordBelonging.REVERSE_POOL
                       }

    def assign(self):
        if WordStatus.ASSIGNED in self._next_statuses:
            prev_status = self.status
            self.status = WordStatus.ASSIGNED
            self.metadata.modify()
            logging.info(f"word {self.word_to_translate} changed status from {prev_status} to ASSIGNED")
        else:
            logging.info(f"Change status to translate word {self.word_to_translate} was not permitted")

    def translate(self):
        if WordStatus.TRANSLATED in self._next_statuses:
            prev_status = self.status
            self.status = WordStatus.TRANSLATED
            self.metadata.modify()
            logging.info(f"word {self.word_to_translate} changed status from {prev_status} to TRANSLATED")
        else:
            logging.info(f"Change status to translate word {self.word_to_translate} was not permitted")

    def fail(self):
        if WordStatus.ASSIGNED in self._next_statuses:
            prev_status = self.status
            self.status = WordStatus.ASSIGNED
            self.metadata.modify()
            logging.info(f"word {self.word_to_translate} changed status from {prev_status} to ASSIGNED")
        else:
            logging.info(f"Change status to translate word {self.word_to_translate} was not permitted")

    def next_belonging(self):
        self.belonging = self._next_belonging[self.belonging]
