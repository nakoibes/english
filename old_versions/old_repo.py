
# class AbstractWordRepository(metaclass=ABCMeta):
#     @abstractmethod
#     def get_current(self) -> List[Word]:
#         pass
#
#     @abstractmethod
#     def get_current_swap(self) -> List[Word]:
#         pass
#
#     @abstractmethod
#     def get_previous(self) -> List[Word]:
#         pass
#
#     @abstractmethod
#     def get_pre_previous(self) -> List[Word]:
#         pass
#
#     @abstractmethod
#     def put_current(self, data: List[Word], method: str = 'w') -> None:
#         pass
#
#     @abstractmethod
#     def put_current_swap(self, data: List[Word], method: str = 'w') -> None:
#         pass
#
#     @abstractmethod
#     def put_previous(self, data: List[Word], method: str = 'w') -> None:
#         pass
#
#     @abstractmethod
#     def put_pre_previous(self, data: List[Word], method: str = 'w') -> None:
#         pass


# class FileWordRepository(AbstractWordRepository):
#     def __init__(self, current: str, current_swap: str, previous: str, pre_previous: str):
#         self.current = current
#         self.current_swap = current_swap
#         self.previous = previous
#         self.pre_previous = pre_previous
#
#     def get_current(self):
#         return self._get_data(self.current)
#
#     def get_current_swap(self):
#         return self._get_data(self.current_swap)
#
#     def get_previous(self):
#         return self._get_data(self.previous)
#
#     def get_pre_previous(self):
#         return self._get_data(self.pre_previous)
#
#     def put_current(self, data: List[Word], method: str = 'w'):
#         self._put_data(self.current, method, data)
#
#     def put_current_swap(self, data: List[Word], method: str = 'w'):
#         self._put_data(self.current_swap, method, data)
#
#     def put_previous(self, data: List[Word], method: str = 'w'):
#         self._put_data(self.previous, method, data)
#
#     def put_pre_previous(self, data: List[Word], method: str = 'w'):
#         self._put_data(self.pre_previous, method, data)
#
#     def _get_data(self, filename) -> List[Word]:
#         data = list()
#         with open(filename) as f:
#             number_of_strings = self.count_number_of_pairs(filename)
#             for _ in range(number_of_strings):
#                 word_one = f.readline().strip()
#                 word_two = f.readline().strip()
#                 data.append(Word(word_one, word_two))
#         return data
#
#     @staticmethod
#     def _put_data(filename: str, method: str, data: List[Word]) -> None:
#         with open(filename, method) as f:
#             for pair in data:
#                 f.write(pair.word1 + '\n')
#                 f.write(pair.word2 + '\n')
#
#     @staticmethod
#     def count_number_of_pairs(filename: str):
#         counter = 0
#         with open(filename) as f:
#             for _ in f:
#                 counter += 1
#
#         return counter // 2

