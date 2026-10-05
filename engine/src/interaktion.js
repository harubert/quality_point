/* ==========================================================
   Interaktionsbausteine – auf einer Folie per Klasse + data-Attribute einsetzen.
   Alle Bausteine funktionieren ohne Server und ohne fremde Dienste.

   ia-schaetz    <div class="ia-schaetz" data-frage="…" data-wert="67" data-min="0" data-max="100" data-einheit="%"></div>
   ia-vergleich  <div class="ia-vergleich" data-a=BILD_VORHER data-b=BILD_NACHHER data-la="vorher" data-lb="nachher"></div>
   ia-ausschnitt <div class="ia-ausschnitt" data-img=BILD data-x="30" data-y="20" data-w="30" data-h="40"></div>  (Ausschnitt in % des Bildes)
   ia-quiz       <div class="ia-quiz" data-loesung="fake" data-text="Erklärung …"><img …></div>   (Abstimmung echt/fake)
   ia-sort       <div class="ia-sort" data-felder="Säugetier|Vogel"><span data-ziel="Vogel">Amsel</span> …</div>
   ia-timer      <div class="ia-timer" data-min="10"></div>
   ia-rad        <div class="ia-rad" data-items="Gruppe 1|Gruppe 2|Gruppe 3"></div>
   ia-wolke      <div class="ia-wolke" data-frage="Was fällt euch zum Thema ein?"></div>
   ia-karte      <div class="ia-karte" data-vorne="Frage" data-hinten="Antwort"></div>
   ia-qr         <div class="ia-qr" data-url="https://…" data-text="Folie am Handy"></div>   (ohne data-url: Adresse dieser Folie)
   ia-ampel      <div class="ia-ampel" data-frage="Darf man das posten?"></div>
   Spotlight     Taste X: alles abdunkeln bis auf einen Lichtkreis um die Maus
   ========================================================== */
