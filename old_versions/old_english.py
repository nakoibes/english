import random


class Lesson:

    def __init__(self):
        self.eng_ru_dict = dict()
        self.ru_eng_dict = dict()
        self.side_ru_eng_dict = dict()
        self.side_eng_ru_dict = dict()
        self.prev_prev_dict = dict()
        self.prev_dict = dict()

    def enter_new(self):
        n = self._count_number_of_strings('../current_eng_ru.txt') // 2
        with open('../current_eng_ru.txt', 'a') as f:
            for _ in range(50 - n):
                print('--------')
                f.write(input() + '\n')
                f.write(input() + '\n')

    def start_lesson(self):
        self._get_data('../current_eng_ru.txt', self.eng_ru_dict)
        self.eng_ru_dict = self._shuffle_dict(self.eng_ru_dict)
        self.eng_ru_dict = self._forward(self.eng_ru_dict)
        print('--------------------------')
        self._get_data('../prev_prev.txt', self.prev_prev_dict, )
        self.prev_prev_dict = self._forward(self.prev_prev_dict)
        print('--------------------------')
        self._get_data('../prev.txt', self.prev_dict)

        self._get_data('../current_eng_ru.txt', self.side_eng_ru_dict)

        self._put_data('../prev_prev.txt', 'w', self.prev_dict)
        self._put_data('../prev.txt', 'w', self.eng_ru_dict)
        self._put_data('../current_eng_ru.txt', 'w', self.prev_prev_dict)

        self.eng_ru_dict = self.side_eng_ru_dict.copy()

        self.eng_ru_dict = self._shuffle_dict(self.eng_ru_dict)

        self.eng_ru_dict = self._reverse(self.eng_ru_dict)
        print('--------------------------')
        if self._count_number_of_strings('../current_ru_eng.txt') > 104:
            print('REVERSE PREPARE')
            self._get_data('../current_ru_eng.txt', self.side_ru_eng_dict)
            self.side_ru_eng_dict = self._reverse(self.side_ru_eng_dict)
            self._put_data('../current_ru_eng.txt', 'w', self.side_ru_eng_dict)
        self._put_data('../current_ru_eng.txt', 'a', self.eng_ru_dict)
        print('-----END-----')

    def _get_data(self, filename, d) -> None:
        number_of_strings = self._count_number_of_strings(filename)

        with open(filename) as f:
            for _ in range(number_of_strings // 2):
                word_one = f.readline().strip()
                word_two = f.readline().strip()
                d.update({word_one: word_two})

    @staticmethod
    def _put_data(filename, method, d) -> None:
        with open(filename, method) as f:
            for key in d.keys():
                f.write(key + '\n')
                f.write(d[key] + '\n')

    @staticmethod
    def _count_number_of_strings(filename):
        counter = 0
        with open(filename) as f:
            for _ in f:
                counter += 1

        return counter

    @staticmethod
    def _shuffle_dict(d):
        keys = list(d.keys())
        random.shuffle(keys)
        support_dict = {k: d[k] for k in keys}
        return support_dict

    @staticmethod
    def _forward(d):
        result = dict()
        for key in d.keys():
            print(key)
            print('translate or 0')
            inp = input()
            if inp == '0':
                result.update({key: d[key]})
                print(f'translation is {d[key]}')
                input()
            else:
                print(f'translation is {d[key]}')
                inp = input()
                if inp == '0':
                    result.update({key: d[key]})
                    input()

        d = result.copy()
        keys = list(d.keys())
        while d:
            for key in list(keys):
                print(key)
                print('translate or 0')
                inp = input()
                if inp == '0':
                    print(f'translation is {d[key]}')
                    input()
                else:
                    print(f'translation is {d[key]}')
                    inp = input()
                    if inp == '0':
                        input()
                    else:
                        d.pop(key)
            keys = d.keys()
        return result

    @staticmethod
    def _reverse(d):
        result = dict()
        support_dict = dict()
        for key in d.keys():
            print(d[key])
            print('translate or 0')
            inp = input()
            if inp == '0':
                result.update({key: d[key]})
                print(f'translation is {key}')
                input()
            else:
                print(f'translation is {key}')
                inp = input()
                if inp == '0':
                    result.update({key: d[key]})
                    input()

        d = result.copy()
        keys = list(d.keys())
        while d:
            for key in list(keys):
                print(d[key])
                print('translate or 0')
                inp = input()
                if inp == '0':
                    print(f'translation is {key}')
                    input()
                else:
                    print(f'translation is {key}')
                    inp = input()
                    if inp == '0':
                        input()
                    else:
                        d.pop(key)
            keys = d.keys()
        return result


def main():
    lesson = Lesson()
    while True:
        print('1.Start lesson')
        print('2.Enter new words')
        print('3.Exit')
        print('Enter you choice')
        case = input()
        if case == '1':
            lesson.start_lesson()
        elif case == '2':
            lesson.enter_new()
        else:
            break
    print('Good bye!')



if __name__ == '__main__':
    main()
