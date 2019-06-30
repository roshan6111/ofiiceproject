ACCOUNT_STR = 'account'
FROM_STR = 'from'
TO_STR = 'to'
NAME_STR = 'name'
ADDRESS_STR = 'address'
BRANCH_STR = 'branch'
BRANCH_ADDRESS_STR = 'branch_address'
IFSC_STR = 'ifsc'
OPENING_BALANCE_STR = 'opening_balance'
TRANSACTIONS_STR = 'transactions'
DEPOSIT_TYPE = 'deposit'
WITHDRAW_TYPE = 'withdraw'
DATE_STR = 'date'
DESCRIPTION_STR = 'description'
AMOUNT_STR = 'amount'
WITHDRAW_AMOUNT_STR = 'withdraw_amount'
DEPOSIT_AMOUNT_STR = 'deposit_amount'
TYPE_STR = 'type'
CLOSING_BALANCE_STR = 'closing_balance'
TRANSACTION_TYPE_STR = 'transaction_type'
VALUE_DATE_STR = 'value_date'

##########################################Karur Vysya Bank CONSTANTS #######################################################
# KARUR_VYSYA_BANK_ACCOUNT_DETAILS_REGEX ='.*Account\s*Name\s*(?P<'+NAME_STR+'>[a-zA-Z\s]*)\s*Account\s*Number\s*(?P<'+ACCOUNT_STR+'>[\d]*)\s*Branch\s*(?P<'+BRANCH_STR+'>[\s\S\d\D\w\W]*)Opening\s*Balance\s\(\s*Balance\s*B/F\s*\)\s*(?P<'+OPENING_BALANCE_STR+'>[\d,.]*)\s*Closing\s*Balance\s*(?P<'+CLOSING_BALANCE_STR+'>[\d.,]*)\s*[\d\W\w\s\S]*From\s*Date\s*(?P<'+FROM_STR+'>\d{2}-\w{3}-\d{4})\s*To\s*Date\s*(?P<'+TO_STR+'>\d{2}-\w{3}-\d{4})'
KARUR_VYSYA_BANK_ACCOUNT_DETAILS_REGEX = '[\s\S\d\D\w\W]*Account\s*Name\s*(?P<' + NAME_STR + '>[a-zA-Z\s]*)\s*Account\s*Number\s*(?P<' + ACCOUNT_STR + '>[\d]*)\s*Branch\s*(?P<' + BRANCH_STR + '>[\s\S\d\D\w\W]*)\s*Customer\s*Id[\s\S\d\D\w\W]*Opening\s*Balance\s\(\s*Balance\s*B/F\s*\)\s*(?P<' + OPENING_BALANCE_STR + '>[\d,.]*)\s*Closing\s*Balance\s*(?P<' + CLOSING_BALANCE_STR + '>[\d.,]*)\s*[\d\W\w\s\S]*From\s*Date\s*(?P<' + FROM_STR + '>\d{2}-\w{3}-\d{4})\s*To\s*Date\s*(?P<' + TO_STR + '>\d{2}-\w{3}-\d{4})'
KARUR_VYSYA_BANK_HEADER_REGEX = '\s*Transaction\sDate\s*Value\sDate\s*Branch\s*Cheque\s*No\s*Description\s*Debit\s*Credit\s*Balance'
KARUR_VYSYA_BANK_TRANSACTION_REGEX = '.*(?P<' + DATE_STR + '>\d{2}-\d{2}-\d{4})\s*\d{2}:\d{2}:\d{2}\s*\d{2}-\w{3}-\d{4}\s*(?P<' + DESCRIPTION_STR + '>[\s\S\d\D\w\W]+)\s(?P<' + AMOUNT_STR + '>[\d,.-]+)\s+(?P<' + CLOSING_BALANCE_STR + '>[\d,.-]+)'
KARUR_VYSYA_BANK_STATEMENT_END_REGEX = '\s*Note\s*:-\s*'
KARUR_VYSYA_BANK_IGNORABLE_REGEXS = ['\s*Page\s*No\s*.']
KARUR_VYSYA_BANK_DESC_REGEX = '(?P<' + DESCRIPTION_STR + '>[\s\S\d\D\w\W]*)'

########################################## AXIS BANK CONSTANTS ############################################################
AXIS_BANK_ACCOUNT_DETAILS_REGEX = '\s*(?P<' + NAME_STR + '>[\s\S\d\D\w\W]+)Joint Holder :[\s\S\d\D\w\W]+Statement of Axis Account No ' \
                                                         ':(?P<' + ACCOUNT_STR + '>\d+) for the period \(From : (?P<' + FROM_STR + \
                                  '>\d{2}-\d{2}-\d{4}) To : (?P<' + TO_STR + '>\d{2}-\d{2}-\d{4})\)\s*'

