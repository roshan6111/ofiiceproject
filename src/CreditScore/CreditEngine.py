from itertools import groupby

from src.CreditScore.Utils import Calculations, Constants, Helper
from src.Service import DbConnection
from src.Utils import api_utils, bsr_utils
import json

def grouped_data_string(group_data):
    result_object = {}
    for group_key, group_value in group_data.items():
        result_object[str(group_key)] = group_value
    return result_object 

def credit_engine(body_data):
    """
    Main function to calculate credit score
    :param body_data: Json input
    :return: Json with credit result
    """
    overDraftAmount = 0 
    credit_decision = True
    xpressid = body_data['xpressId']
    taskid = body_data['taskId']
    file_name = body_data['fileName']
    output_response = {}
    raw_parameters_null_check = False
    user_details = api_utils.get_name_duration(xpressid, taskid, file_name)
    # create the amount which have to add in amount in creditReport
    overDraftAmount = api_utils.get_min_account_value(xpressid, taskid, file_name)
    # user_details = CreditFormUtils.get_name_duration(xpressid, taskid, file_name)
    if user_details != 0 and "rawParameters" in user_details:
        raw_parameters_null_check = api_utils.check_null_raw_parameters(user_details['rawParameters'])
        # raw_parameters_null_check = CreditFormUtils.check_null_raw_parameters(user_details['rawParameters'])
    if user_details == 0 or raw_parameters_null_check:
        output_response['taskId'] = taskid
        output_response['xpressId'] = xpressid
        output_response['amount'] = 0
        output_response['creditScore'] = 0
        output_response['creditDecision'] = 0
        output_response['interest'] = "0"
        if raw_parameters_null_check:
            output_response['_id'] = user_details['_id']
            output_response['errorCode'] = 121
            output_response['error'] = bsr_utils.get_error_description("121")
        else:
            output_response['_id'] = None
            output_response['errorCode'] = 120
            output_response['error'] = bsr_utils.get_error_description("120")
        return output_response
    else:
        output_response['errorCode'] = 100
        output_response['error'] = bsr_utils.get_error_description("100")

    #  adding overdraft to averageMonthly balance and max10DaysAverageMonthlyBalance
    if "averageMonthlyBalance" in user_details["rawParameters"]:
        user_details["rawParameters"]["averageMonthlyBalance"] = user_details["rawParameters"]["averageMonthlyBalance"] + overDraftAmount
    if "max10DayAverageBalance" in user_details["rawParameters"]:
        user_details["rawParameters"]["max10DayAverageBalance"] = user_details["rawParameters"]["max10DayAverageBalance"] + overDraftAmount
    parameters_from_bs = user_details["rawParameters"]
    final_parameters = bsr_utils.merge_two_dic(body_data, parameters_from_bs)
    parameter_after_calculations = Calculations.final_parameters(final_parameters)
    
    # list of 30 parameters with their numerator and denominator values.
    final_parameters_numerator_denominator = Calculations.final_parameters_numerator_denominator(final_parameters)

    # decision CreditDecision
    # if (parameter_after_calculations["pastLoanDefaultsNumberKP"] >= 1 or
    #         parameter_after_calculations["defaultedLoansNumberBusiness"] >= 1
    #         # parameter_after_calculations["bankAccountChange"] >= 2 or
    #         #parameter_after_calculations["yearlyIncomeRatio"] <= 0.5 or
    #         #parameter_after_calculations["yearlyProfitRatio"] <= 0.5 or
    #         #parameter_after_calculations["creditSpreadRatio"] <= 0.05
    #         # parameter_after_calculations["defaultedTransaction"] >= 3
    # ):

    if (parameter_after_calculations["pastLoanDefaultsNumberKP"] >= 1 or parameter_after_calculations["defaultedLoansNumberBusiness"] >= 1):
        credit_decision = False

    new_parameters = []
    keys_array = Constants.PARAMETERS.keys()
    for element in keys_array:
        if parameter_after_calculations[element] is None and Constants.PARAMETERS[element]['redundant'] == True:
            parameter_obj = {
                "name": Constants.PARAMETERS[element]["name"],
                "comparing_value": Constants.PARAMETERS[element]["comparing_value"],
                "priority_score": 0,
                "minimum_score": Constants.PARAMETERS[element]["minimum_score"],
                "maximum_score": Constants.PARAMETERS[element]["maximum_score"],
                "model": Constants.PARAMETERS[element]["model"],
                "true_score": Constants.PARAMETERS[element]["true_score"],
                "frontend_value": parameter_after_calculations[element]
            }
        elif parameter_after_calculations[element] is None and Constants.PARAMETERS[element]['redundant'] == False:
            parameter_obj = {
                "name": Constants.PARAMETERS[element]["name"],
                "comparing_value": Constants.PARAMETERS[element]["comparing_value"],
                "priority_score": Constants.PARAMETERS[element]["priority_score"],
                "minimum_score": Constants.PARAMETERS[element]["minimum_score"],
                "maximum_score": Constants.PARAMETERS[element]["maximum_score"],
                "model": Constants.PARAMETERS[element]["model"],
                "true_score": 0,
                "frontend_value": parameter_after_calculations[element]
            }
        else:
            parameter_obj = {
                "name": Constants.PARAMETERS[element]["name"],
                "comparing_value": Constants.PARAMETERS[element]["comparing_value"],
                "priority_score": Constants.PARAMETERS[element]["priority_score"],
                "minimum_score": Constants.PARAMETERS[element]["minimum_score"],
                "maximum_score": Constants.PARAMETERS[element]["maximum_score"],
                "model": Constants.PARAMETERS[element]["model"],
                "true_score": Constants.PARAMETERS[element]["true_score"],
                "frontend_value": parameter_after_calculations[element]
            }
        new_parameters.append(parameter_obj)
    grouped_results = {}
    new_parameters.sort(key=lambda x: x['priority_score'])
    for key, value in groupby(new_parameters, key=lambda x: x['priority_score']):
        grouped_results[key] = list(value)
    incomplete_number_of_parameter_array = Helper.incomplete_number_of_parameter(grouped_results)
    complete_number_of_parameter_array = Helper.complete_number_of_parameter(incomplete_number_of_parameter_array)
    complete_number_of_parameter_array_with_multiply_index = Helper.complete_number_of_parameter_multiply_index(
        complete_number_of_parameter_array)
    numerator = Helper.numerator(complete_number_of_parameter_array)
    denominator = Helper.denominator(complete_number_of_parameter_array_with_multiply_index)
    alpha = float(numerator) / float(denominator)
    group_of_weightage_array = Helper.group_of_weightag_array(complete_number_of_parameter_array, alpha)
    sum_of_group_weightage_array = Helper.sum_of_group_weightag_array(group_of_weightage_array)
    max_score = Helper.max_score(group_of_weightage_array, sum_of_group_weightage_array,
                                 complete_number_of_parameter_array)
    Helper.put_max_score(grouped_results, max_score)
    sum_of_true_value = Helper.true_score(grouped_results, final_parameters_numerator_denominator)
    db_connection = DbConnection.DbConnection()
    db = db_connection.connection_start()
    collections = db.analyses
    # grouped results insert
    try:
        updated_grouped_data = grouped_data_string(grouped_results)
        collections.update({'xpressId': xpressid, 'taskId': taskid}, {
            '$set': {'trueScore':updated_grouped_data}})
    except:
        pass
    Helper.update_parameter_after_calculations(grouped_results, parameter_after_calculations)
    amount = (parameters_from_bs['max10DayAverageBalance']) * sum_of_true_value / 1000
    response = {}
    [response for response in collections.find({'taskId': taskid, 'xpressId': xpressid},
                                               {'_id': 1, 'taskId': 1, 'xpressId': 1})]


    # interest
    intersetRate = 1
    if round(sum_of_true_value) < 450: 
        intersetRate = 24
    elif round(sum_of_true_value) < 500 and round(sum_of_true_value) >= 450: 
        intersetRate = 23
    elif round(sum_of_true_value) < 550 and round(sum_of_true_value) >= 500: 
        intersetRate = 22
    elif round(sum_of_true_value) < 600 and round(sum_of_true_value) >= 550: 
        intersetRate = 21
    elif round(sum_of_true_value) < 650 and round(sum_of_true_value) >= 600: 
        intersetRate = 20
    elif round(sum_of_true_value) < 700 and round(sum_of_true_value) >= 650: 
        intersetRate = 19
    elif round(sum_of_true_value) < 750 and round(sum_of_true_value) >= 700: 
        intersetRate = 18
    elif round(sum_of_true_value) < 800 and round(sum_of_true_value) >= 750: 
        intersetRate = 17
    elif round(sum_of_true_value) < 850 and round(sum_of_true_value) >= 800: 
        intersetRate = 16
    elif round(sum_of_true_value) >= 850: 
        intersetRate = 15


    # check for Credit decision (it should be just above credit score)
    if sum_of_true_value < 500:
        credit_decision = False

    # amount check according credit decision (it should be just above credit score)
    if not credit_decision:
        amount = 0

    response_credit_report = {
        "amount": round(amount),
        "creditScore": round(sum_of_true_value),
        "creditDecision": credit_decision,
        "interest": intersetRate,
        "errorCode": output_response['errorCode'],
        "error": output_response['error']
    }
    final_parameters.pop('taskId', None)
    final_parameters.pop('xpressId', None)
    final_parameters.pop('fileName', None)

    collections.update({'xpressId': xpressid, 'taskId': taskid}, {
        '$set': {'rawParameters': final_parameters, 'credit': parameter_after_calculations,
                 'creditReport': response_credit_report}})

    db_connection.connection_close()
    output_response['_id'] = str(response['_id'])
    output_response['taskId'] = taskid
    output_response['xpressId'] = xpressid
    output_response['amount'] = round(amount)
    output_response['creditScore'] = round(sum_of_true_value)
    output_response['creditDecision'] = credit_decision
    output_response['interest'] = str(intersetRate)+"%"

    return output_response
