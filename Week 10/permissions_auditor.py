import json
from datetime import datetime
from collections import defaultdict

# =========================
# DATA LOADING
# =========================
def load_json(filepath):
    """Load JSON file and return list of dictionaries"""
    with open(filepath, 'r') as f:
        return json.load(f)

# =========================
# DATA STRUCTURES / JOIN
# =========================
def build_user_lookup(users_data):
    """Create dictionary for O(1) user lookup"""
    return {user['user_id']: user for user in users_data}

def group_roles_by_user(roles_data):
    """Group roles by user_id"""
    user_roles = defaultdict(list)
    for role_entry in roles_data:
        user_roles[role_entry['user_id']].append(role_entry['role'])
    return dict(user_roles)

# =========================
# VIOLATION RULES
# =========================
def check_disabled_with_roles(users_dict, roles_data):
    """Rule 1: Disabled users should not have roles"""
    violations = []
    users_with_roles = {r['user_id'] for r in roles_data}
    user_roles = group_roles_by_user(roles_data)
    for user_id, user in users_dict.items():
        if user['status'] == 'disabled' and user_id in users_with_roles:
            roles = user_roles.get(user_id, [])
            violations.append({
                'user_id': user_id,
                'username': user['username'],
                'violation_type': 'disabled_with_roles',
                'severity': 'CRITICAL',
                'details': f"Disabled account has roles: {', '.join(roles)}"
            })
    return violations

def check_unauthorized_admins(users_dict, roles_data, authorized_depts={'IT', 'Security'}):
    """Rule 2: Only IT/Security should have admin roles"""
    violations = []
    for entry in roles_data:
        if 'admin' in entry['role'].lower():
            user_id = entry['user_id']
            user = users_dict.get(user_id)
            if user and user['department'] not in authorized_depts:
                violations.append({
                    'user_id': user_id,
                    'username': user['username'],
                    'violation_type': 'unauthorized_admin',
                    'severity': 'HIGH',
                    'details': f"{user['department']} user has admin role"
                })
    return violations

def check_stale_accounts(users_dict, stale_days=90):
    """Rule 3: Accounts not logged in for X days"""
    violations = []
    now = datetime.now()
    for user_id, user in users_dict.items():
        if user['status'] == 'active':
            last_login = user.get('last_login')
            if not last_login:
                violations.append({
                    'user_id': user_id,
                    'username': user['username'],
                    'violation_type': 'stale_account',
                    'severity': 'MEDIUM',
                    'details': 'No login recorded'
                })
                continue
            last_login_date = datetime.strptime(last_login, '%Y-%m-%d')
            days_since = (now - last_login_date).days
            if days_since > stale_days:
                violations.append({
                    'user_id': user_id,
                    'username': user['username'],
                    'violation_type': 'stale_account',
                    'severity': 'MEDIUM',
                    'details': f"Last login {days_since} days ago"
                })
    return violations

# =========================
# ADDITIONAL (AI) RULES
# =========================
import json
from datetime import datetime
from collections import defaultdict

# =========================
# DATA LOADING
# =========================
def load_json(filepath):
    """Load JSON file and return list of dictionaries"""
    with open(filepath, 'r') as f:
        return json.load(f)

# =========================
# DATA STRUCTURES / JOIN
# =========================
def build_user_lookup(users_data):
    """Create dictionary for O(1) user lookup"""
    return {user['user_id']: user for user in users_data}

def group_roles_by_user(roles_data):
    """Group roles by user_id"""
    user_roles = defaultdict(list)
    for role_entry in roles_data:
        user_roles[role_entry['user_id']].append(role_entry['role'])
    return dict(user_roles)

