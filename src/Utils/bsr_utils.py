import datetime
import os
import re
import urllib
from datetime import date
from difflib import SequenceMatcher
import base64
import requests
from flask import Flask, current_app
import copy

from src.Service import ErrorCode
from src.Utils import constants, business_constants

date_json = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10,
             "Nov": 11, "Dec": 12, "JAN": 1, "FEB": 2, "MAR": 3, "APR": 4, "MAY": 5, "JUN": 6, "JUL": 7, "AUG": 8,
             "SEP": 9, "OCT": 10, "NOV": 11, "DEC": 12}


def sort_transaction(transaction, reverse=False):
    """
    Sort transaction list of dictionary
    :param transaction: list of transaction
    :param reverse: reverse indicator
    :return: sorted transaction list
    """
    try:
        start_date = transaction[0]['date']
        _format = _get_date_format(start_date)
        transaction.sort(key=lambda x: datetime.datetime.strptime(x['date'], _format), reverse=reverse)
    except:
        transaction.sort(key=lambda x: x['month'][4:20], reverse=reverse)
    return transaction


def sequence_match_ratio(sequence_one, sequence_two):
    """
    Calculate Ratio match of two description
    :param sequence_one: A string, description one
    :param sequence_two: A string,
    :return: A float, percentage description match
    """
    _ratio = SequenceMatcher(None, str(sequence_one), str(sequence_two)).ratio()
    return _ratio * 100


def _get_date_format(_date):
    """
    Return date format
    :param _date: A String, date
    :return: A String, date format
    """
    month_in_string_flag_upper = False
    month_in_string_flag = False
    month = ''
    year = ''
    day = ''
    if '/' in _date:
        day, month, year = _date.split('/')
        if len(year) != 4:
            year = '20' + year
    elif '-' in _date:
        day, month, year = _date.split('-')
        if len(year) != 4:
            year = '20' + year
    else:
        day, month, year = _date.split(' ')
        if len(year) != 4:
            year = '20' + year
    if len(month) > 2:
        month_in_string_flag = True
        month = month.strip()
        if month.isupper():
            month_in_string_flag_upper = True
    else:
        month = int(month)
    year = int(year)
    day = int(day)
    if '/' in _date:
        if month_in_string_flag:
            if month_in_string_flag_upper:
                return "%d/%b/%Y"
            else:
                return "%d/%b/%Y"
        else:
            return "%d/%m/%Y"
    elif '-' in _date:
        if month_in_string_flag:
            if month_in_string_flag_upper:
                return "%d-%b-%Y"
            else:
                return "%d-%b-%Y"
        else:
            return "%d-%m-%Y"
    else:
        if month_in_string_flag:
            if month_in_string_flag_upper:
                return "%d %b %Y"
            else:
                return "%d %b %Y"
        else:
            return "%d %m %Y"


def _iso_date_converter(_date):
    """
    convert date to iso format
    :param _date: A String, date
    :return: A String, iso date Format
    """
    month_in_string_flag_upper = False
    month_in_string_flag = False
    month = ''
    year = ''
    day = ''
    if '/' in _date:
        day, month, year = _date.split('/')
        if len(year) != 4:
            year = '20' + year
    elif '-' in _date:
        day, month, year = _date.split('-')
        if len(year) != 4:
            year = '20' + year
    else:
        if _date.strip():
            day, month, year = _date.split(' ')
            if len(year) != 4:
                year = '20' + year
    if len(month) > 2:
        month_in_string_flag = True
        month = month.strip()
        if month.isupper():
            month_in_string_flag_upper = True
        month = date_json[month]
    else:
        month = int(month)
    year = int(year)
    day = int(day)
    if '/' in _date:
        if month_in_string_flag:
            if month_in_string_flag_upper:
                formatted_date = datetime.datetime.strptime(datetime.date(year, month, day).strftime('%d/%b/%Y'),
                                                            '%d/%b/%Y').isoformat()
            else:
                formatted_date = datetime.datetime.strptime(datetime.date(year, month, day).strftime('%d/%b/%Y'),
                                                            '%d/%b/%Y').isoformat()
        else:
            formatted_date = datetime.datetime.strptime(datetime.date(year, month, day).strftime('%d/%m/%Y'),
                                                        '%d/%m/%Y').isoformat()
    elif '-' in _date:
        if month_in_string_flag:
            if month_in_string_flag_upper:
                formatted_date = datetime.datetime.strptime(
                    datetime.date(year, month, day).strftime('%d-%b-%Y').upper(),
                    '%d-%b-%Y').isoformat()
            else:
                formatted_date = datetime.datetime.strptime(datetime.date(year, month, day).strftime('%d-%b-%Y'),
                                                            '%d-%b-%Y').isoformat()
        else:
            formatted_date = datetime.datetime.strptime(datetime.date(year, month, day).strftime('%d-%m-%Y'),
                                                        '%d-%m-%Y').isoformat()
    else:
        if month_in_string_flag:
            if month_in_string_flag_upper:
                formatted_date = datetime.datetime.strptime(
                    datetime.date(year, month, day).strftime('%d %b %Y').upper(),
                    '%d %b %Y').isoformat()
            else:
                formatted_date = datetime.datetime.strptime(datetime.date(year, month, day).strftime('%d %b %Y'),
                                                            '%d %b %Y').isoformat()
        else:
            formatted_date = datetime.datetime.strptime(datetime.date(year, month, day).strftime('%d %m %Y'),
                                                        '%d %m %Y').isoformat()
    return formatted_date


