PARAMETERS = {
    # Past Loan Defaults of the Key Persons of the company (Director, Propreitor)
    "pastLoanDefaultsNumberKP": {
        "name": "pastLoanDefaultsNumberKP",
        "comparing_value": "independent",
        "priority_score": 7,
        "minimum_score": 0,
        "maximum_score": None,
        "model": "binary",
        "true_score": None,
        "frontend_value": None,
        "redundant": True
    },
    # /** 3. Current running loans of the key persons */
    "runningLoanRatioBusiness": {
        "name": "runningLoanRatioBusiness",
        "comparing_value": "independent",
        "priority_score": 6,
        "minimum_score": 0,
        "maximum_score": None,
        "model": "linear",
        "true_score": None,
        "frontend_value": None,
        "redundant": True
    },
    # /** 4. Other Income Sources of the Key Persons */
    "incomeRatioKP": {
        "name": "incomeRatioKP",
        "comparing_value": "independent",
        "priority_score": 4,
        "minimum_score": 0,
        "maximum_score": None,
        "model": "linear",
        "true_score": None,
        "frontend_value": None,
        "redundant": False
    },
    # /** 5. The number of times the bank statement has been changed or sudden activity reduction in a particular bank */
    "bankAccountChange": {
        "name": "bankAccountChange",
        "comparing_value": "independent",
        "priority_score": 6,
        "minimum_score": 0,
        "maximum_score": None,
        "model": "linear",
        "true_score": None,
        "frontend_value": None,
        "redundant": True
    },
    # /** 6. Total assets worth (House, land, vehicle) */
    "assetWorthRatioKP": {
        "name": "assetWorthRatioKP",
        "comparing_value": "independent",
        "priority_score": 6,
        "minimum_score": 0,
        "maximum_score": None,
        "model": "linear",
        "true_score": None,
        "frontend_value": None,
        "redundant": False
    },
    # /** 7. Asset worth of business with loan applied ratio */
    "assetWorthRatioBusiness": {
        "name": "assetWorthRatioBusiness",
        "comparing_value": "independent",
        "priority_score": 6,
        "minimum_score": 0,
        "maximum_score": None,
        "model": "linear",
        "true_score": None,
        "frontend_value": None,
        "redundant": False
    },
    # /** 8. No. of children? */
    "totalChildren": {
        "name": "totalChildren",
        "comparing_value": "independent",
        "priority_score": 5,
        "minimum_score": 0,
        "maximum_score": None,
        "model": "split",
        "true_score": None,
        "frontend_value": None,
        "redundant": False
    },
    # /** 9. Married? */
    "maritalStatus": {
        "name": "maritalStatus",
        "comparing_value": "independent",
        "priority_score": 4,
        "minimum_score": 0,
        "maximum_score": None,
        "model": "binary",
        "true_score": None,
        "frontend_value": None,
        "redundant": False
    },
    # /** 10. Total dependants (including spouse & children) */
    "totalDependants": {
        "name": "totalDependants",
        "comparing_value": "independent",
        "priority_score": 5,
        "minimum_score": 0,
        "maximum_score": None,
        "model": "split",
        "true_score": None,
        "frontend_value": None,
        "redundant": False
    },
    # /** 11. Part of any Social Club */
    "clubMembership": {
        "name": "clubMembership",
        "comparing_value": "independent",
        "priority_score": 4,
        "minimum_score": 0,
        "maximum_score": None,
        "model": "binary",
        "true_score": None,
        "frontend_value": None,
        "redundant": False
    },
    # /** 12. Travelling Abroad */
    "abroadTravels": {
        "name": "abroadTravels",
        "comparing_value": "independent",
        "priority_score": 6,
        "minimum_score": 0,
        "maximum_score": None,
        "model": "linear",
        "true_score": None,
        "frontend_value": None,
        "redundant": False
    },
    # /** 13. Hobbies/Interests */
    "hobbyCount": {
        "name": "hobbyCount",
        "comparing_value": "independent",
        "priority_score": 3,
        "minimum_score": 0,
        "maximum_score": None,
        "model": "linear",
        "true_score": None,
        "frontend_value": None,
        "redundant": False
    },
    # /** 14. Turnover:Capital Deployed */
    "turnoverCapitalDeployedRatio": {
        "name": "turnoverCapitalDeployedRatio",
        "comparing_value": "independent",
        "priority_score": 8,
        "minimum_score": 0,
        "maximum_score": None,
        "model": "linear",
        "true_score": None,
        "frontend_value": None,
        "redundant": True
    },
    # /** 15. If loans and advances given to company with same "name"s/last-"name"s as proprietors, consider negative */
    "loanCapitalInvestedRatioKP": {
        "name": "loanCapitalInvestedRatioKP",
        "comparing_value": "independent",
        "priority_score": 6,
        "minimum_score": 0,
        "maximum_score": None,
        "model": "linear",
        "true_score": None,
        "frontend_value": None,
        "redundant": False
    },
    # /** 16. Total Income(Gross+Monthly) + m-o-m change + Flag Hikes */
    "yearlyIncomeRatio": {
        "name": "yearlyIncomeRatio",
        "comparing_value": "independent",
        "priority_score": 6,
        "minimum_score": 0,
        "maximum_score": None,
        "model": "linear",
        "true_score": None,
        "frontend_value": None,
        "redundant": False
    },
    # /** 17. Profit (Total + Monthly) + m-o-m Change */
    "yearlyProfitRatio": {
        "name": "yearlyProfitRatio",
        "comparing_value": "independent",
        "priority_score": 7,
        "minimum_score": 0,
        "maximum_score": None,
        "model": "linear",
        "true_score": None,
        "frontend_value": None,
        "redundant": False
    },
    # /** 18. Profit:Income (Monthly) + m-o-m growth */
    "yearlyMarginRatio": {
        "name": "yearlyMarginRatio",
        "comparing_value": "independent",
        "priority_score": 6,
        "minimum_score": 0,
        "maximum_score": None,
        "model": "linear",
        "true_score": None,
        "frontend_value": None,
        "redundant": False
    },
    # /** 19. Credits vs Account Spread */
    "creditSpreadRatio": {
        "name": "creditSpreadRatio",
        "comparing_value": "independent",
        "priority_score": 6,
        "minimum_score": 0,
        "maximum_score": None,
        "model": "linear",
        "true_score": None,
        "frontend_value": None,
        "redundant": True
    },
    # /** 20. Monthly outgoing EMIs for existing loans */
    "outgoingEmiRatio": {
        "name": "outgoingEmiRatio",
        "comparing_value": "independent",
        "priority_score": 8,
        "minimum_score": 0,
        "maximum_score": None,
        "model": "linear",
        "true_score": None,
        "frontend_value": None,
        "redundant": False
    },
    # /** 21. Personal Drawings from account (Monthly) */
    "ctcProfitRatioKP": {
        "name": "ctcProfitRatioKP",
        "comparing_value": "independent",
        "priority_score": 4,
        "minimum_score": 0,
        "maximum_score": None,
        "model": "linear",
        "true_score": None,
        "frontend_value": None,
        "redundant": False
    },
    # /** 22. No. of Defaulted Transactions  */
    "defaultedTransaction": {
        "name": "defaultedTransaction",
        "comparing_value": "independent",
        "priority_score": 8,
        "minimum_score": 0,
        "maximum_score": None,
        "model": "linear",
        "true_score": None,
        "frontend_value": None,
        "redundant": False
    },
    # /** 23. No. and amount of Overdraft Transactions */
    "overdraftTransactions": {
        "name": "overdraftTransactions",
        "comparing_value": "independent",
        "priority_score": 4,
        "minimum_score": 0,
        "maximum_score": None,
        "model": "linear",
        "true_score": None,
        "frontend_value": None,
        "redundant": False
    },
    # /** 24 Average Quaterly/Monthly/Daily Balance */
    "averageMonthlyBalance": {
        "name": "averageMonthlyBalance",
        "comparing_value": "independent",
        "priority_score": 7,
        "minimum_score": 0,
        "maximum_score": None,
        "model": "linear",
        "true_score": None,
        "frontend_value": None,
        "redundant": True
    },
    # /** 25. Monthly Surplus in accounts and m-o-m change */
    "yearlySurplusRatio": {
        "name": "yearlySurplusRatio",
        "comparing_value": "independent",
        "priority_score": 3,
        "minimum_score": 0,
        "maximum_score": None,
        "model": "linear",
        "true_score": None,
        "frontend_value": None,
        "redundant": True
    },
    # /** 26. Payments towards Savings and Investment */
    "paymentTowardsSavingsRatio": {
        "name": "paymentTowardsSavingsRatio",
        "comparing_value": "independent",
        "priority_score": 6,
        "minimum_score": 0,
        "maximum_score": None,
        "model": "linear",
        "true_score": None,
        "frontend_value": None,
        "redundant": False
    },
    # /** 27. Absolute income tax */
    "yearlyTaxRatio": {
        "name": "yearlyTaxRatio",
        "comparing_value": "independent",
        "priority_score": 4,
        "minimum_score": 0,
        "maximum_score": None,
        "model": "linear",
        "true_score": None,
        "frontend_value": None,
        "redundant": False
    },
    # /** 29. Past Loan Defaults */
    "defaultedLoansNumberBusiness": {
        "name": "defaultedLoansNumberBusiness",
        "comparing_value": "independent",
        "priority_score": 10,
        "minimum_score": 0,
        "maximum_score": None,
        "model": "binary",
        "true_score": None,
        "frontend_value": None,
        "redundant": False
    },
    # /** 30. Short-term vs Long-term borrowings */
    "longTermLoansRatio": {
        "name": "longTermLoansRatio",
        "comparing_value": "independent",
        "priority_score": 6,
        "minimum_score": 0,
        "maximum_score": None,
        "model": "binary",
        "true_score": None,
        "frontend_value": None,
        "redundant": True
    },
    # /** 31. Cash Deposits */
    "cashDepositRatio": {
        "name": "cashDepositRatio",
        "comparing_value": "independent",
        "priority_score": 6,
        "minimum_score": 0,
        "maximum_score": None,
        "model": "binary",
        "true_score": None,
        "frontend_value": None,
        "redundant": False
    },
    # /** 31. GST Score */
    "GSTScore": {
        "name": "GSTScore",
        "comparing_value": "independent",
        "priority_score": 6,
        "minimum_score": 0,
        "maximum_score": None,
        "model": "binary",
        "true_score": None,
        "frontend_value": None,
        "redundant": False
    }
}