# =========================
# VIOLATION RULES
# =========================
def check_disabled_with_roles(users_dict, roles_data):
    """Rule 1: Disabled users should not have roles"""
    violations = []
    users_with_roles = {r['user_id'] for r in roles_data}
    user_roles = group_roles_by_user(roles_data)
    for user_id, user in users_dict.items():
        if user['status'] == 'disabled' and user_id in users_with_roles:
            roles = user_roles.get(user_id, [])
            violations.append({
                'user_id': user_id,
                'username': user['username'],
                'violation_type': 'disabled_with_roles',
                'severity': 'CRITICAL',
                'details': f"Disabled account has roles: {', '.join(roles)}"
            })
    return violations

def check_unauthorized_admins(users_dict, roles_data, authorized_depts={'IT', 'Security'}):
    """Rule 2: Only IT/Security should have admin roles"""
    violations = []
    for entry in roles_data:
        if 'admin' in entry['role'].lower():
            user_id = entry['user_id']
            user = users_dict.get(user_id)
            if user and user['department'] not in authorized_depts:
                violations.append({
                    'user_id': user_id,
                    'username': user['username'],
                    'violation_type': 'unauthorized_admin',
                    'severity': 'HIGH',
                    'details': f"{user['department']} user has admin role"
                })
    return violations

def check_stale_accounts(users_dict, stale_days=90):
    """Rule 3: Accounts not logged in for X days"""
    violations = []
    now = datetime.now()
    for user_id, user in users_dict.items():
        if user['status'] == 'active':
            last_login = user.get('last_login')
            if not last_login:
                violations.append({
                    'user_id': user_id,
                    'username': user['username'],
                    'violation_type': 'stale_account',
                    'severity': 'MEDIUM',
                    'details': 'No login recorded'
                })
                continue
            last_login_date = datetime.strptime(last_login, '%Y-%m-%d')
            days_since = (now - last_login_date).days
            if days_since > stale_days:
                violations.append({
                    'user_id': user_id,
                    'username': user['username'],
                    'violation_type': 'stale_account',
                    'severity': 'MEDIUM',
                    'details': f"Last login {days_since} days ago"
                })
    return violations

# =========================
# ADDITIONAL (AI) RULES
# =========================
def check_excessive_roles(users_dict, roles_data, threshold=3):
    """Extra Rule: Users with too many roles"""
    violations = []
    user_roles = group_roles_by_user(roles_data)
    for user_id, roles in user_roles.items():
        if len(roles) > threshold:
            user = users_dict.get(user_id, {'username': 'UNKNOWN'})
            violations.append({
                'user_id': user_id,
                'username': user['username'],
                'violation_type': 'excessive_roles',
                'severity': 'LOW',
                'details': f"User has {len(roles)} roles: {', '.join(roles)}"
            })
    return violations

def check_orphaned_roles(users_dict, roles_data):
    """Extra Rule: Roles assigned to non-existent users"""
    violations = []
    valid_users = set(users_dict.keys())
    for entry in roles_data:
        if entry['user_id'] not in valid_users:
            violations.append({
                'user_id': entry['user_id'],
                'username': 'UNKNOWN',
                'violation_type': 'orphaned_role',
                'severity': 'HIGH',
                'details': f"Role {entry['role']} assigned to non-existent user"
            })
    return violations

# =========================
# REPORTING
# =========================
def generate_json_report(all_violations, users_dict, roles_data):
    """Generate machine-readable JSON audit report"""
    violations_by_user = {}
    for v in all_violations:
        uid = v['user_id']
        violations_by_user.setdefault(uid, []).append(v)

    report = {
        'audit_metadata': {
            'timestamp': datetime.now().isoformat(),
            'total_users_audited': len(users_dict),
            'total_role_assignments': len(roles_data),
            'total_violations': len(all_violations),
            'auditor': 'Automated IAM Audit System v1.0'
        },
        'violation_summary': {
            'by_severity': {
                'CRITICAL': len([v for v in all_violations if v['severity'] == 'CRITICAL']),
                'HIGH': len([v for v in all_violations if v['severity'] == 'HIGH']),
                'MEDIUM': len([v for v in all_violations if v['severity'] == 'MEDIUM']),
                'LOW': len([v for v in all_violations if v['severity'] == 'LOW'])
            },
            'by_type': {}
        },
        'violations_by_user': violations_by_user,
        'all_violations': all_violations
    }

    for v in all_violations:
        t = v['violation_type']
        report['violation_summary']['by_type'][t] = report['violation_summary']['by_type'].get(t,0) + 1

    return report

