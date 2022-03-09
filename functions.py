import random
from collections import deque

from typing import Dict


def get_data(filename: str) -> Dict[str, str]:
    data = {}
    number_of_strings = count_number_of_strings(filename)
    with open(filename) as f:
        for _ in range(number_of_strings // 2):
            word_one = f.readline().strip()
            word_two = f.readline().strip()
            data.update({word_one: word_two})
    return data


def count_number_of_strings(filename: str):
    counter = 0
    with open(filename) as f:
        for _ in f:
            counter += 1

    return counter


def shuffle_dict(d: Dict[str, str]):
    keys = list(d.keys())
    random.shuffle(keys)
    support_dict = {k: d[k] for k in keys}
    return support_dict


def put_data(filename: str, method: str, d: Dict[str, str]) -> None:
    with open(filename, method) as f:
        for key in d.keys():
            f.write(key + '\n')
            f.write(d[key] + '\n')


def passage(data: Dict[str, str], flag='forward'):
    result = dict()
    for key, value in data.items():
        if flag == 'forward':
            status = word_check(key, value)
        else:
            status = word_check(value, key)
        if not status:
            result.update({key: data[key]})
    items = list(result.items())
    words = deque(items)
    while words:
        left_value, right_value = words.popleft()
        if flag == 'forward':
            status = word_check(left_value, right_value)
        else:
            status = word_check(right_value, left_value)
        if not status:
            words.append((left_value, right_value))

    return result


def word_check(question: str, answer: str):
    print(question)
    inp = input()
    while inp != '0' and inp != '1' and len(inp) < 2:  # and not isdigit(inp)
        inp = input()
    if inp == '0':
        print(f'translation is {answer}')
        input()
        return False
    else:
        print(f'translation is {answer}')
        inp = input()
        while inp != '0' and inp != '1':
            inp = input()
        if inp == '0':
            input()
            return False
    return True


def start_lesson(number: int):
    eng_ru_dict = get_data('current_eng_ru.txt')
    eng_ru_dict = shuffle_dict(eng_ru_dict)
    eng_ru_dict = passage(eng_ru_dict)
    print('--------------------------')
    prev_prev_dict = get_data('prev_prev.txt')
    prev_prev_dict = passage(prev_prev_dict)
    print('--------------------------')
    prev_dict = get_data('prev.txt')
    side_eng_ru_dict = get_data('current_eng_ru.txt')
    put_data('prev_prev.txt', 'w', prev_dict)
    put_data('prev.txt', 'w', eng_ru_dict)
    put_data('current_eng_ru.txt', 'w', prev_prev_dict)
    eng_ru_dict = side_eng_ru_dict.copy()
    eng_ru_dict = shuffle_dict(eng_ru_dict)
    eng_ru_dict = passage(eng_ru_dict, 'reverse')
    print('--------------------------')
    if count_number_of_strings('current_ru_eng.txt') > 2 * number:
        print('REVERSE PREPARE')
        side_ru_eng_dict = get_data('current_ru_eng.txt')
        side_ru_eng_dict = shuffle_dict(side_ru_eng_dict)
        side_ru_eng_dict = passage(side_ru_eng_dict, 'reverse')
        put_data('current_ru_eng.txt', 'w', side_ru_eng_dict)
    put_data('current_ru_eng.txt', 'a', eng_ru_dict)
    print('-----END-----')


def enter_new(number: int):
    n = count_number_of_strings('current_eng_ru.txt') // 2
    with open('current_eng_ru.txt', 'a') as f:
        for _ in range(number - n):
            print('--------')
            f.write(input() + '\n')
            f.write(input() + '\n')
