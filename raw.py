from collections import deque


def word_check(question, answer):
    print(question)
    inp = input()
    while inp != '0' and inp != '1' and len(inp) < 2:
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


def passage(data, flag='forward'):
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


passage({"cat": "кошка", "dog": "собака", "mouse": "мышь", "parrot": "попугай"})
