import re

S={
1:[3,4,4,3,2,2,5],2:[4,4,3,4,3,3,4],3:[5,4,5,4,3,3,4],4:[5,3,2,2,1,1,4],5:[5,4,3,3,2,2,5],6:[3,4,5,2,2,2,3],7:[3,4,1,2,1,1,2],
8:[5,4,5,4,3,3,5],9:[5,4,3,4,3,3,5],10:[5,3,2,3,2,2,4],11:[4,5,4,4,2,2,4],12:[4,4,4,2,2,2,3],13:[4,3,1,2,1,1,3],14:[4,4,4,3,1,1,2],
15:[5,4,5,4,3,3,5],16:[5,5,5,4,3,2,5],17:[5,3,3,2,1,1,5],18:[5,4,3,2,2,2,4],19:[5,3,3,3,2,2,4],20:[5,3,3,3,2,2,4],21:[4,3,1,2,1,1,2],
22:[5,4,5,2,1,2,5],23:[5,2,3,3,2,3,4],24:[5,2,3,3,2,2,4],25:[5,2,3,2,2,2,4],26:[5,2,1,2,1,2,3],27:[4,2,2,2,1,2,3],28:[3,4,4,2,2,2,2],
29:[5,5,5,5,5,4,5],30:[5,5,4,4,5,4,5],31:[4,5,5,3,4,3,4],32:[4,5,2,3,2,2,4],33:[3,4,3,4,3,2,3],34:[2,4,4,5,3,3,3],35:[4,4,2,2,1,1,3],
36:[5,5,3,3,2,1,5],37:[3,5,3,4,4,4,4],38:[3,4,4,4,4,4,4],39:[3,4,4,5,4,4,3],40:[5,4,3,4,3,3,4],41:[3,5,3,2,1,1,3],42:[2,4,3,5,5,5,3],
43:[5,5,5,5,5,4,5],44:[3,5,3,4,4,3,4],45:[5,4,3,4,4,4,4],46:[4,5,3,3,2,2,4],47:[4,4,5,4,5,4,4],48:[3,5,4,3,3,3,4],
49:[5,5,5,4,5,4,5],50:[4,5,4,4,5,5,5],51:[4,4,4,4,5,4,4],52:[3,4,3,4,5,4,3],53:[2,4,2,2,4,3,2],54:[2,4,3,5,5,5,3],
55:[3,5,5,5,4,5,4],56:[5,4,3,3,3,3,4],57:[4,5,3,3,2,2,3],58:[2,5,3,4,3,3,3],59:[3,4,3,4,4,4,3],60:[3,4,3,2,1,1,2],61:[2,4,4,4,3,5,2],
62:[3,4,3,3,3,2,5],63:[5,4,4,4,3,3,5],64:[3,4,3,4,3,3,5],65:[3,4,3,3,4,4,5],66:[3,4,3,4,3,3,4],67:[4,4,5,2,3,3,3],68:[4,4,2,2,3,3,3],
69:[5,4,2,3,1,1,4],70:[4,5,4,4,2,2,5],71:[4,3,2,3,2,2,5],72:[5,4,3,4,3,3,4],73:[5,4,2,3,1,1,4],74:[4,4,2,3,1,1,3],75:[3,4,3,4,2,3,4],
76:[5,5,5,4,3,3,5],77:[5,5,3,4,2,2,5],78:[5,4,5,3,3,3,5],79:[3,4,3,3,4,3,5],80:[4,4,3,3,3,2,4],81:[5,5,4,3,2,2,5],82:[4,4,2,3,2,2,3],
83:[5,4,3,3,2,2,5],84:[3,5,5,4,2,2,4],85:[5,4,5,4,3,3,4],86:[4,4,3,3,3,3,3],87:[3,4,2,2,1,1,3],88:[3,5,3,3,2,3,3],
89:[4,4,5,5,3,3,5],90:[4,5,4,3,1,2,4],91:[4,5,3,4,2,1,4],92:[2,4,3,4,3,4,4],93:[2,3,2,4,2,3,4],94:[4,3,4,4,2,2,3],95:[3,4,3,4,2,3,3],
96:[5,5,3,4,4,4,5],97:[5,4,2,2,2,1,4],98:[5,4,5,4,3,3,4],99:[3,4,3,3,2,3,3],100:[5,3,2,3,4,3,4],101:[5,4,2,2,1,1,3],
102:[4,4,2,5,1,1,5],103:[3,4,4,3,1,2,5],104:[4,5,3,3,1,1,4],105:[3,4,3,3,2,2,3],106:[3,4,1,4,1,1,4],107:[4,5,2,2,1,1,4],108:[3,3,4,4,1,2,3],
109:[3,5,4,2,2,3,5],110:[3,4,5,4,3,4,4],111:[4,5,4,2,1,1,5],112:[4,5,3,3,2,2,5],113:[4,4,4,2,1,2,4],114:[2,3,2,1,1,1,4],
115:[5,3,5,4,2,2,5],116:[5,2,3,3,2,2,5],117:[5,3,3,2,1,1,5],118:[5,3,3,3,2,2,4],119:[5,4,4,3,2,2,4],120:[5,3,3,3,2,2,4],121:[4,4,5,3,2,3,3],
}
assert len(S)==121, len(S)

