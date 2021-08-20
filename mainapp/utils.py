from random import randint, random


def get_random_number():
    return randint(4, 15) * random()


def del_slashes(subsequence):
    return [item.replace(item[0], '') for item in subsequence]