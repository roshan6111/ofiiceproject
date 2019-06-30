import calendar
import collections
import datetime
import difflib
import operator
from collections import OrderedDict
from itertools import groupby

import pydash

from src.Utils import bsr_utils

date_json = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10,
             "Nov": 11, "Dec": 12, "JAN": 1, "FEB": 2, "MAR": 3, "APR": 4, "MAY": 5, "JUN": 6, "JUL": 7, "AUG": 8,
             "SEP": 9, "OCT": 10, "NOV": 11, "DEC": 12}

def findAccountMinValue(value):
    minAmount = 0
    if "transactions" in value:
        for transaction in value['transactions']:
            closingBalance = (float(str(transaction['closing_balance']).replace(',', '')))
            if closingBalance < minAmount:
                minAmount = closingBalance

    return minAmount

def monthlyTransactionListWithMedian(median, monthlyTransactionList, transactionFirstDate, transactionLastDate, num_days, days):

    monthlyTransactionListSorted = collections.defaultdict(dict)

    for transactionlistDate, allTransactionListInDate in monthlyTransactionList.items():
        monthlyTransactionListSorted[transactionlistDate] = collections.OrderedDict(sorted(allTransactionListInDate.items()))

        for dayInDays  in days:
            if (bsr_utils._iso_date_converter(dayInDays)) < (bsr_utils._iso_date_converter(transactionFirstDate)) or (bsr_utils._iso_date_converter(dayInDays) > bsr_utils._iso_date_converter(transactionLastDate)):
                monthlyTransactionListSorted[transactionlistDate][dayInDays] = median

    monthlyTransactionListSorted[transactionlistDate] = collections.OrderedDict(sorted(monthlyTransactionListSorted[transactionlistDate].items()))
    return monthlyTransactionListSorted


def getMedian(monthlyTransactionList):
    closingBanlanceList = []
    median = 0
    for transactionListKey, transactionListValue in monthlyTransactionList.items():
        for date , closingamount in transactionListValue.items():
            closingBanlanceList.append(float(closingamount))

    closingBanlanceListSorted = sorted(closingBanlanceList)
    numberOfTerms = len(closingBanlanceListSorted)
    if (numberOfTerms % 2) == 0:
        median = (closingBanlanceListSorted[int(round(numberOfTerms / 2)) - 1] + closingBanlanceListSorted[int(round((numberOfTerms / 2) + 1)) - 1]) / 2
    else:
        index = int(round((numberOfTerms + 1) / 2))
        median = closingBanlanceListSorted[index - 1]

    return median
        


def getPdfDateList(days,startDate,endDate):
    """
    give all date list between startdate and end date of pdf statement
    """
    start = False
    pdfDateList = []
    for day in sorted(days):
        if day == startDate:
            start = True
        if start:
            pdfDateList.append(day)
        if day == endDate:
            start = False
    return pdfDateList

def _accounts80credit(accounts80credit_list):
    """
    List of Individual person description
    :param accounts80credit_list: A dictionary, with individual description with amount.
    :return: A number, no of users.
    """
    count = 0
    sum_counter = 0
    accounts80credit_sum = pydash.numerical.sum_by(accounts80credit_list, lambda y: y)
    accounts80credit_list = sorted(accounts80credit_list.items(), key=operator.itemgetter(1), reverse=True)
    _80_percent = float(accounts80credit_sum * 80) / 100
    for per_amount_list in accounts80credit_list:
        if sum_counter < _80_percent:
            sum_counter += per_amount_list[1]
            count += 1
    accounts_no = ("{0:.2f}".format(float(count)))
    return accounts_no


