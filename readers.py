class RatingsReader:
    file_path = ""

    def __init__(self, file_path):
        self.file_path = file_path

    def get_ratings_on_position(self, position):
        file_ratings = open(self.file_path, 'r')
        ratings = {}

        for row in file_ratings:
            elements = row.split(',')
            if elements[0].startswith('P'):
                ratings[elements[0]] = int(elements[position])

        file_ratings.close()
        return ratings

    def get_ratings(self):
        return self.get_ratings_on_position(1)

    def get_max_ratings(self):
        return self.get_ratings_on_position(2)


class RelevanceMatrixReader:
    file_path = ""

    def __init__(self, file_path):
        self.file_path = file_path

    def get_relevant_processors(self, array, header):
        result = {}
        i = 0

        while i < len(array):
            element = array[i]
            try:
                result[header[i].replace('\n', '')] = int(element)
            except:
                pass
            i += 1

        return result

    def get_relevance_matrix(self):
        file_relevance_matrix = open(self.file_path, 'r')
        relevance_matrix = {}

        header = []
        for row in file_relevance_matrix:
            elements = row.split(',')
            if elements[0].startswith('P'):
                relevance_matrix[elements[0]] = self.get_relevant_processors(elements, header)
            else:
                header = elements

        file_relevance_matrix.close()
        return relevance_matrix