AXIS_BANK_HEADER_REGEX = '\s*Tran\s*Date\s*Value\s*Date\s*Transaction\s*Particulars\s*Chq\s*No\s*Amount\(INR\)\s*DR\/CR\s*Balance\(INR\)\s*Branch\s*Name'
AXIS_BANK_TRANSACTION_REGEX = '\s*\d{2}-\d{2}-\d{4}\s*(?P<' + DATE_STR + '>\d{2}-\d{2}-\d{4})\s+(?P<' + DESCRIPTION_STR + '>[\s\S\d\D\w\W]*)\s+(?P<' + AMOUNT_STR + '>[\d,.]+)\s*(?P<' + TRANSACTION_TYPE_STR + '>(CR|DR))\s+(?P<' + CLOSING_BALANCE_STR + '>[\d,.]+)\s+(?P<' + BRANCH_STR + '>[\s\S\d\D\w\W].+)'

AXIS_BANK_STATEMENT_END_REGEX = '\s*TRANSACTION TOTAL\s*[\d.]+\s*[\d.]+'
AXIS_BANK_DESC_REGEX = '(?P<' + DESCRIPTION_STR + '>[\s\S\d\D\w\W]*)'
AXIS_BANK_IGNORABLE_REGEXS = []
########################################################################################################################


########################################## YES BANK CONSTANTS ##########################################################
YES_BANK_ACCOUNT_DETAILS_REGEX = '[\s\S\d\D\w\W]+Period : (?P<' + FROM_STR + '>.*) to (?P<' + TO_STR + \
                                 '>.*)[\s\S\d\D\w\W]+\n(?P<' + NAME_STR + '>[\s\S\d\D\w\W]+)Your Branch Details :' \
                                                                          '[\s\S\d\D\w\W]+IFSC : (?P<' + IFSC_STR + \
                                 '>\w+)\s+MICR :[\s\S\d\D\w\W]+Transaction details for your ACCOUNT No\.(?P<' + ACCOUNT_STR + '>\d+) \('

YES_BANK_HEADER_REGEX = '\s*Transaction\s*Value Date\s*Description\s*Debit\s*Credit\s*Balance|\s*Value\s*Date\s*Description\s*Withdrawals\s*Deposits\s*Balance'
YES_BANK_TRANSACTION_REGEX = '\s*(?P<' + DATE_STR + '>\d{2}/\d{2}/\d{4})\s+\d{2}/\d{2}/\d{4}\s+(?P<' + DESCRIPTION_STR \
                             + '>[\s\S\d\D\w\W]*)\s+(?P<' + WITHDRAW_AMOUNT_STR + '>[\d,.]+)\s+(?P<' + \
                             DEPOSIT_AMOUNT_STR + '>[\d,.-]+)\s+(?P<' + CLOSING_BALANCE_STR + '>[\d,.-]+)'
YES_BANK_DESC_REGEX = '(?P<' + DESCRIPTION_STR + '>[\s\S\d\D\w\W]*)'
YES_BANK_IGNORABLE_REGEXS = ['\s*Transaction', '\s*Value Date\s*Description\s*Debit\s*Credit\s*Balancee',
                             '\s*Page \d+ of \d+\s*',
                             '\s*This is a system generated statement and does not require signature.', '\s*Date\s*\n',
                             '\n', '\s*Nomination:']
YES_BANK_STATEMENT_END_REGEX = '\s*Opening Balance: (?P<' + OPENING_BALANCE_STR + '>[\d.]+)\s+'
########################################################################################################################

########################################## KOTAK BANK CONSTANTS #######################################################
KOTAK_BANK_ACCOUNT_DETAILS_REGEX = '\s*Account\s*Statement\s*(?P<' + NAME_STR + '>[A-Za-z.\s]+)\s(?P<' + ADDRESS_STR + '>[A-Za-z.\s\-\d]+)Account\s*No.\s+(?P<' + ACCOUNT_STR + '>\d+)[\s\S]*From\s(?P<' + FROM_STR + '>\d{2}/\d{2}/\d{4})\sTo\s(?P<' + TO_STR + '>\d{2}/\d{2}/\d{4})'
# KOTAK_BANK_TRANSACTION_REGEX = '\s*\d\s*(?P<'+DATE_STR+'>\d{2}/\d{2}/\d{4})\s+(?P<'+DESCRIPTION_STR+'>.*)[\s\S\d\D\w\W]+(?P<'+AMOUNT_STR+'>[\d,.]+)[CRDR]*\s+(?P<'+CLOSING_BALANCE_STR+'>[\d,.])'
KOTAK_BANK_TRANSACTION_REGEX = '\s*\d\s*(?P<' + DATE_STR + '>\d{2}/\d{2}/\d{4})\s+(?P<' + DESCRIPTION_STR + '>.*)\s(?P<' + AMOUNT_STR + '>[\d,.-]+)\s*(?P<' + TRANSACTION_TYPE_STR + '>(CR|DR)*)\s+(?P<' + CLOSING_BALANCE_STR + '>[\d,.-]+)'
KOTAK_BANK_HEADER_REGEX = KOTAK_BANK_TRANSACTION_REGEX
KOTAK_BANK_STATEMENT_END_REGEX = '\s*Statement Summary'
KOTAK_BANK_DESC_REGEX = '(?P<' + DESCRIPTION_STR + '>.*)'
# KOTAK_BANK_IGNORABLE_REGEXS = ['.*']
KOTAK_BANK_IGNORABLE_REGEXS = [
    '\s*Sl.\s*No.\s*Date\s*Description\s*Chq\s*/\s*Ref\s*number\s*Amount\s*Dr\s*/\s*Cr\s*Balance\s*Dr\s/\s*Cr',
    '\s*Opening\s*balance', '\s*Closing\s*balance', '\s*Call\s*', '\s*Write\s*']
