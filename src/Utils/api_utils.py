import json
from datetime import datetime
from os import path
from threading import Thread
import dateutil.parser
from itertools import groupby
import copy 

import pydash
from flask import Flask, current_app

from src.PdfAnalyser import PdfAnalysers
from src.Service import BusinessExtractorFactory, DbConnection, PersonalExtractorFactory
from src.Utils import bsr_utils


def checkRequestIdNotExist(requestId, creditResult, creditResultAccount):
    if len(creditResult) > 0:
        for eachCreditResult in creditResult:
            if "requestId" in eachCreditResult and  "accountNumber" in eachCreditResult:
                if eachCreditResult['requestId'] == requestId and eachCreditResult["accountNumber"] == creditResultAccount:
                    return False
    return True


# function to create exising overlap condition
def appendExistingOverLappingResult(find_result,_file_name_list):
    for results in find_result:
        _file_name = {}    
        if "startDate" in results:
            if results["startDate"].strip():
                _file_name['startDate'] = results['startDate']
                if "endDate" in results:
                    if results['endDate'].strip():
                        _file_name['endDate'] = results['endDate']
                if "accountHolderName" in results:
                    if results["accountHolderName"].strip():
                        _file_name['name'] = results['accountHolderName']
                if "error" in results:
                    _file_name['error'] = results['error']
                if "accountNumber" in results:
                    _file_name['account'] = results['accountNumber']

        if len(_file_name) > 0:
            _file_name_list.append(_file_name)

    return _file_name_list


def removeFileName(matching_details):
    """
    To remove file from json input file already stored and no need in next step (only for the api)
    """
    if "business" in matching_details:
        for filesData in matching_details['business']:
            if "file" in filesData:
                del filesData['file']
    if "personal" in matching_details:
        for filesData in matching_details['personal']:
            if "file" in filesData:
                del filesData['file']


def get_calculated_Final_result_AverageBalance(result_business, credit_result, averageParameter):
        result = 0.0
        account_grouped_data = {}
        avg_list = {}
        credit_result.sort(key=lambda x: x['accountNumber'])
        for k, v in groupby(credit_result, key=lambda x: x['accountNumber']):
            account_grouped_data[k] = list(v)
        for account_number, account_details in account_grouped_data.items():
            pdf_number_in_account_number = len(account_details)
            sum_averageBalance = pydash.numerical.sum_by(account_details,lambda y: float(y[averageParameter]))
            avg_list[account_number] = float(sum_averageBalance)/pdf_number_in_account_number

        for values in avg_list.values():
            result += float(values)

        return result


def calculation_parameters(credit_result):
    """
    Sum all pdf result for rawParameters
    :param credit_result:  list of all pdf result
    :return:  rawParameters
    """
    raw_parameters_result = {}
    raw_parameters_result['totalCredits'] = pydash.numerical.sum_by(credit_result, lambda y: float(y['totalCredits']))
    raw_parameters_result['totalDebits'] = pydash.numerical.sum_by(credit_result, lambda y: float(y['totalDebits']))
    raw_parameters_result['accounts80credit'] = pydash.numerical.sum_by(credit_result,
                                                                        lambda y: float(y['accounts80credit']))
    raw_parameters_result['cashDepositTotalLastYear'] = pydash.numerical.sum_by(credit_result, lambda y: float(
        y['cashDepositTotalLastYear']))
    raw_parameters_result['max10DayAverageBalance'] = pydash.numerical.sum_by(credit_result, lambda y: float(
        y['max10DayAverageBalance']))
    raw_parameters_result['averageMonthlyBalance'] = pydash.numerical.sum_by(credit_result,
                                                                             lambda y: float(
                                                                                 y['averageMonthlyBalance']))
    raw_parameters_result['lastYearOverdraftTransactions'] = pydash.numerical.sum_by(credit_result, lambda y: float(
        y['lastYearOverdraftTransactions']))
    raw_parameters_result['lastYearDefaultedTransactions'] = pydash.numerical.sum_by(credit_result, lambda y: float(
        y['lastYearDefaultedTransactions']))
    raw_parameters_result['totalCreditAccounts'] = pydash.numerical.sum_by(credit_result,
                                                                           lambda y: float(y['totalCreditAccounts']))
    raw_parameters_result['averageMonthlyEmilast2'] = pydash.numerical.sum_by(credit_result, lambda y: float(
        y['averageMonthlyEmilast2']))
    return raw_parameters_result


def create_incomekp1(result):
    total_income = 0
    total_days = 0
    income_kp1_result = 0
    if len(result) >= 0:
        for monthly_result in result:
            start_date = monthly_result['startDate']
            end_date = monthly_result['endDate']
            if start_date and end_date:
                start_date = dateutil.parser.parse(bsr_utils._iso_date_converter(start_date))
                end_date =  dateutil.parser.parse(bsr_utils._iso_date_converter(end_date))
                days = end_date - start_date
                days = int((str(days)).split('days')[0])
                total_income += monthly_result['totalCredit']
                total_days += days
        if total_days != 0:
            income_kp1_result = (total_income/total_days)*365
    return income_kp1_result


def update_result_personal_with_incomekp1(incomekp1, result_personal, credits_result_personal):
    if result_personal:
        for monthly_transaction_details in result_personal:
            if "incomeKP1" in monthly_transaction_details:
                monthly_transaction_details["incomeKP1"] = incomekp1
    if credits_result_personal:
        for monthly_transaction_details in credits_result_personal:
            if "incomeKP1" in monthly_transaction_details:
                monthly_transaction_details["incomeKP1"] = incomekp1

def update_result_personal_with_account_change(result_business_combined, result_credit_result_business, account_change):
    if result_business_combined:
        for monthly_transaction_details in result_business_combined:
            if "bankAccountChange" in monthly_transaction_details:
                monthly_transaction_details["bankAccountChange"] = account_change
    if result_credit_result_business:
        for monthly_transaction_details in result_credit_result_business:
            if "bankAccountChange" in monthly_transaction_details:
                monthly_transaction_details["bankAccountChange"] = account_change

