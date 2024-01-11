"""
asdf
"""
from calculation import dots, goodlift, ipf, wilks, wilks_2


def get_scores(body_weight, total, is_kg, is_female, competition):
    """
    generate scores based on inputs
    :param body_weight: the body weight of the lifter
    :param total: the sum of best squat, benchpress and dead lift
    :param is_kg: boolean,
    :param is_female: boolean, is_female = TRUE or FALSE
    :param competition:
    :return: calculated old wilks, new wilks, dots, IPF and goodlift scores
    """
    weight_coeff = 0.45359237
    body_weight = body_weight if is_kg else body_weight * weight_coeff
    wl = total if is_kg else total * weight_coeff
    unit = "KG" if is_kg else "LB"
    gender = "Female" if is_female else "Male"

    # instantiate the classes
    wilks_calculator = wilks.Wilks()
    new_wilks_calc = wilks_2.NewWilks()
    dots_calc = dots.DOTS()
    ipf_calc = ipf.IPF()
    goodlifts_calc = goodlift.GoodLift()

    return {
        "body_weight": body_weight,
        "total": total,
        "gender": gender,
        "unit": "KG" if is_kg else "LB",
        "old_wilks": wilks_calculator.calc_old_wilks(body_weight, wl, is_female),
        "new_wilks": new_wilks_calc.calculate_new_wilks(body_weight, wl, is_female),
        "dots": dots_calc.calc_dots(body_weight, wl, is_female),
        "ipf": ipf_calc.calc_ipf(body_weight, wl, is_female, competition),
        "good_lifts": goodlifts_calc.calc_goodlift(body_weight, wl, is_female, competition),
    }