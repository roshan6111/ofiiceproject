def pastLoanDefaultsNumberKP(minimum_score, maximum_score, model, frontend_value, numerator_denominator_obj):
    vh = 1
    vl = 0
    score_vh = minimum_score
    score_vl = maximum_score
    c = maximum_score
    true_value = 0
    if vl <= frontend_value and frontend_value <= vh:
        true_value = (((score_vl - score_vh) / (vl - vh)) * frontend_value) + c
    elif vh < frontend_value:
        true_value = score_vh
    elif frontend_value < vl:
        true_value = score_vl

    return true_value


def runningLoanRatioBusiness(minimum_score, maximum_score, model, frontend_value, numerator_denominator_obj):
    vh = 1
    vl = 0
    score_vh = minimum_score
    score_vl = maximum_score
    c = maximum_score
    true_value = 0
    if vl <= frontend_value and frontend_value <= vh:
        true_value = (((score_vl - score_vh) / (vl - vh)) * frontend_value) + c
    elif vh < frontend_value:
        true_value = score_vh
    elif frontend_value < vl:
        true_value = score_vl

    return true_value


def incomeRatioKP(minimum_score, maximum_score, model, frontend_value, numerator_denominator_obj):
    vh = 1
    vl = 0.1
    score_vh = minimum_score
    score_vl = maximum_score
    # c = -(maximum_score / 9)
    c = (10.0/9.0) * maximum_score
    true_value = 0
    if numerator_denominator_obj['denominator'] == 0:
        true_value = 0
    elif vl <= frontend_value and frontend_value <= vh:
        true_value = (((score_vl - score_vh) / (vl - vh)) * frontend_value) + c
    elif vh < frontend_value:
        true_value = score_vh
    elif frontend_value < vl:
        true_value = score_vl

    return true_value


def bankAccountChange(minimum_score, maximum_score, model, frontend_value, numerator_denominator_obj):
    vh = 3
    vl = 0
    score_vh = minimum_score
    score_vl = maximum_score
    c = maximum_score
    true_value = 0
    if vl <= frontend_value and frontend_value <= vh:
        true_value = (((score_vl - score_vh) / (vl - vh)) * frontend_value) + c
    elif vh < frontend_value:
        true_value = score_vh
    elif frontend_value < vl:
        true_value = score_vl

    return true_value


def assetWorthRatioKP(minimum_score, maximum_score, model, frontend_value, numerator_denominator_obj):
    true_value = 0
    if numerator_denominator_obj["carOwner"] == True and numerator_denominator_obj["houseOwner"] == True:
        true_value = maximum_score
    elif numerator_denominator_obj["carOwner"] == False and numerator_denominator_obj["houseOwner"] == True:
        true_value = maximum_score / 2
    elif numerator_denominator_obj["carOwner"] == True and numerator_denominator_obj["houseOwner"] == False:
        true_value = maximum_score / 4
    elif numerator_denominator_obj["carOwner"] == False and numerator_denominator_obj["houseOwner"] == False:
        true_value = 0

    return true_value


def assetWorthRatioBusiness(minimum_score, maximum_score, model, frontend_value, numerator_denominator_obj):
    vh = 5
    # vl = 1
    vl = 0
    score_vh = maximum_score
    score_vl = minimum_score
    # c = -(maximum_score / 4)
    c = 0
    true_value = 0
    if vl <= frontend_value and frontend_value <= vh:
        true_value = (((score_vl - score_vh) / (vl - vh)) * frontend_value) + c
    elif vh < frontend_value:
        true_value = score_vh
    elif frontend_value < vl:
        true_value = score_vl

    return true_value


def totalChildren(minimum_score, maximum_score, model, frontend_value, numerator_denominator_obj):
    true_value = 0
    if 4 <= frontend_value and frontend_value <= 0:
        true_value = minimum_score
    elif frontend_value == 2:
        true_value = maximum_score
    elif frontend_value == 1 or frontend_value == 2:
        true_value = maximum_score / 2

    return true_value


def maritalStatus(minimum_score, maximum_score, model, frontend_value, numerator_denominator_obj):
    true_value = 0
    if frontend_value:
        true_value = maximum_score
    else:
        true_value = minimum_score
    return true_value


def totalDependants(minimum_score, maximum_score, model, frontend_value, numerator_denominator_obj):
    true_value = 0
    if 6 <= frontend_value:
        true_value = minimum_score
    elif frontend_value == 3 or frontend_value == 4:
        true_value = maximum_score
    elif frontend_value == 1 or frontend_value == 2 or frontend_value == 5:
        true_value = maximum_score / 2

    return true_value