def _transaction_counter(transaction_json_list, reverse_indicator):
    """
    Create 5 parameters
    :param transaction_json_list: A list, only Transaction details.
    :param reverse_indicator: A boolean value, pdf reverse or not indicator.
    :return: A dictionary, with 5 parameters.
    """
    default_transaction_count = 0
    overdraft_transaction_count = 0
    not_calculatable_transaction = ''
    transaction_type = ''
    cashDeposite_compare_list = ['ATM', 'CASH','CSH']
    cashDespositeCount = 0
    result = {}
    accounts80credit_list = {}

    if 'type' in transaction_json_list[0]:
        transaction_type = 'type'
    elif 'transaction_type' in transaction_json_list[0]:
        transaction_type = 'transaction_type'
    if transaction_type != '':
        if reverse_indicator:
            not_calculatable_transaction = transaction_json_list[-1]
        else:
            not_calculatable_transaction = transaction_json_list[0]
        for transaction in transaction_json_list:
            Description = transaction['description'].upper()

            # create accounts80credit 
            if transaction_type in transaction:
                if transaction[transaction_type] == 'deposit':
                    accounts80credit_matched_list = difflib.get_close_matches(Description, accounts80credit_list.keys())
                    if len(accounts80credit_matched_list) == 1:
                        _ratio = bsr_utils.sequence_match_ratio(accounts80credit_matched_list[0], Description)
                        if _ratio >= 70.0:
                            accounts80credit_list[accounts80credit_matched_list[0]] += float(
                                str(transaction['amount']).replace(',', ''))
                        else:
                            accounts80credit_list[Description] = float(str(transaction['amount']).replace(',', ''))
                    else:
                        accounts80credit_list[Description] = float(str(transaction['amount']).replace(',', ''))
                # end accounts80credit

            # calculate the sum of the cashDepositTotalLastYear

            if any(y in Description for y in cashDeposite_compare_list):
                if transaction_type in transaction:
                    if transaction[transaction_type] == 'deposit':
                        cashDespositeCount += float(str(transaction['amount']).replace(',', ''))

            # calculate the sum of the cashDepositTotalLastYear
            # commented to remove cound overdraft
            # if 'closing_balance' in transaction:
            #     if float(str(transaction['closing_balance']).replace(',', '')) < 0:
            #         overdraft_transaction_count += 1

            if transaction_type in transaction:
                if transaction[transaction_type] == 'withdraw' and transaction != not_calculatable_transaction:
                    compare_value = 0
                    if reverse_indicator:
                        compare_value = float(transaction_json_list[transaction_json_list.index(transaction) + 1][
                                                  'closing_balance'].replace(',', ''))
                    else:
                        compare_value = float(transaction_json_list[transaction_json_list.index(transaction) - 1][
                                                  'closing_balance'].replace(',', ''))
                    if float(str(transaction['amount']).replace(',', '')) > compare_value:
                        default_transaction_count += 1

    accounts80credit = _accounts80credit(accounts80credit_list)
    no_of_unique_transaction = len(accounts80credit_list)
    # end of calculate accounts80credit 

    result = {
        "default_transaction_count": default_transaction_count,
        "overdraft_transaction_count": overdraft_transaction_count,
        "cashDepositTotalLastYear": cashDespositeCount,
        "accounts80credit": accounts80credit,
        "totalCreditAccounts": no_of_unique_transaction
    }
    return result


def _monthly_emi(transaction_month_wise):
    """
    Calculate emi deposit.
    :param transaction_month_wise: A list, transaction details
    :return: A dictionary, with emi deposit
    """
    Emi_deposit = 0
    result = 0
    transaction_type = ''
    monthlyemi_list = [' EMI','EMI ', ' EMI ', ' LOAN', 'LOAN ',' LOAN ']
    # monthlyemi_list = ['EMI']
    if 'type' in transaction_month_wise[0]:
        transaction_type = 'type'
    elif 'transaction_type' in transaction_month_wise[0]:
        transaction_type = 'transaction_type'
    if transaction_type != '':
        for transaction in transaction_month_wise:
            Description = transaction['description'].upper()
            if any(y in Description for y in monthlyemi_list) and transaction[transaction_type] == 'withdraw':
                Emi_deposit += float(str(transaction['amount']).replace(',', ''))
    result = {
        "averageMonthlyEmilast2": Emi_deposit
    }
    return result