def generate_text_report(all_violations, users_dict, roles_data):
    """Generate human-readable text audit report"""
    lines = []
    lines.append("="*80)
    lines.append("USER ACCOUNT & PERMISSIONS AUDIT REPORT")
    lines.append("="*80)
    lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("Auditor: Automated IAM Audit System v1.0\n")

    lines.append("EXECUTIVE SUMMARY")
    lines.append("-"*80)
    lines.append(f"Total Users Audited: {len(users_dict)}")
    lines.append(f"Total Role Assignments: {len(roles_data)}")
    lines.append(f"Total Violations Found: {len(all_violations)}\n")

    # Severity
    sev_counts = {}
    for v in all_violations:
        sev_counts[v['severity']] = sev_counts.get(v['severity'],0)+1
    lines.append("VIOLATIONS BY SEVERITY")
    lines.append("-"*80)
    for sev in ['CRITICAL','HIGH','MEDIUM','LOW']:
        count = sev_counts.get(sev,0)
        lines.append(f"{sev:12s} [{count:3d}] {'█'*count}")
    lines.append("")

    # Type
    type_counts = {}
    for v in all_violations:
        type_counts[v['violation_type']] = type_counts.get(v['violation_type'],0)+1
    lines.append("VIOLATIONS BY TYPE")
    lines.append("-"*80)
    for t,c in sorted(type_counts.items(), key=lambda x:-x[1]):
        lines.append(f"{t:30s} {c:3d}")
    lines.append("")

    # Detailed
    lines.append("DETAILED VIOLATIONS")
    lines.append("="*80)
    for sev in ['CRITICAL','HIGH','MEDIUM','LOW']:
        sv = [v for v in all_violations if v['severity']==sev]
        if sv:
            lines.append(f"\n{sev} ({len(sv)} issues)")
            lines.append("-"*80)
            for i,v in enumerate(sv,1):
                lines.append(f"{i}. {v['username']} ({v['user_id']})")
                lines.append(f"   Type: {v['violation_type']}")
                lines.append(f"   Details: {v['details']}")
    lines.append("\n"+"="*80)
    lines.append("END OF REPORT")
    lines.append("="*80)
    return "\n".join(lines)

# =========================
# MAIN FUNCTION
# =========================
def main():
    # Load data
    users_data = load_json('users.json')
    roles_data = load_json('roles.json')

    # Build lookup
    users_dict = build_user_lookup(users_data)

    # Run violation checks
    all_violations = []
    all_violations.extend(check_disabled_with_roles(users_dict, roles_data))
    all_violations.extend(check_unauthorized_admins(users_dict, roles_data))
    all_violations.extend(check_stale_accounts(users_dict))
    all_violations.extend(check_excessive_roles(users_dict, roles_data))
    all_violations.extend(check_orphaned_roles(users_dict, roles_data))

    # Generate reports
    json_report = generate_json_report(all_violations, users_dict, roles_data)
    text_report = generate_text_report(all_violations, users_dict, roles_data)

    # Save reports with UTF-8 encoding (fixes Windows Unicode errors)
    with open('audit_report.json', 'w', encoding='utf-8') as f:
        json.dump(json_report, f, indent=2)

    with open('audit_report.txt', 'w', encoding='utf-8') as f:
        f.write(text_report)

    # Console output
    print(f"Audit complete! Found {len(all_violations)} violations.")
    print("Reports saved: audit_report.json, audit_report.txt")


if __name__ == '__main__':
    main()