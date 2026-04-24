WHAT WORKS:
This CLI budget analyzer can successfully processes transaction data from the JSON file with multiple transactions which each include their own date, amount spent, category, and small description. The tool analyzes spending by category, compares totals to their set budgets, and indicates any over spending per category.


WHAT'S MISSING:
The script is still missing vital error handeling. If invalid data is put in, the script ignores it but does not make a warning about it. This could lead to incorrect budget analyzation. There are also some optional features that could be added such as severity levels for when overspending occurs and a more noticeable and urgent over spending anaylzation.


CHANGES FROM PROPOSAL:
The main design of the tool did not have any large changes. The only thing that changed was moving the budget limits from the python tool to the top of the actual input data. This was suggested by AI as it improves efficency and clearness. 


AI USAGE:
I used AI to create the input data to make sure there was a large amount of input data and a large varity. I specified what kind of categories I wanted for the test data and to make sure one category had overspending to make sure that analyzation function works properly. I also had AI help me to break down how I would build the script, simular to the instructions that were given for past python assignments. Breaking the process of building the tool down helped a lot.