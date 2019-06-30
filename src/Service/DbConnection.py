from collections import OrderedDict

from pymongo import MongoClient


class DbConnection:
    def connection_start(self):
        self.mongo = MongoClient('mongodb://admin:codespider@localhost:27017/')
        db = self.mongo.analysis
        schema = {
            "$jsonSchema": {
                "bsonType": "object",
                "additionalProperties": False,
                "properties": {
                    "_id": {
                        "bsonType": "objectId"
                    },
                    "timestamp": {
                        "bsonType": "date",
                        "description": "must be a date and is required"
                    },
                    "taskId": {
                        "bsonType": "string",
                        "description": "must be a string and is required"
                    },
                    "xpressId": {
                        "bsonType": "string",
                        "description": "must be a string and is required"
                    },
                    "fileName": {
                        "bsonType": "object",
                        "additionalProperties": False,
                        "properties": {
                            "personal": {
                                "bsonType": ["array"],
                                "items":
                                    {
                                        "bsonType": ["object"],
                                        "required": ["requestId", "filename", "bankName", "password"],
                                        "additionalProperties": False,
                                        "description": "personal don't have parameter proper",
                                        "properties": {
                                            "requestId": {"bsonType": "string"},
                                            "filename": {"bsonType": "string"},
                                            "bankName": {"bsonType": "string"},
                                            "password": {"bsonType": "string"}}}
                            },
                            "business": {
                                "bsonType": ["array"],
                                "items":
                                    {
                                        "bsonType": ["object"],
                                        "required": ["requestId", "filename", "bankName", "password"],
                                        "additionalProperties": False,
                                        "description": "personal don't have parameter proper",
                                        "properties": {
                                            "requestId": {"bsonType": "string"},
                                            "filename": {"bsonType": "string"},
                                            "bankName": {"bsonType": "string"},
                                            "password": {"bsonType": "string"}
                                        }
                                    }
                            }
                        }
                    },
                    "CreditResultPersonal": {
                        "bsonType": ["array"],
                        "items": {
                            "bsonType": ["object"],
                            "additionalProperties": False,
                            "description": "personal don't have parameter proper",
                            "properties": {
                                "max10DayAverageBalance": {"bsonType": ["double", "int"]},
                                "totalDebits": {"bsonType": ["double", "int"]},
                                "lastYearDefaultedTransactions": {"bsonType": ["double", "int"]},
                                "averageMonthlyBalance": {"bsonType": ["double", "int"]},
                                "totalCredits": {"bsonType": ["double", "int"]},
                                "lastYearOverdraftTransactions": {"bsonType": ["double", "int"]},
                                "averageMonthlyEmilast2": {"bsonType": ["double", "int"]},
                                "totalCreditAccounts": {"bsonType": ["double", "int"]},
                                "accounts80credit": {"bsonType": "string"},
                                "cashDepositTotalLastYear": {"bsonType": ["double", "int"]},
                                "requestId": {"bsonType": "string"},
                                "incomeKP1": {"bsonType": ["double", "int"]},
                                "overDraftLimit":{"bsonType": ["int","double"]},
                                "accountNumber":{"bsonType": "string"}

                            }
                        }
                    },
                    "resultPersonal": {
                        "bsonType": ["array"],
                        "items": {
                            "bsonType": ["object"],
                            "additionalProperties": False,
                            "description": "personal don't have parameter proper",
                            "properties": {
                                "startDate": {"bsonType": "string"},
                                "totalDebit": {"bsonType": ["int", "double"]},
                                "endDate": {"bsonType": "string"},
                                "accountNumber": {"bsonType": "string"},
                                "pdfName": {"bsonType": "string"},
                                "errorCode": {"bsonType": ["double", "int"]},
                                "requestId": {"bsonType": "string"},
                                "totalCredit": {"bsonType": ["int", "double"]},
                                "error": {"bsonType": "string"},
                                "accountHolderName": {"bsonType": "string"},
                                "max10DayAverageBalance": {"bsonType": ["int", "double"]},
                                "lastYearDefaultedTransactions": {"bsonType": ["int", "double"]},
                                "averageMonthlyBalance": {"bsonType": ["int", "double"]},
                                "lastYearOverdraftTransactions": {"bsonType": ["int", "double"]},
                                "averageMonthlyEmilast2": {"bsonType": ["int", "double"]},
                                "totalCreditAccounts": {"bsonType": ["int", "double"]},
                                "accounts80credit": {"bsonType": ["int", "double"]},
                                "incomeKP1": {"bsonType": ["double", "int"]},
                                "cashDepositTotalLastYear": {"bsonType": ["double", "int"]},
                                "overDraftLimit":{"bsonType": ["int","double"]}
                            }
                        }
                    },
                    "CreditResultBusiness": {
                        "bsonType": ["array"],
                        "items": {
                            "bsonType": ["object"],
                            "additionalProperties": False,
                            "description": "personal don't have parameter proper",
                            "properties": {
                                "max10DayAverageBalance": {"bsonType": ["double", "int"]},
                                "totalDebits": {"bsonType": ["double", "int"]},
                                "lastYearDefaultedTransactions": {"bsonType": ["double", "int"]},
                                "averageMonthlyBalance": {"bsonType": ["double", "int"]},
                                "totalCredits": {"bsonType": ["double", "int"]},
                                "lastYearOverdraftTransactions": {"bsonType": ["double", "int"]},
                                "averageMonthlyEmilast2": {"bsonType": ["double", "int"]},
                                "totalCreditAccounts": {"bsonType": ["double", "int"]},
                                "accounts80credit": {"bsonType": "string"},
                                "cashDepositTotalLastYear": {"bsonType": ["double", "int"]},
                                "requestId": {"bsonType": "string"},
                                "bankAccountChange": {"bsonType": ["double", "int"]},
                                "overDraftLimit":{"bsonType": ["int","double"]},
                                "accountNumber":{"bsonType": "string"},
                            }
                        }
                    },
                    "resultBusiness": {
                        "bsonType": ["array"],
                        "items": {
                            "bsonType": ["object"],
                            "additionalProperties": False,
                            "description": "personal don't have parameter proper",
                            "properties": {
                                "startDate": {"bsonType": "string"},
                                "totalDebit": {"bsonType": ["double", "int"]},
                                "endDate": {"bsonType": "string"},
                                "accountNumber": {"bsonType": "string"},
                                "pdfName": {"bsonType": "string"},
                                "errorCode": {"bsonType": ["double", "int"]},
                                "requestId": {"bsonType": "string"},
                                "totalCredit": {"bsonType": ["double", "int"]},
                                "error": {"bsonType": "string"},
                                "accountHolderName": {"bsonType": "string"},
                                "max10DayAverageBalance": {"bsonType": ["double", "int"]},
                                "lastYearDefaultedTransactions": {"bsonType": ["double", "int"]},
                                "averageMonthlyBalance": {"bsonType": ["double", "int"]},
                                "bankAccountChange": {"bsonType": ["double", "int"]},
                                "lastYearOverdraftTransactions": {"bsonType": ["double", "int"]},
                                "averageMonthlyEmilast2": {"bsonType": ["double", "int"]},
                                "totalCreditAccounts": {"bsonType": ["double", "int"]},
                                "accounts80credit": {"bsonType": ["int", "double"]},
                                "cashDepositTotalLastYear": {"bsonType": ["int", "double"]},
                                "overDraftLimit":{"bsonType": ["int","double"]}
                            }
                        }
                    },
                    "rawParameters": {
                        "bsonType": ["object"],
                        "additionalProperties": False,
                        "description": "personal don't have parameter proper",
                        "properties": {
                            "max10DayAverageBalance": {"bsonType": ["int", "double"]},
                            "totalDebits": {"bsonType": ["int", "double"]},
                            "lastYearDefaultedTransactions": {"bsonType": ["int", "double"]},
                            "averageMonthlyBalance": {"bsonType": ["int", "double"]},
                            "totalCredits": {"bsonType": ["int", "double"]},
                            "lastYearOverdraftTransactions": {"bsonType": ["int", "double"]},
                            "averageMonthlyEmilast2": {"bsonType": ["int", "double"]},
                            "totalCreditAccounts": {"bsonType": ["int", "double"]},
                            "accounts80credit": {"bsonType": ["int", "double"]},
                            "cashDepositTotalLastYear": {"bsonType": ["int", "double"]},
                            "bankAccountChange": {"bsonType": ["int", "double"]},
                            "incomeBusiness1": {"bsonType": ["int", "double"]},
                            "incomeBusiness2": {"bsonType": ["int", "double"]},
                            "runningLoansKP": {"bsonType": ["int", "double"]},
                            "capitalDeployed1": {"bsonType": ["int", "double"]},
                            "maxLoanToKP": {"bsonType": ["int", "double"]},
                            "capitalInvestedByKP": {"bsonType": ["int", "double"]},
                            "profit1": {"bsonType": ["int", "double"]},
                            "profit2": {"bsonType": ["int", "double"]},
                            "ctcKP1": {"bsonType": ["int", "double"]},
                            "closingBankBalanceYear1": {"bsonType": ["int", "double"]},
                            "closingBankBalanceYear2": {"bsonType": ["int", "double"]},
                            "tax1": {"bsonType": ["int", "double"]},
                            "tax2": {"bsonType": ["int", "double"]},
                            "incomeKP1": {"bsonType": ["int", "double"]},
                            "pastLoanDefaultsNumberKP": {"bsonType": ["int", "double"]},
                            "pastLoanDefaultsNumberBusiness": {"bsonType": ["int", "double"]},
                            "totalLoansNumberKP": {"bsonType": ["int", "double"]},
                            "totalLoansNumberPersonal": {"bsonType": ["int", "double"]},
                            "loanApplied": {"bsonType": ["int", "double"]},
                            "totalChildren": {"bsonType": ["int", "double"]},
                            "maritalStatus": {"bsonType": ["bool"]},
                            "totalDependants": {"bsonType": ["int", "double"]},
                            "clubMembership": {"bsonType": ["bool"]},
                            "abroadTravels": {"bsonType": ["int", "double"]},
                            "hobbyCount": {"bsonType": ["string"]},
                            "paymentTowardsSavings": {"bsonType": ["int", "double"]},
                            "GST1": {"bsonType": ["int", "double"]},
                            "GST2": {"bsonType": ["int", "double"]},
                            "GST3": {"bsonType": ["int", "double"]},
                            "fixedAssetBusiness1": {"bsonType": ["int", "double"]},
                            "fixedAssetBusiness2": {"bsonType": ["int", "double"]},
                            "businessBorrowings1": {"bsonType": ["int", "double"]},
                            "businessBorrowings2": {"bsonType": ["int", "double"]},
                            "carOwner": {"bsonType": ["bool"]},
                            "houseOwner": {"bsonType": ["bool"]},
                        }
                    },
                    "creditReport": {
                        "bsonType": ["object"],
                        "additionalProperties": False,
                        "description": "personal don't have parameter proper",
                        "properties": {
                            "amount": {"bsonType": ["double", "int"]},
                            "interest": {"bsonType": ["int", "double"]},
                            "errorCode": {"bsonType": ["int", "double"]},
                            "creditScore": {"bsonType": ["double", "int"]},
                            "error": {"bsonType": "string"},
                            "creditDecision": {"bsonType": "bool"},
                        }
                    },
                    "credit": {
                        "bsonType": ["object"],
                        "additionalProperties": False,
                        "description": "credit don't have proper paramters",
                        "properties": {
                            "pastLoanDefaultsNumberKP": {"bsonType": ["double", "int"]},
                            "runningLoanRatioBusiness": {"bsonType": ["double", "int"]},
                            "incomeRatioKP": {"bsonType": ["double", "int"]},
                            "bankAccountChange": {"bsonType": ["double", "int"]},
                            "assetWorthRatioKP": {"bsonType": ["double", "int"]},
                            "totalChildren": {"bsonType": ["double", "int"]},
                            "maritalStatus": {"bsonType": "bool"},
                            "totalDependants": {"bsonType": ["double", "int"]},
                            "clubMembership": {"bsonType": "bool"},
                            "abroadTravels": {"bsonType": ["double", "int"]},
                            "hobbyCount": {"bsonType": ["double", "int"]},
                            "turnoverCapitalDeployedRatio": {"bsonType": ["double", "int"]},
                            "loanCapitalInvestedRatioKP": {"bsonType": ["double", "int"]},
                            "yearlyIncomeRatio": {"bsonType": ["double", "int"]},
                            "yearlyProfitRatio": {"bsonType": ["double", "int"]},
                            "yearlyMarginRatio": {"bsonType": ["double", "int"]},
                            "creditSpreadRatio": {"bsonType": ["double", "int"]},
                            "outgoingEmiRatio": {"bsonType": ["double", "int"]},
                            "ctcProfitRatioKP": {"bsonType": ["double", "int"]},
                            "defaultedTransaction": {"bsonType": ["double", "int"]},
                            "overdraftTransactions": {"bsonType": ["double", "int"]},
                            "averageMonthlyBalance": {"bsonType": ["double", "int"]},
                            "yearlySurplusRatio": {"bsonType": ["double", "int"]},
                            "paymentTowardsSavingsRatio": {"bsonType": ["double", "int"]},
                            "yearlyTaxRatio": {"bsonType": ["double", "int"]},
                            "defaultedLoansNumberBusiness": {"bsonType": ["double", "int"]},
                            "longTermLoansRatio": {"bsonType": ["double", "int"]},
                            "cashDepositRatio": {"bsonType": ["double", "int"]},
                            "GSTScore": {"bsonType": ["double", "int"]},
                            "assetWorthRatioBusiness": {"bsonType": ["double", "int"]},
                        }
                    },
                    "trueScore":{
                        "bsonType":["object"]
                    }
                }
            }
        }
        try:
            if "analyses" in db.list_collection_names():
                query = [('collMod', 'analyses'),
                         ('validator', schema),
                         ('validationLevel', 'moderate')]
                query = OrderedDict(query)
                db.command(query)
            else:
                db.create_collection("analyses", validator=schema)
        except Exception as e:
            print(e)
        return db

    def connection_close(self):
        self.mongo.close()
        return True
