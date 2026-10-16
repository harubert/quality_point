/* ==========================================================
   Interaktionsbausteine – auf einer Folie per Klasse + data-Attribute einsetzen.
   Alle Bausteine funktionieren ohne Server (Handzeichen zählen, am Vortragsrechner eintippen).
   Im Server-Modus (quality_point.json „live“) antworten Teilnehmer*innen am eigenen Gerät; die
   Bausteine schicken dann ihre Antworten über live.js und zeigen die Ergebnisse aller.

   ia-schaetz    <div class="ia-schaetz" data-frage="…" data-wert="67" data-min="0" data-max="100" data-einheit="%"></div>
   ia-vergleich  <div class="ia-vergleich" data-a=BILD_VORHER data-b=BILD_NACHHER data-la="vorher" data-lb="nachher"></div>
   ia-ausschnitt <div class="ia-ausschnitt" data-img=BILD data-x="30" data-y="20" data-w="30" data-h="40"></div>  (Ausschnitt in % des Bildes)
   ia-quiz       <div class="ia-quiz" data-loesung="fake" data-text="Erklärung …"><img …></div>   (Abstimmung echt/fake)
   ia-umfrage    <div class="ia-umfrage" data-frage="…" data-optionen="A|B|C" data-mehrfach="0" data-richtig="B"></div>  (Umfrage/Quiz mit Balken)
   ia-sort       <div class="ia-sort" data-felder="Säugetier|Vogel"><span data-ziel="Vogel">Amsel</span> …</div>
   ia-timer      <div class="ia-timer" data-min="10"></div>
   ia-rad        <div class="ia-rad" data-items="Gruppe 1|Gruppe 2|Gruppe 3"></div>
   ia-wolke      <div class="ia-wolke" data-frage="Was fällt euch zum Thema ein?"></div>
   ia-karte      <div class="ia-karte" data-vorne="Frage" data-hinten="Antwort"></div>
   ia-qr         <div class="ia-qr" data-url="https://…" data-text="Folie am Handy"></div>   (ohne data-url: Adresse dieser Folie)
   ia-ampel      <div class="ia-ampel" data-frage="Darf man das posten?"></div>
   Spotlight     Taste X: alles abdunkeln bis auf einen Lichtkreis um die Maus

   Live-Attribute (Server-Modus): data-id (vergibt build.py), data-ergebnis="sofort|freigabe|nie" – wann Teilnehmer*innen
   die Ergebnisse sehen (Standard aus den Einstellungen). Lösungen (data-wert, data-loesung, data-richtig, data-ziel, data-text)
   entfernt build.py aus der Teilnehmer-Fassung; sie kommen erst mit der Freigabe.
   ========================================================== */