def total(v):
    d1,d2,d3,d4,d5,d6,d7=v
    raw=3*d1+3*d2+2*d3+1*d4+2*(6-d5)+2*(6-d6)+2*d7
    return raw, round(raw/75*100)

src=open('webgpu-kernel-projects.html',encoding='utf-8').read()

css_add = """
  .sc{margin:6px 0 4px; font-size:.78rem; color:var(--muted); letter-spacing:.02em}
  .sc b{color:var(--accent2); font-weight:600}
  .sc .tot{color:var(--accent); font-weight:700}
  .sc span{display:inline-block; margin-right:10px; white-space:nowrap}
  table.rank{width:100%; border-collapse:collapse; font-size:.82rem; margin:0 0 4px}
  table.rank th,table.rank td{border-bottom:1px solid var(--border2); padding:6px 7px; text-align:right}
  table.rank th:nth-child(2),table.rank td:nth-child(2){text-align:left}
  table.rank th{color:var(--accent); font-weight:600; position:sticky; top:44px;
                background:var(--card); cursor:pointer; user-select:none; white-space:nowrap}
  table.rank th:hover{color:var(--accent2)}
  table.rank tbody tr:hover{background:var(--bg)}
  table.rank td.t{color:var(--accent); font-weight:700}
  table.rank td a{text-decoration:none}
  .rwrap{overflow-x:auto; border:1px solid var(--border2); border-radius:8px;
         padding:0 14px 10px; background:var(--card); margin-bottom:24px}
"""
src=src.replace("  @media(max-width:620px){ .toc ol{columns:1} }", css_add+"  @media(max-width:620px){ .toc ol{columns:1} }")

src=src.replace('<a href="#cost">Cost</a>','<a href="#scores">Scores</a>\n    <a href="#cost">Cost</a>')

projs=list(re.finditer(r'<div class="proj">(.*?)</div>',src,re.S))
cats=[(m.start(),m.group(1)) for m in re.finditer(r'<h2 id="c(\d+)"',src)]
rows=[];out=[];last=0;i=0
for m in projs:
    i+=1
    v=S[i]; raw,pct=total(v)
    cat=[c for c in cats if c[0]<m.start()][-1][1]
    title=re.search(r'<h3>(.*?)</h3>',m.group(1),re.S).group(1)
    tclean=re.sub(r'<[^>]*>','',title).strip()
    badge=('<p class="sc"><span>visual <b>%d</b></span><span>explain <b>%d</b></span>'
           '<span>surprise <b>%d</b></span><span>kernel <b>%d</b></span>'
           '<span>cost <b>%d</b></span><span>risk <b>%d</b></span>'
           '<span>standalone <b>%d</b></span><span class="tot">total %d/100</span></p>'
           )%(v[0],v[1],v[2],v[3],v[4],v[5],v[6],pct)
    body=m.group(1)
    body=body.replace('<h3>','<h3 id="p%d">'%i,1)
    body=body.rstrip()+'\n'+badge+'\n'
    out.append(src[last:m.start()]); out.append('<div class="proj">'+body+'</div>')
    last=m.end()
    rows.append((i,cat,tclean,v,pct))
out.append(src[last:])
src=''.join(out)

tr=[]
for i,cat,t,v,pct in sorted(rows,key=lambda r:(-r[4],r[0])):
    tr.append('<tr><td>%d</td><td><a href="#p%d">%s</a></td><td>%d</td><td>%d</td><td>%d</td><td>%d</td><td>%d</td><td>%d</td><td>%d</td><td class="t">%d</td></tr>'
              %(int(cat),i,t,v[0],v[1],v[2],v[3],v[4],v[5],v[6],pct))
table='\n'.join(tr)

