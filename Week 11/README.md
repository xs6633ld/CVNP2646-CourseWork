This python script detects changes in configuration. It compares a baseline JSON configuration which is the expected configuration, to the current configuration to detect differences. It identifies missing, changed, or extra values and creates a report on the analyzation. It is super important to monitor your configurations as accidental changes and unatjorized changes may occur. This script provides you with the steps to take if something so happens to be changed. 

To run this script successfuly, create a working directory containing your baseline and current json configurations as well as the python script. Then run python drift_checker.py and you will get a report on any findings. 

The script checked for any values that have been deleted or are missing, any extra values, as well as changed values. 

In the drift report you will see the sections of path, type, basline value, current value, and sevirity. The path indicates the location of the change in the configuration, the type indicates if something is missing, changed or if something has been added, the baseline value shows the value for that section of what should be there, the current value shows the value for that section of what was changed, and the sevirty ranks from high to medium to low based on different factors. 


Changed values get a high severity if configuration change happens in the location of either password, secret, admin, root, or enabled. They get a medium severity if a value is missing, and low severity for all other changes such as a value changed or added.

From my test files, 6 drifts were detected with 1 high severity, 1 medium servity, and 4 low severities. 

Here is a sample of my drift report:
 {
    "path": "rules[0].port",
    "type": "changed",
    "baseline_value": 443,
    "current_value": 8080,
    "severity": "low"
  },
  {
    "path": "rules[1].source",
    "type": "changed",
    "baseline_value": "10.0.0.0/8",
    "current_value": "0.0.0.0/0",
    "severity": "low"
  }

The most difficult part about this project was figuring out how to do the comparision of the two config files but with the help me AI I was able to break it down and figure it out.

Some common real world vulnerablities this script could detect are removed security controls, unauthorized changes, and exposed services.
