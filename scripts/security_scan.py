"""Minimal demonstration secret scan; NOT a replacement for enterprise scanning."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
FILES = [*sorted((ROOT / 'site').rglob('*')), *sorted((ROOT / '.github' / 'workflows').rglob('*.yml'))]
PATTERNS = [
    re.compile(r'AKIA[0-9A-Z]{16}'),
    re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
    re.compile(r'ghp_[A-Za-z0-9]{36}'),
    re.compile(r'(?i)\b(?:password|api[_-]?key|secret)\s*[:=]\s*[\'\"][^\'\"]{6,}[\'\"]'),
]


def scan_file(path):
    content = path.read_text(encoding='utf-8')
    return [p.pattern for p in PATTERNS if p.search(content)]


def main():
    problems = []
    for file in FILES:
        if file.is_file():
            for pattern in scan_file(file):
                problems.append(f'{file.relative_to(ROOT)} matched {pattern}')
    if problems:
        print('Potential committed secret(s) detected:')
        print('\n'.join(problems))
        return 1
    print(f'PASS: No potential secrets detected in {sum(f.is_file() for f in FILES)} scanned files.')
    print('Note: lightweight demonstration scan; production teams should use a dedicated scanner.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
