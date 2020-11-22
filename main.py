import readers
import matrixanalyzer

reader = readers.RatingsReader('ratings.csv')

ratings = reader.get_ratings()
max_ratings = reader.get_max_ratings()

reader = readers.RelevanceMatrixReader('relevance_matrix.csv')

relevance_matrix = reader.get_relevance_matrix()


def calculate_func(hash_vector):
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


analyzer = matrixanalyzer.MatrixAnalyzer(relevance_matrix, ratings, max_ratings)


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
    for item in vector_list:
        if calculate_func(item) == 1:
            counter_1 += 1
        else:
            counter_0 += 1
    return {
        'ok': counter_1,
        'not-ok': counter_0
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


def calculate_durability(vector):
    result = 1.0
    vector_len = len(vector.items())
    p = (1 - 1 / vector_len)
    q = 1 / vector_len

    for key in vector.keys():
        V = vector[key]
        result = result * (V * p + (1 - V) * q)

    return result

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

    result_list = []
    for item in lists:
        print(len(item))
        result_list.append(calculate_list_of_vectors(item))

    durability = calculate_durability(lists[0][5])
    print(f"Durability = {durability}")

    counter = 0
    for item in result_list:
        counter += 1
        print(f"result of {counter}: {item}")
