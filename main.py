import os

import matrixanalyzer
import readers
from random import randint
import pandas as pd

reader = readers.RatingsReader('ratings.csv')

ratings = reader.get_ratings()
max_ratings = reader.get_max_ratings()

reader = readers.RelevanceMatrixReader('relevance_matrix.csv')

relevance_matrix = reader.get_relevance_matrix()

analyzer = matrixanalyzer.MatrixAnalyzer(relevance_matrix, ratings, max_ratings)


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
    processors_can_be_replaced = matrixanalyzer \
        .MatrixAnalyzer(relevance_matrix, ratings, max_ratings) \
        .get_analysis_result()
    hash_vector = hash_vector_input
    list_of_vectors = []
    for key in hash_vector.keys():
        if not (key.startswith('P') and processors_can_be_replaced[key]):
            hash_vector[key] = 0
        list_of_vectors.append(hash_vector.copy())
        hash_vector[key] = 1
    return list_of_vectors


def generating(hash_vector, hash_vector_popped, list_of_vectors, deep):
    deep -= 1

    processors_can_be_replaced = analyzer.get_analysis_result()
    for key in hash_vector_popped.keys():

        hash_vector_copy = hash_vector.copy()

        if not (key.startswith('P') and processors_can_be_replaced[key]):
            hash_vector_copy[key] = 0
        else:
            analyzer.replace_processor(key)

        popped_hash_vector = hash_vector_popped.copy()
        popped_hash_vector.pop(key)

        if deep == 1:
            for key_max in popped_hash_vector.keys():
                if not (key.startswith('P') and processors_can_be_replaced[key]):
                    hash_vector_copy[key_max] = 0
                list_of_vectors.append(hash_vector_copy.copy())
                hash_vector_copy[key_max] = 1
        else:
            list_of_vectors = generating(hash_vector_copy, popped_hash_vector, list_of_vectors, deep)

    return list_of_vectors


def calculate_list_of_vectors(vector_list):
    counter_1 = 0
    counter_0 = 0
    shits = []
    for item in vector_list:
        if calculate_func(item) == 1:
            counter_1 += 1
        else:
            counter_0 += 1
            shits.append(item)
    return {
        'ok': counter_1,
        'not-ok': counter_0,
        'shits': shits
    }


def clear(l):
    seen = set()
    new_l = []
    for d in l:
        t = tuple(d.items())
        if t not in seen:
            seen.add(t)
            new_l.append(d)
    return new_l


def bullshit_element_finding(input_list):
    bullshits_vector = {
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
    for key in bullshits_vector.keys():
        bullshits_vector[key] = 0
    for item in input_list:
        for key in item.keys():
            if item[key] == 0:
                bullshits_vector[key] += 1
    max_bullshit_count = max([bullshits_vector[key] for key in bullshits_vector.keys()])
    for key in bullshits_vector.keys():
        if bullshits_vector[key] == max_bullshit_count:
            return [key, bullshits_vector]


def create_results(lists, input_len):
    result_list = []
    for item in lists:
        final_len = int(round(len(item) * input_len / 100))
        print(f"{final_len}")
        new_item = item.copy()
        while len(new_item) > final_len:
            new_item.pop(randint(0, len(new_item) - 1))
        result_list.append(calculate_list_of_vectors(new_item))
    counter = 0
    edf = pd.DataFrame()
    for item in result_list:
        bullshit_elements_couple = bullshit_element_finding(item['shits'])
        ndf = pd.DataFrame(bullshit_elements_couple[1], index=[1])
        ndf['worse'] = bullshit_elements_couple[0]
        edf = pd.concat([edf, ndf])
        edf.to_excel(os.path.join(f'{input_len}.xlsx'))
        counter += 1
        print(
            f"{input_len}% result of {counter}: 'ok = ' {item['ok']}, not-ok = {item['not-ok']}, bullshit-element = {bullshit_elements_couple}")


def calculate_durability(vector):
    q = {
        'Pi': 1.2 * (1 / (10 ** 4)),
        'Ai': 1.1 * (1 / (10 ** 4)),
        'Ci': 1.9 * (1 / (10 ** 4)),
        'Di': 3.2 * (1 / (10 ** 5)),
        'Bi': 1.4 * (1 / (10 ** 5)),
        'Mi': 3.3 * (1 / (10 ** 4))
    }
    result = 1.0

    for key in vector.keys():
        V = vector[key]
        if key.startswith('P'):
            result = result * get_result_for('Pi', q, V)
        elif key.startswith('A'):
            result = result * get_result_for('Ai', q, V)
        elif key.startswith('C'):
            result = result * get_result_for('Ci', q, V)
        elif key.startswith('D'):
            result = result * get_result_for('Di', q, V)
        elif key.startswith('B'):
            result = result * get_result_for('Bi', q, V)
        elif key.startswith('M'):
            result = result * get_result_for('Mi', q, V)

    return result


def get_result_for(elem, q, V):
    p = (1.0 - q[elem])
    return V * p + (1 - V) * q[elem]


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
        duplicates_list = generating(hash_vector, hash_vector, [], i)
        lists.append(clear(duplicates_list))

    with open('durability.data', 'w+') as file:
        file.writelines('')

    for i in range(0, 4):
        durability_sum = 0
        durability_count = 0
        for j in range(0, len(lists[i])):
            durability_sum += calculate_durability(lists[i][j])
            durability_count += 1
        durability = durability_sum / durability_count
        print(f"Durability = {durability}")
        with open('durability.data', 'a+') as file:
            file.writelines(f'{durability}\n')

    create_results(lists, 100)
    create_results(lists, 50)
    create_results(lists, 10)
