"""Wrap an existing lesson fragment for optional offline browser preview; never run a model."""
import argparse
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CSS='''
:root {color-scheme:light dark;--foreground:light-dark(#20252b,#f0f2f5);--background:light-dark(#fff,#171a20);--border:light-dark(#d2d8df,#505763);--viz-series-1:light-dark(#315bbb,#8aaeff);--viz-series-2:light-dark(#be681b,#ecad65);--viz-series-3:light-dark(#288765,#72cdb1);--viz-series-4:light-dark(#9d52a9,#d995e4);}
body {font:16px/1.5 system-ui,sans-serif;background:var(--background);color:var(--foreground);margin:16px auto;padding:0 16px;max-width:736px;box-sizing:border-box;}
h3 {font-size:1.15em;font-weight:500;} .viz-controls {display:flex;flex-wrap:wrap;gap:12px;} .form-label{display:flex;flex-direction:column;flex:1 1 200px;} .form-select{font:inherit;padding:6px;max-width:100%;} .table{border-collapse:collapse;width:100%;} th,td{padding:6px;text-align:left;border-bottom:1px solid var(--border);} .text-end{text-align:right;} .text-small{font-size:12px;} .tabular-nums{font-variant-numeric:tabular-nums;} details{margin-block:12px;} p{overflow-wrap:anywhere;} .table-responsive{max-width:100%;overflow-x:auto;}
'''

def document(lesson_id):
    fragment=(ROOT/f'courses/visuals/lesson-{lesson_id}.html').read_text()
    return '<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Lesson '+lesson_id+'</title><style>'+CSS+'</style></head><body>'+fragment+'</body></html>'

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--id',required=True,choices=['01','02','03','04','05','06']);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    with a.output.open('x') as f:f.write(document(a.id))
    print(a.output)

if __name__=='__main__':main()