def clubMembership(minimum_score, maximum_score, model, frontend_value, numerator_denominator_obj):
    if frontend_value:
        true_value = maximum_score
    else:
        true_value = minimum_score
    return true_value


def abroadTravels(minimum_score, maximum_score, model, frontend_value, numerator_denominator_obj):
    vh = 2
    vl = 0
    score_vh = maximum_score
    score_vl = minimum_score
    c = minimum_score
    true_value = 0
    if vl <= frontend_value and frontend_value <= vh:
        true_value = (((score_vl - score_vh) / (vl - vh)) * frontend_value) + c
    elif vh < frontend_value:
        true_value = score_vh
    elif frontend_value < vl:
        true_value = score_vl

    return true_value


def hobbyCount(minimum_score, maximum_score, model, frontend_value, numerator_denominator_obj):
    vh = 3
    vl = 0
    score_vh = maximum_score
    score_vl = minimum_score
    c = minimum_score
    true_value = 0
    if vl <= frontend_value and frontend_value <= vh:
        true_value = (((score_vl - score_vh) / (vl - vh)) * frontend_value) + c
    elif vh < frontend_value:
        true_value = score_vh
    elif frontend_value < vl:
        true_value = score_vl

    return true_value


def turnoverCapitalDeployedRatio(minimum_score, maximum_score, model, frontend_value, numerator_denominator_obj):
    vh = 15
    vl = 5
    score_vh = maximum_score
    score_vl = minimum_score
    c = -(maximum_score / 2)
    true_value = 0
    if numerator_denominator_obj["denominator"] == 0 and numerator_denominator_obj["numerator"] == 0:
        true_value = 0
    elif numerator_denominator_obj["denominator"] == 0 and numerator_denominator_obj["numerator"] != 0:
        true_value = maximum_score
    elif vl <= frontend_value and frontend_value <= vh:
        true_value = (((score_vl - score_vh) / (vl - vh)) * frontend_value) + c
    elif vh < frontend_value:
        true_value = score_vh
    elif frontend_value < vl:
        true_value = score_vl

    return true_value


def loanCapitalInvestedRatioKP(minimum_score, maximum_score, model, frontend_value, numerator_denominator_obj):
    vh = 1
    vl = 0
    score_vh = minimum_score
    score_vl = maximum_score
    c = maximum_score
    true_value = 0
    if numerator_denominator_obj["denominator"] == 0 and numerator_denominator_obj["numerator"] == 0:
        true_value = maximum_score
    elif numerator_denominator_obj["denominator"] == 0 and numerator_denominator_obj["numerator"] != 0:
        true_value = 0
    elif vl <= frontend_value and frontend_value <= vh:
        true_value = (((score_vl - score_vh) / (vl - vh)) * frontend_value) + c
    elif vh < frontend_value:
        true_value = score_vh
    elif frontend_value < vl:
        true_value = score_vl

    return true_value


def yearlyIncomeRatio(minimum_score, maximum_score, model, frontend_value, numerator_denominator_obj):
    vh = 0.25
    vl = 0
    score_vh = maximum_score
    score_vl = minimum_score
    c = 0
    true_value = 0
    if numerator_denominator_obj["denominator"] == 0 and numerator_denominator_obj["numerator"] == 0:
        true_value = 0
    elif numerator_denominator_obj["denominator"] == 0 and numerator_denominator_obj["numerator"] != 0:
        true_value = maximum_score
    elif vl <= frontend_value and frontend_value <= vh:
        true_value = (((score_vl - score_vh) / (vl - vh)) * frontend_value) + c
    elif vh < frontend_value:
        true_value = score_vh
    elif frontend_value < vl:
        true_value = score_vl

    return true_value


def yearlyProfitRatio(minimum_score, maximum_score, model, frontend_value, numerator_denominator_obj):
    vh = 0.25
    vl = 0
    score_vh = maximum_score
    score_vl = minimum_score
    c = 0
    true_value = 0
    if numerator_denominator_obj["denominator"] == 0 and numerator_denominator_obj["numerator"] == 0:
        true_value = maximum_score
    elif numerator_denominator_obj["denominator"] == 0 and numerator_denominator_obj["numerator"] != 0:
        true_value = maximum_score / 2
    elif vl <= frontend_value and frontend_value <= vh:
        true_value = (((score_vl - score_vh) / (vl - vh)) * frontend_value) + c
    elif vh < frontend_value:
        true_value = score_vh
    elif frontend_value < vl:
        true_value = score_vl

    return true_value