def get_boundary_date(credit_result_business):
    min_date = ''
    max_date = ''
    for individual_pdf_result in credit_result_business:
        if individual_pdf_result['errorCode'] == 100:
            current_dates = date_order(individual_pdf_result['startDate'], individual_pdf_result['endDate'])
            if min_date:
                if dateutil.parser.parse(bsr_utils._iso_date_converter(min_date)) > dateutil.parser.parse(bsr_utils._iso_date_converter(current_dates['startDate'])):
                    min_date = current_dates['startDate']
            else:
                min_date = current_dates['startDate']
            if max_date:
                if dateutil.parser.parse(bsr_utils._iso_date_converter(max_date)) < dateutil.parser.parse(bsr_utils._iso_date_converter(current_dates['endDate'])):
                    max_date = current_dates['endDate']
            else:
                max_date = current_dates['endDate']
    result = {
        "boundary_min_date" : min_date,
        "boundary_max_date" : max_date
    }

    return  result

def get_account_change(group_boundary_dates,boundary_dates):
    group_max = group_boundary_dates["boundary_max_date"]
    group_min = group_boundary_dates["boundary_min_date"]
    boundary_max = boundary_dates["boundary_max_date"]
    boundary_min = boundary_dates["boundary_min_date"]
    if group_max and group_min and boundary_max and boundary_min:
        if dateutil.parser.parse(bsr_utils._iso_date_converter(group_max)) < dateutil.parser.parse(bsr_utils._iso_date_converter(boundary_max)):
            return 1
        elif dateutil.parser.parse(bsr_utils._iso_date_converter(group_min)) > dateutil.parser.parse(bsr_utils._iso_date_converter(boundary_min)):
            return 1
        else:
            return 0
    else:
        return 0

def create_account_change(result_credit_result_business, filename):
    result_credit_business_copy = copy.deepcopy(result_credit_result_business)
    boundary_dates = get_boundary_date(result_credit_result_business)
    bank_requestid_map = {}
    result_credit_business_grouped = {}
    group_boundary_dates = {}
    account_change_counter = 0
    # create map for requestId with bankname
    for bank_details in filename:
        bank_requestid_map[bank_details["requestId"]] = bank_details["bankName"]
    # create result with bankname and request
    for business_result in result_credit_business_copy:
        if business_result["requestId"] in bank_requestid_map:
            business_result["bankName"] = bank_requestid_map[business_result["requestId"]]
        else:
            business_result["bankName"] = ''
    # group with bankname 
    for key, value in groupby(result_credit_business_copy, key=lambda x: x['bankName']):
        if key in result_credit_business_grouped and len(result_credit_business_grouped[key]) > 0:
            value = result_credit_business_grouped[key] + list(value)
            result_credit_business_grouped[key] = value
        else:
            result_credit_business_grouped[key] = list(value)
    # get boudary value each group
    for each_group_key, each_group_value  in result_credit_business_grouped.items():
        boundary_dates_variable = get_boundary_date(each_group_value)
        group_boundary_dates[each_group_key] = boundary_dates_variable
        account_change_counter += get_account_change(boundary_dates_variable,boundary_dates)
    
    return account_change_counter


def get_min_account_value(xpressId, taskId, fileName):
    overdraftAmount = 0
    db_connection = DbConnection.DbConnection()
    db = db_connection.connection_start()
    dataList = {}
    collections = db.analyses
    minAccountValueList = []

    [dataList for dataList in collections.find({'taskId': taskId, 'xpressId': xpressId},
                                                     {'_id': 1, 'taskId': 1, 'xpressId': 1, 'CreditResultPersonal': 1,
                                                      'CreditResultBusiness': 1,  'resultBusiness': 1})]


    if len(dataList) > 0:
        if 'CreditResultBusiness' in dataList and 'business' in fileName:
            for parentObjects in dataList['CreditResultBusiness']:
                for childObject in fileName['business']:
                    if 'requestId' in parentObjects and 'requestId' in childObject:
                        if str(parentObjects['requestId']) == str(childObject['requestId']):
                            notReplaceStatus = True
                            minAccountValueObject = {}
                            if len(minAccountValueList) > 0:
                                for eachMinAccountValue in minAccountValueList:
                                    if  eachMinAccountValue['accountNumber'] == parentObjects['accountNumber']:
                                        if "overDraftLimit" in parentObjects:
                                            if eachMinAccountValue['minAccountValue'] > parentObjects['overDraftLimit']:
                                                eachMinAccountValue['minAccountValue'] = parentObjects['overDraftLimit']
                                        notReplaceStatus = False
                                
                                if notReplaceStatus:
                                    if "overDraftLimit" in parentObjects:
                                        if parentObjects['overDraftLimit'] < 0:
                                            minAccountValueObject['accountNumber'] = parentObjects['accountNumber']
                                            minAccountValueObject['minAccountValue'] = parentObjects['overDraftLimit']
                                            minAccountValueList.append(minAccountValueObject)
                            else:
                                if "overDraftLimit" in parentObjects:
                                    if parentObjects['overDraftLimit'] < 0:
                                        minAccountValueObject['accountNumber'] = parentObjects['accountNumber']
                                        minAccountValueObject['minAccountValue'] = parentObjects['overDraftLimit']
                                        minAccountValueList.append(minAccountValueObject)

    # now add to the new project
    for amounts in minAccountValueList:
        overdraftAmount = overdraftAmount + (amounts['minAccountValue'] * -1)
    db_connection.connection_close()                             
    return overdraftAmount


    # # # for min value
    # minValueObject = {} 
    # if ("minAccountValue" in analyser_data) and ('accountNumber' in analyser_data):
    #     # find and replace
    #     notReplaceStatus = True
    #     if len(minValueList) > 0:
    #         for minValue in minValueList:
    #             if minValue['accountNumber'] == analyser_data['accountNumber']:
    #                 if minValue['minAccountValue'] > analyser_data['minAccountValue']:
    #                     minValue['minAccountValue'] = analyser_data['minAccountValue']
    #                 notReplaceStatus = False

    #         if notReplaceStatus:
    #             if analyser_data['minAccountValue'] < 0:
    #                 minValueObject['accountNumber'] = analyser_data['accountNumber']
    #                 minValueObject['minAccountValue'] = analyser_data['minAccountValue']
    #                 minValueList.append(minValueObject)
    #     else:
    #         if analyser_data['minAccountValue'] < 0:
    #             minValueObject['accountNumber'] = analyser_data['accountNumber']
    #             minValueObject['minAccountValue'] = analyser_data['minAccountValue']
    #             minValueList.append(minValueObject)

    # # # for min value ends

