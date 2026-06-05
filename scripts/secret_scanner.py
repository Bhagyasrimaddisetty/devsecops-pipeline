import os
import re
import sys

# Patterns that indicate hardcoded secrets
PATTERNS = [
    (r'(?i)(password|passwd|pwd)\s*=\s*["\'][^"\']{4,}["\']', "Hardcoded password"),
    (r'(?i)(api_key|apikey|api-key)\s*=\s*["\'][^"\']{8,}["\']', "Hardcoded API key"),
    (r'(?i)(secret|token)\s*=\s*["\'][^"\']{8,}["\']', "Hardcoded secret/token"),
    (r'AKIA[0-9A-Z]{16}', "AWS Access Key ID"),
    (r'(?i)aws_secret_access_key\s*=\s*["\'][^"\']{20,}["\']', "AWS Secret Key"),
    (r'-----BEGIN (RSA|EC|OPENSSH) PRIVATE KEY-----', "Private key"),
]

SKIP_DIRS  = {'.git', '__pycache__', 'node_modules', '.github'}
SKIP_FILES = {'secret_scanner.py'}

def scan_file(filepath):
    findings = []
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for line_num, line in enumerate(f, 1):
                for pattern, label in PATTERNS:
                    if re.search(pattern, line):
                        findings.append({
                            "file": filepath,
                            "line": line_num,
                            "issue": label,
                            "content": line.strip()[:80]
                        })
    except Exception:
        pass
    return findings

def scan_directory(root="."):
    all_findings = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for filename in filenames:
            if filename in SKIP_FILES:
                continue
            if filename.endswith(('.py', '.yml', '.yaml', '.env', '.json', '.sh', '.tf')):
                filepath = os.path.join(dirpath, filename)
                all_findings.extend(scan_file(filepath))
    return all_findings

if __name__ == "__main__":
    print("Running secret scanner...")
    findings = scan_directory(".")
    if findings:
        print(f"\n❌ FAILED — {len(findings)} secret(s) detected:\n")
        for f in findings:
            print(f"  [{f['issue']}] {f['file']}:{f['line']}")
            print(f"  → {f['content']}\n")
        sys.exit(1)
    else:
        print("✅ PASSED — No secrets detected.")
        sys.exit(0)