def _creadit_debit_averageMonthlyEmilast2_generater(arrayMonth):
    """
    :param arrayMonth:
    :return:
    """
    total_creadit_debit_averageMonthlyEmilast2_result = {}
    total_debit = pydash.numerical.sum_by(arrayMonth, lambda y: (float(str(y['total_debit']))))
    total_credit = pydash.numerical.sum_by(arrayMonth, lambda y: (float(str(y['total_credit']))))
    count_averageMonthlyEmilast2 = pydash.numerical.sum_by(arrayMonth, lambda y: 1 if (float(
        str(y['averageMonthlyEmilast2']))) > 0 else 0)
    try:
        total_averageMonthlyEmilast2 = pydash.numerical.sum_by(arrayMonth, lambda y: (
            float(str(y['averageMonthlyEmilast2'])))) / float(count_averageMonthlyEmilast2)
    except:
        total_averageMonthlyEmilast2 = 0
    total_creadit_debit_averageMonthlyEmilast2_result = {
        "totalCredit": float('%.3f' % total_credit),
        "totalDebit": float('%.3f' % total_debit),
        "averageMonthlyEmilast2": float('%.3f' % total_averageMonthlyEmilast2)
    }
    return total_creadit_debit_averageMonthlyEmilast2_result


def averageCalculater(final_list_result):
    averageCalculater = {}
    # averageBalance = pydash.numerical.sum_by(final_list_result, lambda y: (float(str(y['averageBalance']))))
    averageBalance = [x['averageBalance'] for x in final_list_result]
    averageBalance = float(min(averageBalance))
    # fiveDaysAverage = pydash.numerical.sum_by(final_list_result, lambda y: (float(str(y['fiveDaysAverage']))))
    fiveDaysAverage = [x['fiveDaysAverage'] for x in final_list_result]
    fiveDaysAverage = float(min(fiveDaysAverage))
    averageCalculater = {
        "averageMonthlyBalance": float('%.3f' % averageBalance),
        "max10DayAverageBalance": float('%.3f' % fiveDaysAverage)
    }
    return averageCalculater


def sbi(json_data):
    count = 0
    for i in json_data['transactions']:
        date, month, year = i['date'].split(' ')
        if len(date) == 1:
            json_data['transactions'][count]['date'] = '0' + json_data['transactions'][count]['date']
        count += 1
    return json_data