(function(){
  const $=(t,c,h)=>{ const e=document.createElement(t); if(c) e.className=c; if(h!=null) e.innerHTML=h; return e; };
  const esc=t=>String(t==null?'':t).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
  // Klicks und Rad bleiben im Baustein (kein Folienwechsel); Tasten nur in Eingabefeldern – ein angeklickter Knopf gibt den Fokus
  // sofort wieder ab, damit Presenter und Pfeiltasten weiter die Folien steuern.
  const stop=el=>{ ['click','pointerdown','wheel'].forEach(ev=>el.addEventListener(ev,e=>e.stopPropagation()));
    el.addEventListener('keydown',e=>{ if(['INPUT','TEXTAREA','SELECT'].includes(e.target.tagName)) e.stopPropagation(); });
    el.addEventListener('click',e=>{ const b=e.target.closest('button'); if(b) b.blur(); }); };
  const fmt=v=>Number(v).toLocaleString(document.documentElement.lang||'de',{maximumFractionDigits:1});
  const TN=document.body.classList.contains('tn');              // Teilnehmer-Fassung (teilnehmer.html)
  const L=()=>window.qpLive||null;                               // Live-Modul, nur im Server-Modus vorhanden
  const live=()=>!!L();
  const senden=(el,wert,mehrfach)=>{ const l=L(); if(l) l.antwort(el.dataset.id,wert,!!mehrfach); };
  const freigeben=(el,loesung)=>{ const l=L(); if(l&&!TN) l.freigeben(el.dataset.id,true,loesung); };
  const pct=(n,m)=>m?Math.round(n/m*100):0;
  /* Balkendiagramm: zeilen [{label,n,ok}] */
  function balken(box,zeilen,gesamt){
    const m=Math.max(1,...zeilen.map(z=>z.n));
    box.innerHTML='<div class="ia-balken">'+zeilen.map(z=>'<div class="ia-bz'+(z.ok===true?' ok':z.ok===false?' nein':'')+'"><span class="ia-bl">'+esc(z.label)+'</span><span class="ia-bt"><i style="width:'+pct(z.n,m)+'%"></i></span><span class="ia-bn">'+z.n+(gesamt?' · '+pct(z.n,gesamt)+' %':'')+'</span></div>').join('')+'</div>'
      +(gesamt!=null?'<div class="ia-n">'+gesamt+' '+(gesamt===1?'Antwort':'Antworten')+'</div>':'');
  }
  const median=a=>{ if(!a.length) return null; const s=a.slice().sort((x,y)=>x-y), h=s.length>>1; return s.length%2?s[h]:(s[h-1]+s[h])/2; };

  /* 1 Schätzregler */
  function schaetz(el){
    const min=+(el.dataset.min||0), max=+(el.dataset.max||100), wahr=el.dataset.wert!=null?+el.dataset.wert:null, ein=el.dataset.einheit||'';
    el.innerHTML='<div class="ia-frage">'+esc(el.dataset.frage||'Schätzen Sie!')+'</div>'
      +'<div class="ia-skala"><input type="range" min="'+min+'" max="'+max+'" step="'+(el.dataset.schritt||1)+'" value="'+((min+max)/2)+'"><i class="ia-wahr"></i><div class="ia-hist"></div></div>'
      +'<div class="ia-zeile"><span class="ia-tipp">Schätzung: <b>'+fmt((min+max)/2)+'</b> '+esc(ein)+'</span>'+(TN?'<button class="ia-send">Abschicken</button>':'<button class="ia-los">Auflösen</button>')+'<span class="ia-erg"></span></div><div class="ia-live"></div>';
    const r=el.querySelector('input'), w=el.querySelector('.ia-wahr'), tip=el.querySelector('.ia-tipp b'), erg=el.querySelector('.ia-erg'), lv=el.querySelector('.ia-live'), hist=el.querySelector('.ia-hist');
    r.addEventListener('input',()=>{ tip.textContent=fmt(r.value); });
    const zeigeWahr=v=>{ w.style.left=((v-min)/(max-min)*100)+'%'; el.classList.add('aufgeloest'); const d=Math.abs(v-r.value);
      erg.innerHTML='Wirklich: <b>'+fmt(v)+' '+esc(ein)+'</b> · '+(d===0?'genau getroffen!':'daneben um '+fmt(d)+' '+esc(ein)); };
    if(TN){ el.querySelector('.ia-send').addEventListener('click',e=>{ senden(el,+r.value); e.target.textContent='Gesendet ✓'; setTimeout(()=>e.target.textContent='Erneut schicken',2500); }); }
    else el.querySelector('.ia-los').addEventListener('click',()=>{ if(wahr==null) return; zeigeWahr(wahr); freigeben(el,{wert:wahr}); });
    el._loesung=()=>({wert:wahr});
    el._live=(antworten,frei)=>{                                   // antworten: Zahlen aller Teilnehmer*innen
      const a=(antworten||[]).map(Number).filter(x=>!isNaN(x));
      if(frei&&frei.loesung&&frei.loesung.wert!=null&&!el.classList.contains('aufgeloest')) zeigeWahr(+frei.loesung.wert);
      if(!a.length){ lv.textContent=''; hist.innerHTML=''; return; }
      const k=12, z=new Array(k).fill(0); a.forEach(v=>{ z[Math.min(k-1,Math.max(0,Math.floor((v-min)/(max-min)*k)))]++; });
      const mx=Math.max(...z); hist.innerHTML=z.map(n=>'<i style="height:'+Math.round(n/mx*100)+'%"></i>').join('');
      lv.innerHTML='<b>'+a.length+'</b> '+(a.length===1?'Schätzung':'Schätzungen')+' · Median <b>'+fmt(median(a))+' '+esc(ein)+'</b> · von '+fmt(Math.min(...a))+' bis '+fmt(Math.max(...a));
    };
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
    const inhalt=el.innerHTML, loes=el.dataset.loesung||null;
    el.innerHTML='<div class="ia-q-bild">'+inhalt+'</div><div class="ia-zeile"><button data-s="echt">Echt <i>0</i></button><button data-s="fake">Fake <i>0</i></button>'+(TN?'':'<button class="ia-los">Auflösen</button>')+'</div><div class="ia-erg"></div>';
    const z={echt:0,fake:0}, erg=el.querySelector('.ia-erg');
    const zeige=()=>el.querySelectorAll('button[data-s]').forEach(b=>b.querySelector('i').textContent=z[b.dataset.s]);
    el.querySelectorAll('button[data-s]').forEach(b=>b.addEventListener('click',()=>{
      if(TN){ senden(el,b.dataset.s); el.querySelectorAll('button[data-s]').forEach(x=>x.classList.toggle('gewaehlt',x===b)); erg.textContent='Deine Antwort: '+b.textContent.replace(/\d+$/,'').trim(); return; }
      if(live()) return; z[b.dataset.s]++; zeige(); }));
    const aufloesen=(l,text)=>{ const n=z.echt+z.fake; el.classList.add('aufgeloest');
      erg.innerHTML='<b>'+(l==='fake'?'Fake':'Echt')+'</b>'+(n?' · '+pct(z[l],n)+' % lagen richtig':'')+(text?' – '+esc(text):''); };
    if(!TN) el.querySelector('.ia-los').addEventListener('click',()=>{ if(!loes) return; aufloesen(loes,el.dataset.text); freigeben(el,{loesung:loes,text:el.dataset.text||''}); });
    el._loesung=()=>({loesung:loes,text:el.dataset.text||''});
    el._live=(antworten,frei)=>{
      if(antworten){ z.echt=antworten.filter(v=>v==='echt').length; z.fake=antworten.filter(v=>v==='fake').length; if(!TN||frei) zeige(); }
      if(frei&&frei.loesung&&!el.classList.contains('aufgeloest')) aufloesen(frei.loesung.loesung,frei.loesung.text);
    };
    stop(el);
  }
  /* 4b Umfrage / Quiz mit Balken */
  function umfrage(el){
    const opt=(el.dataset.optionen||'Ja|Nein').split('|').map(s=>s.trim()).filter(Boolean), mehr=el.dataset.mehrfach==='1', richtig=el.dataset.richtig?el.dataset.richtig.split('|').map(s=>s.trim()):null;
    el.innerHTML='<div class="ia-frage">'+esc(el.dataset.frage||'Ihre Meinung?')+'</div><div class="ia-opt">'+opt.map((o,i)=>'<button data-i="'+i+'">'+esc(o)+(TN?'':' <i>0</i>')+'</button>').join('')+'</div>'
      +'<div class="ia-zeile">'+(TN?(mehr?'<button class="ia-send">Abschicken</button>':''):(richtig?'<button class="ia-los">Auflösen</button>':'')+'<button class="ia-reset" title="zurücksetzen">↺</button>')+'<span class="ia-erg"></span></div><div class="ia-live"></div>';
    const z=opt.map(()=>0), lv=el.querySelector('.ia-live'), erg=el.querySelector('.ia-erg'), gew=new Set();
    const zeige=(gesamt)=>{ el.querySelectorAll('.ia-opt button i').forEach((i,k)=>i.textContent=z[k]); if(live()||TN) balken(lv,opt.map((o,k)=>({label:o,n:z[k],ok:el.classList.contains('aufgeloest')&&richtig?richtig.includes(o):null})),gesamt); };
    el.querySelectorAll('.ia-opt button').forEach(b=>b.addEventListener('click',()=>{ const k=+b.dataset.i;
      if(TN){ if(mehr){ b.classList.toggle('gewaehlt'); gew.has(k)?gew.delete(k):gew.add(k); } else { senden(el,opt[k]); el.querySelectorAll('.ia-opt button').forEach(x=>x.classList.toggle('gewaehlt',x===b)); erg.textContent='Gesendet ✓'; } return; }
      if(live()) return; z[k]++; zeige(z.reduce((a,b)=>a+b,0)); }));
    if(TN&&mehr) el.querySelector('.ia-send').addEventListener('click',e=>{ senden(el,[...gew].map(k=>opt[k])); e.target.textContent='Gesendet ✓'; });
    if(!TN){ el.querySelector('.ia-reset').addEventListener('click',()=>{ z.fill(0); el.classList.remove('aufgeloest'); zeige(0); });
      const los=el.querySelector('.ia-los'); if(los) los.addEventListener('click',()=>{ el.classList.add('aufgeloest'); zeige(z.reduce((a,b)=>a+b,0)); freigeben(el,{richtig}); }); }
    el._loesung=()=>({richtig});
    el._live=(antworten,frei)=>{
      if(antworten){ z.fill(0); antworten.forEach(v=>(Array.isArray(v)?v:[v]).forEach(o=>{ const k=opt.indexOf(o); if(k>=0) z[k]++; })); }
      if(frei&&frei.loesung&&frei.loesung.richtig){ el.classList.add('aufgeloest'); el.querySelectorAll('.ia-opt button').forEach((b,k)=>b.classList.toggle('ok',frei.loesung.richtig.includes(opt[k]))); }
      if(antworten&&(!TN||frei)) zeige(antworten.length); else if(TN) lv.innerHTML='';
    };
    zeige(0); stop(el);
  }
  /* 5 Zuordnen per Ziehen */
  function sort(el){
    const felder=(el.dataset.felder||'').split('|'), items=[...el.querySelectorAll('[data-ziel],[data-item]')];
    const vorrat=$('div','ia-vorrat'), reihe=$('div','ia-felder');
    felder.forEach(f=>{ const d=$('div','ia-feld','<b>'+esc(f)+'</b>'); d.dataset.feld=f; reihe.appendChild(d); });
    items.sort(()=>Math.random()-.5).forEach(it=>{ it.classList.add('ia-item'); it.draggable=true; vorrat.appendChild(it); });
    const knopf=$('button','ia-pruefen',TN?'Abschicken':'Prüfen'), lv=$('div','ia-live'); el.innerHTML=''; el.append(vorrat,reihe,knopf,lv);
    let gezogen=null;
    el.addEventListener('dragstart',e=>{ gezogen=e.target.closest('.ia-item'); });
    [vorrat,...reihe.children].forEach(z=>{ z.addEventListener('dragover',e=>e.preventDefault()); z.addEventListener('drop',e=>{ e.preventDefault(); if(gezogen){ z.appendChild(gezogen); gezogen.classList.remove('ok','falsch'); } }); });
    // Antippen statt Ziehen (Touch): Karte wählen, dann Feld antippen
    let gewaehlt=null;
    el.addEventListener('click',e=>{ const it=e.target.closest('.ia-item'), fd=e.target.closest('.ia-feld,.ia-vorrat');
      if(it){ if(gewaehlt) gewaehlt.classList.remove('gewaehlt'); gewaehlt=it; it.classList.add('gewaehlt'); return; }
      if(fd&&gewaehlt){ fd.appendChild(gewaehlt); gewaehlt.classList.remove('gewaehlt','ok','falsch'); gewaehlt=null; } });
    const zuordnung=()=>{ const m={}; el.querySelectorAll('.ia-feld .ia-item').forEach(it=>{ m[it.textContent.trim()]=it.parentElement.dataset.feld; }); return m; };
    const loesung=()=>{ const m={}; items.forEach(it=>{ if(it.dataset.ziel) m[it.textContent.trim()]=it.dataset.ziel; }); return m; };
    const markiere=(l)=>el.querySelectorAll('.ia-feld .ia-item').forEach(it=>{ const ok=l[it.textContent.trim()]===it.parentElement.dataset.feld; it.classList.toggle('ok',ok); it.classList.toggle('falsch',!ok); });
    knopf.addEventListener('click',e=>{ e.stopPropagation();
      if(TN){ senden(el,zuordnung()); knopf.textContent='Gesendet ✓'; setTimeout(()=>knopf.textContent='Erneut schicken',2500); return; }
      markiere(loesung()); freigeben(el,{zuordnung:loesung()}); });
    el._loesung=()=>({zuordnung:loesung()});
    el._live=(antworten,frei)=>{
      if(frei&&frei.loesung&&frei.loesung.zuordnung&&TN) markiere(frei.loesung.zuordnung);
      if(!antworten||!antworten.length||(TN&&!frei)){ lv.innerHTML=''; return; }
      const l=TN?(frei&&frei.loesung&&frei.loesung.zuordnung)||{}:loesung(), namen=Object.keys(l); let richtig=0, gesamt=0;
      antworten.forEach(a=>{ if(a&&typeof a==='object') namen.forEach(n=>{ if(a[n]!=null){ gesamt++; if(a[n]===l[n]) richtig++; } }); });
      lv.innerHTML='<b>'+antworten.length+'</b> '+(antworten.length===1?'Einsendung':'Einsendungen')+(gesamt?' · <b>'+pct(richtig,gesamt)+' %</b> der Zuordnungen richtig':'');
    };
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
  /* 8 Wortwolke (ohne Server: nur auf diesem Rechner; mit Server: Begriffe aller Teilnehmer*innen) */
  function wolke(el){
    el.innerHTML='<div class="ia-frage">'+esc(el.dataset.frage||'Ihre Begriffe')+'</div><div class="ia-zeile"><input type="text" maxlength="40" placeholder="Begriff eintippen, Enter"><button class="ia-send">Senden</button>'+(TN?'':'<button class="ia-leer">leeren</button>')+'</div><div class="ia-woerter"></div><div class="ia-live"></div>';
    const inp=el.querySelector('input'), box=el.querySelector('.ia-woerter'), lv=el.querySelector('.ia-live'), z={}, eigene=[];
    const zeig=()=>{ const m=Math.max(1,...Object.values(z)); box.innerHTML=Object.entries(z).sort(()=>Math.random()-.5).map(([w,n])=>'<span style="font-size:'+(22+n/m*46)+'px">'+esc(w)+'</span>').join(''); };
    const schick=()=>{ const w=inp.value.trim(); if(!w) return; inp.value='';
      if(TN){ eigene.push(w); lv.innerHTML='Deine Begriffe: '+eigene.map(esc).join(', '); senden(el,w,true); return; }
      if(live()){ senden(el,w,true); return; } z[w]=(z[w]||0)+1; zeig(); };
    inp.addEventListener('keydown',e=>{ e.stopPropagation(); if(e.key==='Enter') schick(); });
    el.querySelector('.ia-send').addEventListener('click',schick);
    if(!TN) el.querySelector('.ia-leer').addEventListener('click',()=>{ for(const k in z) delete z[k]; zeig(); const l=L(); if(l) l.zuruecksetzen('antworten',el.dataset.id); });
    el._live=(antworten,frei)=>{ if(!antworten||(TN&&!frei)) return; for(const k in z) delete z[k]; antworten.forEach(w=>{ const t=String(w).trim().toLowerCase(); if(t) z[t]=(z[t]||0)+1; }); zeig(); };
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
    const l=L(); const url=el.dataset.url||(l&&l.teilnehmerUrl?l.teilnehmerUrl()+'#'+(sec.dataset.nr||idx):(location.href.split('#')[0]+'#'+idx));
    const q=qrcode(0,'M'); q.addData(url); q.make();
    el.innerHTML=q.createSvgTag({cellSize:6,margin:2,scalable:true})+'<div class="ia-qrt">'+esc(el.dataset.text||(l?'Mitmachen am Handy':'Mit dem Handy öffnen'))+'</div>';
    el.title=url; stop(el);
  }
  /* 11 Ampel-Abstimmung (ohne Server: Handzeichen zählen) */
  function ampel(el){
    const F=['rot','gelb','gruen'], N={rot:'Nein',gelb:'Unentschieden',gruen:'Ja'};
    el.innerHTML='<div class="ia-frage">'+esc(el.dataset.frage||'Wie sehen Sie das?')+'</div><div class="ia-lichter">'+F.map(f=>'<div class="ia-l ia-'+f+'"><button title="'+(TN?N[f]:'eine Stimme dazu')+'">'+(TN?N[f]:'+')+'</button><i></i><b>0</b></div>').join('')+'</div>'+(TN?'':'<button class="ia-reset">↺</button>')+'<div class="ia-erg"></div>';
    const z={rot:0,gelb:0,gruen:0};
    const zeig=()=>{ const m=Math.max(1,z.rot+z.gelb+z.gruen); F.forEach(f=>{ const l=el.querySelector('.ia-'+f); l.querySelector('b').textContent=z[f]; l.querySelector('i').style.height=Math.round(z[f]/m*200)+'px'; }); };
    F.forEach(f=>el.querySelector('.ia-'+f+' button').addEventListener('click',e=>{
      if(TN){ senden(el,f); F.forEach(g=>el.querySelector('.ia-'+g+' button').classList.toggle('gewaehlt',g===f)); el.querySelector('.ia-erg').textContent='Gesendet ✓'; return; }
      if(live()) return; z[f]++; zeig(); }));
    if(!TN) el.querySelector('.ia-reset').addEventListener('click',()=>{ z.rot=z.gelb=z.gruen=0; zeig(); const l=L(); if(l) l.zuruecksetzen('antworten',el.dataset.id); });
    el._live=(antworten,frei)=>{ if(!antworten||(TN&&!frei)) return; el.classList.add('frei'); z.rot=z.gelb=z.gruen=0; antworten.forEach(v=>{ if(z[v]!=null) z[v]++; }); zeig(); };
    zeig(); stop(el);
  }
  const BAU={'ia-schaetz':schaetz,'ia-vergleich':vergleich,'ia-ausschnitt':ausschnitt,'ia-quiz':quiz,'ia-umfrage':umfrage,'ia-sort':sort,'ia-timer':timer,'ia-rad':rad,'ia-wolke':wolke,'ia-karte':karte,'ia-qr':qr,'ia-ampel':ampel};
  function init(root){ Object.entries(BAU).forEach(([k,f])=>root.querySelectorAll('#stage .'+k+':not(.ia-fertig)').forEach(el=>{ try{ f(el); el.classList.add('ia-fertig'); }catch(e){ console.warn(k,e); } })); }
  init(document);
  window.qpBausteine={init,LIVE_TYPEN:['ia-schaetz','ia-quiz','ia-umfrage','ia-sort','ia-wolke','ia-ampel']};

  /* 12 Spotlight (Taste X) */
  const spot=$('div',''); spot.id='spot'; document.body.appendChild(spot);
  document.addEventListener('mousemove',e=>{ spot.style.setProperty('--x',e.clientX+'px'); spot.style.setProperty('--y',e.clientY+'px'); });
  document.addEventListener('keydown',e=>{ if(e.target.tagName==='INPUT'||e.target.tagName==='TEXTAREA') return; if(e.key==='x'||e.key==='X') spot.classList.toggle('on'); if(e.key==='Escape') spot.classList.remove('on'); });
  document.addEventListener('wheel',e=>{ if(!spot.classList.contains('on')) return; const r=parseFloat(getComputedStyle(spot).getPropertyValue('--r'))||180; spot.style.setProperty('--r',Math.max(60,Math.min(600,r-e.deltaY*.3))+'px'); },{passive:true});
})();