def yearlyMarginRatio(minimum_score, maximum_score, model, frontend_value, numerator_denominator_obj):
    vh = 0.1
    vl = 0
    score_vh = maximum_score
    score_vl = minimum_score
    c = 0
    true_value = 0
    if numerator_denominator_obj["numerator_denominator_one"] == 0 or numerator_denominator_obj[
        "numerator_denominator_two"] == 0:
        true_value = 0
    elif vl <= frontend_value and frontend_value <= vh:
        true_value = (((score_vl - score_vh) / (vl - vh)) * frontend_value) + c
    elif vh < frontend_value:
        true_value = score_vh
    elif frontend_value < vl:
        true_value = score_vl

    return true_value


def creditSpreadRatio(minimum_score, maximum_score, model, frontend_value, numerator_denominator_obj):
    vh = 0.5
    vl = 0.2
    score_vh = maximum_score
    score_vl = minimum_score
    c = -(maximum_score * (2.0 / 3.0))
    true_value = 0
    if vl <= frontend_value and frontend_value <= vh:
        true_value = (((score_vl - score_vh) / (vl - vh)) * frontend_value) + c
    elif vh < frontend_value:
        true_value = score_vh
    elif frontend_value < vl:
        true_value = score_vl

    return true_value


def outgoingEmiRatio(minimum_score, maximum_score, model, frontend_value, numerator_denominator_obj):
    vh = 0.7
    vl = 0
    score_vh = minimum_score
    score_vl = maximum_score
    c = maximum_score
    true_value = 0
    if vl <= frontend_value and frontend_value <= vh:
        true_value = (((score_vl - score_vh) / (vl - vh)) * frontend_value) + c
    elif vh < frontend_value:
        true_value = score_vh
    elif frontend_value < vl:
        true_value = score_vl

    return true_value


def ctcProfitRatioKP(minimum_score, maximum_score, model, frontend_value, numerator_denominator_obj):
    vh = 0.6
    vl = 0.4
    score_vh = minimum_score
    score_vl = maximum_score
    c = maximum_score * 3
    true_value = 0
    if numerator_denominator_obj["denominator"] == 0:
        true_value = 0
    if vl <= frontend_value and frontend_value <= vh:
        true_value = (((score_vl - score_vh) / (vl - vh)) * frontend_value) + c
    elif vh < frontend_value:
        true_value = score_vh
    elif frontend_value < vl:
        true_value = score_vl

    return true_value


def defaultedTransaction(minimum_score, maximum_score, model, frontend_value, numerator_denominator_obj):
    vh = 3
    vl = 0
    score_vh = minimum_score
    score_vl = maximum_score
    c = maximum_score
    true_value = 0
    if vl <= frontend_value and frontend_value <= vh:
        true_value = (((score_vl - score_vh) / (vl - vh)) * frontend_value) + c
    elif vh < frontend_value:
        true_value = score_vh
    elif frontend_value < vl:
        true_value = score_vl

    return true_value


def overdraftTransactions(minimum_score, maximum_score, model, frontend_value, numerator_denominator_obj):
    vh = 8
    vl = 4
    score_vh = minimum_score
    score_vl = maximum_score
    c = maximum_score * 2
    true_value = 0
    if vl <= frontend_value and frontend_value <= vh:
        true_value = (((score_vl - score_vh) / (vl - vh)) * frontend_value) + c
    elif vh < frontend_value:
        true_value = score_vh
    elif frontend_value < vl:
        true_value = score_vl

    return true_value


def averageMonthlyBalance(minimum_score, maximum_score, model, frontend_value, numerator_denominator_obj):
    vh = 1
    vl = 0.5
    score_vh = maximum_score
    score_vl = minimum_score
    c = -maximum_score
    true_value = 0
    if vl <= frontend_value and frontend_value <= vh:
        true_value = (((score_vl - score_vh) / (vl - vh)) * frontend_value) + c
    elif vh < frontend_value:
        true_value = score_vh
    elif frontend_value < vl:
        true_value = score_vl

    return true_value



def yearlySurplusRatio(minimum_score, maximum_score, model, frontend_value, numerator_denominator_obj):
    vh = 0.25
    vl = 0
    score_vh = maximum_score
    score_vl = minimum_score
    c = 0
    true_value = 0
    if numerator_denominator_obj["numerator"] == 0 and numerator_denominator_obj["denominator"] == 0:
        true_value = 0
    elif numerator_denominator_obj["denominator"] == 0 and numerator_denominator_obj["numerator"] != 0:
        true_value = (((score_vl - score_vh) / (vl - vh)) * frontend_value + c) / 2
    elif vl <= frontend_value and frontend_value <= vh:
        true_value = (score_vl - score_vh) / (vl - vh) * frontend_value + c
    elif vh < frontend_value:
        true_value = score_vh
    elif frontend_value < vl:
        true_value = score_vl

    return true_value


