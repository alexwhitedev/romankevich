class MatrixAnalyzer:
    rates = {}
    max_rates = {}
    relevance_matrix = {}
    delta_rates = {}
    analysis_result = {}

    def __init__(self, relevance_matrix, rates, max_rates):
        self.rates = rates
        self.max_rates = max_rates
        self.relevance_matrix = relevance_matrix

    def get_analysis_result(self):
        self.calculate_delta_rating()
        self.analyze()
        return self.analysis_result

    def replace_processor(self, processor):
        if len(self.relevance_matrix.items()) == 0:
            return

        processors_to_replace = self.remove_overloads(self.relevance_matrix[processor])
        num_of_replacements = len(processors_to_replace.items())

        for replacement in processors_to_replace.keys():
            if not(self.analysis_result[processor]):
                raise Exception("Processor " + processor + " can't be replaced")
            self.rates[replacement] += self.rates[processor] / num_of_replacements

        if len(self.relevance_matrix.items()) != 0:
            del self.relevance_matrix[processor]
            for key in self.relevance_matrix.keys():
                if len(self.relevance_matrix[key].items()) != 0:
                    del self.relevance_matrix[key][processor]

        self.analysis_result[processor] = False

    def calculate_delta_rating(self):
        for key in self.rates:
            rate = self.rates[key]
            max_rate = self.max_rates[key]
            self.delta_rates[key] = max_rate - rate

    def analyze(self):
        for key in self.relevance_matrix.keys():
            possible_replacements = self.relevance_matrix[key]
            current_processor_rate = self.rates[key]
            self.analysis_result[key] = \
                self.is_possible_to_replace(current_processor_rate, possible_replacements)

    def is_possible_to_replace(self, current_processor_rate, possible_processors):
        filtered_processors = self.remove_overloads(possible_processors)

        total_rate = 0
        for processor in filtered_processors.keys():
            checking_processor_rate = possible_processors[processor]
            if checking_processor_rate >= current_processor_rate:
                return True
            else:
                total_rate += checking_processor_rate

        return total_rate >= current_processor_rate

    def remove_overloads(self, processor_rates):
        result = {}

        for processor in processor_rates.keys():
            rate = processor_rates[processor]
            if rate > self.delta_rates[processor]:
                continue
            result[processor] = rate

        return result
