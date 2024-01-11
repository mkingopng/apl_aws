import math


class GoodLift:  # todo: code this up, test, docstring
    def __init__(self):
        self.male_coeff_clpl = [1199.72839, 1025.18162, 0.00921]
        self.male_coeff_clbn = [320.98041, 281.40258, 0.01008]
        self.male_coeff_eqpl = [1236.25115, 1449.21864, 0.01644]
        self.male_coeff_eqbn = [381.22073, 733.79378, 0.02398]

        self.female_coeff_clpl = [610.32796, 1045.59282, 0.03048]
        self.female_coeff_clbn = [142.40398, 442.52671, 0.04724]
        self.female_coeff_eqpl = [758.63878, 949.31382, 0.02435]
        self.female_coeff_eqbn = [221.82209, 357.00377, 0.02937]

    def calc_goodlift(self, body_weight, total, is_female, competition):
        """

        :param body_weight:
        :param total:
        :param is_female:
        :param competition:
        :return:
        """
        if is_female:
            if competition == "CLBN":
                coeff = self.female_coeff_clbn
            elif competition == "EQPL":
                coeff = self.female_coeff_eqpl
            elif competition == "EQBN":
                coeff = self.female_coeff_eqbn
            else:
                coeff = self.female_coeff_clpl
        else:
            if competition == "CLBN":
                coeff = self.male_coeff_clbn
            elif competition == "EQPL":
                coeff = self.male_coeff_eqpl
            elif competition == "EQBN":
                coeff = self.male_coeff_eqbn
            else:
                coeff = self.male_coeff_clpl

        if body_weight < 35:
            return "0.00"

        power = -coeff[2] * body_weight
        score = total * (100 / (coeff[0] - coeff[1] * math.exp(power)))
        return "0.00" if score < 0 else "{:.2f}".format(score)

