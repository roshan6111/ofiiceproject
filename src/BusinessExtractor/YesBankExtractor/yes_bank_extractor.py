import re

from src.Utils import business_constants, bsr_utils


def process_desc(json_formatted_data, desc_pattern, line):
    m = desc_pattern.match(line)
    description_extended = m.group(business_constants.DESCRIPTION_STR)
    json_formatted_data[business_constants.TRANSACTIONS_STR][-1][
        business_constants.DESCRIPTION_STR] += ' ' + bsr_utils.pretty_format(description_extended)


def get_transaction(deposit):
    if deposit == 0:
        return business_constants.WITHDRAW_TYPE
    return business_constants.DEPOSIT_TYPE


def process_transaction(json_formatted_data, line, transaction_regex, desc_regex, ignorable_regexes):
    transaction_pattern = re.compile(transaction_regex)
    desc_pattern = re.compile(desc_regex)
    ignorable_patterns = [re.compile(ignorable_regex) for ignorable_regex in ignorable_regexes]
    m = transaction_pattern.match(line)

    if transaction_pattern.match(line):
        withdraw = float(bsr_utils.pretty_format(m.group(business_constants.WITHDRAW_AMOUNT_STR)).replace(',', ''))
        deposit = float(bsr_utils.pretty_format(m.group(business_constants.DEPOSIT_AMOUNT_STR)).replace(',', ''))
        amount = withdraw + deposit
        transaction_type = get_transaction(deposit)
        json_formatted_data[business_constants.TRANSACTIONS_STR].append({
            business_constants.DATE_STR: bsr_utils.pretty_format(m.group(business_constants.DATE_STR)),
            business_constants.DESCRIPTION_STR: bsr_utils.pretty_format(m.group(business_constants.DESCRIPTION_STR)),
            business_constants.TYPE_STR: transaction_type,
            business_constants.AMOUNT_STR: amount,
            business_constants.CLOSING_BALANCE_STR: bsr_utils.pretty_format(
                m.group(business_constants.CLOSING_BALANCE_STR))
        })
    elif bsr_utils.is_ignorable(ignorable_patterns, line):
        pass
    elif desc_pattern.match(line):
        process_desc(json_formatted_data, desc_pattern, line)


def extract(_file, password):
    header_pattern = re.compile(business_constants.YES_BANK_HEADER_REGEX)
    file_end_pattern = re.compile(business_constants.YES_BANK_STATEMENT_END_REGEX)
    file_content = bsr_utils.get_file_content(_file, password)
    json_formatted_data = {
        business_constants.TRANSACTIONS_STR: []
    }
    is_transaction_started = False
    acc_details = ''
    i = 0
    if file_content == 'wrongpassword':
        return 'wrongpassword'
    elif file_content == 'pdfnotreadable':
        return 'pdfnotreadable'
    while i < len(file_content):
        line = file_content[i]
        if file_end_pattern.match(line):
            json_formatted_data.update(
                {business_constants.OPENING_BALANCE_STR: file_end_pattern.match(line).group(
                    business_constants.OPENING_BALANCE_STR)})
            break
        elif is_transaction_started:
            process_transaction(json_formatted_data, line, business_constants.YES_BANK_TRANSACTION_REGEX,
                                business_constants.YES_BANK_DESC_REGEX, business_constants.YES_BANK_IGNORABLE_REGEXS)
        elif header_pattern.match(line):
            is_transaction_started = True
            bsr_utils.put_acc_details(json_formatted_data, acc_details,
                                      business_constants.YES_BANK_ACCOUNT_DETAILS_REGEX)
        else:
            acc_details += line + '\n'
        i += 1
    return json_formatted_data
