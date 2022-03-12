import logging

from adapters import InputAdapter, OutputAdapter
from develop import Lesson
from config import Config
from service import WordService
from word_repository import JsonWordRepository

logging.basicConfig(format=Config.LOG_FORMAT,
                    level=Config.LOG_LEVEL,
                    filename=Config.LOG_FILENAME,
                    filemode=Config.LOG_FILEMOD)
logger = logging.getLogger(__name__)


def main():
    input_adapter = InputAdapter(input)
    output_adapter = OutputAdapter(print)
    repository = JsonWordRepository("word_storage.json")
    service = WordService(repository, input_adapter, output_adapter)
    lesson = Lesson(service)
    while True:
        output_adapter.send_output('1.Start lesson')
        output_adapter.send_output('2.Enter new words')
        output_adapter.send_output('3.Exit')
        output_adapter.send_output('Enter you choice')
        case = input_adapter.get_input()
        if case == '1':
            lesson.start_lesson()
        elif case == '2':
            pass
            lesson.enter_new()
        else:
            break
    output_adapter.send_output('Good bye!')


if __name__ == '__main__':
    main()
