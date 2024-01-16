class NewWilks:  # todo: code this up, test, docstring
    def __init__(self):
        self.male_coeff = [
            47.4617885411949,
            8.47206137941125,
            0.073694103462609,
            -1.39583381094385e-3,
            7.07665973070743e-6,
            -1.20804336482315e-8,
        ]
        self.female_coeff = [
            -125.425539779509,
            13.7121941940668,
            -0.0330725063103405,
            -1.0504000506583e-3,
            9.38773881462799e-6,
            -2.3334613884954e-8,
        ]

    def calculate_new_wilks(self, body_weight, total, is_female):
        denominator = self.female_coeff[0] if is_female else self.male_coeff[0]
        coeff = self.female_coeff if is_female else self.male_coeff
        min_bw = 40
        max_bw = 150.95 if is_female else 200.95
        bw = min(max(body_weight, min_bw), max_bw)
        for i in range(1, len(coeff)):
            denominator += coeff[i] * pow(bw, i)
        score = (600 / denominator) * total
        return round(score, 2)