def get_name_duration(xpressid, taskid, filename):
    """
    Return rawParameters
    :param xpressid:
    :param taskid: Individual taskid
    :param filename: dict with list of personal and business requestId
    :return: xpressid, taskid, 10 parameters
    """
    db_connection = DbConnection.DbConnection()
    db = db_connection.connection_start()
    collections = db.analyses
    find_result = {}
    result_business = {}
    incomeKP1 = 0
    account_change_variable = 0
    [find_result for find_result in collections.find({'taskId': taskid, 'xpressId': xpressid},
                                                     {'_id': 1, 'taskId': 1, 'xpressId': 1, 'CreditResultPersonal': 1,
                                                      'CreditResultBusiness': 1,  'resultBusiness': 1})]
    if len(find_result) > 0:
        update_response = 1
        if 'CreditResultPersonal' in find_result and 'personal' in filename:
            raw_parameters_result_input = []
            for parentObjects in find_result['CreditResultPersonal']:
                for childObject in filename['personal']:
                    if 'requestId' in parentObjects and 'requestId' in childObject:
                        if str(parentObjects['requestId']) == str(childObject['requestId']):
                            raw_parameters_result_input.append(parentObjects)
            # unused result_personal variable but stored for future use
            result_personal = calculation_parameters(find_result['CreditResultPersonal'])
            if len(find_result['CreditResultPersonal']) > 0:
                incomeKP1 = find_result['CreditResultPersonal'][0]["incomeKP1"]
        if 'CreditResultBusiness' in find_result and 'business' in filename:
            raw_parameters_result_input = []
            for parentObjects in find_result['CreditResultBusiness']:
                for childObject in filename['business']:
                    if 'requestId' in parentObjects and 'requestId' in childObject:
                        if str(parentObjects['requestId']) == str(childObject['requestId']):
                            raw_parameters_result_input.append(parentObjects)

            result_business = calculation_parameters(raw_parameters_result_input)
            if len(find_result['CreditResultBusiness']) > 0:
                account_change_variable =  find_result['CreditResultBusiness'][0]["bankAccountChange"]
            # temperary adding incomekp1 and bankAccountChange 
            result_business['incomeKP1'] =  incomeKP1
            result_business['bankAccountChange'] = account_change_variable
            # temperary adding incomekp1 and bankAccountChange

            # creating max10DayAverageBalance Calculation
            # result_business['max10DayAverageBalance'] = get_calculated_Final_result_AverageBalance(result_business, find_result['resultBusiness'], "max10DayAverageBalance")
            result_business['max10DayAverageBalance'] = get_calculated_Final_result_AverageBalance(result_business, raw_parameters_result_input, "max10DayAverageBalance")
            # end of creating max10DayAverageBalance Calculation

            # creating averageMonthlyBalance Calculation
            # result_business['averageMonthlyBalance'] = get_calculated_Final_result_AverageBalance(result_business, find_result['resultBusiness'], "averageMonthlyBalance")
            result_business['averageMonthlyBalance'] = get_calculated_Final_result_AverageBalance(result_business, raw_parameters_result_input, "averageMonthlyBalance")
            # end of creating averageMonthlyBalance Calculation  
                      
        update_response = collections.update({'taskId': taskid, 'xpressId': xpressid},
                                             {'$set': {'rawParameters': result_business}})
        if update_response:
            result_json = {
                "_id": str(find_result['_id']),
                "taskId": find_result['taskId'],
                "xpressId": find_result['xpressId'],
                "rawParameters": result_business,
            }
        else:
            db_connection.connection_close()
            return 0
        db_connection.connection_close()
        return result_json
    else:
        db_connection.connection_close()
        return 0


def verification_call_back(taskid, xpressid):
    """
    :param taskid: Individual taskId
    :param xpressid: Individual xpressId
    :return: Dict with all pdf information
    """
    db_connection = DbConnection.DbConnection()
    db = db_connection.connection_start()
    collections = db.analyses
    find_result = ''
    [find_result for find_result in
     collections.find({'taskId': taskid, 'xpressId': xpressid},
                      {'taskId': 1, 'xpressId': 1, 'resultPersonal': 1, 'resultBusiness': 1})]
    db_connection.connection_close()
    if len(find_result) > 0:
        find_result['errorCode'] = 100
        find_result['error'] = bsr_utils.get_error_description("100")
        return find_result
    else:
        return 0


