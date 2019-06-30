from __future__ import division
from src.CreditScore.Utils import Helper


def final_parameters(raw_parameters):
    """
    create credit score parameter
    :param raw_parameters: Json input with parameter value
    :return: 30 credit parameter dictionary
    """
    parameters = {}
    parameters["pastLoanDefaultsNumberKP"] = raw_parameters["pastLoanDefaultsNumberKP"]
    parameters["runningLoanRatioBusiness"] = Helper._divide(
        raw_parameters["businessBorrowings1"] + raw_parameters["businessBorrowings2"],
        raw_parameters["loanApplied"])  # option 2 data from cibil
    parameters["incomeRatioKP"] = Helper._divide(raw_parameters["incomeKP1"], raw_parameters["incomeBusiness1"])
    parameters["bankAccountChange"] = raw_parameters["bankAccountChange"]
    parameters["assetWorthRatioKP"] = Helper._divide(100000, raw_parameters["loanApplied"])
    parameters["assetWorthRatioBusiness"] = Helper._divide(raw_parameters["fixedAssetBusiness1"],
                                                           raw_parameters["loanApplied"])
    parameters["totalChildren"] = raw_parameters["totalChildren"]
    parameters["maritalStatus"] = raw_parameters["maritalStatus"]
    parameters["totalDependants"] = raw_parameters["totalDependants"]
    parameters["clubMembership"] = raw_parameters["clubMembership"]
    parameters["abroadTravels"] = raw_parameters["abroadTravels"]
    parameters["hobbyCount"] = len(raw_parameters["hobbyCount"].split(','))
    parameters["turnoverCapitalDeployedRatio"] = Helper._divide(raw_parameters["incomeBusiness1"],
                                                                raw_parameters["capitalDeployed1"])
    parameters["loanCapitalInvestedRatioKP"] = Helper._divide(raw_parameters["maxLoanToKP"],
                                                              raw_parameters["capitalInvestedByKP"])
    parameters["yearlyIncomeRatio"] = Helper._divide(
        raw_parameters["incomeBusiness1"] - raw_parameters["incomeBusiness2"], abs(raw_parameters["incomeBusiness2"]))
    parameters["yearlyProfitRatio"] = Helper._divide(raw_parameters["profit1"] - raw_parameters["profit2"],
                                                     abs(raw_parameters['profit2']))
    parameters["yearlyMarginRatio"] = Helper._divide(
        Helper._divide(raw_parameters["profit1"], raw_parameters["incomeBusiness1"]) - Helper._divide(
            raw_parameters["profit2"], raw_parameters["incomeBusiness2"]),
        abs(Helper._divide(raw_parameters["profit2"], raw_parameters["incomeBusiness2"])))
    parameters["creditSpreadRatio"] = Helper._divide(raw_parameters["accounts80credit"],
                                                     raw_parameters["totalCreditAccounts"])
    parameters["outgoingEmiRatio"] = Helper._divide(raw_parameters["averageMonthlyEmilast2"],
                                                    raw_parameters["loanApplied"])
    parameters["ctcProfitRatioKP"] = Helper._divide(raw_parameters["ctcKP1"], raw_parameters["profit1"])
    parameters["defaultedTransaction"] = raw_parameters["lastYearDefaultedTransactions"]
    parameters["overdraftTransactions"] = raw_parameters["lastYearOverdraftTransactions"]
    parameters["averageMonthlyBalance"] = Helper._divide(raw_parameters["averageMonthlyBalance"],
                                                         raw_parameters["loanApplied"])
    parameters["yearlySurplusRatio"] = Helper._divide(raw_parameters["closingBankBalanceYear1"] - raw_parameters["closingBankBalanceYear2"],
                                                      abs(raw_parameters["closingBankBalanceYear2"]))
    parameters["paymentTowardsSavingsRatio"] = Helper._divide(raw_parameters["paymentTowardsSavings"],
                                                              raw_parameters["profit1"])
    parameters["yearlyTaxRatio"] = Helper._divide(raw_parameters["tax1"] - raw_parameters["tax2"],
                                                  abs(raw_parameters["tax2"]))
    parameters["defaultedLoansNumberBusiness"] = raw_parameters["pastLoanDefaultsNumberBusiness"]
    parameters["longTermLoansRatio"] = Helper._divide(
        raw_parameters["fixedAssetBusiness1"] - raw_parameters["fixedAssetBusiness2"],
        raw_parameters["businessBorrowings1"])
    parameters["cashDepositRatio"] = Helper._divide(raw_parameters["cashDepositTotalLastYear"],
                                                    raw_parameters["incomeBusiness1"])
    parameters["GSTScore"] = 1800000

    return parameters


