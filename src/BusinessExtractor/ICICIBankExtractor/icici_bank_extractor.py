import re

from src.Utils import bsr_utils, business_constants


def process_desc_down(json_formatted_data, desc_pattern, line):
    m = desc_pattern.match(line)
    description_extended = m.group(business_constants.DESCRIPTION_STR)
    if len(json_formatted_data[business_constants.TRANSACTIONS_STR]) > 0:
        json_formatted_data[business_constants.TRANSACTIONS_STR][-1][
            business_constants.DESCRIPTION_STR] += ' ' + bsr_utils.pretty_format(description_extended)

def process_desc(desc_pattern, line, existing_desc):
    m = desc_pattern.match(line)
    existing_desc += ' ' + bsr_utils.pretty_format(m.group(business_constants.DESCRIPTION_STR))
    return existing_desc

def get_transaction_type(transaction_type):
    if transaction_type == 'CR':
        return business_constants.DEPOSIT_TYPE
    return business_constants.WITHDRAW_TYPE


def process_transaction(json_formatted_data, line, existing_desc, transaction_regex, desc_regex, ignorable_regexes, append_down):
    transaction_pattern = re.compile(transaction_regex)
    desc_pattern = re.compile(desc_regex)
    ignorable_patterns = [re.compile(ignorable_regex) for ignorable_regex in ignorable_regexes]
    m = transaction_pattern.search(line)
    if transaction_pattern.search(line):
        transaction_type = get_transaction_type(
            bsr_utils.pretty_format(m.group(business_constants.TRANSACTION_TYPE_STR)))
        json_formatted_data[business_constants.TRANSACTIONS_STR].append({
            business_constants.DATE_STR: bsr_utils.pretty_format(m.group(business_constants.DATE_STR)),
            business_constants.DESCRIPTION_STR: existing_desc + bsr_utils.pretty_format(m.group(business_constants.DESCRIPTION_STR)),
            business_constants.TYPE_STR: transaction_type,
            business_constants.AMOUNT_STR: bsr_utils.pretty_format(m.group(business_constants.AMOUNT_STR)),
            business_constants.CLOSING_BALANCE_STR: bsr_utils.pretty_format(
                m.group(business_constants.CLOSING_BALANCE_STR))
        })
        existing_desc = ''
    elif bsr_utils.is_ignorable(ignorable_patterns, line):
        pass
    elif desc_pattern.search(line):
        if append_down:
            existing_desc = process_desc(desc_pattern, line, existing_desc)
        else:
            process_desc_down(json_formatted_data, desc_pattern, line)
    return existing_desc



def extract(_file, password):
    header_pattern = re.compile(business_constants.ICICI_BANK_HEADER_REGEX)
    file_content = bsr_utils.get_file_content(_file, password)
    json_formatted_data = {
        business_constants.TRANSACTIONS_STR: []
    }
    is_transaction_started = False
    acc_details = ''
    i = 0
    existing_desc = ''
    if file_content == 'wrongpassword':
        return 'wrongpassword'
    elif file_content == 'pdfnotreadable':
        return 'pdfnotreadable'
    while i < len(file_content):
        line = file_content[i]
        if is_transaction_started:
            existing_desc = process_transaction(json_formatted_data, line, existing_desc ,business_constants.ICICI_BANK_TRANSACTION_REGEX,
                                                business_constants.ICICI_BANK_DESC_REGEX,
                                                business_constants.ICICI_BANK_IGNORABLE_REGEXS, True)
            transaction_pattern = re.compile(business_constants.ICICI_BANK_TRANSACTION_REGEX)
            # there must be transaction and existing desc should be empty
            if transaction_pattern and not existing_desc:
                i = i+1
                line = file_content[i]
                existing_desc = process_transaction(json_formatted_data, line, existing_desc ,business_constants.ICICI_BANK_TRANSACTION_REGEX,
                                                    business_constants.ICICI_BANK_DESC_REGEX,
                                                    business_constants.ICICI_BANK_IGNORABLE_REGEXS, False)
        elif header_pattern.match(line):
            i += 2
            is_transaction_started = True
            bsr_utils.put_custum_acc_details(json_formatted_data, acc_details,
                                             business_constants.ICICI_BANK_ACCOUNT_DETAILS_REGEX)
        else:
            acc_details += line + '\n'
        i += 1
    return json_formatted_data
