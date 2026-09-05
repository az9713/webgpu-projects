
// ponytail: one click-to-sort handler, no library. Column 2 sorts as text, the rest as numbers.
document.querySelectorAll('#ranktable th').forEach(function(th,i){
  th.addEventListener('click',function(){
    var tb=th.closest('table').tBodies[0], rows=[].slice.call(tb.rows);
    // numeric columns start descending, the name column starts ascending
    var first=th.dataset.asc===undefined;
    var asc=first?(i===1):(th.dataset.asc!=='1'); th.dataset.asc=asc?'1':'0';
    rows.sort(function(a,b){
      var x=a.cells[i].textContent, y=b.cells[i].textContent;
      var r=(i===1)?x.localeCompare(y):(parseFloat(x)-parseFloat(y));
      return asc?r:-r;
    });
    rows.forEach(function(r){tb.appendChild(r)});
  });
});