def merge_credit_result(existing_object, new_object, name):
    """
    Merge CreditResultPersonal To existing
    :param existing_object: A dictionary, All existing data
    :param new_object: A List, CreditResult Business/Personal
    :param name: A String, Indicator of resultBusiness/resultPersonal
    :return: A List, All pdf 10 parameters calculated result
    """
    result_data = {}
    if 'CreditResultPersonal' in existing_object and name == 'resultPersonal':
        existing_object = removeExistingRequestIdCreditResult(existing_object, new_object,'CreditResultPersonal')
        result_data = existing_object['CreditResultPersonal'] + new_object
    elif 'CreditResultBusiness' in existing_object and name == 'resultBusiness':
        existing_object = removeExistingRequestIdCreditResult(existing_object, new_object,'CreditResultBusiness')
        result_data = existing_object['CreditResultBusiness'] + new_object
    else:
        result_data = new_object
    return result_data


def add_existing_input(existing_object, new_object):
    """
    add input in existing input data
    :param existing_object: A pymongo cursor, existing data
    :param new_object: A dictionary, new data
    :return: A dictionary, with all data.
    """
    object_data = {}
    existing_personal = {}
    existing_business = {}
    new_personal = {}
    new_business = {}
    for existing_object_data in existing_object:
        object_data = existing_object_data
    if 'fileName' in object_data and 'fileName' in new_object:
        if 'personal' in object_data['fileName']:
            existing_personal = object_data['fileName']['personal']
        if 'business' in object_data['fileName']:
            existing_business = object_data['fileName']['business']
        if 'personal' in new_object['fileName']:
            new_personal = new_object['fileName']['personal']
        if 'business' in new_object['fileName']:
            new_business = new_object['fileName']['business']
        if new_personal:
            if new_personal and existing_personal:
                object_data['fileName']['personal'] = existing_personal + new_personal
            else:
                object_data['fileName']['personal'] = new_personal
        if new_business:
            if new_business and existing_business:
                object_data['fileName']['business'] = existing_business + new_business
            else:
                object_data['fileName']['business'] = new_business

        return object_data


def add_existing_output(object_data, new_data, name):
    """
    Merge in existing Results
    :param object_data: A dictionary,
    :param new_data: A list,
    :param name: A string, Indicator of resultBusiness/resultPersonal
    :return: A List, with merged output
    """
    result_data = {}
    if 'resultPersonal' in object_data and name == 'resultPersonal':
        object_data = removeExistingRequestId(object_data, new_data,'resultPersonal')
        result_data = object_data['resultPersonal'] + new_data
    elif 'resultBusiness' in object_data and name == 'resultBusiness':
        object_data = removeExistingRequestId(object_data, new_data,'resultBusiness')
        result_data = object_data['resultBusiness'] + new_data
    else:
        result_data = new_data
    return result_data

def removeExistingRequestIdCreditResult(object_data, new_data, name):
    for indexObjectData in range(len(object_data[name])):
        requests_id = object_data[name][indexObjectData]['requestId']
        for newData in new_data:
            if newData['requestId'] == requests_id:
                if len(object_data[name]) > indexObjectData:
                    del object_data[name][indexObjectData]

    return object_data

