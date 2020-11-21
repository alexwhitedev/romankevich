import sys
import os
import csv


def calculate_func(hash_vector):
    f1 = hash_vector['D1'] and hash_vector['D2'] and hash_vector['D3'] and hash_vector['C1'] and hash_vector['C2'] and (
            hash_vector['B1'] or hash_vector['B2']) and (
                 hash_vector['P1'] or hash_vector['P2'] or hash_vector['A1'] and hash_vector['M1'] and hash_vector['A2'] and (
                         hash_vector['B3'] or hash_vector['B5']) and hash_vector['P6'])
    f2 = hash_vector['D6'] and hash_vector['C4'] and hash_vector['M1'] and hash_vector['A1'] and (
            hash_vector['B3'] or hash_vector['B5']) and (hash_vector['P2'] or hash_vector['P3'])

    f3 = hash_vector['D7'] and hash_vector['D8'] and hash_vector['C5'] and hash_vector['B3'] and (
            hash_vector['P6'] or hash_vector['A2'] and hash_vector['M1'] and hash_vector['A1'] and (
            hash_vector['B1'] or hash_vector['B2']) and hash_vector['P3'])

    f4 = hash_vector['D8'] and hash_vector['C6'] and (
            hash_vector['B3'] and hash_vector['P6'] or hash_vector['B4'] and hash_vector['P6'] or hash_vector['B4'] and
            hash_vector['A3'] and hash_vector['B5'] and hash_vector['A2'] and hash_vector['M1'] and hash_vector[
                'A1'] and (
                    hash_vector['B1'] or hash_vector['B2']
            ) and hash_vector['P1']
    )

    F = f1 and f2 and f3 and f4
    return F


def uno_zero_generating(hash_vector_input):
    hash_vector = hash_vector_input
    list_of_vectors = []
    for key in hash_vector.keys():
        hash_vector[key] = 0
        list_of_vectors.append(hash_vector.copy())
        hash_vector[key] = 1
    return list_of_vectors


def generating(hash_vector, hash_vector_popped, list_of_vectors, deep):
    # print(deep)
    deep -= 1
    for key in hash_vector_popped.keys():

        hash_vector_copy = hash_vector.copy()
        hash_vector_copy[key] = 0

        popped_hash_vector = hash_vector_popped.copy()
        popped_hash_vector.pop(key)

        if deep == 1:
            for key_max in popped_hash_vector.keys():
                hash_vector_copy[key_max] = 0
                if hash_vector_copy not in list_of_vectors:
                    list_of_vectors.append(hash_vector_copy.copy())
                hash_vector_copy[key_max] = 1
        else:
            list_of_vectors = generating(hash_vector_copy, popped_hash_vector, list_of_vectors, deep)

    return list_of_vectors


def calculate_list_of_vectors(vector_list):
    counter_1 = 0
    counter_0 = 0
    for item in vector_list:
        if calculate_func(item) == 1:
            counter_1 += 1
        else:
            counter_0 += 1
    return {
        'ok': counter_1,
        'not-ok': counter_0
    }


if __name__ == '__main__':
    hash_vector = {
        'P1': 1,
        'P2': 1,
        'P3': 1,
        'P6': 1,
        'A1': 1,
        'A2': 1,
        'A3': 1,
        'C1': 1,
        'C2': 1,
        'C4': 1,
        'C5': 1,
        'C6': 1,
        'D1': 1,
        'D2': 1,
        'D3': 1,
        'D6': 1,
        'D7': 1,
        'D8': 1,
        'B1': 1,
        'B2': 1,
        'B3': 1,
        'B4': 1,
        'B5': 1,
        'M1': 1
    }

    calculate_func(hash_vector)
    lists = [uno_zero_generating(hash_vector)]
    for i in range(2, 5):
        lists.append(generating(hash_vector, hash_vector, [], i))


    result_list = []
    for item in lists:
        print(len(item))
        result_list.append(calculate_list_of_vectors(item))

    counter = 0
    for item in result_list:
        counter += 1
        print(f"result of {counter}: {item}")




#
# def double_zero_generating(hash_vector):
#     list_of_vectors = []
#
#     for key_first in hash_vector.keys():
#
#         hash_vector_copy = hash_vector.copy()
#         hash_vector_copy[key_first] = 0
#
#         poped_hash_vector = hash_vector_copy.copy()
#         poped_hash_vector.pop(key_first)
#         for key_second in poped_hash_vector.keys():
#             hash_vector_copy[key_second] = 0
#             if hash_vector_copy not in list_of_vectors:
#                 list_of_vectors.append(hash_vector_copy.copy())
#             hash_vector_copy[key_second] = 1
#
#     return list_of_vectors

#
# def tripple_zero_generating(hash_vector):
#     list_of_vectors = []
#
#     for key_first in hash_vector.keys():
#
#         hash_vector_copy = hash_vector.copy()
#         hash_vector_copy[key_first] = 0
#
#         poped_hash_vector = hash_vector_copy.copy()
#         poped_hash_vector.pop(key_first)
#
#         for key_second in poped_hash_vector.keys():
#             hash_vector_copy[key_second] = 0
#
#             double_poped_hash_vector = poped_hash_vector.copy()
#             double_poped_hash_vector.pop(key_second)
#
#             for key_third in double_poped_hash_vector.keys():
#                 hash_vector_copy[key_third] = 0
#                 if hash_vector_copy not in list_of_vectors:
#                     list_of_vectors.append(hash_vector_copy.copy())
#                 hash_vector_copy[key_third] = 1
#
#             hash_vector_copy[key_second] = 1
#
#     return list_of_vectors