##CLI Budget Analyzer##


To run this tool, put the file of the tool as well as the input json data file into the same folder. Once you are directed into that folder with the two files, run: python budget_analyzer.py --input transactions_MM_YYYY.json. Make sure to replace the MM and the YYYY with the file that correlates to what you want to analyze, the MM is replaced by the month and the YYYY is replaced by the year.


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