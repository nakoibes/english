from functions import *


def main():
    number = 50
    while True:
        print('1.Start lesson')
        print('2.Enter new words')
        print('3.Exit')
        print('Enter you choice')
        case = input()
        if case == '1':
            start_lesson(number)
        elif case == '2':
            pass
            enter_new(number)
        else:
            break
    print('Good bye!')


if __name__ == '__main__':
    main()