def paymentTowardsSavingsRatio(minimum_score, maximum_score, model, frontend_value, numerator_denominator_obj):
    vh = 0.25
    vl = 0
    score_vh = maximum_score
    score_vl = minimum_score
    c = minimum_score
    true_value = 0
    if numerator_denominator_obj["numerator"] == 0 and numerator_denominator_obj["denominator"] == 0:
        true_value = 0
    elif numerator_denominator_obj["denominator"] == 0 and numerator_denominator_obj["numerator"] != 0:
        true_value = maximum_score / 2
    elif vl <= frontend_value and frontend_value <= vh:
        true_value = (((score_vl - score_vh) / (vl - vh)) * frontend_value) + c
    elif vh < frontend_value:
        true_value = score_vh
    elif frontend_value < vl:
        true_value = score_vl

    return true_value


def yearlyTaxRatio(minimum_score, maximum_score, model, frontend_value, numerator_denominator_obj):
    vh = 0.2
    vl = 0
    score_vh = maximum_score
    score_vl = minimum_score
    c = 0
    true_value = 0
    if numerator_denominator_obj["numerator"] == 0 or numerator_denominator_obj["denominator"] == 0:
        true_value = 0
    elif vl <= frontend_value and frontend_value <= vh:
        true_value = (((score_vl - score_vh) / (vl - vh)) * frontend_value) + c
    elif vh < frontend_value:
        true_value = score_vh
    elif frontend_value < vl:
        true_value = score_vl

    return true_value


def defaultedLoansNumberBusiness(minimum_score, maximum_score, model, frontend_value, numerator_denominator_obj):
    vh = 1
    vl = 0
    score_vh = minimum_score
    score_vl = maximum_score
    c = maximum_score
    true_value = 0
    if numerator_denominator_obj["numerator"] == 0 and numerator_denominator_obj["denominator"] == 0:
        true_value = 0
    elif numerator_denominator_obj["numerator"] != 0 and numerator_denominator_obj["denominator"] == 0:
        true_value = maximum_score
    elif vl <= frontend_value and frontend_value <= vh:
        true_value = (((score_vl - score_vh) / (vl - vh)) * frontend_value) + c
    elif vh < frontend_value:
        true_value = score_vh
    elif frontend_value < vl:
        true_value = score_vl

    return true_value


def longTermLoansRatio(minimum_score, maximum_score, model, frontend_value, numerator_denominator_obj):
    vh = 0.25
    vl = 0
    score_vh = minimum_score
    score_vl = maximum_score
    c = maximum_score
    true_value = 0
    if vl <= frontend_value and frontend_value <= vh:
        true_value = (((score_vl - score_vh) / (vl - vh)) * frontend_value) + c
    elif vh < frontend_value:
        true_value = score_vh
    elif frontend_value < vl:
        true_value = score_vl

    return true_value


def cashDepositRatio(minimum_score, maximum_score, model, frontend_value, numerator_denominator_obj):
    vh = 0.5
    vl = 0
    score_vh = minimum_score
    score_vl = maximum_score
    c = maximum_score
    true_value = 0
    if numerator_denominator_obj["denominator"] == 0:
        true_value = 0
    elif vl <= frontend_value and frontend_value <= vh:
        true_value = (((score_vl - score_vh) / (vl - vh)) * frontend_value) + c
    elif vh < frontend_value:
        true_value = score_vh
    elif frontend_value < vl:
        true_value = score_vl

    return true_value


def GSTScore(minimum_score, maximum_score, model, frontend_value, numerator_denominator_obj):
    true_value = 0
    if numerator_denominator_obj["GST1"] > numerator_denominator_obj["GST2"] and numerator_denominator_obj["GST2"] > \
            numerator_denominator_obj["GST3"]:
        true_value = maximum_score
    elif numerator_denominator_obj["GST3"] > numerator_denominator_obj["GST2"] and numerator_denominator_obj["GST2"] > \
            numerator_denominator_obj["GST1"]:
        true_value = minimum_score
    elif numerator_denominator_obj["GST1"] > numerator_denominator_obj["GST2"] and numerator_denominator_obj["GST2"] < \
            numerator_denominator_obj["GST3"]:
        true_value = maximum_score / 2
    return true_value

