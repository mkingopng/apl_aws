
class Wilks:  # todo: docstring
    def __init__(self):
        self.male_coeff = [
            -216.0475144,
            16.2606339,
            -0.002388645,
            -0.00113732,
            7.01863e-6,
            -1.291e-8
        ]
        self.female_coeff = [
            594.31747775582,
            -27.23842536447,
            0.82112226871,
            -0.00930733913,
            4.731582e-5,
            -9.054e-8]
        # self.event = event  # raw or equipped
        # self.category = category  # full meet or bench

    def calc_old_wilks(self, body_weight, total, is_female):
        """

        :param body_weight:
        :param total:
        :param is_female:
        :return:
        """
        denominator = self.female_coeff[0] if is_female else self.male_coeff[0]
        coeff = self.female_coeff if is_female else self.male_coeff
        min_bw = 26.51 if is_female else 40
        max_bw = 154.53 if is_female else 201.9
        bw = min(max(body_weight, min_bw), max_bw)
        for i in range(1, len(coeff)):
            denominator += coeff[i] * pow(bw, i)
        score = (500 / denominator) * total
        return round(score, 2)