def get_verification(matching_details):
    """
    verification API main function
    :param matching_details: json input with xpressId, taskId, 
    :return: response and run thread on background
    """
    response = {
        'errorCode': 100,
        '_id': '',
        'xpressId': '',
        'taskId': '',
        'error': ''
    }
    if 'xpressId' not in matching_details and 'taskId' not in matching_details:
        response['errorCode'] = 120
        response['error'] = bsr_utils.get_error_description("120")
        return json.dumps(response)
    # parameter verification
    if 'xpressId' not in matching_details or matching_details['xpressId'] == "":
        response['errorCode'] = 116
        response['taskId'] = matching_details['taskId']
        response['error'] = bsr_utils.get_error_description("116")
        return json.dumps(response)
    else:
        response['xpressId'] = matching_details['xpressId']
    if 'taskId' not in matching_details or matching_details['taskId'] == "":
        response['errorCode'] = 115
        response['xpressId'] = matching_details['xpressId']
        response['error'] = bsr_utils.get_error_description("115")
        return json.dumps(response)
    else:
        response['taskId'] = matching_details['taskId']

    if 'fileName' not in matching_details or matching_details['fileName'] == "":
        response['errorCode'] = 114
        response['error'] = bsr_utils.get_error_description("114")
        return json.dumps(response)
    # end of parameter verification

    if response['errorCode'] == 100:
        try:
            db_connection = DbConnection.DbConnection()
            db = db_connection.connection_start()
            collections = db.analyses
            matching_details['timestamp'] = datetime.now()
            find_result = collections.find(
                {'xpressId': matching_details['xpressId'], 'taskId': matching_details['taskId']})
            if find_result.count() > 0:
                # update with new data
                matching_details_copy = copy.deepcopy(matching_details)
                if "fileName" in matching_details_copy:
                    removeFileName(matching_details_copy["fileName"])
                details_merged = bsr_utils.add_existing_input(find_result, matching_details_copy)
                object_result = collections.find_and_modify(
                    {'xpressId': matching_details['xpressId'], 'taskId': matching_details['taskId']},
                    {'$set': details_merged}, upsert=True)
                if object_result['_id']:
                    response['_id'] = str(object_result['_id'])
                    for cursor_index in find_result:
                        response['_id'] = str(cursor_index['_id'])
                else:
                    response['errorCode'] = 117
                    response['error'] = bsr_utils.get_error_description("117")
            else:



                # api testing code 
                matching_details_copy = copy.deepcopy(matching_details)
                if "fileName" in matching_details_copy:
                    removeFileName(matching_details_copy["fileName"])
                object_result = collections.insert_one(matching_details_copy).inserted_id    
                # api testing code ends



                # object_result = collections.insert_one(matching_details).inserted_id
                if object_result:
                    response['_id'] = str(object_result)
                    response['errorCode'] = 100
                else:
                    response['errorCode'] = 117
                    response['error'] = bsr_utils.get_error_description("117")
        except:
            response['errorCode'] = 117
            response['error'] = bsr_utils.get_error_description("117")
        finally:
            if response['errorCode'] != 100:
                db_connection.connection_close()
    if response['errorCode'] == 100:
        thread = Thread(target=user_details_verification,
                        kwargs={'filename': matching_details['fileName'], 'xpressid': matching_details['xpressId'],
                                'taskid': matching_details['taskId'], 'collections': collections})
        thread.start()
        db_connection.connection_close()
    return json.dumps(response)


