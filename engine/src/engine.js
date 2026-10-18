/* Präsentations-Engine: Folien, Schritte, Notizen, Referentenfenster, Glossar, Quellenlinks, Layoutprüfung.
   Beschreibung: ../ANLEITUNG.md */
(function(){
  const stage=document.getElementById('stage');
  const vp=document.getElementById('viewport');
  const slides=[...stage.querySelectorAll(':scope > section.slide')];
  const N=slides.length;
  let cur=0, step=0, popup=null, t0=null, nfs=19;
  const orderFr=l=>l.map((el,i)=>({el,k:el.dataset.o!=null?+el.dataset.o:i})).sort((a,b)=>a.k-b.k).map(o=>o.el);
  try{ nfs=+localStorage.getItem('praes-nfs')||19; }catch(e){}

  /* ---- Vorbereitung jeder Folie ---- */
  let chap='';
  slides.forEach((s,i)=>{
    if(s.dataset.chap) chap=s.dataset.chap;
    s.dataset.c=chap;
    // Schritte sammeln
    const fr=orderFr([...s.querySelectorAll('.f,.fs')]);
    const groups=[];
    fr.forEach(el=>{ if(el.classList.contains('fw')&&groups.length) groups[groups.length-1].push(el); else groups.push([el]); });
    s._steps=groups;
    // Fußzeile
    const cite=s.querySelector(':scope > cite.src, :scope cite.src');
    const ft=document.createElement('footer');
    const nolbl=cite&&cite.classList.contains('nolabel');
    ft.innerHTML='<span class="chap">'+(s.classList.contains('s-title')?'':chap)+'</span><span class="src'+(nolbl?' nolabel':'')+'">'+(cite?cite.innerHTML:'')+'</span><span class="pg">'+(i+1)+' / '+N+'</span>';
    if(!cite) ft.querySelector('.src').style.visibility='hidden';
    if(cite) cite.remove();
    if(!s.classList.contains('s-title')) s.appendChild(ft);
    // Pointe-Banner auf der Folie
    if(s.dataset.pointe){ const pb=document.createElement('div'); pb.className='pointe'; pb.innerHTML='<b>Pointe</b><span></span>'; pb.querySelector('span').textContent=s.dataset.pointe; s.appendChild(pb); }
    // Stagger-Kinder
    s.querySelectorAll('.stagger').forEach(g=>[...g.children].forEach((c,k)=>c.style.setProperty('--i',k)));
    s.querySelectorAll('[data-d]').forEach(el=>el.style.setProperty('--d',el.dataset.d));
  });
  // Linienlängen für Zeichen-Animation
  function measure(){
    stage.querySelectorAll('.draw').forEach(p=>{ try{ const L=Math.ceil(p.getTotalLength())+4; p.style.setProperty('--len',L);}catch(e){} });
  }

  /* ---- Skalierung ---- */
  function fit(){
    const w=vp.clientWidth,h=vp.clientHeight,sc=Math.min(w/1920,h/1080);
    stage.style.transform='translate('+(-960*sc)+'px,'+(-540*sc)+'px) scale('+sc+')';
  }
  window.addEventListener('resize',fit);
  new ResizeObserver(fit).observe(vp);

  /* ---- Anzeige ---- */
  function title(s){ return s.dataset.title || (s.querySelector('h2,h1')||{}).textContent || ''; }
  function apply(){
    slides.forEach((s,i)=>{ s.classList.toggle('cur',i===cur); s.classList.toggle('past',i<cur); });
    const s=slides[cur];
    s._steps.forEach((g,k)=>g.forEach(el=>{ el.classList.toggle('vis',k<step); el.classList.toggle('last',k===step-1); }));
    for(let k=1;k<=Math.max(12,s._steps.length);k++) s.classList.toggle('st-'+k,k<=step);
    s.dataset.step=step;
    document.getElementById('progress').style.width=((cur+ (s._steps.length? step/(s._steps.length+1):0))/(N-1)*100)+'%';
    try{ history.replaceState(null,'','#'+(cur+1)); }catch(e){}
    runCounts(s); renderNotes(); syncPopup(); navBtns(); if(typeof vinSync==='function') vinSync(); if(typeof zs!=='undefined'&&zs.on) zCanvas(slides[cur]);
    // Aufgeklappte Bilder (Lupe), Glossar-Ebene, Video-Inhalt und laufende Videos schließen sich beim Weiterklicken von selbst
    ['glx','vinlay'].forEach(id=>{ const o=document.getElementById(id); if(o) o.classList.remove('on'); }); vidClose();
    document.dispatchEvent(new CustomEvent('qp-folie',{detail:{cur,step,nr:+(s.dataset.nr||cur+1)}}));   // für Live-Modul u. a.
  }
  /* Presenter/Tastatur: die Steuerleiste ist dann meist ausgeblendet – kurz nur die Weiter-Schaltfläche mit den Teilschritten zeigen */
  let peekT=null;
  function peek(){ if(document.body.classList.contains('maus')) return; document.body.classList.add('peek'); clearTimeout(peekT); peekT=setTimeout(()=>document.body.classList.remove('peek'),1600); }
  let lock=false;                                               // Teilnehmer-Modus: Navigation gesperrt, solange sie der Referentenfolie folgen
  /* Weiter/Zurück zeigen, was der nächste Klick bewirkt. Pfeile als SVG.
     Hat die Folie Teilschritte, ist die Weiter-Schaltfläche in n Felder geteilt und füllt sich Schritt für Schritt. */
  const SV=d=>'<svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><path d="'+d+'"/></svg>';
  const IC={next:SV('M3.5 12h16M13 5.5l6.5 6.5-6.5 6.5'), back:SV('M20.5 12h-16M11 5.5L4.5 12l6.5 6.5'),
    whole:SV('M12.5 5.5L6 12l6.5 6.5M19.5 5.5L13 12l6.5 6.5'), stepF:SV('M9 5.5l6.5 6.5L9 18.5'), stepB:SV('M15 5.5L8.5 12l6.5 6.5'),
    end:'<svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><rect x="6" y="6" width="12" height="12" rx="2"/></svg>'};
  function btnState(){
    const s=slides[cur], n=s._steps.length;
    const fw=step<n?{k:'plus',n:n,h:'<span class="lb">Teil '+(step+1)+' von '+n+'</span>'+IC.stepF,t:'Nächster Klick: weiterer Inhalt auf dieser Folie ('+(step+1)+' von '+n+')'}
      :cur<N-1?{k:'next',h:'<span class="lb">Folie '+(cur+2)+'</span>'+IC.next,t:'Nächster Klick: nächste Folie ('+(cur+2)+'. '+title(slides[cur+1])+')'}
      :{k:'end',h:IC.end+'<span class="lb">Ende</span>',t:'Letzte Folie'};
    const bw=step>0?{k:'minus',h:IC.stepB,t:'Zurück: Inhalt ausblenden (Schritt '+step+' von '+n+')'}
      :cur>0?{k:'back',h:IC.back,t:'Zurück: vorige Folie'}:{k:'end',h:IC.back,t:'Erste Folie'};
    // Zusätzlich „ganze Folie zurück“, solange ein Teilschritt zurückgenommen werden kann
    const bs=step>0&&cur>0?{k:'back',h:IC.whole,t:'Ganze Folie zurück ('+cur+'. '+title(slides[cur-1])+')'}:null;
    return {fw,bw,bs};
  }
  function setBtn(b,o){
    if(!b) return; if(!o){ b.style.display='none'; return; } b.style.display=''; b.title=o.t; b.setAttribute('aria-label',o.t);
    if(o.k==='plus'){
      const pct=(step/o.n*100)+'%';
      // gleiche Folie, gleiche Teilung: nur Füllstand ändern, damit er weich nachläuft
      if(b.className==='nb-plus'&&b.dataset.n==String(o.n)&&b._sl===cur){ b.querySelector('.fl').style.width=pct; b.querySelector('.ct').innerHTML=o.h; return; }
      let t=''; for(let k=1;k<o.n;k++) t+='<i class="tk" style="left:'+(k/o.n*100)+'%"></i>';
      b.className='nb-plus'; b.dataset.n=o.n; b._sl=cur;
      b.innerHTML='<span class="sg"><i class="fl" style="width:'+pct+'"></i>'+t+'</span><span class="ct">'+o.h+'</span>';
      return;
    }
    b.className='nb-'+o.k; b.dataset.n=''; b.innerHTML='<span class="ct">'+o.h+'</span>';
  }
  /* Lokale Videokopien (Ordner video_lokal/ nur auf dem Vortragsrechner, nicht im Webpaket):
     Schaltfläche erscheint nur, wenn die Datei abspielbar ist; Wiedergabe in einer Ebene über der Folie. */
  // nur bei lokal geöffneter Datei suchen – online gibt es den Ordner nicht (vermeidet 404-Anfragen)
  if(location.protocol==='file:') document.querySelectorAll('[data-lokal]').forEach(a=>{
    const v=document.createElement('video'); v.preload='metadata'; v.muted=true;
    v.addEventListener('loadedmetadata',()=>{ a.hidden=false; },{once:true}); v.src=a.dataset.lokal;
    a.addEventListener('click',ev=>{ ev.preventDefault(); ev.stopPropagation(); vidOpen(a.dataset.lokal); });
  });
  function vidOpen(src){
    let o=document.getElementById('vidlay');
    if(!o){ o=document.createElement('div'); o.id='vidlay'; o.innerHTML='<button class="vx" title="schließen (Esc)">✕</button><video controls playsinline></video>'; document.body.appendChild(o);
      o.addEventListener('click',ev=>{ if(ev.target===o||ev.target.closest('.vx')) vidClose(); }); }
    const v=o.querySelector('video'); v.src=src; o.classList.add('on'); v.play().catch(()=>{});
  }
  function vidClose(){ const o=document.getElementById('vidlay'); if(!o) return; const v=o.querySelector('video'); v.pause(); o.classList.remove('on'); }
  /* Video-Inhalte zum Nachlesen (src/video_inhalte.json): Knopf unten links, wenn die aktuelle Folie Videos mit Inhaltsangabe verlinkt */
  const VI=(typeof VIDEOINHALT!=='undefined')?VIDEOINHALT:{};
  const vidIds=s=>[...new Set([...s.querySelectorAll('a[href*="youtube.com/watch"],a[href*="youtu.be/"]')].filter(a=>!a.closest('ul.ql')).map(a=>{ const m=a.href.match(/(?:v=|youtu\.be\/)([\w-]{11})/); return m&&m[1]; }).filter(k=>k&&VI[k]))];
  const vbtn=document.createElement('button'); vbtn.id='vinb'; vbtn.innerHTML='<svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 5h14M5 10h14M5 15h9M5 20h6"/></svg><span>Video-Inhalt lesen</span>'; vbtn.hidden=true; document.body.appendChild(vbtn);
  function vinSync(){ vbtn.hidden=!vidIds(slides[cur]).length; }
  const ve=t=>String(t).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
  function vinOpen(){
    const ids=vidIds(slides[cur]); if(!ids.length) return;
    let o=document.getElementById('vinlay');
    if(!o){ o=document.createElement('div'); o.id='vinlay'; document.body.appendChild(o); o.addEventListener('click',ev=>{ if(ev.target===o||ev.target.closest('.vx')) o.classList.remove('on'); }); }
    o.innerHTML='<div class="vin"><button class="vx" title="schließen (Esc)">✕</button><div class="vkopf">Video-Inhalt zum Nachlesen</div>'+ids.map(k=>{ const v=VI[k];
      return '<article><h3>'+ve(v.titel||k)+'</h3><div class="vmeta">'+ve([v.kanal,v.dauer,(v.datum||'').split('-').reverse().join('. ')].filter(Boolean).join(' · '))+'</div>'
        +(v.kurz?'<p class="vkurz">'+ve(v.kurz)+'</p>':'')
        +'<ul>'+(v.punkte||[]).map(x=>{ const m=String(x).match(/^(\d+:\d\d)\s*(.*)$/); return '<li>'+(m?'<span class="tc">'+m[1]+'</span>'+ve(m[2]):ve(x))+'</li>'; }).join('')+'</ul>'
        +((v.zitate||[]).length?'<div class="vzit">'+v.zitate.map(z=>'<p>'+ve(z)+'</p>').join('')+'</div>':'')
        +'<div class="vfuss">Eigene Inhaltsangabe ('+ve(v.basis||'')+'). Die vollständige Abschrift zeigt YouTube unter „… mehr → Transkript anzeigen“. <a href="https://www.youtube.com/watch?v='+k+'" target="_blank" rel="noopener">Video auf YouTube öffnen ↗</a></div></article>'; }).join('')+'</div>';
    o.classList.add('on'); o.querySelector('.vin').scrollTop=0;
  }
  vbtn.addEventListener('click',vinOpen);
  { const bs=document.getElementById('bS'); if(bs) bs.addEventListener('click',ev=>{ ev.stopPropagation(); zweiSchirme(); }); }
  { const bz=document.getElementById('bZ'); if(bz) bz.addEventListener('click',ev=>{ ev.stopPropagation(); zSet(!zs.on); }); }
  /* ---- Zeichnen auf der Folie (Taste Z): Malstift, Leuchtstift, Emoji-Stempel, Radierer ----
     Jede Folie hat eine eigene Zeichenebene; Zeichnungen bleiben beim Blättern erhalten, bis sie gelöscht werden. */
  const ZF={mal:['#C8452F','#1F2A30','#1F5F5B','#2F6FB5','#FFFFFF'], leucht:['#FFE14D','#7EE08A','#FF8FC8','#7FD3FF','#FFB347']};
  const EMO=['👍','❤️','⭐','❓','❗','✅','❌','😮','😂','🤔','💡','👀'];
  const FN={'#C8452F':'Rot','#1F2A30':'Schwarz','#1F5F5B':'Petrol','#2F6FB5':'Blau','#FFFFFF':'Weiß','#FFE14D':'Gelb','#7EE08A':'Grün','#FF8FC8':'Pink','#7FD3FF':'Hellblau','#FFB347':'Orange'};
  const EN={'👍':'Daumen hoch','❤️':'Herz','⭐':'Stern','❓':'Frage','❗':'Achtung','✅':'richtig','❌':'falsch','😮':'staunen','😂':'lachen','🤔':'nachdenken','💡':'Idee','👀':'genau hinschauen'};
  const zs={on:false,tool:'mal',farbe:{mal:'#C8452F',leucht:'#FFE14D'},emo:'👍',dick:{mal:6,leucht:34}};
  const zbar=document.createElement('div'); zbar.id='zbar'; zbar.hidden=true; document.body.appendChild(zbar);
  const ZIC={mal:'<svg viewBox="0 0 24 24"><path d="M4 20l4-1 11-11-3-3L5 16z"/><path d="M14 6l3 3"/></svg>',
    leucht:'<svg viewBox="0 0 24 24"><path d="M5 19h6"/><path d="M9 15l-2 2 2 2 2-2"/><path d="M9 15l7-7 3 3-7 7z"/></svg>',
    emo:'<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="8.5"/><path d="M8.5 14.5c1.8 2 5.2 2 7 0"/><path d="M9.5 9.8h.01M14.5 9.8h.01"/></svg>',
    radier:'<svg viewBox="0 0 24 24"><path d="M8 20h11"/><path d="M5 15l8-8 6 6-6 6H9z"/></svg>'};
  function zRender(){
    const t=zs.tool, cols=(t==='mal'||t==='leucht')?ZF[t]:[];
    zbar.innerHTML='<div class="zg">'+['mal','leucht','emo','radier'].map(k=>'<button data-tool="'+k+'" class="'+(t===k?'on':'')+'" title="'+({mal:'Malstift – frei zeichnen',leucht:'Leuchtstift – Text markieren',emo:'Emoji-Stempel – Symbol auf die Folie setzen',radier:'Radierer – Zeichnung wegwischen'})[k]+'">'+ZIC[k]+'</button>').join('')+'</div>'
      +(cols.length?'<div class="zg">'+cols.map(c=>'<button data-farbe="'+c+'" class="zf'+(zs.farbe[t]===c?' on':'')+'" style="--c:'+c+'" title="'+(t==='mal'?'Malstift':'Leuchtstift')+': '+(FN[c]||c)+'"></button>').join('')+'</div>'
        +'<div class="zg"><button data-dick="-" title="dünner">−</button><span class="zd">'+zs.dick[t]+'</span><button data-dick="+" title="dicker">+</button></div>':'')
      +(t==='emo'?'<div class="zg ze">'+EMO.map(e=>'<button data-emo="'+e+'" class="'+(zs.emo===e?'on':'')+'" title="Stempel: '+(EN[e]||e)+' – auf die Folie klicken">'+e+'</button>').join('')+'</div>':'')
      +'<div class="zg"><button data-act="leer" title="Folie säubern">Folie säubern</button><button data-act="aus" title="Zeichnen beenden (Z oder Esc)">✕</button></div>';
  }
  function zCanvas(sec){ let c=sec.querySelector('canvas.zeich'); if(!c){ c=document.createElement('canvas'); c.className='zeich'; c.width=1920; c.height=1080; sec.appendChild(c); } return c; }
  function zSet(on){ zs.on=on; zbar.hidden=!on; document.body.classList.toggle('zeichnen',on); if(on){ zCanvas(slides[cur]); zRender(); } }
  zbar.addEventListener('click',ev=>{ const b=ev.target.closest('button'); if(!b) return; ev.stopPropagation();
    if(b.dataset.tool){ zs.tool=b.dataset.tool; } else if(b.dataset.farbe){ zs.farbe[zs.tool]=b.dataset.farbe; }
    else if(b.dataset.emo){ zs.emo=b.dataset.emo; } else if(b.dataset.dick){ const t=zs.tool; zs.dick[t]=Math.max(2,Math.min(80,zs.dick[t]+(b.dataset.dick==='+'?(t==='leucht'?8:2):(t==='leucht'?-8:-2)))); }
    else if(b.dataset.act==='leer'){ const c=slides[cur].querySelector('canvas.zeich'); if(c) c.getContext('2d').clearRect(0,0,1920,1080); }
    else if(b.dataset.act==='aus'){ zSet(false); return; }
    zRender(); });
  // Zeichnen mit Maus, Stift oder Finger
  let zd=null;
  const zPos=(c,ev)=>{ const r=c.getBoundingClientRect(); return {x:(ev.clientX-r.left)*1920/r.width, y:(ev.clientY-r.top)*1080/r.height}; };
  stage.addEventListener('pointerdown',ev=>{ if(!zs.on) return; const c=ev.target.closest('canvas.zeich'); if(!c) return; ev.preventDefault(); ev.stopPropagation();
    const g=c.getContext('2d'), p=zPos(c,ev);
    if(zs.tool==='emo'){ g.globalCompositeOperation='source-over'; g.globalAlpha=1; g.font='96px "Segoe UI Emoji","Apple Color Emoji","Noto Color Emoji",sans-serif'; g.textAlign='center'; g.textBaseline='middle'; g.fillText(zs.emo,p.x,p.y); return; }
    c.setPointerCapture(ev.pointerId); zd={c,g,last:p};
    g.lineCap='round'; g.lineJoin='round';
    if(zs.tool==='radier'){ g.globalCompositeOperation='destination-out'; g.globalAlpha=1; g.lineWidth=60; }
    else if(zs.tool==='leucht'){ g.globalCompositeOperation='multiply'; g.globalAlpha=.38; g.strokeStyle=zs.farbe.leucht; g.lineWidth=zs.dick.leucht; g.lineCap='butt'; }
    else { g.globalCompositeOperation='source-over'; g.globalAlpha=1; g.strokeStyle=zs.farbe.mal; g.lineWidth=zs.dick.mal; }
    zd.pts=[p]; if(zs.tool==='leucht'){ zd.snap=g.getImageData(0,0,1920,1080); } });
  stage.addEventListener('pointermove',ev=>{ if(!zd) return; const p=zPos(zd.c,ev), g=zd.g;
    if(zs.tool==='leucht'){ // ganze Linie neu zeichnen, damit sich die Transparenz nicht aufaddiert
      zd.pts.push(p); g.putImageData(zd.snap,0,0); g.beginPath(); g.moveTo(zd.pts[0].x,zd.pts[0].y); zd.pts.forEach(q=>g.lineTo(q.x,q.y)); g.stroke(); return; }
    g.beginPath(); g.moveTo(zd.last.x,zd.last.y); g.lineTo(p.x,p.y); g.stroke(); zd.last=p; });
  const zEnde=()=>{ if(zd){ zd.g.globalAlpha=1; zd.g.globalCompositeOperation='source-over'; } zd=null; };
  stage.addEventListener('pointerup',zEnde); stage.addEventListener('pointercancel',zEnde);
  /* Schwarzbild (B, Punkt): kurzer Hinweis, wie es weitergeht; Klick setzt fort */
  let blackT=null;
  function blackHint(){ const bl=document.getElementById('black'); bl.classList.add('hint'); clearTimeout(blackT); blackT=setTimeout(()=>bl.classList.remove('hint'),3500); }
  function setBlack(on){ const bl=document.getElementById('black'); bl.classList.toggle('on',on); if(on) blackHint(); else bl.classList.remove('hint');
    if(popup&&!popup.closed){ const x=popup.document.getElementById('pblk'); if(x) x.style.display=on?'':'none'; } }
  (function(){ const bl=document.getElementById('black'); if(!bl) return;
    bl.innerHTML='<div class="bhint">Bildschirm schwarz &nbsp;·&nbsp; fortsetzen mit <kbd>B</kbd>, <kbd>.</kbd> oder Klick</div>';
    bl.addEventListener('click',()=>setBlack(false)); bl.addEventListener('mousemove',blackHint); })();
  function prevWhole(){ go(cur-1,slides[cur-1]._steps.length); }
  function setAll(d,ids){ const {fw,bw,bs}=btnState(); setBtn(d.getElementById(ids[0]),bs); setBtn(d.getElementById(ids[1]),bw); setBtn(d.getElementById(ids[2]),fw); }
  function navBtns(){
    setAll(document,['bB','bP','bX']);
    if(popup&&!popup.closed) setAll(popup.document,['pb','pp','pn']);
  }
  /* Hochzählen: .count data-to (sichtbar = Slide aktiv und ggf. Fragment sichtbar) */
  function runCounts(s){
    s.querySelectorAll('.count').forEach(el=>{
      // Zähler laufen beim Aufrufen der Folie hoch, nicht erst beim Aufdecken des Schritts (Wunsch des Autors)
      if(el._done) return; el._done=true;
      const to=parseFloat(el.dataset.to), from=parseFloat(el.dataset.from||0), dur=+(el.dataset.dur||1400), t1=performance.now(), dec=+(el.dataset.dec||0);
      const fmt=v=>v.toLocaleString((document.documentElement.lang||'de'),{minimumFractionDigits:dec,maximumFractionDigits:dec});
      (function tick(t){ const k=Math.min(1,(t-t1)/dur), e=1-Math.pow(1-k,3); el.textContent=fmt(from+(to-from)*e); if(k<1) requestAnimationFrame(tick); })(t1);
    });
    slides.forEach(o=>{ if(o!==s) o.querySelectorAll('.count').forEach(el=>el._done=false); });
  }
  function go(i,st,frei){ if(lock&&!frei) return; i=Math.max(0,Math.min(N-1,i)); const ch=i!==cur; cur=i; step=st==null?0:st; if(ch&&!t0) t0=Date.now(); apply(); }
  function next(){ if(lock) return; const s=slides[cur]; if(!t0) t0=Date.now(); if(step<s._steps.length){ step++; apply(); } else if(cur<N-1) go(cur+1,0); }
  function prev(){ if(lock) return; if(step>0){ step--; apply(); } else if(cur>0) go(cur-1,slides[cur-1]._steps.length); }
  function nextSlide(){ go(cur+1,0); } function prevSlide(){ go(cur-1,0); }

  /* ---- Notizen (Leiste) ---- */
  const notes=document.getElementById('notes');
  const esc=t=>String(t||'').replace(/&/g,'&amp;').replace(/</g,'&lt;');
  function noteHTML(s){
    const a=s.querySelector('aside.notes');
    let h='';
    if(s.dataset.zweck) h+='<div class="nz"><div class="nzh">Worum geht es auf dieser Folie?</div>'+esc(s.dataset.zweck)+'</div>';
    if(s.dataset.pointe) h+='<div class="np"><div class="nzh">Pointe</div>'+esc(s.dataset.pointe)+'</div>';
    if(h) h+='<div class="nsep">Ausführlich</div>';
    let body=h+(a?a.innerHTML:'<p class="mut">Keine weiteren Notizen.</p>');
    const gs=[...new Set([...s.querySelectorAll('.gl')].map(x=>x.dataset.g))];
    if(gs.length) body+='<div class="nsep">Fachbegriffe auf dieser Folie</div><dl class="ngl">'+gs.map(id=>{ const g=GL[id]; return g?'<dt>'+esc(g.term)+'</dt><dd>'+esc(g.e)+'</dd>':''; }).join('')+'</dl>';
    return body;
  }
  const GL={}; GLOSSAR.forEach(g=>GL[g.id]=g);
  function renderNotes(){
    const s=slides[cur];
    notes.querySelector('.st').textContent=(cur+1)+'. '+title(s);
    notes.querySelector('.fx').textContent=s._steps.length?('Schritt '+step+' von '+s._steps.length):'';
    const nb=notes.querySelector('.nb'); nb.innerHTML=noteHTML(s); nb.style.setProperty('--nfs',nfs+'px');
    const nx=slides[cur+1]; notes.querySelector('.nnext').textContent=nx?('Als Nächstes: '+(cur+2)+'. '+title(nx)):'Ende der Präsentation';
  }
  function toggleNotes(){ document.body.classList.toggle('notes-open'); document.getElementById('bN').classList.toggle('on'); setTimeout(fit,480); }
  function fontNotes(d){ nfs=Math.max(13,Math.min(40,nfs+d)); try{localStorage.setItem('praes-nfs',nfs);}catch(e){} renderNotes(); syncPopup(); }
  // Notizen nachträglich eingesetzt (z. B. Notizschutz nach PIN): Pointe-Banner ergänzen, Leiste und Fenster neu zeichnen
  document.addEventListener('qp-notizen',()=>{
    slides.forEach(s=>{ if(s.dataset.pointe&&!s.querySelector(':scope > .pointe')){ const pb=document.createElement('div'); pb.className='pointe'; pb.innerHTML='<b>Pointe</b><span></span>'; pb.querySelector('span').textContent=s.dataset.pointe; s.appendChild(pb); } });
    renderNotes(); syncPopup();
  });

  /* ---- Referentenfenster ---- */
  const css=[...document.querySelectorAll('style')].map(s=>s.textContent).join('\n');
  function openPopup(){
    if(popup&&!popup.closed){ popup.focus(); return; }
    popup=window.open('','praesentation-notizen','width=1280,height=860');
    if(!popup){ alert('Das Notizfenster wurde vom Browser blockiert. Bitte Pop-ups für diese Datei erlauben.'); return; }
    const d=popup.document;
    d.open();
    d.write('<!doctype html><html lang="de"><head><meta charset="utf-8"><title>Referentenansicht – Notizen</title><base href="'+location.href.split('#')[0]+'">'
      +'<style>'+css+POPCSS+'</style></head><body class="pop">'
      +'<div class="ph"><div class="clock"><span id="tm">00:00</span><button id="tr" title="Timer zurücksetzen">↺</button><span id="ck"></span></div><div id="pos"></div><div id="pblk" style="display:none">Beamer schwarz · B zum Fortsetzen</div>'
      +'<div class="btns"><button id="pv" title="Umschalten: Notizen oder große Folie (V)">▣ Folie groß</button><button id="pb">←</button><button id="pp">◀</button><button id="pn">▶</button><button id="fm">A−</button><button id="fp">A+</button></div></div>'
      +'<div class="pm"><div class="pv-col"><div class="lbl2">Aktuelle Folie</div><div class="pv" id="pvc"></div><div class="lbl2">Als Nächstes <span id="nxs"></span></div><div class="pv sm" id="pvn"></div><div class="lbl2">Notizen der nächsten Folie</div><div id="pnn"></div></div>'
      +'<div class="pn-col"><div id="ptitle"></div><div id="pnotes"></div></div></div></body></html>');
    d.close();
    const P=k=>d.getElementById(k);
    P('pb').onclick=()=>prevWhole(); P('pp').onclick=()=>prev(); P('pn').onclick=()=>next(); P('fm').onclick=()=>fontNotes(-1); P('fp').onclick=()=>fontNotes(1);
    P('tr').onclick=()=>{ t0=Date.now(); };
    P('pv').onclick=()=>popGross();
    d.addEventListener('keydown',e=>onKey(e,true));
    popup.addEventListener('resize',()=>syncPopup());
    syncPopup();
  }
  const POPCSS=`
  body.pop{background:#14222A;color:#EDE6D8;display:flex;flex-direction:column;height:100vh;overflow:hidden;font-family:var(--ui)}
  .ph{display:flex;align-items:center;gap:26px;padding:12px 22px;background:#0E171C;border-bottom:1px solid #2A3A43}
  .clock{display:flex;align-items:center;gap:12px;font:600 30px/1 var(--ui)} #tm{color:var(--yellow);font-variant-numeric:tabular-nums} #ck{font:400 20px var(--ui);color:#8C969B;margin-left:10px}
  #pos{flex:1;font:500 18px var(--ui);color:#C9C2B4}
  .ph button{font:600 18px/1 var(--ui);background:#22323B;color:#EDE6D8;border:1px solid #3A4B55;border-radius:10px;padding:10px 14px;cursor:pointer;margin-left:6px}
  .ph button:hover{filter:brightness(1.15)}
  .ph button b{font-size:22px;margin-right:2px} .ph button small{font:500 13px var(--ui);opacity:.75;margin-left:4px}
  #pn{min-width:150px;padding:10px 18px} #pp,#pb{min-width:54px}
  .ph button.nb-plus{background:var(--yellow);color:#14222A;border-color:var(--yellow)}
  .ph button.nb-next{background:var(--teal);color:#fff;border-color:var(--teal)}
  .ph button.nb-minus,.ph button.nb-back{background:#22323B}
  .ph button.nb-end{opacity:.45}
  .ph button{position:relative;overflow:hidden;min-height:52px;min-width:58px;padding:8px 14px}
  .ph button .ct{position:relative;z-index:1;display:inline-flex;align-items:center;gap:8px}
  .ph button .ic{width:28px;height:28px;fill:none;stroke:currentColor;stroke-width:2.6;stroke-linecap:round;stroke-linejoin:round}
  .ph button .ic rect{fill:currentColor;stroke:none}
  .ph button .lb{font:600 16px/1 var(--ui)} .ph button .lb b{font-size:inherit}
  .ph button.nb-plus{background:#F3E7C9;color:#14222A;border-color:var(--yellow);min-width:170px}
  .ph button .sg{position:absolute;inset:0} .ph button .fl{position:absolute;left:0;top:0;bottom:0;background:var(--yellow);transition:width .7s cubic-bezier(.3,.7,.2,1)}
  .ph button .tk{position:absolute;top:0;bottom:0;width:2px;margin-left:-1px;background:rgba(20,34,42,.35)}
  #pblk{font:700 14px/1 var(--ui);letter-spacing:.08em;text-transform:uppercase;color:#14222A;background:var(--yellow);padding:8px 12px;border-radius:8px}
  .pm{flex:1;display:flex;min-height:0}
  .pv-col{flex:0 0 40%;padding:16px;display:flex;flex-direction:column;gap:8px;border-right:1px solid #2A3A43;overflow:hidden}
  #pnn{flex:1;min-height:0;overflow:auto;font:400 var(--nfs,16px)/1.5 var(--ui);color:#C9C2B4;background:#0E171C;border-radius:10px;padding:12px 16px}
  #pnn p{font-size:inherit;line-height:inherit;margin-bottom:.6em} #pnn li{font-size:inherit;margin-left:1.1em} #pnn b{color:#9FD6CF}
  #pnn .lbl{display:inline-block;font:600 .66em/1 var(--ui);letter-spacing:.1em;text-transform:uppercase;color:#14222A;background:#9FD6CF;padding:.3em .5em;border-radius:5px;margin-right:.3em}
  #pnn .lbl.q{background:var(--coral);color:#fff} #pnn .lbl.v{background:#C9C2B4} #pnn .nz{background:#1F5E5B;color:#EDE6D8} #pnn .np{background:#F2B63C;color:#14222A}
  #pnn dt{font-weight:600;color:#EDE6D8} #pnn dd{margin:0 0 .5em 0}
  #pnotes dl.ngl dt{font-weight:600;color:#fff;margin-top:.4em} #pnotes dl.ngl dd{margin:0 0 .3em 0;color:#C9C2B4}
  .lbl2{font:600 12px/1 var(--ui);letter-spacing:.16em;text-transform:uppercase;color:#8C969B} .lbl2 span{text-transform:none;letter-spacing:0;color:#C9C2B4;font-weight:400}
  .pv{position:relative;width:100%;aspect-ratio:16/9;overflow:hidden;border-radius:10px;background:#000;flex:none}
  .pv.sm{width:70%}
  .pv .slide{transition:none!important;transform:none!important}
  .pv .a,.pv .az{animation:none!important;opacity:1!important;transform:none!important}
  .pv .draw{transition:none!important}
  .pv .holder{position:absolute;left:0;top:0;width:1920px;height:1080px;transform-origin:0 0}
  body.pop.gross .pn-col,body.pop.gross .pv-col>:not(#pvc){display:none}
  body.pop.gross .pv-col{flex:1;border:0;align-items:center;justify-content:center;padding:10px}
  body.pop.gross #pvc{width:min(100%,calc((100vh - 90px)*16/9));border-radius:4px}
  .ph button#pv{background:#2A4A55}
  .pn-col{flex:1;display:flex;flex-direction:column;min-width:0}
  #ptitle{padding:18px 30px 10px;font:600 26px/1.25 var(--serif);color:#fff;border-bottom:1px solid #2A3A43}
  #ptitle small{display:block;font:500 15px var(--ui);color:var(--yellow);letter-spacing:.06em;margin-top:6px}
  #pnotes{flex:1;overflow:auto;padding:20px 34px 60px;font:400 var(--nfs,19px)/1.62 var(--ui);color:#EDE6D8}
  #pnotes p{font-size:inherit;line-height:inherit;margin-bottom:.8em} #pnotes li{font-size:inherit;line-height:inherit;margin:0 0 .45em 1.2em} #pnotes ul,#pnotes ol{margin-bottom:.8em}
  #pnotes :is(p,li,td,th,span:not(.lbl)){color:inherit}   /* Stile wie riso/journal färben p,li global dunkel – im dunklen Fenster wäre das unlesbar */
  #pnotes b{color:#9FD6CF}
  #pnotes .lbl{display:inline-block;font:600 .66em/1 var(--ui);letter-spacing:.12em;text-transform:uppercase;color:#14222A;background:#9FD6CF;padding:.35em .6em;border-radius:6px;margin-right:.4em;vertical-align:.12em}
  #pnotes .lbl.q{background:var(--coral);color:#fff}#pnotes .lbl.v{background:#C9C2B4}#pnotes .lbl.z{background:var(--yellow)}
  `;
  /* Referentenfenster: zwischen Notizansicht und großer Folie umschalten (V) */
  function popGross(){ if(!popup||popup.closed) return; const b=popup.document.body; b.classList.toggle('gross');
    const k=popup.document.getElementById('pv'); if(k) k.textContent=b.classList.contains('gross')?'☰ Notizen':'▣ Folie groß'; syncPopup(); }
  /* Zwei Bildschirme (S oder Knopf „⧉ Beamer“): Referentenansicht auf diesem Bildschirm, Folien als Vollbild auf dem anderen.
     Nutzt die Fensterverwaltung von Chrome/Edge (getScreenDetails); der Browser fragt beim ersten Mal nach der Erlaubnis. */
  function hinweis(t,ms){ let h=document.getElementById('hinweis'); if(!h){ h=document.createElement('div'); h.id='hinweis'; document.body.appendChild(h); }
    h.innerHTML=t; h.classList.add('on'); clearTimeout(h._t); h._t=setTimeout(()=>h.classList.remove('on'),ms||6000); }
  async function zweiSchirme(){
    openPopup();
    if(!('getScreenDetails' in window)){
      hinweis('<b>Zwei Bildschirme:</b> Dieser Browser kann Fenster nicht selbst verteilen. Ziehen Sie dieses Fenster auf den Beamer und drücken Sie dort <kbd>F</kbd> (Vollbild). Das Notizfenster bleibt auf dem Laptop. Am besten klappt es in Chrome oder Edge.',9000); return; }
    let sd; try{ sd=await window.getScreenDetails(); }catch(e){
      hinweis('<b>Zwei Bildschirme:</b> Der Browser hat die Fensterverwaltung nicht erlaubt. Erlauben Sie sie über das Schloss-Symbol in der Adresszeile („Fensterverwaltung“) und drücken Sie dann erneut <kbd>S</kbd>.',9000); return; }
    const hier=sd.currentScreen, dort=sd.screens.find(x=>x!==hier);
    if(popup&&!popup.closed){ try{ popup.moveTo(hier.availLeft,hier.availTop); popup.resizeTo(hier.availWidth,hier.availHeight); }catch(e){} }
    if(!dort){ hinweis('<b>Nur ein Bildschirm erkannt.</b> Schließen Sie den Beamer an (Anzeige „Erweitern“, nicht „Duplizieren“) und drücken Sie dann erneut <kbd>S</kbd>.',8000); return; }
    try{ await document.documentElement.requestFullscreen({screen:dort}); hinweis('Folien laufen auf dem Beamer. Steuerung im Notizfenster; <kbd>V</kbd> dort schaltet zwischen Notizen und großer Folie um.',5000); }
    catch(e){ hinweis('<b>Fast geschafft:</b> Bitte noch einmal <kbd>S</kbd> drücken oder auf „⧉ Beamer“ klicken – der Browser verlangt für das Vollbild einen frischen Klick.',8000); }
  }
  function preview(box,s,st,isCur){
    box.innerHTML='';
    const h=box.ownerDocument.createElement('div'); h.className='holder';
    const c=s.cloneNode(true); c.classList.add('cur'); c.classList.remove('past');
    const fr=orderFr([...c.querySelectorAll('.f,.fs')]); const groups=[];
    fr.forEach(el=>{ if(el.classList.contains('fw')&&groups.length) groups[groups.length-1].push(el); else groups.push([el]); });
    groups.forEach((g,k)=>g.forEach(el=>el.classList.toggle('vis',k<st)));
    for(let k=1;k<=st;k++) c.classList.add('st-'+k);
    c.querySelectorAll('aside.notes').forEach(a=>a.remove());
    h.appendChild(c); box.appendChild(h);
    const sc=box.clientWidth/1920; h.style.transform='scale('+sc+')';
  }
  function syncPopup(){
    if(!popup||popup.closed) return;
    const d=popup.document, s=slides[cur], nx=slides[cur+1];
    if(!d.getElementById('pnotes')) return;
    d.getElementById('pos').textContent='Folie '+(cur+1)+' von '+N+(s._steps.length?'  ·  Schritt '+step+' von '+s._steps.length:'');
    d.getElementById('ptitle').innerHTML=(cur+1)+'. '+title(s)+'<small>'+(s.dataset.c||'')+'</small>';
    const pn=d.getElementById('pnotes'); pn.innerHTML=noteHTML(s); pn.style.setProperty('--nfs',(nfs+2)+'px');
    preview(d.getElementById('pvc'),s,step,true);
    const pnn=d.getElementById('pnn'); if(pnn){ pnn.innerHTML=nx?noteHTML(nx):''; pnn.style.setProperty('--nfs',Math.max(13,nfs-3)+'px'); }
    if(nx){ preview(d.getElementById('pvn'),nx,0,false); d.getElementById('nxs').textContent='– '+(cur+2)+'. '+title(nx); }
    else { d.getElementById('pvn').innerHTML=''; d.getElementById('nxs').textContent='– Ende'; }
    setAll(d,['pb','pp','pn']);
  }
  setInterval(()=>{
    if(!popup||popup.closed) return; const d=popup.document; const tm=d.getElementById('tm'); if(!tm) return;
    const sec=t0?Math.floor((Date.now()-t0)/1000):0; tm.textContent=String(Math.floor(sec/60)).padStart(2,'0')+':'+String(sec%60).padStart(2,'0');
    const n=new Date(); d.getElementById('ck').textContent=n.toLocaleTimeString((document.documentElement.lang||'de'),{hour:'2-digit',minute:'2-digit'});
  },1000);

  /* ---- Übersicht ---- */
  const ov=document.getElementById('overview');
  function buildOverview(){
    const box=ov.querySelector('.ovl'); box.innerHTML=''; let lastC=null,grid=null;
    const q=(ov.querySelector('input').value||'').toLowerCase();
    slides.forEach((s,i)=>{
      const t=title(s); if(q&&!(t.toLowerCase().includes(q)||(s.textContent||'').toLowerCase().includes(q))) return;
      if(s.dataset.c!==lastC){ lastC=s.dataset.c; const h=document.createElement('h3'); h.textContent=lastC||'Einstieg'; box.appendChild(h); grid=document.createElement('div'); grid.className='ovs'; box.appendChild(grid); }
      const a=document.createElement('a'); a.href='#'+(i+1); a.innerHTML='<b>'+(i+1)+'</b><span>'+t+'</span>';
      if(i===cur) a.classList.add('cur'); if(s.classList.contains('s-auftrag')) a.classList.add('wk');
      a.onclick=e=>{ e.preventDefault(); toggleOverview(false); go(i,0); }; grid.appendChild(a);
    });
  }
  function toggleOverview(v){ const on=v==null?!ov.classList.contains('on'):v; ov.classList.toggle('on',on); if(on){ buildOverview(); ov.querySelector('input').value=''; buildOverview(); setTimeout(()=>{ const c=ov.querySelector('a.cur'); if(c) c.scrollIntoView({block:'center'}); },30);} }
  ov.querySelector('input').addEventListener('input',buildOverview);

  /* ---- Tastatur ---- */
  let numBuf='', numT=null; const gt=document.getElementById('goto');
  function onKey(e,fromPopup){
    if(e.target&&e.target.tagName==='INPUT') { if(e.key==='Escape') toggleOverview(false); return; }
    const k=e.key;
    if(/^[0-9]$/.test(k)){ numBuf+=k; gt.textContent='Gehe zu Folie '+numBuf; gt.classList.add('on'); clearTimeout(numT); numT=setTimeout(()=>{numBuf='';gt.classList.remove('on');},2500); return; }
    if(k==='Enter'&&numBuf){ go(parseInt(numBuf,10)-1,0); numBuf=''; gt.classList.remove('on'); e.preventDefault(); return; }
    switch(k){
      case 'ArrowRight': case 'PageDown': case ' ': case 'ArrowDown': e.shiftKey?nextSlide():next(); peek(); e.preventDefault(); break;
      case 'ArrowLeft': case 'PageUp': case 'ArrowUp': case 'Backspace': e.shiftKey?prevSlide():prev(); peek(); e.preventDefault(); break;
      case 'Home': go(0,0); break; case 'End': go(N-1,0); break;
      case 'n': case 'N': toggleNotes(); break;
      case 'p': case 'P': openPopup(); break;
      case 'o': case 'O': toggleOverview(); break;
      case 'h': case 'H': case '?': document.getElementById('help').classList.toggle('on'); break;
      case 'z': case 'Z': zSet(!zs.on); break;
      case 's': case 'S': if(!fromPopup) zweiSchirme(); break;
      case 'v': case 'V': popGross(); break;
      case 'b': case 'B': case '.': setBlack(!document.getElementById('black').classList.contains('on')); break;
      case 'f': case 'F': if(!fromPopup){ document.fullscreenElement?document.exitFullscreen():document.documentElement.requestFullscreen(); } break;
      case 'l': case 'L': document.body.classList.toggle('laser'); break;
      case '+': fontNotes(1); break; case '-': fontNotes(-1); break;
      case 'r': case 'R': t0=Date.now(); break;
      case 'k': case 'K': document.body.classList.toggle('no-pointe'); break;
      case 'g': case 'G': window.__gl.isOpen()?window.__gl.close():window.__gl.showAll(); e.preventDefault(); break;
      case 'Escape': if(zs.on) zSet(false); vidClose(); { const o=document.getElementById('vinlay'); if(o) o.classList.remove('on'); } window.__gl&&window.__gl.close(); toggleOverview(false); document.getElementById('help').classList.remove('on'); setBlack(false); break;
    }
  }
  document.addEventListener('keydown',e=>onKey(e,false));
  const laser=document.getElementById('laser');
  document.addEventListener('mousemove',e=>{ laser.style.left=e.clientX+'px'; laser.style.top=e.clientY+'px'; });
  /* Steuerleiste: bei jeder Mausbewegung einblenden, nach 2,5 s Ruhe ausblenden (außer die Maus steht darauf) */
  let navT=null;
  document.addEventListener('mousemove',()=>{ document.body.classList.add('maus'); clearTimeout(navT); navT=setTimeout(()=>document.body.classList.remove('maus'),2500); });
  // Wischen
  let tx=null; vp.addEventListener('touchstart',e=>{tx=e.touches[0].clientX},{passive:true});
  vp.addEventListener('touchend',e=>{ if(tx==null) return; const dx=e.changedTouches[0].clientX-tx; if(Math.abs(dx)>50) dx<0?next():prev(); tx=null; });
  // Knöpfe
  document.getElementById('bB').onclick=prevWhole; document.getElementById('bP').onclick=prev; document.getElementById('bX').onclick=next;
  document.getElementById('bN').onclick=toggleNotes; document.getElementById('bW').onclick=openPopup;
  document.getElementById('bO').onclick=()=>toggleOverview(); document.getElementById('bH').onclick=()=>document.getElementById('help').classList.toggle('on');
  document.getElementById('help').onclick=e=>{ if(e.target.id==='help') e.currentTarget.classList.remove('on'); };
  window.addEventListener('beforeunload',()=>{ if(popup&&!popup.closed) popup.close(); });

  /* ---- Quellenlinks: Sprung ins Verzeichnis und zurück ---- */
  const back=document.createElement('button'); back.id='qback'; document.body.appendChild(back);
  let backTo=null;
  back.onclick=()=>{ if(backTo!=null){ go(backTo.c,backTo.s); backTo=null; back.classList.remove('on'); } };
  stage.addEventListener('click',e=>{
    const a=e.target.closest('a.ql'); if(!a) return;
    e.preventDefault();
    const li=document.getElementById('q-'+a.dataset.q); if(!li) return;
    const k=slides.indexOf(li.closest('section.slide'));
    backTo={c:cur,s:step}; back.textContent='← zurück zu Folie '+(cur+1); back.classList.add('on');
    go(k,slides[k]._steps.length);
    li.classList.remove('flash'); void li.offsetWidth; li.classList.add('flash');
  });

  /* ---- Sprungkarten ---- */
  stage.addEventListener('click',e=>{ const j=e.target.closest('.jump'); if(!j) return; const k=slides.findIndex(x=>x.dataset.title===j.dataset.to); if(k>=0){ backTo={c:cur,s:step}; back.textContent='← zurück zu Folie '+(cur+1); back.classList.add('on'); go(k,0); } });

  /* ---- Glossar ---- */
  const glx=document.createElement('div'); glx.id='glx'; document.body.appendChild(glx);
  function qLink(q){ if(!q||!QUELLEN[q]) return ''; return ' <a class="ql glq" data-q="'+q+'">Quellenverzeichnis</a> <a class="qo" href="'+QUELLEN[q].url+'" target="_blank" rel="noopener">↗ Original</a>'; }
  function showGl(id){ const g=GL[id]; if(!g) return;
    glx.innerHTML='<div class="gb"><button class="gx" title="schließen">✕</button><div class="gk">Fachbegriff</div><h3>'+esc(g.term)+'</h3><p>'+esc(g.e)+'</p>'+(g.q?'<p class="gq">Quelle:'+qLink(g.q)+'</p>':'')+'<button class="gall">Ganzes Glossar (G)</button></div>';
    glx.classList.add('on'); }
  function showAll(){ const list=GLOSSAR.slice().sort((a,b)=>a.term.localeCompare(b.term,'de'));
    glx.innerHTML='<div class="gb gbig"><button class="gx" title="schließen">✕</button><div class="gk">Glossar · '+list.length+' Fachbegriffe</div><input type="search" placeholder="Begriff suchen …"><dl>'+list.map(g=>'<div class="ge" data-t="'+esc((g.term+' '+g.e).toLowerCase())+'"><dt>'+esc(g.term)+'</dt><dd>'+esc(g.e)+(g.q?' <span class="gq">'+qLink(g.q)+'</span>':'')+'</dd></div>').join('')+'</dl></div>';
    glx.classList.add('on'); const inp=glx.querySelector('input'); inp.focus();
    inp.oninput=()=>{ const t=inp.value.toLowerCase(); glx.querySelectorAll('.ge').forEach(e=>e.style.display=e.dataset.t.includes(t)?'':'none'); }; }
  glx.addEventListener('click',e=>{
    if(e.target===glx||e.target.classList.contains('gx')){ glx.classList.remove('on'); return; }
    if(e.target.classList.contains('gall')){ showAll(); return; }
    const a=e.target.closest('a.ql');
    if(a){ e.preventDefault(); glx.classList.remove('on'); const li=document.getElementById('q-'+a.dataset.q);
      if(li){ const k=slides.indexOf(li.closest('section.slide')); backTo={c:cur,s:step}; back.textContent='← zurück zu Folie '+(cur+1); back.classList.add('on'); go(k,slides[k]._steps.length); li.classList.remove('flash'); void li.offsetWidth; li.classList.add('flash'); } }
  });
  /* Bildansicht mit Lupe: Einpassen, volle Breite, + / −; verschieben mit Maus (ziehen), Mausrad oder Pfeiltasten */
  const LUP='<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.5 15.5L21 21"/></svg>';
  stage.addEventListener('click',e=>{ const z=e.target.closest('.zoom'); if(!z) return;
    glx.innerHTML='<div class="gb gimg"><button class="gx" title="schließen">✕</button>'
      +'<div class="lupe"><span class="li">'+LUP+'Lupe</span><button data-z="fit" class="on">Einpassen</button><button data-z="width">Volle Breite</button><button data-z="out" title="kleiner (−)">−</button><button data-z="in" title="größer (+)">+</button><span class="lz"></span></div>'
      +'<div class="gview"><img src="'+z.dataset.img+'" alt=""></div><p>'+esc(z.dataset.cap||'')+(z.dataset.url?' · <a class="qo" href="'+z.dataset.url+'" target="_blank" rel="noopener">↗ Original</a>':'')+'</p></div>';
    glx.classList.add('on'); lupeInit(); });
  let lupe=null;
  function lupeInit(){
    const box=glx.querySelector('.gimg'), v=glx.querySelector('.gview'), im=v.querySelector('img'), lz=glx.querySelector('.lz');
    const st={k:0,fit:true};
    function fitK(){ return Math.min(v.clientWidth/im.naturalWidth, (window.innerHeight*.72)/im.naturalHeight, 1.6); }
    function set(k,mode){ const old=st.k||fitK(), cx=(v.scrollLeft+v.clientWidth/2)/old, cy=(v.scrollTop+v.clientHeight/2)/old;
      st.fit=mode==='fit'; st.k=Math.max(.1,Math.min(6,k)); box.classList.toggle('gross',!st.fit);
      im.style.width=Math.round(im.naturalWidth*st.k)+'px'; im.style.maxWidth='none'; im.style.maxHeight='none';
      lz.textContent=Math.round(st.k*100)+' %';
      glx.querySelectorAll('.lupe button[data-z]').forEach(b=>b.classList.toggle('on',b.dataset.z===mode));
      void v.offsetWidth; if(mode==='width'){ v.scrollLeft=0; v.scrollTop=0; } else if(!st.fit){ v.scrollLeft=cx*st.k-v.clientWidth/2; v.scrollTop=cy*st.k-v.clientHeight/2; } }
    const go=()=>{ set(fitK(),'fit'); };
    if(im.complete) go(); else im.onload=go;
    glx.querySelector('.lupe').addEventListener('click',ev=>{ const b=ev.target.closest('button[data-z]'); if(!b) return; ev.stopPropagation();
      const z=b.dataset.z; if(z==='fit') set(fitK(),'fit'); else if(z==='width'){ box.classList.add('gross'); void v.offsetWidth; set((v.clientWidth-20)/im.naturalWidth,'width'); }
      else set(st.k*(z==='in'?1.4:1/1.4),'z'); });
    // Ziehen zum Verschieben
    let drag=null;
    v.addEventListener('pointerdown',ev=>{ if(st.fit) return; drag={x:ev.clientX,y:ev.clientY,l:v.scrollLeft,t:v.scrollTop}; v.setPointerCapture(ev.pointerId); v.classList.add('zieh'); });
    v.addEventListener('pointermove',ev=>{ if(!drag) return; v.scrollLeft=drag.l-(ev.clientX-drag.x); v.scrollTop=drag.t-(ev.clientY-drag.y); });
    const ende=()=>{ drag=null; v.classList.remove('zieh'); }; v.addEventListener('pointerup',ende); v.addEventListener('pointercancel',ende);
    v.addEventListener('dblclick',()=>{ if(st.fit) set(fitK()*2,'z'); else set(fitK(),'fit'); });
    lupe={set,st,v,fitK};
  }
  // Tasten in der Bildansicht: + / − zoomen, Pfeile verschieben, 0 einpassen, W volle Breite
  document.addEventListener('keydown',ev=>{
    if(!lupe||!glx.classList.contains('on')||!glx.querySelector('.gview')) return;
    const k=ev.key, v=lupe.v, d=Math.round(v.clientHeight*.25);
    if(k==='+'||k==='='){ lupe.set(lupe.st.k*1.4,'z'); } else if(k==='-'){ lupe.set(lupe.st.k/1.4,'z'); }
    else if(k==='0'){ lupe.set(lupe.fitK(),'fit'); } else if(k==='w'||k==='W'){ glx.querySelector('.lupe button[data-z="width"]').click(); }
    else if(k==='ArrowDown'&&!lupe.st.fit) v.scrollTop+=d; else if(k==='ArrowUp'&&!lupe.st.fit) v.scrollTop-=d;
    else if(k==='ArrowRight'&&!lupe.st.fit) v.scrollLeft+=d; else if(k==='ArrowLeft'&&!lupe.st.fit) v.scrollLeft-=d;
    else return;
    ev.preventDefault(); ev.stopImmediatePropagation();
  },true);
  stage.addEventListener('click',e=>{ const g=e.target.closest('.gl'); if(g){ e.stopPropagation(); showGl(g.dataset.g); } });
  window.__gl={showAll,close:()=>glx.classList.remove('on'),isOpen:()=>glx.classList.contains('on')};

  /* ---- Start ---- */
  fit(); measure();
  const hp=(location.hash||'').slice(1).split('.');
  const h=parseInt(hp[0],10);
  if(h>0) cur=Math.min(N-1,h-1);
  if(hp[1]) step=Math.min(slides[cur]._steps.length,parseInt(hp[1],10)||0);
  apply();
  if(location.search.includes('notes')) toggleNotes();
  if(document.fonts) document.fonts.ready.then(()=>{ measure(); });
  window.deck={go,next,prev,slides,N,cur:()=>cur,step:()=>step,title,setLock:v=>{ lock=!!v; document.body.classList.toggle('gesperrt',lock); },
    goNr:(nr,st)=>{ let k=slides.findIndex(s=>+(s.dataset.nr||0)===nr); if(k<0){ k=slides.findIndex(s=>+(s.dataset.nr||0)>nr)-1; if(k<0) k=nr>N?N-1:0; } go(k,Math.min(st||0,slides[Math.max(0,k)]._steps.length),true); }};
  /* Foliensprung über die Adresse auch bei geöffneter Präsentation (#115 oder #115.2) */
  window.addEventListener('hashchange',()=>{
    const q=(location.hash||'').slice(1).split('.'), k=parseInt(q[0],10);
    if(!(k>0)) return; const i=Math.min(N-1,k-1);
    go(i, q[1]?Math.min(slides[i]._steps.length,parseInt(q[1],10)||0):0);
  });
  /* Layout-Prüfung: index.html?check */
  if(location.search.includes('check')) document.fonts.ready.then(()=>setTimeout(function layoutCheck(){
    const out=[];
    slides.forEach((sl,i)=>{
      sl.classList.add('cur'); sl.style.transition='none';
      sl._steps.forEach(g=>g.forEach(el=>el.classList.add('vis')));
      const r0=sl.getBoundingClientRect(), sc=r0.width/1920;
      const ft=sl.querySelector(':scope > footer'); const fTop=ft?(ft.getBoundingClientRect().top-r0.top)/sc:1080;
      sl.querySelectorAll('*').forEach(el=>{
        if(el.closest('footer')||el.closest('aside')||el.closest('svg')&&el.tagName!=='svg'||el.classList.contains('bignum')||el.classList.contains('hero')) return;
        const r=el.getBoundingClientRect(); if(!r.width||!r.height) return;
        const b=(r.bottom-r0.top)/sc, rt=(r.right-r0.left)/sc;
        if(b>fTop-4||rt>1920-60) out.push((i+1)+' '+el.tagName+'.'+(el.className.baseVal!=null?el.className.baseVal:el.className)+' bottom='+Math.round(b)+' right='+Math.round(rt)+' footerTop='+Math.round(fTop)+' :: '+(el.textContent||'').trim().slice(0,40));
      });
      sl.classList.remove('cur');
    });
    const pre=document.createElement('pre'); pre.id='checkout'; pre.textContent=out.join(String.fromCharCode(10))||'OK'; document.body.appendChild(pre);
  },500));
})();
