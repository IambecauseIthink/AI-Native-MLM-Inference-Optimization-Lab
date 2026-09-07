"""Build offline inline fragments from the Python source of truth. --check is read-only."""
import argparse
import json
from pathlib import Path
from lessons import SPECS, cases, run

ROOT = Path(__file__).resolve().parents[1]

def render(lesson_id):
    spec = SPECS[lesson_id]
    bundle = {'spec':spec, 'records':[run(lesson_id,p) for p in cases(lesson_id)]}
    payload = json.dumps(bundle, ensure_ascii=False, separators=(',',':'), allow_nan=False).replace('<','\\u003c')
    template = (ROOT/'courses/visuals/lesson-template.html').read_text()
    return template.replace('__ID__',lesson_id).replace('__TITLE__',spec['title']).replace('__KIND__',spec['kind']).replace('__PAYLOAD__',payload)

def main():
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('--check',action='store_true'); a=p.parse_args()
    for lesson_id in SPECS:
        dest=ROOT/f'courses/visuals/lesson-{lesson_id}.html'; html=render(lesson_id)
        if len(html.encode())>=1_000_000:raise SystemExit(f'{dest.name} exceeds inline size budget')
        if a.check:
            if not dest.exists() or dest.read_text()!=html:raise SystemExit(f'Stale visual: {dest.name}')
        else:dest.write_text(html)
    print('Six visuals match Python presets.' if a.check else 'Built six offline lesson fragments.')

if __name__=='__main__':main()