def user_details_verification(filename, xpressid, taskid, collections):
    """
    Function run on thread called by get_verification
    :param filename: dict with list of personal and business requestId
    :param xpressid: A int, Individual xpressId
    :param taskid: A int, Individual taskId
    :param collections: Database connection
    :return: A json, API callback
    """

    _file_name_list = []

    user_details_app = Flask(__name__)
    user_details_app.config.from_object('config.BaseConfig')
    # variable for callback api with all data
    result_call_back = {'xpressId': xpressid, 'taskId': taskid}
    income_kp1 = 0
    _result_personal = []
    _result_business = []
    credit_result_personal_result = []
    credit_result_business_result = []
    # extractor_counter = 1
    # result of existing data for xpressId and taskId
    find_result = collections.find_one({'xpressId': xpressid, 'taskId': taskid})
    check_personal = filename.get("personal")
    if check_personal and len(check_personal) > 0:

        # # for min value
        # minValueList = []
        # # for min value end

        personal_file = filename['personal']
        # Download personal file
        for _file_index in range(len(personal_file)):
            download_attepts = 1
            # bsr_utils.download_pdf(download_attepts, personal_file, _file_index)
            # adding taskId to that
            bsr_utils.download_pdf(download_attepts, personal_file, _file_index, taskid, "personal")

        for _file_index in range(len(personal_file)):
            extractor_counter = 1
            _file_name = {}

            credit_result_personal_dic = {}
            result_personal = {}
            raw_parameters = {}
            result_personal['errorCode'] = 100
            result_personal['error'] = ""
            result_personal['endDate'] = ""
            result_personal['startDate'] = ""
            result_personal['totalDebit'] = 0
            result_personal['totalCredit'] = 0
            result_personal['accountHolderName'] = ""
            result_personal['accountNumber'] = ""
            result_personal['averageMonthlyEmilast2'] = 0
            result_personal['totalCreditAccounts'] = 0
            result_personal['lastYearDefaultedTransactions'] = 0
            result_personal['lastYearOverdraftTransactions'] = 0
            result_personal['averageMonthlyBalance'] = 0
            result_personal['max10DayAverageBalance'] = 0
            result_personal['cashDepositTotalLastYear'] = 0
            result_personal['accounts80credit'] = 0
            result_personal['incomeKP1'] = 0
            password = personal_file[_file_index]['password']

            result_personal['requestId'] = personal_file[_file_index]['requestId']
            result_personal['pdfName'] = personal_file[_file_index]['filename']
            with user_details_app.app_context():
                # edited for api base64 file system
                # file = current_app.config.get('LOCAL_FILE_PATH') + personal_file[_file_index]['filename']
                file = current_app.config.get('LOCAL_FILE_PATH') + taskid + "/personal/" + personal_file[_file_index]['filename'].replace(" ","")
            if path.exists(file) and file.lower().endswith('.pdf'):
                if personal_file[_file_index]['bankName'] in PersonalExtractorFactory.EXTRACTOR_MAP_1:
                    if personal_file[_file_index]['bankName'] in PersonalExtractorFactory.EXTRACTOR_TYPE_MAP:
                        extractor_counter = PersonalExtractorFactory.EXTRACTOR_TYPE_MAP[
                            personal_file[_file_index]['bankName']]
                    counter = 1
                    while counter <= extractor_counter:
                        EXTRACTOR_MAP = 'EXTRACTOR_MAP_' + str(counter)
                        extractor = getattr(PersonalExtractorFactory, EXTRACTOR_MAP)[
                            personal_file[_file_index]['bankName']]
                        result = extractor.extract(file, password)
                        if 'transactions' in result:
                            if len(result['transactions']) > 0:
                                break
                            else:
                                counter += 1
                        else:
                            counter += 1
                    if result == 'wrongpassword':
                        result_personal['errorCode'] = 104
                        result_personal['error'] = bsr_utils.get_error_description("104")
                    elif result == 'pdfnotreadable':
                        result_personal['errorCode'] = 105
                        result_personal['error'] = bsr_utils.get_error_description("105")
                    else:
                        if 'account' in result:
                            _file_name['account'] = result['account']
                        if 'name' in result:
                            _file_name['name'] = result['name']

                        if len(result['transactions']) > 0:
                            analyser_data = PdfAnalysers.analyser(result, personal_file[_file_index]['bankName'])
                            if 'totalDebit' in analyser_data:
                                result_personal['totalDebit'] = analyser_data['totalDebit']
                            if 'totalCredit' in analyser_data:
                                result_personal['totalCredit'] = analyser_data['totalCredit']
                            if 'accountHolderName' in analyser_data:
                                result_personal['accountHolderName'] = analyser_data['accountHolderName']
                            if 'accountNumber' in analyser_data:
                                result_personal['accountNumber'] = analyser_data['accountNumber']
                            if 'averageMonthlyEmilast2' in analyser_data:
                                result_personal['averageMonthlyEmilast2'] = analyser_data['averageMonthlyEmilast2']
                            if 'totalCreditAccounts' in analyser_data:
                                result_personal['totalCreditAccounts'] = analyser_data['totalCreditAccounts']
                            if 'lastYearDefaultedTransactions' in analyser_data:
                                result_personal['lastYearDefaultedTransactions'] = analyser_data[
                                    'lastYearDefaultedTransactions']
                            if 'lastYearOverdraftTransactions' in analyser_data:
                                result_personal['lastYearOverdraftTransactions'] = analyser_data[
                                    'lastYearOverdraftTransactions']
                            if 'averageMonthlyBalance' in analyser_data:
                                result_personal['averageMonthlyBalance'] = analyser_data['averageMonthlyBalance']
                            if 'max10DayAverageBalance' in analyser_data:
                                result_personal['max10DayAverageBalance'] = analyser_data['max10DayAverageBalance']
                            if 'cashDepositTotalLastYear' in analyser_data:
                                result_personal['cashDepositTotalLastYear'] = analyser_data['cashDepositTotalLastYear']
                            if 'accounts80credit' in analyser_data:
                                result_personal['accounts80credit'] = float(analyser_data['accounts80credit'])
                            if 'minAccountValue' in analyser_data:
                                result_personal['overDraftLimit'] = analyser_data['minAccountValue']

                            orderd_date = date_order(analyser_data['startDate'], analyser_data['endDate'])

                            _file_name['startDate'] = orderd_date['startDate']
                            _file_name['endDate'] = orderd_date['endDate']

                            result_personal['startDate'] = orderd_date['startDate']
                            result_personal['endDate'] = orderd_date['endDate']

                            # overlapping

                            # if some data exist then overlapping data generated file_name_list 
                            if len(find_result) > 0:
                                 if "resultPersonal" in find_result:
                                     appendExistingOverLappingResult(find_result['resultPersonal'],_file_name_list)

                            _file_name['error'] = result_personal['error']
                            if len(_file_name_list) > 0:
                                _overlapping_result = result
                                # _pdf_details_index with all the details of that file
                                for _pdf_details_index in _file_name_list:
                                    _overlapping_status = check_for_overlapping(_pdf_details_index, result_personal,
                                                                                result)

                                    # roshan check for to do overlapping or not
                                    checkRequestIdNotExistResult = True
                                    if len(find_result) > 0:
                                        if "CreditResultPersonal" in find_result:
                                            CreditResultPersonal = find_result['CreditResultPersonal']
                                            checkRequestIdNotExistResult = checkRequestIdNotExist(result_personal['requestId'],CreditResultPersonal,result_personal['accountNumber'])
                                    # # roshan check for to do overlapping or not

                                    if checkRequestIdNotExistResult:
                                        if _overlapping_status['status'] == 'overlapping':
                                            _overlapping_date_start = _overlapping_status['overlapping_date_start']
                                            _overlapping_date_end = _overlapping_status['overlapping_date_end']
                                            _overlapping_result = overlapping_result(result, _overlapping_date_start,
                                                                                    _overlapping_date_end)
                                            if len(_overlapping_result['transactions']) > 0:
                                                analyser_data = PdfAnalysers.analyser(_overlapping_result,
                                                                                    personal_file[_file_index][
                                                                                        'bankName'])
                                                orderd_date = date_order(analyser_data['startDate'],
                                                                        analyser_data['endDate'])
                                if len(_overlapping_result['transactions']) > 0:
                                    credit_result_personal_dic = credit_result_personal(credit_result_personal_dic,
                                                                                        analyser_data,
                                                                                        result_personal)
                                    credit_result_personal_result.append(credit_result_personal_dic)
                            else:
                                # check and remove _overlapping_status
                                _overlapping_status = False
                                credit_result_personal_dic = credit_result_personal(credit_result_personal_dic,
                                                                                    analyser_data,
                                                                                    result_personal)
                                credit_result_personal_result.append(credit_result_personal_dic)
                            _file_name_list.append(_file_name)
                        else:
                            result_personal['errorCode'] = 201
                            result_personal['error'] = bsr_utils.get_error_description("201")
                else:
                    result_personal['errorCode'] = 119
                    result_personal['error'] = bsr_utils.get_error_description("119")
            else:
                if file.lower().endswith('.pdf'):
                    result_personal['errorCode'] = 101
                    result_personal['error'] = bsr_utils.get_error_description("101")
                else:
                    result_personal['errorCode'] = 111
                    result_personal['error'] = bsr_utils.get_error_description("111")
            _result_personal.append(result_personal)

        if len(credit_result_personal_result) > 0:
            raw_parameters = calculation_parameters(credit_result_personal_result)
        if len(find_result) > 0:
            if '_id' in find_result:
                result_call_back['_id'] = str(find_result['_id'])
            if 'resultPersonal' in find_result:
                # merage and replace existing requestId in result business
                result_personal_combined = bsr_utils.add_existing_output(find_result, _result_personal,
                                                                         'resultPersonal')
                # merage and replace existing requestId in credit result business
                result_credit_result_personal = bsr_utils.merge_credit_result(find_result,
                                                                              credit_result_personal_result,
                                                                              'resultPersonal')
                #update result personal with incomekp1
                income_kp1 = create_incomekp1(_result_personal)
                update_result_personal_with_incomekp1(income_kp1, result_personal_combined,result_credit_result_personal)
                collections.update({'xpressId': xpressid, 'taskId': taskid},
                                   {'$set': {'resultPersonal': result_personal_combined,
                                             'CreditResultPersonal': result_credit_result_personal}})
            else:
                #update result personal with incomekp1
                income_kp1 = create_incomekp1(_result_personal)
                update_result_personal_with_incomekp1(income_kp1, _result_personal, credit_result_personal_result)
                collections.update({'xpressId': xpressid, 'taskId': taskid}, {
                    '$set': {'resultPersonal': _result_personal,
                             'CreditResultPersonal': credit_result_personal_result}})

    # tesing overlapping
    _file_name_list = []
    # testing overlapping ends

    check_business = filename.get("business")
    if check_business and len(check_business) > 0:
        business_file = filename['business']
        # downloading files
        for _file_index in range(len(business_file)):
            download_attepts = 1
            # bsr_utils.download_pdf(download_attepts, business_file, _file_index)
            # adding taskId to that
            bsr_utils.download_pdf(download_attepts, business_file, _file_index, taskid, "business")

        for _file_index in range(len(business_file)):
            extractor_counter = 1
            # find negetive value so that it can be added to
            # minValue = 0 
            _file_name = {}
            credit_result_business_dic = {}
            result_business = {}
            raw_parameters = {}
            result_business['errorCode'] = 100
            result_business['error'] = ""
            result_business['endDate'] = ""
            result_business['startDate'] = ""
            result_business['totalDebit'] = 0
            result_business['totalCredit'] = 0
            result_business['accountHolderName'] = ""
            result_business['accountNumber'] = ""
            result_business['averageMonthlyEmilast2'] = 0
            result_business['totalCreditAccounts'] = 0
            result_business['lastYearDefaultedTransactions'] = 0
            result_business['lastYearOverdraftTransactions'] = 0
            result_business['averageMonthlyBalance'] = 0
            result_business['max10DayAverageBalance'] = 0
            result_business['cashDepositTotalLastYear'] = 0
            result_business['accounts80credit'] = 0
            result_business['bankAccountChange'] = 1
            raw_parameters_business = {}
            password = business_file[_file_index]['password']
            result_business['requestId'] = business_file[_file_index]['requestId']
            result_business['pdfName'] = business_file[_file_index]['filename']
            with user_details_app.app_context():

                # edited for api base64 file system
                # file = current_app.config.get('LOCAL_FILE_PATH') + business_file[_file_index]['filename']
                file = current_app.config.get('LOCAL_FILE_PATH') + taskid + "/business/" + business_file[_file_index]['filename'].replace(" ","")


            if path.exists(file) and file.lower().endswith('.pdf'):
                if business_file[_file_index]['bankName'] in BusinessExtractorFactory.EXTRACTOR_MAP_1:
                    if business_file[_file_index]['bankName'] in BusinessExtractorFactory.EXTRACTOR_TYPE_MAP:
                        extractor_counter = BusinessExtractorFactory.EXTRACTOR_TYPE_MAP[
                            business_file[_file_index]['bankName']]
                    counter = 1
                    while counter <= extractor_counter:
                        EXTRACTOR_MAP = 'EXTRACTOR_MAP_' + str(counter)
                        extractor = getattr(BusinessExtractorFactory, EXTRACTOR_MAP)[
                            business_file[_file_index]['bankName']]
                        result = extractor.extract(file, password)
                        if 'transactions' in result:
                            if len(result['transactions']) > 0:
                                break
                            else:
                                counter += 1
                        else:
                            counter += 1
                    if result == 'wrongpassword':
                        result_business['errorCode'] = 104
                        result_business['error'] = bsr_utils.get_error_description("104")
                    elif result == 'pdfnotreadable':
                        result_business['errorCode'] = 105
                        result_business['error'] = bsr_utils.get_error_description("105")
                    else:
                        if 'account' in result:
                            _file_name['account'] = result['account']
                        if 'name' in result:
                            _file_name['name'] = result['name']

                        if len(result['transactions']) > 0:
                            analyser_data = PdfAnalysers.analyser(result, business_file[_file_index]['bankName'])
                            if 'totalDebit' in analyser_data:
                                result_business['totalDebit'] = analyser_data['totalDebit']
                            if 'totalCredit' in analyser_data:
                                result_business['totalCredit'] = analyser_data['totalCredit']
                            if 'accountHolderName' in analyser_data:
                                result_business['accountHolderName'] = analyser_data['accountHolderName']
                            if 'accountNumber' in analyser_data:
                                result_business['accountNumber'] = analyser_data['accountNumber']
                            if 'averageMonthlyEmilast2' in analyser_data:
                                result_business['averageMonthlyEmilast2'] = analyser_data['averageMonthlyEmilast2']
                            if 'totalCreditAccounts' in analyser_data:
                                result_business['totalCreditAccounts'] = analyser_data['totalCreditAccounts']
                            if 'lastYearDefaultedTransactions' in analyser_data:
                                result_business['lastYearDefaultedTransactions'] = analyser_data[
                                    'lastYearDefaultedTransactions']
                            if 'lastYearOverdraftTransactions' in analyser_data:
                                result_business['lastYearOverdraftTransactions'] = analyser_data[
                                    'lastYearOverdraftTransactions']
                            if 'averageMonthlyBalance' in analyser_data:
                                result_business['averageMonthlyBalance'] = analyser_data['averageMonthlyBalance']
                            if 'max10DayAverageBalance' in analyser_data:
                                result_business['max10DayAverageBalance'] = analyser_data['max10DayAverageBalance']
                            if 'cashDepositTotalLastYear' in analyser_data:
                                result_business['cashDepositTotalLastYear'] = analyser_data['cashDepositTotalLastYear']
                            if 'accounts80credit' in analyser_data:
                                result_business['accounts80credit'] = float(analyser_data['accounts80credit'])
                            if 'minAccountValue' in analyser_data:
                                result_business['overDraftLimit'] = analyser_data['minAccountValue']
                            # if 'bankAccountChange' in analyser_data:
                            #     result_business['bankAccountChange'] = analyser_data['bankAccountChange']

                            orderd_date = date_order(analyser_data['startDate'], analyser_data['endDate'])

                            _file_name['startDate'] = orderd_date['startDate']
                            _file_name['endDate'] = orderd_date['endDate']

                            result_business['startDate'] = orderd_date['startDate']
                            result_business['endDate'] = orderd_date['endDate']

                            # overlapping Code status
                            # if some data exist then overlapping data generated file_name_list 
                            if len(find_result) > 0:
                                 if "resultBusiness" in find_result:
                                     appendExistingOverLappingResult(find_result['resultBusiness'],_file_name_list)
                            _file_name['error'] = result_business['error']
                            if len(_file_name_list) > 0:
                                _overlapping_result = result
                                for _pdf_details_index in _file_name_list:
                                    _overlapping_status = check_for_overlapping(_pdf_details_index, result_business,
                                                                                result)

                                    # roshan check for to do overlapping or not
                                    checkRequestIdNotExistResult = True
                                    if len(find_result) > 0:
                                        if "CreditResultBusiness" in find_result:
                                            CreditResultBusiness = find_result['CreditResultBusiness']
                                            checkRequestIdNotExistResult = checkRequestIdNotExist(result_business['requestId'],CreditResultBusiness,result_business['accountNumber'])
                                    # # roshan check for to do overlapping or not

                                    if checkRequestIdNotExistResult:
                                        if _overlapping_status['status'] == 'overlapping':
                                            _overlapping_date_start = _overlapping_status['overlapping_date_start']
                                            _overlapping_date_end = _overlapping_status['overlapping_date_end']
                                            _overlapping_result = overlapping_result(_overlapping_result,
                                                                                    _overlapping_date_start,
                                                                                    _overlapping_date_end)
                                            if len(_overlapping_result['transactions']) > 0:
                                                analyser_data = PdfAnalysers.analyser(_overlapping_result,
                                                                                    business_file[_file_index][
                                                                                        'bankName'])
                                                orderd_date = date_order(analyser_data['startDate'],
                                                                        analyser_data['endDate'])
                                if len(_overlapping_result['transactions']) > 0:
                                    credit_result_business_dic = credit_result_business(credit_result_business_dic,
                                                                                        analyser_data,
                                                                                        result_business)
                                    credit_result_business_result.append(credit_result_business_dic)
                            else:
                                _overlapping_status = False
                                credit_result_business_dic = credit_result_business(credit_result_business_dic,
                                                                                    analyser_data,
                                                                                    result_business)
                                credit_result_business_result.append(credit_result_business_dic)
                            _file_name_list.append(_file_name)
                        else:
                            result_business['errorCode'] = 201
                            result_business['error'] = bsr_utils.get_error_description("201")
                else:
                    result_business['errorCode'] = 119
                    result_business['error'] = bsr_utils.get_error_description("119")
            else:
                if file.lower().endswith('.pdf'):
                    result_business['errorCode'] = 101
                    result_business['error'] = bsr_utils.get_error_description("101")
                else:
                    result_business['errorCode'] = 111
                    result_business['error'] = bsr_utils.get_error_description("111")
            _result_business.append(result_business)
        if len(credit_result_business_result) > 0:
            raw_parameters_business = calculation_parameters(credit_result_business_result)
            raw_parameters_business["incomeKP1"] = income_kp1

        if len(find_result) > 0:
            if '_id' in find_result:
                result_call_back['_id'] = str(find_result['_id'])
            if 'resultBusiness' in find_result:
                # merage and replace existing requestId in result business
                result_business_combined = bsr_utils.add_existing_output(find_result, _result_business,
                                                                         'resultBusiness')
                # merage and replace existing requestId in credit result business
                result_credit_result_business = bsr_utils.merge_credit_result(find_result,
                                                                              credit_result_business_result,
                                                                              'resultBusiness')
                merged_list = find_result['fileName']['business'] + filename["business"]
                account_change = create_account_change(result_business_combined, merged_list)
                update_result_personal_with_account_change(result_business_combined, result_credit_result_business, account_change)
                collections.update({'xpressId': xpressid, 'taskId': taskid},
                                   {'$set': {'resultBusiness': result_business_combined,
                                             'CreditResultBusiness': result_credit_result_business}})
            else:
                account_change = create_account_change(_result_business, filename["business"])
                update_result_personal_with_account_change(_result_business, credit_result_business_result, account_change)
                raw_parameters_business["bankAccountChange"] = account_change
                collections.update({'xpressId': xpressid, 'taskId': taskid}, {
                    '$set': {'rawParameters': raw_parameters_business, 'resultBusiness': _result_business,
                             'CreditResultBusiness': credit_result_business_result}})
                             
    result_call_back['resultPersonal'] = _result_personal
    result_call_back['resultBusiness'] = _result_business

    print (json.dumps(result_call_back))


