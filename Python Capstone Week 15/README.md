To run this tool, put the file of the tool as well as the input json data file into the same folder. Once you are directed into that folder with the two files, run: python budget_analyzer.py --input transactions_MM_YYYY.json. Make sure to replace the MM and the YYYY with the file that correlates to what you want to analyze, the MM is replaced by the month and the YYYY is replaced by the year.


Here is what your input json file should look like:
{
  "budgets": {
    "Subscription": 8000,
    "Equipment Purchase": 12000,
    "Repair": 4000,
    "Cloud Services": 10000,
    "Security": 7000,
    "Maintenance": 5000,
    "Licensing": 6000,
    "Networking": 8000
  },
  "transactions": [
    {"date": "2026-04-01", "amount": 320, "category": "Subscription", "description": "Software license renewal"},
    {"date": "2026-04-01", "amount": 1500, "category": "Cloud Services", "description": "Cloud hosting fees"},
    {"date": "2026-04-02", "amount": 220, "category": "Subscription", "description": "Antivirus subscription"},
    {"date": "2026-04-02", "amount": 4000, "category": "Equipment Purchase", "description": "Network switches"},
    {"date": "2026-04-03", "amount": 450, "category": "Cloud Services", "description": "Backup storage"},
    {"date": "2026-04-03", "amount": 120, "category": "Subscription", "description": "Domain renewal"},
    {"date": "2026-04-04", "amount": 2080, "category": "Equipment Purchase", "description": "Workstation upgrade"},
    {"date": "2026-04-04", "amount": 300, "category": "Subscription", "description": "IT training course"},
    {"date": "2026-04-05", "amount": 75, "category": "Equipment Purchase", "description": "USB drives"},
    {"date": "2026-04-05", "amount": 600, "category": "Security", "description": "Firewall maintenance"},
  ]
}

Here is the expected CLI output:

INFO: Loaded 50 transactions.
INFO: Completed spending aggregation.
INFO: Completed budget comparison.
INFO: Detected 1 overspending categories.
INFO: Results written to results.json


Here is a sample of the output json file: 

"Cloud Services": {
            "total_spent": 5755.0,
            "budget": 10000,
            "difference": -4245.0
        },
        "Equipment Purchase": {
            "total_spent": 14425.0,
            "budget": 12000,
            "difference": 2425.0
        },
        "Security": {
            "total_spent": 3930.0,
            "budget": 7000,
            "difference": -3070.0



This python tool is an effective budget analyzer. This tool is under a file named budget_analyzer.py. Many businesses struggle with their budgets, especially in IT. Few businesses have a structured budgeting tool that analyzes and tracks there spending, but that is what this tool is here for! Without using an effective tool that this one, businesses can end up having unnoticed overspending, lack of visibility of where their money is going, and poor financial decisions. This tool solves every one of those problems by analyzing different transactions, categorizing expenses, and identifying when spending exceeds defined budgets.

The python tool will have five main features/functions. The first feature is named transaction_processing which reads and parses the json transaction data. The second feature is named spending_aggregation which calculates total spending for each individual category and all categories combined. The third feature is named budget_comparison which compares the spending against the predefined spending limits. The fourth feature is named overspending_detection which flags the categories that have exceeded their budget if any. The fifth and final feature is named output_generation which generates the json results showing total analyzation.

To run this tool, you need Python 3.10 or higher installed onto your computer. Create a folder for your python tool and input file to go into. Download the python tool and place it in the designated folder. You are now prepared to run the tool.

To run tests, you need to have pytest installed. In the folder with the test_budget_analyzer.py file run pytest from the terminal, it will then create a output file of the results and show you the results in the terminal. 

This project contains multiple key files. The first one is budget_analyzer.py which is the main application of the script. test_budget_analyzer.py contains tests written using pytest. transactions_04_2026.json is the main input dataset.