def removeExistingRequestId(object_data, new_data, name):
    objectDeepCopy = copy.deepcopy(object_data)
    for indexObjectData in range(len(objectDeepCopy[name])):
        requests_id = objectDeepCopy[name][indexObjectData]['requestId']
        for newData in new_data:
            if newData['requestId'] == requests_id:
                if name == 'resultPersonal':
                    if 'CreditResultPersonal' in object_data:
                        for creditresult in object_data['CreditResultPersonal']:
                            if len(creditresult) > 0:
                                if requests_id == creditresult['requestId']:
                                    indexCreditResult = object_data['CreditResultPersonal'].index(creditresult)
                                    if len(object_data['creditResultPersonal']) > indexCreditResult:
                                        del object_data['creditResultPersonal'][indexCreditResult]
                                    # removeExistingRequestId(object_data, new_data, name)
                                    break
                if name == 'resultBusiness':
                    if 'CreditResultBusiness' in object_data:
                        for creditresult in object_data['CreditResultBusiness']:
                            if len(creditresult) > 0:
                                if requests_id == creditresult['requestId']:
                                    indexCreditResult = object_data['CreditResultBusiness'].index(creditresult)
                                    if len(object_data['CreditResultBusiness']) > indexCreditResult:
                                        del object_data['CreditResultBusiness'][indexCreditResult]
                                    # removeExistingRequestId(object_data, new_data, name)
                                    break
                if len(object_data[name]) > indexObjectData:
                    del object_data[name][indexObjectData]
                removeExistingRequestId(object_data, new_data, name)
                break

    return object_data


def get_error_description(code):
    """
    Return description of code
    :param code: A int, error code
    :return: A string, description
    """
    error_description = ErrorCode.ERROR_CODE[code]
    return error_description


def merge_two_dic(dict_one, dict_two):
    """
    merge two dictionary
    :param dict_one: A dictionary
    :param dict_two: A dictionary
    :return: A dictionary with merged data
    """
    merged = dict_one.copy()
    merged.update(dict_two)
    return merged


def get_duration(start_date, end_date):
    """
    Get two date duration
    :param start_date: A string, Start date
    :param end_date: A string, End date
    :return: A number, duration date
    """
    start_year, start_month, start_day = start_date.split('-')
    end_year, end_month, end_day = end_date.split('-')
    start_date = date(int(start_year), int(start_month), int(start_day))
    end_date = date(int(end_year), int(end_month), int(end_day))
    duration = start_date - end_date
    return duration


def download_pdf(download_attempt, file_list, index, taskId,filetype):
    """
    download file
    :param download_attempt: A int, Number of attempts to download
    :param file_list: A list, with all file details
    :param index: A int, index
    :return: 
    """
    download_status = download_file(file_list[index]['filename'],file_list[index]['file'],taskId, filetype)
    if (download_status == 0) and download_attempt <= 3:
        download_attempt += 1
        download_pdf(download_attempt, file_list, index, taskId,filetype)
    if download_attempt == 4:
        return '101'


def get_file_content(_file, password=None):
    """
    Convert file to text
    :param _file: A string file name
    :param password: password
    :return: file content
    """
    _file = _file.replace(" ", "")
    if password != "" and password is not None:
        response = os.system('pdftotext -layout -upw %s %s Tmp/test.txt' % (password, _file))
        if response:
            return "wrongpassword"
    else:
        response = os.system('pdftotext -layout %s Tmp/test.txt' % _file)
        if response:
            return "pdfnotreadable"
    with open('Tmp/test.txt') as f:
        content = f.readlines()
    os.system('rm -f Tmp/test.txt')
    return content


def download_file(file_name, filedata, taskId, file_type):
    """
    download file from server
    :param file_name: A string, filename
    :return: A integer, response code
    """
    inner_app = Flask(__name__)
    inner_app.config.from_object('config.BaseConfig')
    with inner_app.app_context():
        # to remove space from fileName
        file_name = file_name.replace(" ","")
        # base64 create 
        path = current_app.config.get('LOCAL_FILE_PATH') + taskId + "/" + file_type

        if not os.path.exists(current_app.config.get('LOCAL_FILE_PATH') + taskId + "/" + file_type):
            os.makedirs(path)
        filepath = current_app.config.get('LOCAL_FILE_PATH') + taskId +"/"+ file_type +"/"+ file_name
        try:
            with open(os.path.expanduser(filepath), 'wb') as fout:
                fout.write(base64.decodestring(filedata))
        except:
            return 0
        
        if not os.path.exists(current_app.config.get('LOCAL_FILE_PATH') + taskId +"/"+ file_type + "/" + file_name):
            return 0
        else:
            return 1
        
        # base64 create end