def date_order(start_date, end_date):
    """
    Sort Date in case of reverse pdf
    :param start_date:
    :param end_date:
    :return: dict with start date and end date
    """
    dates = {}
    start = bsr_utils._iso_date_converter(start_date)
    end = bsr_utils._iso_date_converter(end_date)
    if dateutil.parser.parse(start) > dateutil.parser.parse(end):
        dates['startDate'] = end_date
        dates['endDate'] = start_date
    else:
        dates['startDate'] = start_date
        dates['endDate'] = end_date
    return dates


def check_for_overlapping(_pdf_details_index, result_personal, result):
    """
    check for overlapping in pdf date.
    :param _pdf_details_index: A list, previous file details contains.
    :param result_personal: A dic, with single pdf result.
    :param result: A dic, with whole result.
    :return: A boolean, overlapping result.
    """
    _result = False
    _account_indicator = False
    _date_indicator = False
    _result_overlapping = {}

    if 'account' in _pdf_details_index and 'account' in result:
        if _pdf_details_index['account'] == result['account']:
            _account_indicator = True
    if 'endDate' in _pdf_details_index and 'startDate' in result_personal:
        _pre_date = bsr_utils._iso_date_converter(_pdf_details_index['endDate'])
        _next_date = bsr_utils._iso_date_converter(result_personal['startDate'])
        if _pre_date >= _next_date:
            _date_indicator = True
    if _account_indicator and _date_indicator:
        _result_overlapping['status'] = 'overlapping'
        _result_overlapping['overlapping_date_start'] = _pdf_details_index['startDate']
        _result_overlapping['overlapping_date_end'] = _pdf_details_index['endDate']
        return _result_overlapping
    else:
        _result_overlapping['status'] = 'success'
    return _result_overlapping


