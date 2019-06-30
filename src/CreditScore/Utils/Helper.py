import Functions


def incomplete_number_of_parameter(grouped_results):
    """
    Create the grouped results with number of parameters in group
    :param grouped_results: grouped result.
    :return: A list with number of parameters in group.
    """
    number_of_parameter_array = [None] * 11
    for key, value in grouped_results.items():
        number_of_parameter_array[key] = len(value)
    return number_of_parameter_array


def complete_number_of_parameter(incomplete_number_of_parameter_array):
    for index, element in enumerate(incomplete_number_of_parameter_array):
        if element is None:
            incomplete_number_of_parameter_array[index] = 0
    return incomplete_number_of_parameter_array


def complete_number_of_parameter_multiply_index(complete_number_of_parameter_array):
    number_of_parameter_array_with_multiply_index = [None] * 11
    for index, element in enumerate(complete_number_of_parameter_array):
        number_of_parameter_array_with_multiply_index[index] = index * element
    return number_of_parameter_array_with_multiply_index


def numerator(complete_number_of_parameter_array):
    numerator_value = 0
    for element in complete_number_of_parameter_array:
        numerator_value = numerator_value + element
    return numerator_value


def denominator(complete_number_of_parameter_array_with_multiply_index):
    denominator_value = 0
    for element in complete_number_of_parameter_array_with_multiply_index:
        denominator_value = denominator_value + element
    return denominator_value


def group_of_weightag_array(complete_number_of_parameter_array, alpha):
    group_weightag_array = [None] * 11
    for index, element in enumerate(complete_number_of_parameter_array):
        group_weightag_array[index] = index * element * alpha
    return group_weightag_array


def sum_of_group_weightag_array(group_weightag):
    sum_of_group_weightag = 0
    for element in group_weightag:
        sum_of_group_weightag = sum_of_group_weightag + element
    return sum_of_group_weightag


def max_score(_group_of_weightag_array, _sum_of_group_weightag_array, complete_number_of_parameter_array):
    max_score_array = [None] * 11
    for index, element in enumerate(_group_of_weightag_array):
        max_score_array[index] = _divide(element, _sum_of_group_weightag_array) * (
            _divide(1, complete_number_of_parameter_array[index])) * 1000
    return max_score_array


def put_max_score(grouped_results, _max_score):
    for index, element in enumerate(_max_score):
        if index in grouped_results:
            for grouped_results_element in grouped_results[index]:
                grouped_results_element['maximum_score'] = _max_score[index]


def true_score(grouped_results, final_parameters_numerator_denominator):
    sum_of_true_value = 0
    for index in range(1, 11):
        if index in grouped_results:
            for element in grouped_results[index]:
                element_name = getattr(Functions, element['name'])
                _true_score = element_name(element['minimum_score'], element['maximum_score'], element['model'],
                                           element['frontend_value'],
                                           final_parameters_numerator_denominator[element['name']])
                sum_of_true_value = sum_of_true_value + _true_score
                element['true_score'] = _true_score

    return sum_of_true_value


def _divide(numerator_value, denominator_value):
    try:
        return float(numerator_value) / float(denominator_value)
    except ZeroDivisionError as zero_division_error:
        return 0
    except Exception as exception:
        return 0

def update_parameter_after_calculations(grouped_results, parameter_after_calculations):
    for group in grouped_results:
        for params in grouped_results[group]:
            if "GSTScore" in params.values():
                parameter_after_calculations["GSTScore"] = params["priority_score"]
            elif "assetWorthRatioKP" in params.values():
                 parameter_after_calculations["assetWorthRatioKP"] = params["priority_score"]

