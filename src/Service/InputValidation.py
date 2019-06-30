from jsonschema import validate


def verification_input(input_value):
    schema = {
        "type": "object",
        "required": ["xpressId", "taskId"],
        "properties": {
            "xpressId": {"type": "string","minLength": 1},
            "taskId": {"type": "string","minLength": 1},
            "fileName": {
                "type": "object",
                "properties": {
                    "business": {
                        "type": "array",
                        "items": {
                            "required": ["filename", "bankName", "password", "requestId","file"],
                            "additionalProperties": False,
                            "properties": {
                                "filename": {"type": "string","minLength": 1},
                                "bankName": {"type": "string","minLength": 1},
                                "password": {"type": "string"},
                                "requestId": {"type": "string","minLength": 1},
                                "file": {"type": "string","minLength": 1},
                            }

                        }
                    },
                    "personal": {
                        "type": "array",
                        "items": {
                            "required": ["filename", "bankName", "password", "requestId","file"],
                            "additionalProperties": False,
                            "properties": {
                                "filename": {"type": "string","minLength": 1},
                                "bankName": {"type": "string","minLength": 1},
                                "password": {"type": "string"},
                                "requestId": {"type": "string","minLength": 1},
                                "file": {"type": "string","minLength": 1},
                            }
                        }
                    }
                }
            },

        },
    }
    try:
        return validate(instance=input_value, schema=schema)
    except Exception as e:
        return e.message

def verificationCallBack_input(input_value):
    schema = {
        "type": "object",
        "required": ["xpressId", "taskId"],
        "properties": {
            "xpressId": {"type": "string","minLength": 1},
            "taskId": {"type": "string","minLength": 1},
        },
    }
    try:
        return validate(instance=input_value, schema=schema)
    except Exception as e:
        return e.message


def credit_score_input(input_value):
    # print (json.dumps(input_value))
    credit_score_schema = {
        "type": "object",
        "required": ["xpressId", "taskId", "fileName", "incomeBusiness1", "incomeBusiness2", "runningLoansKP",
                     "capitalDeployed1"
            , "maxLoanToKP", "capitalInvestedByKP", "profit1", "profit2", "ctcKP1", "closingBankBalanceYear1", "closingBankBalanceYear2", "tax1",
                     "tax2", "pastLoanDefaultsNumberKP"
            , "pastLoanDefaultsNumberBusiness", "totalLoansNumberKP", "loanApplied",
                     "totalChildren"
            , "maritalStatus", "totalDependants", "clubMembership", "abroadTravels", "hobbyCount",
                     "paymentTowardsSavings", "GST1", "GST2"
            , "GST3", "fixedAssetBusiness1", "fixedAssetBusiness2", "businessBorrowings1", "businessBorrowings2",
                     "carOwner", "houseOwner"],
        "properties": {
            "xpressId": {"type": "string","minLength": 1},
            "taskId": {"type": "string","minLength": 1},
            "fileName": {
                "type": "object",
                "properties": {
                    "business": {
                        "type": "array",
                        "items": {
                            "required": ["requestId"],
                            "additionalProperties": False,
                            "properties": {
                                "requestId": {"type": "string","minLength": 1},
                            }

                        }
                    },
                    "personal": {
                        "type": "array",
                        "items": {
                            "required": ["requestId"],
                            "additionalProperties": False,
                            "properties": {
                                "requestId": {"type": "string","minLength": 1},
                            }
                        }
                    }
                }
            },
            "incomeBusiness1": {"type": "number"},
            "incomeBusiness2": {"type": "number"},
            "runningLoansKP": {"type": "number"},
            "capitalDeployed1": {"type": "number"},
            "maxLoanToKP": {"type": "number"},
            "capitalInvestedByKP": {"type": "number"},
            "profit1": {"type": "number"},
            "profit2": {"type": "number"},
            "ctcKP1": {"type": "number"},
            "closingBankBalanceYear1": {"type": "number"},
            "closingBankBalanceYear2": {"type": "number"},
            "tax1": {"type": "number"},
            "tax2": {"type": "number"},
            "pastLoanDefaultsNumberKP": {"type": "number"},
            "pastLoanDefaultsNumberBusiness": {"type": "number"},
            "totalLoansNumberKP": {"type": "number"},
            "loanApplied": {"type": "number"},
            "totalChildren": {"type": "number"},
            "maritalStatus": {"type": "boolean"},
            "totalDependants": {"type": "number"},
            "clubMembership": {"type": "boolean"},
            "abroadTravels": {"type": "number"},
            "hobbyCount": {"type": "string"},
            "paymentTowardsSavings": {"type": "number"},
            "GST1": {"type": "number"},
            "GST2": {"type": "number"},
            "GST3": {"type": "number"},
            "fixedAssetBusiness1": {"type": "number"},
            "fixedAssetBusiness2": {"type": "number"},
            "businessBorrowings1": {"type": "number"},
            "businessBorrowings2": {"type": "number"},
            "carOwner": {"type": "boolean"},
            "houseOwner": {"type": "boolean"},
        },
    }
    try:
        return validate(instance=input_value, schema=credit_score_schema)
    except Exception as e:
        return e.message