def overlapping_result(_result, _overlapping_date_start, _overlapping_date_end):
    """
    Sort transaction and call function
    :param _result: A dictionary, pdf extractor result
    :param _overlapping_date_start: A string, start date from where overlapping will be checked.
    :param _overlapping_date_end: A string, last date from where overlapping will be checked.
    :return: A dictionary, result omit overlapping transaction
    """
    _result['transactions'] = bsr_utils.sort_transaction(_result['transactions'])
    # make to function as single overlapping and dic_overlapping if possible
    _result['transactions'] = dic_overlapping(_result['transactions'], _overlapping_date_start, _overlapping_date_end)
    return _result


def dic_overlapping(_result, _overlapping_date_start, _overlapping_date_end):
    """
    Create dictionary with non overlapping transaction.
    :param _result:  A dictionary, pdf extractor result.
    :param _overlapping_date_start: A string, start date from where overlapping will be checked.
    :param _overlapping_date_end: A string, last date from where overlapping will be checked.
    :return: A dictionary, result omit overlapping transaction.
    """
    overlapping_result_list = []
    overlapping_date_start = bsr_utils._iso_date_converter(_overlapping_date_start)
    overlapping_date_end = bsr_utils._iso_date_converter(_overlapping_date_end)
    for dic in _result:
        current_date = bsr_utils._iso_date_converter(dic['date'])
        if overlapping_date_end < current_date or current_date < overlapping_date_start:
            overlapping_result_list.append(dic)
    return overlapping_result_list


