"""Check repository-relative Markdown file targets; does not fetch remote URLs."""
import re
from pathlib import Path
from urllib.parse import unquote

root = Path(__file__).resolve().parents[1]
errors = []
for path in root.rglob('*.md'):
    if '.git' in path.parts or 'local' in path.parts:
        continue
    for target in re.findall(r'\]\(([^)]+)\)', path.read_text()):
        target = target.strip('<>').split('#')[0]
        if not target or re.match(r'^[a-z]+:', target):
            continue
        if not (path.parent / unquote(target)).exists():
            errors.append(f'{path.relative_to(root)}: {target}')
if errors:
    raise SystemExit('\n'.join(errors))
print('All local Markdown file links resolve (anchors and web URLs not checked).')