def get_opening_bal(closing_balance, amount, txn_type):
    """
    get opening balance
    :param closing_balance:
    :param amount:
    :param txn_type:
    :return:
    """
    if txn_type == constants.WITHDRAW_TYPE:
        return float(closing_balance.replace(',', '')) + float(amount.replace(',', ''))
    return float(closing_balance.replace(',', '')) - float(amount.replace(',', ''))


def get_transaction_type(opening_bal, closing_balance):
    """
    To get Transaction type
    :param opening_bal:
    :param closing_balance:
    :return:
    """
    if float(str(opening_bal).replace(',', '')) > float(str(closing_balance).replace(',', '')):
        return constants.WITHDRAW_TYPE
    return constants.DEPOSIT_TYPE


def get_transaction_type_business(opening_bal, closing_balance):
    """
    type of transaction
    :param opening_bal: opening balance
    :param closing_balance: closing balance
    :return: On variable
    """
    if float(str(opening_bal).replace(',', '')) > float(str(closing_balance).replace(',', '')):
        return business_constants.WITHDRAW_TYPE
    return business_constants.DEPOSIT_TYPE


def get_custom_transaction_type(opening_bal, closing_balance):
    """

    :param opening_bal:
    :param closing_balance:
    :return:
    """
    if float(str(opening_bal).replace(',', '')) > float(str(closing_balance).replace(',', '')):
        return constants.DEPOSIT_TYPE
    return constants.WITHDRAW_TYPE


def pretty_format_dictionary(_dict):
    """
    Formate a dict
    :param _dict:
    :return: 
    """
    for key in _dict:
        if not isinstance(_dict[key], str):
            continue
        _dict[key] = _dict[key].replace('\n', ' ')
        _dict[key] = re.sub('\s+', ' ', _dict[key])
        _dict[key] = _dict[key].strip()


def pretty_format(line):
    line = line.replace('\n', ' ')
    line = re.sub('\s+', ' ', line)
    return line.strip()


def get_opening_balance(statement_data):
    transactions = statement_data[constants.TRANSACTIONS_STR]
    if len(transactions) == 0:
        if constants.OPENING_BALANCE_STR in statement_data:
            return statement_data[constants.OPENING_BALANCE_STR]
        return 0
    return transactions[-1][constants.CLOSING_BALANCE_STR]


def get_rev_opening_balance(idx, statement_data):
    transactions = statement_data[constants.TRANSACTIONS_STR]
    if idx == len(transactions) - 1:
        if constants.OPENING_BALANCE_STR in statement_data:
            return statement_data[constants.OPENING_BALANCE_STR]
        return 0
    return transactions[idx + 1][constants.CLOSING_BALANCE_STR]


def get_rev_opening_balance_business(idx, statement_data):
    transactions = statement_data[business_constants.TRANSACTIONS_STR]
    if idx == len(transactions) - 1:
        if business_constants.OPENING_BALANCE_STR in statement_data:
            return statement_data[business_constants.OPENING_BALANCE_STR]
        return 0
    return transactions[idx + 1][business_constants.CLOSING_BALANCE_STR]


def put_acc_details(json_formatted_data, acc_details, account_regex):
    """
    Create account details with match function
    :param json_formatted_data: where data will store
    :param acc_details: A string, with account details
    :param account_regex: regular expression
    :return:
    """
    account_pattern = re.compile(account_regex)
    m = account_pattern.match(acc_details)
    data = {}
    if m:
        for key in m.groupdict():
            data[key] = m.group(key)
    json_formatted_data.update(data)
    pretty_format_dictionary(json_formatted_data)
    print ("success")


def put_custum_acc_details(json_formatted_data, acc_details, account_regex):
    """
    Create account details with search function
    :param json_formatted_data: where data will store
    :param acc_details: A string, with account details
    :param account_regex: regular expression
    :return:
    """
    account_pattern = re.compile(account_regex)
    m = account_pattern.search(acc_details)
    data = {}
    if m:
        for key in m.groupdict():
            data[key] = m.group(key)
    json_formatted_data.update(data)
    pretty_format_dictionary(json_formatted_data)
    print ("success")


def is_ignorable(ignorable_patterns, line):
    """
    To find ignore string
    :param ignorable_patterns: regular expression
    :param line: A string, Description
    :return: boolean value
    """
    for ignorable_pattern in ignorable_patterns:
        if ignorable_pattern.match(line):
            return True

    return False


def reverse_indicator(start_date, end_date):
    """
    compare the dates and find pdf reverse
    :param start_date: starting date
    :param end_date: end date
    :return: boolean value
    """
    if start_date > end_date:
        return True
    else:
        return False
