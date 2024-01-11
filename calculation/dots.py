
class DOTS:  # todo: docstring
    """
    formula:

    $\text{Result} \times \dfrac{500}{A \cdot Bw^4 + B \cdot Bw^3 + C
    \cdot Bw^2 + D \cdot Bw + E$
    """
    def __init__(self):
        self.male_coeff = [
            -307.75076,
            24.0900756,
            -0.1918759221,
            0.0007391293,
            -0.000001093
        ]
        self.female_coeff = [
            -57.96288,
            13.6175032,
            -0.1126655495,
            0.0005158568,
            -0.0000010706
        ]

    def calc_dots(self, body_weight, total, is_female):
        """
        calculate the DOTS score based on total, bodyweight and gender
        :param body_weight: 
        :param total: 
        :param is_female: 
        :return: the DOTS score
        """
        denominator = self.female_coeff[0] if is_female else self.male_coeff[0]
        coeff = self.female_coeff if is_female else self.male_coeff
        max_bw = 150 if is_female else 210
        bw = min(max(body_weight, 40), max_bw)
        for i in range(1, len(coeff)):
            denominator += coeff[i] * pow(bw, i)
        score = (500 / denominator) * total
        return round(score, 2)

    def estimate_deadlift(self, body_weight, best_squat, best_bench, target_dots_score, is_female, is_kg):
        """
        Estimate the deadlift required to achieve a target DOTS score.
        :param body_weight: The body weight of the lifter.
        :param best_squat: Best squat of the lifter.
        :param best_bench: Best bench press of the lifter.
        :param target_dots_score: Target DOTS score to achieve.
        :param is_female: Boolean indicating if the lifter is female.
        :return: Estimated required deadlift weight.
        """
        denominator = self.female_coeff[0] if is_female else self.male_coeff[0]
        coeff = self.female_coeff if is_female else self.male_coeff
        max_bw = 150 if is_female else 210
        bw = min(max(body_weight, 40), max_bw)
        for i in range(1, len(coeff)):
            denominator += coeff[i] * pow(bw, i)

        required_total = (target_dots_score * denominator) / 500
        required_deadlift = required_total - best_squat - best_bench
        return max(0, round(required_deadlift, 2))  # ensure non-negative value