(function(){
  const $=(t,c,h)=>{ const e=document.createElement(t); if(c) e.className=c; if(h!=null) e.innerHTML=h; return e; };
  const esc=t=>String(t==null?'':t).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
  const stop=el=>['click','pointerdown','keydown','wheel'].forEach(ev=>el.addEventListener(ev,e=>e.stopPropagation()));
  const fmt=v=>Number(v).toLocaleString(document.documentElement.lang||'de',{maximumFractionDigits:1});

  /* 1 Schätzregler */
  function schaetz(el){
    const min=+(el.dataset.min||0), max=+(el.dataset.max||100), wahr=+el.dataset.wert, ein=el.dataset.einheit||'';
    el.innerHTML='<div class="ia-frage">'+esc(el.dataset.frage||'Schätzen Sie!')+'</div>'
      +'<div class="ia-skala"><input type="range" min="'+min+'" max="'+max+'" step="'+(el.dataset.schritt||1)+'" value="'+((min+max)/2)+'"><i class="ia-wahr"></i></div>'
      +'<div class="ia-zeile"><span class="ia-tipp">Schätzung: <b>'+fmt((min+max)/2)+'</b> '+esc(ein)+'</span><button>Auflösen</button><span class="ia-erg"></span></div>';
    const r=el.querySelector('input'), b=el.querySelector('button'), w=el.querySelector('.ia-wahr'), tip=el.querySelector('.ia-tipp b'), erg=el.querySelector('.ia-erg');
    r.addEventListener('input',()=>{ tip.textContent=fmt(r.value); });
    b.addEventListener('click',()=>{ const p=(wahr-min)/(max-min)*100; w.style.left=p+'%'; el.classList.add('aufgeloest');
      const d=Math.abs(wahr-r.value); erg.innerHTML='Wirklich: <b>'+fmt(wahr)+' '+esc(ein)+'</b> · '+(d===0?'genau getroffen!':'daneben um '+fmt(d)+' '+esc(ein)); });
    stop(el);
  }
  /* 2 Vorher-nachher-Regler */
  function vergleich(el){
    el.innerHTML='<img src="'+esc(el.dataset.b)+'" alt="'+esc(el.dataset.lb||'nachher')+'"><div class="ia-oben"><img src="'+esc(el.dataset.a)+'" alt="'+esc(el.dataset.la||'vorher')+'"></div>'
      +'<div class="ia-griff"><span>◀ ▶</span></div><b class="ia-la">'+esc(el.dataset.la||'vorher')+'</b><b class="ia-lb">'+esc(el.dataset.lb||'nachher')+'</b>';
    const oben=el.querySelector('.ia-oben'), griff=el.querySelector('.ia-griff');
    const setz=p=>{ p=Math.max(0,Math.min(100,p)); oben.style.clipPath='inset(0 '+(100-p)+'% 0 0)'; griff.style.left=p+'%'; };
    let zieh=false;
    const pos=e=>{ const r=el.getBoundingClientRect(); setz((e.clientX-r.left)/r.width*100); };
    el.addEventListener('pointerdown',e=>{ zieh=true; el.setPointerCapture(e.pointerId); pos(e); });
    el.addEventListener('pointermove',e=>{ if(zieh) pos(e); });
    el.addEventListener('pointerup',()=>zieh=false);
    setz(50); stop(el);
  }
  /* 3 Ausschnitt aufziehen */
  function ausschnitt(el){
    const x=+el.dataset.x||0, y=+el.dataset.y||0, w=+el.dataset.w||100, h=+el.dataset.h||100;
    el.innerHTML='<div class="ia-bild"><img src="'+esc(el.dataset.img)+'" alt=""></div><button>Ganzes Bild zeigen</button>';
    const bild=el.querySelector('.ia-bild'), b=el.querySelector('button');
    const eng='inset('+y+'% '+(100-x-w)+'% '+(100-y-h)+'% '+x+'%)';
    bild.style.clipPath=eng;
    b.addEventListener('click',()=>{ const auf=el.classList.toggle('offen'); bild.style.clipPath=auf?'inset(0 0 0 0)':eng; b.textContent=auf?'Nur den Ausschnitt':'Ganzes Bild zeigen'; });
    stop(el);
  }
  /* 4 Echt oder Fake? */
  function quiz(el){
    const inhalt=el.innerHTML;
    el.innerHTML='<div class="ia-q-bild">'+inhalt+'</div><div class="ia-zeile"><button data-s="echt">Echt <i>0</i></button><button data-s="fake">Fake <i>0</i></button><button class="ia-los">Auflösen</button></div><div class="ia-erg"></div>';
    const z={echt:0,fake:0};
    el.querySelectorAll('button[data-s]').forEach(b=>b.addEventListener('click',()=>{ z[b.dataset.s]++; b.querySelector('i').textContent=z[b.dataset.s]; }));
    el.querySelector('.ia-los').addEventListener('click',()=>{ const l=el.dataset.loesung||'echt', n=z.echt+z.fake;
      el.classList.add('aufgeloest'); el.querySelector('.ia-erg').innerHTML='<b>'+(l==='fake'?'Fake':'Echt')+'</b>'+(n?' · '+Math.round(z[l]/n*100)+' % lagen richtig':'')+(el.dataset.text?' – '+esc(el.dataset.text):''); });
    stop(el);
  }
  /* 5 Zuordnen per Ziehen */
  function sort(el){
    const felder=(el.dataset.felder||'').split('|'), items=[...el.querySelectorAll('[data-ziel]')];
    const vorrat=$('div','ia-vorrat'), reihe=$('div','ia-felder');
    felder.forEach(f=>{ const d=$('div','ia-feld','<b>'+esc(f)+'</b>'); d.dataset.feld=f; reihe.appendChild(d); });
    items.sort(()=>Math.random()-.5).forEach(it=>{ it.classList.add('ia-item'); it.draggable=true; vorrat.appendChild(it); });
    const knopf=$('button','ia-pruefen','Prüfen'); el.innerHTML=''; el.append(vorrat,reihe,knopf);
    let gezogen=null;
    el.addEventListener('dragstart',e=>{ gezogen=e.target.closest('.ia-item'); });
    [vorrat,...reihe.children].forEach(z=>{ z.addEventListener('dragover',e=>e.preventDefault()); z.addEventListener('drop',e=>{ e.preventDefault(); if(gezogen){ z.appendChild(gezogen); gezogen.classList.remove('ok','falsch'); } }); });
    // Antippen statt Ziehen (Touch): Karte wählen, dann Feld antippen
    let gewaehlt=null;
    el.addEventListener('click',e=>{ const it=e.target.closest('.ia-item'), fd=e.target.closest('.ia-feld,.ia-vorrat');
      if(it){ if(gewaehlt) gewaehlt.classList.remove('gewaehlt'); gewaehlt=it; it.classList.add('gewaehlt'); return; }
      if(fd&&gewaehlt){ fd.appendChild(gewaehlt); gewaehlt.classList.remove('gewaehlt','ok','falsch'); gewaehlt=null; } });
    knopf.addEventListener('click',e=>{ e.stopPropagation(); el.querySelectorAll('.ia-feld .ia-item').forEach(it=>{ const ok=it.dataset.ziel===it.parentElement.dataset.feld; it.classList.toggle('ok',ok); it.classList.toggle('falsch',!ok); }); });
    stop(el);
  }
  /* 6 Timer */
  function timer(el){
    const start=(+el.dataset.min||5)*60; let rest=start, lauf=null;
    el.innerHTML='<div class="ia-zeit"></div><div class="ia-zeile"><button class="ia-go">Start</button><button class="ia-plus">+1 Min.</button><button class="ia-reset">↺</button></div>';
    const z=el.querySelector('.ia-zeit'), go=el.querySelector('.ia-go');
    const zeig=()=>{ z.textContent=String(Math.floor(rest/60)).padStart(2,'0')+':'+String(rest%60).padStart(2,'0'); el.classList.toggle('knapp',rest<=60&&rest>0); el.classList.toggle('aus',rest===0); };
    go.addEventListener('click',()=>{ if(lauf){ clearInterval(lauf); lauf=null; go.textContent='Weiter'; return; }
      go.textContent='Pause'; lauf=setInterval(()=>{ if(rest>0){ rest--; zeig(); } if(rest===0){ clearInterval(lauf); lauf=null; go.textContent='Start'; } },1000); });
    el.querySelector('.ia-plus').addEventListener('click',()=>{ rest+=60; zeig(); });
    el.querySelector('.ia-reset').addEventListener('click',()=>{ clearInterval(lauf); lauf=null; rest=start; go.textContent='Start'; zeig(); });
    zeig(); stop(el);
  }
  /* 7 Zufallsrad */
  function rad(el){
    const it=(el.dataset.items||'A|B|C').split('|'), n=it.length, farben=['var(--red)','var(--teal)','var(--yellow)','var(--coral)','var(--teal-d)','var(--ink2)'];
    let grad='conic-gradient('+it.map((_,i)=>farben[i%farben.length]+' '+(i*360/n)+'deg '+((i+1)*360/n)+'deg').join(',')+')';
    el.innerHTML='<div class="ia-scheibe" style="background:'+grad+'">'+it.map((t,i)=>'<span style="transform:rotate('+((i+.5)*360/n)+'deg) translateY(-135px)">'+esc(t)+'</span>').join('')+'</div><i class="ia-zeiger"></i><button>Drehen</button><div class="ia-erg"></div>';
    const s=el.querySelector('.ia-scheibe'); let w=0;
    el.querySelector('button').addEventListener('click',()=>{ const k=Math.floor(Math.random()*n); w+=1440+(360-((k+.5)*360/n))-(w%360);
      s.style.transform='rotate('+w+'deg)'; el.querySelector('.ia-erg').textContent=''; setTimeout(()=>{ el.querySelector('.ia-erg').textContent='→ '+it[k]; },3200); });
    stop(el);
  }
  /* 8 Wortwolke (nur auf diesem Rechner) */
  function wolke(el){
    el.innerHTML='<div class="ia-frage">'+esc(el.dataset.frage||'Ihre Begriffe')+'</div><div class="ia-zeile"><input type="text" placeholder="Begriff eintippen, Enter"><button class="ia-leer">leeren</button></div><div class="ia-woerter"></div>';
    const inp=el.querySelector('input'), box=el.querySelector('.ia-woerter'), z={};
    const zeig=()=>{ const m=Math.max(1,...Object.values(z)); box.innerHTML=Object.entries(z).sort(()=>Math.random()-.5).map(([w,n])=>'<span style="font-size:'+(22+n/m*46)+'px">'+esc(w)+'</span>').join(''); };
    inp.addEventListener('keydown',e=>{ e.stopPropagation(); if(e.key==='Enter'&&inp.value.trim()){ const w=inp.value.trim(); z[w]=(z[w]||0)+1; inp.value=''; zeig(); } });
    el.querySelector('.ia-leer').addEventListener('click',()=>{ for(const k in z) delete z[k]; zeig(); });
    stop(el);
  }
  /* 9 Karteikarte zum Umdrehen */
  function karte(el){
    el.innerHTML='<div class="ia-in"><div class="ia-v">'+esc(el.dataset.vorne||'')+'</div><div class="ia-h">'+esc(el.dataset.hinten||'')+'</div></div>';
    el.addEventListener('click',()=>el.classList.toggle('um')); stop(el);
  }
  /* 10 QR-Code */
  function qr(el){
    if(typeof qrcode!=='function'){ el.textContent='QR nicht verfügbar'; return; }
    const sec=el.closest('section.slide'); const idx=[...document.querySelectorAll('section.slide')].indexOf(sec)+1;
    const url=el.dataset.url||(location.href.split('#')[0]+'#'+idx);
    const q=qrcode(0,'M'); q.addData(url); q.make();
    el.innerHTML=q.createSvgTag({cellSize:6,margin:2,scalable:true})+'<div class="ia-qrt">'+esc(el.dataset.text||'Mit dem Handy öffnen')+'</div>';
    el.title=url; stop(el);
  }
  /* 11 Ampel-Abstimmung (Handzeichen zählen) */
  function ampel(el){
    el.innerHTML='<div class="ia-frage">'+esc(el.dataset.frage||'Wie sehen Sie das?')+'</div><div class="ia-lichter">'+['rot','gelb','gruen'].map(f=>'<div class="ia-l ia-'+f+'"><button title="eine Stimme dazu">+</button><i></i><b>0</b></div>').join('')+'</div><button class="ia-reset">↺</button>';
    const z={rot:0,gelb:0,gruen:0};
    const zeig=()=>{ const m=Math.max(1,z.rot+z.gelb+z.gruen); ['rot','gelb','gruen'].forEach(f=>{ const l=el.querySelector('.ia-'+f); l.querySelector('b').textContent=z[f]; l.querySelector('i').style.height=Math.round(z[f]/m*200)+'px'; }); };
    ['rot','gelb','gruen'].forEach(f=>el.querySelector('.ia-'+f+' button').addEventListener('click',()=>{ z[f]++; zeig(); }));
    el.querySelector('.ia-reset').addEventListener('click',()=>{ z.rot=z.gelb=z.gruen=0; zeig(); });
    zeig(); stop(el);
  }
  const BAU={'ia-schaetz':schaetz,'ia-vergleich':vergleich,'ia-ausschnitt':ausschnitt,'ia-quiz':quiz,'ia-sort':sort,'ia-timer':timer,'ia-rad':rad,'ia-wolke':wolke,'ia-karte':karte,'ia-qr':qr,'ia-ampel':ampel};
  function init(root){ Object.entries(BAU).forEach(([k,f])=>root.querySelectorAll('#stage .'+k+':not(.ia-fertig)').forEach(el=>{ try{ f(el); el.classList.add('ia-fertig'); }catch(e){ console.warn(k,e); } })); }
  init(document);

  /* 12 Spotlight (Taste X) */
  const spot=$('div',''); spot.id='spot'; document.body.appendChild(spot);
  document.addEventListener('mousemove',e=>{ spot.style.setProperty('--x',e.clientX+'px'); spot.style.setProperty('--y',e.clientY+'px'); });
  document.addEventListener('keydown',e=>{ if(e.target.tagName==='INPUT') return; if(e.key==='x'||e.key==='X') spot.classList.toggle('on'); if(e.key==='Escape') spot.classList.remove('on'); });
  document.addEventListener('wheel',e=>{ if(!spot.classList.contains('on')) return; const r=parseFloat(getComputedStyle(spot).getPropertyValue('--r'))||180; spot.style.setProperty('--r',Math.max(60,Math.min(600,r-e.deltaY*.3))+'px'); },{passive:true});
})();
