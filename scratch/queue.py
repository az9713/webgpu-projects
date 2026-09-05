# Reads the score table in scores.py, writes queue.tsv at the repo root.
# Routing only, no state: a page counts as built when its number appears in
# projects/index.html. Safe to re-run -- it only ever writes queue.tsv.
# (scores.py itself is NOT re-runnable; a second run duplicates its injections.)
import re

S = eval(re.search(r'S=(\{.*?\n\})',
                   open('scratch/scores.py', encoding='utf-8').read(), re.S).group(1))
html = open('webgpu-kernel-projects.html', encoding='utf-8').read()
T = {int(m.group(1)): re.sub('<[^>]+>', '', m.group(2)).replace('&middot;', '-').strip()
     for m in re.finditer(r'<h3 id="p(\d+)">(.*?)</h3>', html, re.S)}
built = {16, 22, 36, 81, 111, 76, 77, 70, 90, 115}          # the ten already shipped


def score(v):                                                # same weights as scores.py
    d1, d2, d3, d4, d5, d6, d7 = v
    return round((3*d1 + 3*d2 + 2*d3 + d4 + 2*(6-d5) + 2*(6-d6) + 2*d7) / 75 * 100)


rows = []
for n, v in S.items():
    if n in built:
        continue
    cr = v[4] + v[5]                                         # cost + risk, both 1..5
    m, e = ('sonnet', 'xhigh') if cr <= 5 else ('opus', 'xhigh') if cr <= 7 else ('opus', 'max')
    rows.append((n, T[n], v[4], v[5], score(v), m, e))
rows.sort(key=lambda r: (-r[4], r[0]))                       # best score first

open('queue.tsv', 'w', encoding='utf-8').write(
    'num\ttitle\tcost\trisk\tscore\tmodel\teffort\n' +
    '\n'.join('%d\t%s\t%d\t%d\t%d\t%s\t%s' % r for r in rows) + '\n')

assert len(rows) == 111, len(rows)
assert len(T) == 121, len(T)
from collections import Counter
print(len(rows), 'rows', Counter((r[5], r[6]) for r in rows))
