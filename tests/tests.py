import sys

from functions import get_data
import mock


def t():
    a = input()
    b = input()
    # print(input())
    # print(input())


def test_get_data():
    with open("test_get_data.txt") as data:
        sys.stdin = data
    # with mock.patch("builtins.input", return_value="123\n321"):
    #     t()


# def start_tests():
#     test_get_data()
#
#
# if __name__ == "__main__":
#     start_tests()