def final_parameters_numerator_denominator(raw_parameters):
    """
    Create dictionary of parameter which used to create 30 final parameters.
    :param raw_parameters: parameter value.
    :return: dictionary with list of parameter used to create 30 final parameters.
    """
    parameters_list = {}
    parameters_list["pastLoanDefaultsNumberKP"] = {"numerator": raw_parameters["pastLoanDefaultsNumberKP"],
                                                   "denominator": None}
    parameters_list["runningLoanRatioBusiness"] = {
        "numerator": (raw_parameters["businessBorrowings1"] + raw_parameters["businessBorrowings2"]),
        "denominator": float(raw_parameters["loanApplied"])}
    parameters_list["incomeRatioKP"] = {"numerator": float(raw_parameters["incomeKP1"]),
                                        "denominator": float(raw_parameters["incomeBusiness1"])}
    parameters_list["bankAccountChange"] = {"numerator": float(raw_parameters["bankAccountChange"]),
                                            "denominator": None}
    parameters_list["assetWorthRatioKP"] = {"carOwner": raw_parameters["carOwner"],
                                            "houseOwner": raw_parameters["houseOwner"]}
    parameters_list["assetWorthRatioBusiness"] = {"numerator": float(raw_parameters["fixedAssetBusiness1"]),
                                                  "denominator": float(raw_parameters["loanApplied"])}
    parameters_list["totalChildren"] = {"numerator": raw_parameters["totalChildren"], "denominator": None}
    parameters_list["maritalStatus"] = {"numerator": raw_parameters["maritalStatus"], "denominator": None}
    parameters_list["totalDependants"] = {"numerator": raw_parameters["totalDependants"], "denominator": None}
    parameters_list["clubMembership"] = {"numerator": raw_parameters["clubMembership"], "denominator": None}
    parameters_list["abroadTravels"] = {"numerator": raw_parameters["abroadTravels"], "denominator": None}
    parameters_list["hobbyCount"] = {"numerator": len(raw_parameters["hobbyCount"].split(',')), "denominator": None}
    parameters_list["turnoverCapitalDeployedRatio"] = {"numerator": float(raw_parameters["incomeBusiness1"]),
                                                       "denominator": float(raw_parameters["capitalDeployed1"])}
    parameters_list["loanCapitalInvestedRatioKP"] = {"numerator": float(raw_parameters["maxLoanToKP"]),
                                                     "denominator": float(raw_parameters["capitalInvestedByKP"])}
    parameters_list["yearlyIncomeRatio"] = {
        "numerator": float(raw_parameters["incomeBusiness1"] - raw_parameters["incomeBusiness2"]),
        "denominator": float(raw_parameters["incomeBusiness2"])}
    parameters_list["yearlyProfitRatio"] = {"numerator": float(raw_parameters["profit1"] - raw_parameters["profit2"]),
                                            "denominator": abs(float(raw_parameters['profit2']))}
    parameters_list["yearlyMarginRatio"] = {"numerator_numerator_one": float(raw_parameters["profit1"]),
                                            "numerator_denominator_one": float(raw_parameters["incomeBusiness1"]),
                                            "numerator_numerator_two": float(raw_parameters["profit2"]),
                                            "numerator_denominator_two": float(raw_parameters["incomeBusiness2"])}
    parameters_list["creditSpreadRatio"] = {"numerator": float(raw_parameters["accounts80credit"]),
                                            "denominator": float(raw_parameters["totalCreditAccounts"])}
    parameters_list["outgoingEmiRatio"] = {"numerator": float(raw_parameters["averageMonthlyEmilast2"]),
                                           "denominator": float(raw_parameters["loanApplied"])}
    parameters_list["ctcProfitRatioKP"] = {"numerator": float(raw_parameters["ctcKP1"]),
                                           "denominator": float(raw_parameters["profit1"])}
    parameters_list["defaultedTransaction"] = {"numerator": raw_parameters["lastYearDefaultedTransactions"],
                                               "denominator": None}
    parameters_list["overdraftTransactions"] = {"numerator": raw_parameters["lastYearOverdraftTransactions"],
                                                "denominator": None}
    parameters_list["averageMonthlyBalance"] = {"numerator": float(raw_parameters["averageMonthlyBalance"]),
                                                "denominator": float(raw_parameters["loanApplied"])}
    parameters_list["yearlySurplusRatio"] = {
        "numerator": float(raw_parameters["closingBankBalanceYear1"] - raw_parameters["closingBankBalanceYear2"]),
        "denominator": abs(float(raw_parameters["closingBankBalanceYear2"]))}
    parameters_list["paymentTowardsSavingsRatio"] = {"numerator": float(raw_parameters["paymentTowardsSavings"]),
                                                     "denominator": float(raw_parameters["profit1"])}
    parameters_list["yearlyTaxRatio"] = {"numerator": float(raw_parameters["tax1"] - raw_parameters["tax2"]),
                                         "denominator": abs(float(raw_parameters["tax2"]))}
    parameters_list["defaultedLoansNumberBusiness"] = {"numerator": raw_parameters["pastLoanDefaultsNumberBusiness"],
                                                       "denominator": None}
    parameters_list["longTermLoansRatio"] = {
        "numerator": float(raw_parameters["fixedAssetBusiness1"] - raw_parameters["fixedAssetBusiness2"]),
        "denominator": float(raw_parameters["businessBorrowings1"] + raw_parameters["businessBorrowings2"])}
    parameters_list["cashDepositRatio"] = {"numerator": float(raw_parameters["cashDepositTotalLastYear"]),
                                           "denominator": float(raw_parameters["incomeBusiness1"])}
    parameters_list["GSTScore"] = {"GST1": float(raw_parameters["GST1"]), "GST2": float(raw_parameters["GST2"]),
                                   "GST3": float(raw_parameters["GST3"])}

    return parameters_list