sec = """
<hr>

<h2 id="scores"><span class="cat">Ranking</span>All 121, scored on seven axes</h2>

<p>Every project above now carries a score line. This section says what the seven numbers mean, how the total is weighted, and lists all 121 in one sortable table. The scores are one reader's judgement applied consistently across the whole list. They are not a measurement. Nothing here is built, so no score is confirmed by a running page.</p>

<h3>The seven axes</h3>

<p>Each axis runs from 1 to 5. Each is scored on its own. <strong>Two axes are inverted</strong>, which means a low number is the good one: cost and risk.</p>

<div class="card">
  <span class="label">Axis definitions</span>
  <p><strong>Visual</strong> &mdash; how much the screen shows. 1 is a number or a table. 3 is a static plot. 5 is a live picture you can drag, where the picture <em>is</em> the mathematics.</p>
  <p><strong>Explain</strong> &mdash; what a reader understands afterwards that they did not before. 1 is a feature demonstration. 3 makes a known idea concrete. 5 corrects a common wrong belief.</p>
  <p><strong>Surprise</strong> &mdash; how unexpected the result is to a reader who knows the field. 1 is the expected answer. 3 is a known effect, rarely seen. 5 makes an expert check it again.</p>
  <p><strong>Kernel</strong> &mdash; how hard the project pushes the 207-kernel set. 1 is one kernel plus plumbing. 3 is a chain of four to eight kernels, all on the GPU. 5 hits a documented limit: a <code>com.microsoft</code> packing rule, the missing sort, the missing inverse, or <code>subgroup-matrix: false</code>.</p>
  <p><strong>Cost</strong> <em>(inverted &mdash; low is good)</em> &mdash; build effort. 1 is Tier A, pure kernels, a few hours. 3 is Tier B, which needs input data or a Transformers.js hybrid. 5 is Tier C, which needs real weights or <code>com.microsoft</code> packing.</p>
  <p><strong>Risk</strong> <em>(inverted &mdash; low is good)</em> &mdash; the chance that it does not work, or that it works and is dull. 1 means every dependency is confirmed on this laptop. 3 means one unmeasured assumption. 5 means it depends on something this document lists as absent or unproven.</p>
  <p><strong>Standalone</strong> &mdash; does it hold up outside this catalogue. 1 makes sense only beside its neighbours. 3 is a good page on its own. 5 is a page a stranger would keep, or use for real work.</p>
</div>

<h3>The weighted total</h3>

<p>The two inverted axes are turned around before weighting, so every term rewards a higher number. Cheapness is <code>6 &minus; cost</code>. Safety is <code>6 &minus; risk</code>.</p>

<pre><code>raw = 3&times;visual + 3&times;explain + 2&times;surprise + 1&times;kernel
    + 2&times;(6 &minus; cost) + 2&times;(6 &minus; risk) + 2&times;standalone

total = raw / 75 &times; 100          raw runs from 15 to 75</code></pre>

<p>The weights say what this document is for. It is a set of pages that must <em>show</em> something and <em>teach</em> something, so visual and explain carry three each. Surprise, cheapness, safety and standalone value carry two each. Kernel exercise carries one, because stressing the library interests the builder and stays invisible to the reader.</p>

<p class="note"><strong>Read the total as a build order, not as a quality score.</strong> It rewards cheap and safe work, so a hard project of real importance sits below an easy attractive one. Sort by a single column when that is what you want. The full decoder layer scores 65 and is still the correct headline build.</p>

<h3>The table</h3>

<p>Click a column heading to sort by that column. Click it again to reverse the order. The project name links to its entry above. <strong>Cat</strong> is the category number.</p>

<div class="rwrap">
<table class="rank" id="ranktable">
<thead><tr><th>Cat</th><th>Project</th><th>Visual</th><th>Explain</th><th>Surprise</th><th>Kernel</th><th>Cost</th><th>Risk</th><th>Stand</th><th>Total</th></tr></thead>
<tbody>
__ROWS__
</tbody>
</table>
</div>

<script>
// ponytail: one click-to-sort handler, no library. Column 2 sorts as text, the rest as numbers.
document.querySelectorAll('#ranktable th').forEach(function(th,i){
  th.addEventListener('click',function(){
    var tb=th.closest('table').tBodies[0], rows=[].slice.call(tb.rows);
    var asc=th.dataset.asc!=='1'; th.dataset.asc=asc?'1':'0';
    rows.sort(function(a,b){
      var x=a.cells[i].textContent, y=b.cells[i].textContent;
      var r=(i===1)?x.localeCompare(y):(parseFloat(x)-parseFloat(y));
      return asc?r:-r;
    });
    rows.forEach(function(r){tb.appendChild(r)});
  });
});
</script>

<h3>What the scores say</h3>

<p><strong>The cheap and safe top.</strong> A sort by total puts one kind of page at the head: a large live picture, every dependency confirmed, an afternoon of work. Life at sixteen million cells, the reaction-diffusion grid, the untrained painting network and the quantisation error microscope all sit there. Build from the top of this list when you want finished pages quickly.</p>

<p><strong>The expensive and important tail.</strong> Sort by explain instead, then read upward through the low totals. You find the opposite group: the quantised expert mixture, the fused quantised blocks of a real model, and the state-space block. Each scores 4 or 5 for explain and 5 for both cost and risk. The total punishes these projects and the field cares about them. Do not read a low total as permission to skip one.</p>

<p><strong>The two columns that disagree most.</strong> Visual and explain part company at both ends. The Mandelbrot zoom scores 5 for visual and 2 for explain. The streaming-state proof scores 2 for visual and 5 for explain. Neither is the worse project. They are different projects, and one total cannot say so. That is why the seven numbers stay on the page beside each entry.</p>
"""
sec=sec.replace('__ROWS__',table)
src=src.replace('<h2 id="cost">', sec+'\n<hr>\n\n<h2 id="cost">',1)

src=src.replace('ranked inside each category by visualization, significance and surprise.',
 'ranked inside each category by visualization, significance and surprise, and scored on <a href="#scores">seven independent axes</a> with a weighted total.')

open('webgpu-kernel-projects.html','w',encoding='utf-8').write(src)
top=sorted(rows,key=lambda r:(-r[4],r[0]))
print('rows',len(rows))
print('TOP5',[(r[0],r[2][:30],r[4]) for r in top[:5]])
print('BOT5',[(r[0],r[2][:30],r[4]) for r in top[-5:]])
