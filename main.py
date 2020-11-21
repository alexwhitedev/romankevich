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

if __name__ == '__main__':
    hash_vector = {
        'P1': 0,
        'P2': 0,
        'P3': 0,
        'P6': 0,
        'A1': 0,
        'A2': 0,
        'C1': 0,
        'C2': 0,
        'C4': 0,
        'C5': 0,
        'C6': 0,
        'D1': 0,
        'D2': 0,
        'D3': 0,
        'D6': 0,
        'D7': 0,
        'D8': 0,
        'B1': 0,
        'B2': 0,
        'B3': 0,
        'B4': 0,
        'B5': 0,
        'M1': 0
    }

    # print(1 or 0)
    f1 = hash_vector['D1'] and hash_vector['D2'] and hash_vector['D3'] and hash_vector['C1'] and hash_vector['C2'] and (
            hash_vector['B1'] or hash_vector['B2']) and (
                 hash_vector['P1'] or hash_vector['P2'] or hash_vector['A1'] and hash_vector['M1'] and hash_vector[
             'A2'] and (
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

