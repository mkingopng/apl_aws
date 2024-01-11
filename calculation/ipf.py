import math


class IPF:  # todo: code this up, test, docstring
    def __init__(self):
        """

        """
        self.male_coeff_clpl = [310.67, 857.785, 53.216, 147.0835]
        self.male_coeff_clbn = [86.4745, 259.155, 17.5785, 53.122]
        self.male_coeff_eqpl = [387.265, 1121.28, 80.6324, 222.4896]
        self.male_coeff_eqbn = [133.94, 441.465, 35.3938, 113.0057]
        self.female_coeff_clpl = [125.1435, 228.03, 34.5246, 86.8301]
        self.female_coeff_clbn = [25.0485, 43.848, 6.7172, 13.952]
        self.female_coeff_eqpl = [176.58, 373.315, 48.4534, 110.0103]
        self.female_coeff_eqbn = [49.106, 124.209, 23.199, 67.4926]

    def calc_ipf(self, body_weight, total, is_female, competition):
        """

        :param is_female:
        :param total:
        :param body_weight:
        :param competition:
        :return: IPF score
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

        if body_weight < 40:
            return "0.00"

        lnbw = math.log(body_weight)
        score = 500 + 100 * ((total - (coeff[0] * lnbw - coeff[1])) / (coeff[2] * lnbw - coeff[3]))
        return "0.00" if score < 0 else "{:.2f}".format(score)
