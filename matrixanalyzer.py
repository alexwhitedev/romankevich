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

        self.calculate_delta_rating()
        self.analyze()

    def get_analysis_result(self):
        return self.analysis_result

    def analyze(self):
        for key in self.relevance_matrix.keys():
            possible_replacements = self.relevance_matrix[key]
            current_processor_rate = self.rates[key]
            self.analysis_result[key] = \
                self.is_possible_to_replace(current_processor_rate, possible_replacements)

    def calculate_delta_rating(self):
        for key in self.rates:
            rate = self.rates[key]
            max_rate = self.max_rates
            self.delta_rates[key] = max_rate - rate

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
            if rate > self.delta_rates:
                continue
            result[processor] = rate

        return result
