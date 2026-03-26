This script audits user accounts based on their user account data and their role assignments. It then creates a stuctured json report for easy SOC machine actions and a human readable text report. IAM audting is super important to maintain the integrity of your company. IAM audting prevents unauthorized access and reduces threats inside of your company. It is super important to disable accounts that are no longer used inside your company and to spread out user access to different accounts to limit the access when and if an account gets comprimised. 

To run the script, run python permissions_auditor.py. It will then display in the terminal the total violations found, confirm that the json and text file were generated, as well as actually generate those two reports with actionable data. 

Users.json contains users user ID, username, status, department, and last login. Roles.json contains users user ID, role, and creation date of the user profile. Both contain information for the auditor to effectivly find violations that do not allign with their security requirements such as diabled users with active roles, and active accounts that have not been used in a long time. 

Disabled users with active roles = critical severity.
Unauthorized admin access = high severity.
Stale accounts = medium severity.
Orphaned roles = high severity.
Roles assigned before hire date = high severity.
Admin role assigned within 30 days of hire = high severity.

I used ChatGPT to help with this project. The auditing it suggested I add was to audit roles assigned before hire date and admin roles assigned within 30 days of hire after I prompted it by asking what additional auditing could I add to this script to make it better.

I found a total of six violations after running the script. 

Here is part of my text report showing the critical violations:
DETAILED VIOLATIONS
================================================================================

CRITICAL (3 issues)
--------------------------------------------------------------------------------
1. asmith (U002)
   Type: disabled_with_roles
   Details: Disabled account has roles: hr_manager
2. mjohnson (U005)
   Type: disabled_with_roles
   Details: Disabled account has roles: marketing_user
3. tlarson (U008)
   Type: disabled_with_roles
   Details: Disabled account has roles: it_support

This supports SOC 2 by ensuring of refular access auditing. This supports ISO 27001 by identifying unauthorized access. This supports PCI-DSS by detecting inactive accounts.

This was definitly the most challenging project so far. It was really hard to figure out how to do the auditing part but with the help of AI and the web app I was able to figure out how to impliment it.