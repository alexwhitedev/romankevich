import sys
import os


# import pprint

## TODO 1
##
##
##
##
##
##

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
    print(F)
    return F


def uno_zero_generating(hash_vector):
    list_of_vectors = []
    for key in hash_vector.keys():
        # print(key)
        hash_vector[key] = 0
        list_of_vectors.append(hash_vector.copy())
        hash_vector[key] = 1
    # for item in list_of_vectors:
        # print(item)
    return list_of_vectors


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
    list_of_zero_generator = uno_zero_generating(hash_vector)
    for item in list_of_zero_generator:
        print(item)
        calculate_func(item)