########################################################################################################################

########################################## ICICI BANK LIMITED CONSTANTS #######################################################
ICICI_BANK_ACCOUNT_DETAILS_REGEX = '.*Transactions\s*List[\s-]*(?P<' + NAME_STR + '>[a-zA-Z\s]+)[a-zA-Z\s()-]*(?P<' + ACCOUNT_STR + '>\d+)'
ICICI_BANK_HEADER_REGEX = '.*No.\s*Transaction\sID\s*Value\sDate\s*Txn\sPosted\sDate\s*ChequeNo.\s*Description\s*Cr/Dr\s*Transaction\s*Available'
# ICICI_BANK_TRANSACTION_REGEX = '.*(?P<' + DATE_STR + '>\d{2}-\d{2}-\d{4})s*\s+\d{2}-\d{2}-\d{4}\s*[\d:\sA-Z]*[\s\w-]*\s(?P<' + DESCRIPTION_STR + '>.+)\s(?P<' + TRANSACTION_TYPE_STR + '>[A-Z]+\s)\s*(?P<' + AMOUNT_STR + '>[\d.,-]+)\s*(?P<' + CLOSING_BALANCE_STR + '>[\d.,-]+)\s*'
ICICI_BANK_TRANSACTION_REGEX = '.*(?P<' + DATE_STR + '>\d{2}-\d{2}-\d{4})\s*\d{2}-\d{2}-\d{4}\s*[\d:\sA-Z]*(AM|PM)\s*(?P<' + DESCRIPTION_STR + '>.+)\s(?P<' + TRANSACTION_TYPE_STR + '>(CR|DR))\s*(?P<' + AMOUNT_STR + '>[\d.,-]+)\s*(?P<' + CLOSING_BALANCE_STR + '>[\d.,-]+)\s*'
ICICI_BANK_DESC_REGEX = '(?P<' + DESCRIPTION_STR + '>[\s\S\d\D\w\W]*)'
ICICI_BANK_IGNORABLE_REGEXS = ['\s*\d+\s*\n']
########################################################################################################################

########################################## SBI BANK CONSTANTS #######################################################
# SBI_BANK_ACCOUNT_DETAILS_REGEX = '\s*Account Name\s+:\s*(?P<' + NAME_STR + '>[\s\S\d\D\w\W]+)Address\s+:[\s\S\d\D\w\W]+' \
#                                                                            'Account Number\s+:\s*(?P<' + \
#                                  ACCOUNT_STR + '>\d+)[\s\S\d\D\w\W]+IFS Code\s+:\s*(?P<' + IFSC_STR + \
#                                  '>[\w]+)[\s\S\d\D\w\W]+Balance as on[\s\w]+:\s*(?P<' + OPENING_BALANCE_STR + \
#                                  '>[\d.,]+)[\s\S\d\D\w\W]+Account Statement from (?P<' + FROM_STR + '>.*)\s+to\s+(?P<' + \
#                                  TO_STR + '>.*)'

SBI_BANK_ACCOUNT_DETAILS_REGEX = '\s*Account Name\s+:\s*(?P<'+ NAME_STR +'>[\s\S\d\D\w\W]+)Address\s+[\s\S\d\D\w\W]+Account Number\s+:\s*(?P<'+ACCOUNT_STR+'>\d+)[\s\S\d\D\w\W]+'

SBI_BANK_HEADER_REGEX = '\s*Txn\s*Value\s*Description\s*Ref\s*Branch\s*Debit\s*Credit\s*Balance'
SBI_BANK_TRANSACTION_REGEX = '\s*(?P<' + DATE_STR + '>[\d]+ [A-Za-z]+\s*\d*)\s+(?P<' + VALUE_DATE_STR + '>[\d]+ [A-Za-z]+\s*\d*)\s+(?P<' + DESCRIPTION_STR \
                             + '>.*)\s+(?P<' + AMOUNT_STR + '>([\d,]+[\.][\d]{2}|[\d,]+[\.][\d]))\s+(?P<' + \
                             CLOSING_BALANCE_STR + '>[\d,.-]+)'
SBI_BANK_STATEMENT_END_REGEX = '\s*Please do not share your ATM'
SBI_BANK_DESC_REGEX = '(?P<' + DESCRIPTION_STR + '>.*)'
SBI_BANK_IGNORABLE_REGEXS = ['\s*Date\s+No.\s*', SBI_BANK_HEADER_REGEX]
SBI_BANK_DESC_WITH_DATE_REGEX = '\s*(?P<' + DATE_STR + '>\d{4})\s+(?P<' + VALUE_DATE_STR + '>\d{4})\s+(?P<' + DESCRIPTION_STR + '>.*)'
########################################################################################################################