def analyser(json_data, response_type):
    _name_from_extractor = ''
    _accountNo_from_extractor = ''
    # default_transaction_count = 0
    if 'name' in json_data:
        _name_from_extractor = json_data['name']
    if 'account' in json_data:
        _accountNo_from_extractor = json_data['account']
    start_date = json_data['transactions'][0]['date']
    end_date = json_data['transactions'][-1]['date']
    reverse_indicator = bsr_utils.reverse_indicator(bsr_utils._iso_date_converter(start_date),
                                                    bsr_utils._iso_date_converter(end_date))

    # count of default transaction
    transaction_counter_list = _transaction_counter(json_data['transactions'], reverse_indicator)
    # end of default transactions

    # get -ve min value if there is 
    minvalue = findAccountMinValue(json_data)
    # get -ve min value ends

    if response_type == "STATE BANK OF INDIA":
        json_data = sbi(json_data)
    monthly_transion_grouped = {}
    durationMatch = True

    try:
        format = bsr_utils._get_date_format(start_date)
        json_data['transactions'].sort(key=lambda x: datetime.datetime.strptime(x['date'][:20], format))
    except:
        json_data['transactions'].sort(key=lambda x: x['date'][3:20])

    for k, v in groupby(json_data['transactions'], key=lambda x: x['date'][3:20]):
        monthly_transion_grouped[k] = list(v)
        if len(monthly_transion_grouped[k]) < 11:
            durationMatch = False

    # arraymonth is having all month transtions in month date wise with that month total debit and total credit 
    arrayMonth = {}
    for key, value in monthly_transion_grouped.iteritems():

        # monthly emi calculator
        monthly_emi = _monthly_emi(value)
        # monthly emi calculator end

        total_debit = 0
        total_amount = 0
        total_credit = 0
        # monthly_min_value = {}

        try:

            total_debit = pydash.numerical.sum_by(value, lambda y: (
                float(str(y['amount']).replace(',', '')) if 'type' in y and y['type'] == 'withdraw' else 0))

            total_credit = pydash.numerical.sum_by(value, lambda z: (
                float(str(z['amount']).replace(',', '')) if 'type' in z and z['type'] == 'deposit' else 0))
            
            if total_debit == 0:
                total_debit = pydash.numerical.sum_by(value, lambda y: (
                    float(str(y['amount']).replace(',', '')) if 'transaction_type' in y and y[
                        'transaction_type'] == 'withdraw' else 0))

            if total_credit == 0:
                total_credit = pydash.numerical.sum_by(value, lambda z: (
                    float(str(z['amount']).replace(',', '')) if 'transaction_type' in z and z[
                        'transaction_type'] == 'deposit' else 0))

        except:
            total_debit = pydash.numerical.sum_by(value, lambda y: (
                float(str(y['amount']).replace(',', '')) if 'transaction_type' in y and y[
                    'transaction_type'] == 'withdraw' else 0))
            total_credit = pydash.numerical.sum_by(value, lambda z: (
                float(str(z['amount']).replace(',', '')) if 'transaction_type' in z and z[
                    'transaction_type'] == 'deposit' else 0))
        total_amount = pydash.numerical.sum_by(value, lambda x: float(str(x['amount']).replace(',', '')))
        format_array = {
            "month": key,
            "total_debit": total_debit,
            "total_credit": total_credit,
            "total_amount": total_amount,
            "averageMonthlyEmilast2": monthly_emi['averageMonthlyEmilast2'],
            "transactions": monthly_transion_grouped[key]
        }
        arrayMonth[key] = format_array

    monthly_transion_list = collections.defaultdict(dict)

    final_list = {}
    final_list_result = []
    
    # operation for each month (function for one month work)
    for month_year, monthly_daywise in arrayMonth.iteritems():
        month_last_date = ''
        ten_days_avg = 0
        ten_days_avg_list = []
        closing_amount = 0
        opening_balance = 0
        avg_monthly_amount = 0
        opening_balance_flag = True
        year_as_two = False
        month_in_string_flag = False
        month_in_string_flag_upper = False
        if '/' in month_year:
            month, year = month_year.split('/')
            if len(year) != 4:
                year = '20' + year
                year_as_two = True
        elif '-' in month_year:
            month, year = month_year.split('-')
            if len(year) != 4:
                year = '20' + year
                year_as_two = True
        else:
            month, year = month_year.split(' ')
            if len(year) != 4:
                year = '20' + year
                year_as_two = True
        if len(month) > 2:
            month_in_string_flag = True
            month = month.strip()
            if month.isupper():
                month_in_string_flag_upper = True
        else:
            month = int(month)
        year = int(year)

        # group of months having with last transaction of same date 
        day_wise_with_last_transtion = {}

        monthly_daywise['transactions'].sort(key=lambda x: x['date'][:20])

        # creating day wise group so one date transation can be grouped
        for k, v in groupby(monthly_daywise['transactions'], key=lambda x: x['date'][:20]):
            if opening_balance_flag:  # opening_balance to take only first day closing balance as a opening_balance
                list_all = list(v)
                first_one = list_all[0]
                # conditon for checking transaction type
                if 'transaction_type' in first_one:
                    type_str = first_one['transaction_type']
                elif 'type' in first_one:
                    type_str = first_one['type']
                else:
                    continue
                # end of checking transaction type
                if type_str == 'deposit':
                    opening_balance = float(str(first_one['closing_balance']).replace(',', '')) - float(
                        str(first_one['amount']).replace(',', ''))
                else:
                    opening_balance = float(str(first_one['closing_balance']).replace(',', '')) + float(
                        str(first_one['amount']).replace(',', ''))
                opening_balance_flag = False
                if reverse_indicator:
                    day_wise_with_last_transtion[k] = list_all[0]
                else:
                    day_wise_with_last_transtion[k] = list_all[-1]
            else:
                if reverse_indicator:
                    day_wise_with_last_transtion[k] = list(v)[0]
                else:
                    day_wise_with_last_transtion[k] = list(v)[-1]

        if month_in_string_flag:
            month = date_json[month]
        # total number of days in month
        num_days = calendar.monthrange(year, month)[1]

        # cheking condition for years
        if '/' in month_year:
            if year_as_two:
                if month_in_string_flag:
                    if month_in_string_flag_upper:
                        days = [datetime.date(year, month, day).strftime('%d/%b/%y').upper() for day in
                                range(1, num_days + 1)]
                    else:
                        days = [datetime.date(year, month, day).strftime('%d/%b/%y') for day in range(1, num_days + 1)]
                else:
                    days = [datetime.date(year, month, day).strftime('%d/%m/%y') for day in range(1, num_days + 1)]
            else:
                if month_in_string_flag:
                    if month_in_string_flag_upper:
                        days = [datetime.date(year, month, day).strftime('%d/%b/%Y').upper() for day in
                                range(1, num_days + 1)]
                    else:
                        days = [datetime.date(year, month, day).strftime('%d/%b/%Y') for day in range(1, num_days + 1)]
                else:
                    days = [datetime.date(year, month, day).strftime('%d/%m/%Y') for day in range(1, num_days + 1)]
        elif '-' in month_year:
            if year_as_two:
                if month_in_string_flag:
                    if month_in_string_flag_upper:
                        days = [datetime.date(year, month, day).strftime('%d-%b-%y').upper() for day in
                                range(1, num_days + 1)]
                    else:
                        days = [datetime.date(year, month, day).strftime('%d-%b-%y') for day in range(1, num_days + 1)]
                else:
                    days = [datetime.date(year, month, day).strftime('%d-%m-%y') for day in range(1, num_days + 1)]
            else:
                if month_in_string_flag:
                    if month_in_string_flag_upper:
                        days = [datetime.date(year, month, day).strftime('%d-%b-%Y').upper() for day in
                                range(1, num_days + 1)]
                    else:
                        days = [datetime.date(year, month, day).strftime('%d-%b-%Y') for day in range(1, num_days + 1)]
                else:
                    days = [datetime.date(year, month, day).strftime('%d-%m-%Y') for day in range(1, num_days + 1)]
        else:
            if year_as_two:
                if month_in_string_flag:
                    if month_in_string_flag_upper:
                        days = [datetime.date(year, month, day).strftime('%d %b %y').upper() for day in
                                range(1, num_days + 1)]
                    else:
                        days = [datetime.date(year, month, day).strftime('%d %b %y') for day in range(1, num_days + 1)]
                else:
                    days = [datetime.date(year, month, day).strftime('%d %m %y') for day in range(1, num_days + 1)]
            else:
                if month_in_string_flag:
                    if month_in_string_flag_upper:
                        days = [datetime.date(year, month, day).strftime('%d %b %Y').upper() for day in
                                range(1, num_days + 1)]
                    else:
                        days = [datetime.date(year, month, day).strftime('%d %b %Y') for day in range(1, num_days + 1)]
                else:
                    days = [datetime.date(year, month, day).strftime('%d %m %Y') for day in range(1, num_days + 1)]

        # cheking condition end for years
        # days having the same pattern date list of all month

        # ##############################change here to find the month median and do the calculation################

        # create all transaction within first date and last date
        monthlyTransactionList = collections.defaultdict(dict)
        transactionFirstDate = ""
        transactionLastDate = ""
        pdfDateList = []
        closingAmount = 0
        median = 0
        if len(day_wise_with_last_transtion) > 0:
            sorted_day_wise_with_last_transtion = sorted(day_wise_with_last_transtion)
            transactionFirstDate = sorted_day_wise_with_last_transtion[0]
            transactionLastDate = sorted_day_wise_with_last_transtion[-1]
            pdfDateList = getPdfDateList(days,transactionFirstDate,transactionLastDate)
            for dayPdfDateList in pdfDateList:
                if dayPdfDateList in day_wise_with_last_transtion:
                    monthlyTransactionList[month_year][dayPdfDateList] = day_wise_with_last_transtion[dayPdfDateList]['closing_balance'].replace(',','')
                    closingAmount = day_wise_with_last_transtion[dayPdfDateList]['closing_balance'].replace(',','')
                else:
                    monthlyTransactionList[month_year][dayPdfDateList] = closingAmount

        # calculate the median 
        if len(monthlyTransactionList) > 0:
            median = getMedian(monthlyTransactionList)

            # add median value to above start date and below end date

            monthlyTransactionList = monthlyTransactionListWithMedian(median, monthlyTransactionList, transactionFirstDate, transactionLastDate, num_days, days)

        month_last_date = days[num_days-1]
        # end of create all transaction within first date and last date

        avg_monthly_amount = pydash.numerical.sum_by(monthlyTransactionList[month_year], lambda x: float(x)) / num_days

        # finding tendays avg
        for i in range(num_days - 9):
            amount_sum = 0
            for j in range(i, i + 10):
                amount_sum = amount_sum + float(monthlyTransactionList[month_year][days[j]])
            ten_days_avg_list.append((amount_sum / 10))
        ten_days_avg = max(ten_days_avg_list)
        # end of fivedays avg

        final_list = {
            "month": month_last_date,
            "averageBalance": str(float("{0:.2f}".format(avg_monthly_amount))),
            "fiveDaysAverage": str(float("{0:.2f}".format(ten_days_avg)))
        }
        final_list_result.append(final_list)
        try:
            format = bsr_utils._get_date_format(start_date)
            final_list_result.sort(key=lambda x: datetime.datetime.strptime(x['month'], format), reverse=True)
        except:
            final_list_result.sort(key=lambda x: x['month'][4:20], reverse=True)

    creadit_debit_averageMonthlyEmilast2_generater_result = _creadit_debit_averageMonthlyEmilast2_generater(arrayMonth)

    # generating total average
    averagemonthlybalance = averageCalculater(final_list_result)
    final_result = bsr_utils.merge_two_dic(creadit_debit_averageMonthlyEmilast2_generater_result,
                                           averagemonthlybalance)
    final_result['durationMatch'] = durationMatch
    final_result['accountHolderName'] = _name_from_extractor
    final_result['accountNumber'] = _accountNo_from_extractor
    final_result['startDate'] = start_date
    final_result['endDate'] = end_date
    final_result['lastYearDefaultedTransactions'] = transaction_counter_list['default_transaction_count']
    final_result['lastYearOverdraftTransactions'] = transaction_counter_list['overdraft_transaction_count']
    final_result['cashDepositTotalLastYear'] = transaction_counter_list['cashDepositTotalLastYear']
    final_result['accounts80credit'] = transaction_counter_list['accounts80credit']
    final_result['totalCreditAccounts'] = transaction_counter_list['totalCreditAccounts']
    # to get min in negetive 
    final_result['minAccountValue'] = minvalue
    return final_result