def credit_result_business(credit_result_business_dic, analyser_data, result_business):
    """
    Create credit Result Business for 10 parameters
    :param credit_result_business_dic: A dictionary, For result
    :param analyser_data: A dictionary, analyser output
    :param result_business: A dictionary, Business result
    :return: A dictionary, credit result with 10 parameters
    """
    credit_result_business_dic['averageMonthlyEmilast2'] = analyser_data['averageMonthlyEmilast2']
    credit_result_business_dic['totalCreditAccounts'] = analyser_data['totalCreditAccounts']
    credit_result_business_dic['lastYearDefaultedTransactions'] = analyser_data[
        'lastYearDefaultedTransactions']
    credit_result_business_dic['lastYearOverdraftTransactions'] = analyser_data[
        'lastYearOverdraftTransactions']
    credit_result_business_dic['averageMonthlyBalance'] = analyser_data['averageMonthlyBalance']
    credit_result_business_dic['max10DayAverageBalance'] = analyser_data['max10DayAverageBalance']
    credit_result_business_dic['cashDepositTotalLastYear'] = analyser_data['cashDepositTotalLastYear']
    credit_result_business_dic['accounts80credit'] = analyser_data['accounts80credit']
    credit_result_business_dic['totalDebits'] = analyser_data['totalDebit']
    credit_result_business_dic['totalCredits'] = analyser_data['totalCredit']
    credit_result_business_dic['requestId'] = result_business['requestId']
    credit_result_business_dic['bankAccountChange'] = 1
    credit_result_business_dic['overDraftLimit'] = analyser_data['minAccountValue']
    credit_result_business_dic['accountNumber'] = analyser_data['accountNumber']
    return credit_result_business_dic


def credit_result_personal(credit_result_personal_dic, analyser_data, result_personal):
    """
    Create credit Result Personal for 10 parameters
    :param credit_result_personal_dic: A dictionary, For result
    :param analyser_data: A dictionary, analyser output
    :param result_personal: A dictionary, pdf final result
    :return: A dictionary, credit result with 10 parameters
    """
    credit_result_personal_dic['averageMonthlyEmilast2'] = analyser_data['averageMonthlyEmilast2']
    credit_result_personal_dic['totalCreditAccounts'] = analyser_data['totalCreditAccounts']
    credit_result_personal_dic['lastYearDefaultedTransactions'] = analyser_data[
        'lastYearDefaultedTransactions']
    credit_result_personal_dic['lastYearOverdraftTransactions'] = analyser_data[
        'lastYearOverdraftTransactions']
    credit_result_personal_dic['averageMonthlyBalance'] = analyser_data['averageMonthlyBalance']
    credit_result_personal_dic['max10DayAverageBalance'] = analyser_data['max10DayAverageBalance']
    credit_result_personal_dic['cashDepositTotalLastYear'] = analyser_data['cashDepositTotalLastYear']
    credit_result_personal_dic['accounts80credit'] = analyser_data['accounts80credit']
    credit_result_personal_dic['totalDebits'] = analyser_data['totalDebit']
    credit_result_personal_dic['totalCredits'] = analyser_data['totalCredit']
    credit_result_personal_dic['requestId'] = result_personal['requestId']
    credit_result_personal_dic['incomeKP1'] = 10000
    credit_result_personal_dic['overDraftLimit'] = analyser_data['minAccountValue']
    credit_result_personal_dic['accountNumber'] = analyser_data['accountNumber']
    return credit_result_personal_dic


def check_null_raw_parameters(raw_parameters):
    return all(value == 0 for value in raw_parameters.values())
