"""Notizschutz für das Webpaket: Sprechernotizen erst nach PIN-Eingabe.

deploy.py ruft das Modul auf, wenn quality_point.json einen Abschnitt „notizschutz“ hat:
    "notizschutz": {"bis": "2027-03-01"}            Stichtag optional; ab dann bleibt das Paket unverschlüsselt
Die PIN kommt aus der Umgebungsvariable QP_NOTIZ_PIN (empfohlen – steht so in keiner Datei).
Ersatzweise "pin": "…" im Abschnitt – dann liegt sie im Projektordner, also nicht in ein öffentliches Repo legen.

Was passiert (nur in der Kopie im Veröffentlichungsordner, das Projekt bleibt unverändert):
- <aside class="notes">, data-zweck und data-pointe werden aus allen Folien entfernt,
- zusammen als JSON mit AES-256-GCM verschlüsselt (Schlüssel per PBKDF2-SHA256 aus der PIN) und angehängt,
- N, P, S, V und die Notiz-Schaltflächen öffnen zuerst eine PIN-Abfrage; danach setzt das Skript die Notizen ein
  (Ereignis „qp-notizen“ an die Engine) und merkt sich die Freischaltung für den Browser-Tab (sessionStorage).
Grenzen: Eine kurze PIN hält Neugierige ab, nicht jemanden, der gezielt alle Kombinationen durchprobiert.
Ein Stichtag kann sich nicht selbst „aufsperren“, ohne den Schlüssel mitzuliefern – nach dem Stichtag neu veröffentlichen.
Benötigt: cryptography (pip install cryptography).
"""
import base64, datetime, html, json, os, re, sys

RUNDEN = 250000

SKRIPT = r'''<script>
/* Notizschutz (Quality Point): Notizen erst nach PIN */
(function(){
  var PAKET=__PAKET__, MERK='qp-notizschutz', frei=false, nachher=null;
  function bytes(b64){ return Uint8Array.from(atob(b64),function(c){return c.charCodeAt(0);}); }
  function oeffnen(pin){
    return crypto.subtle.importKey('raw',new TextEncoder().encode(pin),'PBKDF2',false,['deriveKey'])
      .then(function(roh){ return crypto.subtle.deriveKey({name:'PBKDF2',salt:bytes(PAKET.salz),iterations:PAKET.runden,hash:'SHA-256'},roh,{name:'AES-GCM',length:256},false,['decrypt']); })
      .then(function(k){ return crypto.subtle.decrypt({name:'AES-GCM',iv:bytes(PAKET.iv)},k,bytes(PAKET.daten)); })
      .then(function(klar){ return JSON.parse(new TextDecoder().decode(klar)); });
  }
  function einsetzen(N){
    var folien=document.querySelectorAll('#stage > section.slide, section.slide');
    Object.keys(N).forEach(function(i){
      var s=folien[+i], n=N[i]; if(!s) return;
      if(n.z) s.dataset.zweck=n.z; if(n.p) s.dataset.pointe=n.p;
      if(n.n){ var a=document.createElement('aside'); a.className='notes'; a.innerHTML=n.n; s.appendChild(a); }
    });
    frei=true; document.dispatchEvent(new Event('qp-notizen'));
  }
  function versuchen(pin){
    return oeffnen(pin).then(function(N){ einsetzen(N); try{ sessionStorage.setItem(MERK,pin); }catch(e){} return true; }, function(){ return false; });
  }
  function abfrage(){
    var box=document.getElementById('qpNs');
    if(!box){
      box=document.createElement('div'); box.id='qpNs';
      box.style.cssText='position:fixed;inset:0;z-index:300;display:flex;align-items:center;justify-content:center;background:rgba(0,0,0,.6)';
      box.innerHTML='<form style="background:var(--card,#fff);color:var(--ink,#111);font:500 18px/1.45 var(--ui,system-ui,sans-serif);padding:26px 30px;border-radius:14px;width:min(380px,90vw);box-shadow:0 24px 60px rgba(0,0,0,.45)">'
        +'<div style="font-weight:700;font-size:21px">Notizen für Vortragende</div>'
        +'<p style="margin:4px 0 14px;font-size:15px;opacity:.75">Die Sprechernotizen sind geschützt. Bitte PIN eingeben.</p>'
        +'<input name="pin" type="password" autocomplete="off" aria-label="PIN" style="width:100%;box-sizing:border-box;font:600 22px var(--ui,system-ui);padding:9px 12px;border:2px solid #9a9a9a;border-radius:9px">'
        +'<div class="m" role="status" style="min-height:1.5em;margin-top:6px;font-size:15px;color:#b3261e"></div>'
        +'<div style="display:flex;justify-content:flex-end;gap:10px;margin-top:6px">'
        +'<button type="button" class="z" style="font:600 16px var(--ui,system-ui);padding:8px 14px;border-radius:9px;border:1px solid #9a9a9a;background:none;color:inherit;cursor:pointer">Abbrechen</button>'
        +'<button type="submit" style="font:600 16px var(--ui,system-ui);padding:8px 14px;border-radius:9px;border:0;background:var(--teal,#1F5F5B);color:#fff;cursor:pointer">Freischalten</button></div></form>';
      document.body.appendChild(box);
      var f=box.querySelector('form'), feld=f.pin, meldung=box.querySelector('.m');
      function zu(){ box.style.display='none'; nachher=null; feld.value=''; meldung.textContent=''; }
      feld.addEventListener('keydown',function(e){ e.stopPropagation(); if(e.key==='Escape') zu(); });
      box.querySelector('.z').addEventListener('click',zu);
      f.addEventListener('submit',function(e){
        e.preventDefault(); meldung.textContent='Prüfe …';
        versuchen(feld.value.trim()).then(function(ok){
          if(!ok){ meldung.textContent='PIN stimmt nicht.'; feld.select(); return; }
          var aktion=nachher; zu(); if(aktion) aktion();
        });
      });
    }
    box.style.display='flex'; box.querySelector('input').focus();
  }
  var TASTEN={n:'bN',p:'bW',s:'bS',v:null};
  window.addEventListener('keydown',function(e){
    if(frei||e.ctrlKey||e.metaKey||e.altKey) return;
    var t=e.target; if(t&&(t.tagName==='INPUT'||t.tagName==='TEXTAREA'||t.isContentEditable)) return;
    var k=(e.key||'').toLowerCase(); if(!(k in TASTEN)) return;
    e.preventDefault(); e.stopImmediatePropagation();
    var taste=e.key; nachher=function(){ document.dispatchEvent(new KeyboardEvent('keydown',{key:taste,bubbles:true})); };
    abfrage();
  },true);
  window.addEventListener('click',function(e){
    if(frei) return; var b=e.target.closest&&e.target.closest('#bN,#bW,#bS'); if(!b) return;
    e.preventDefault(); e.stopImmediatePropagation(); nachher=function(){ b.click(); }; abfrage();
  },true);
  var gemerkt=null; try{ gemerkt=sessionStorage.getItem(MERK); }catch(e){}
  if(gemerkt) window.addEventListener('load',function(){ versuchen(gemerkt); });
})();
</script>
'''


def pin_aus(cfg):
    return os.environ.get('QP_NOTIZ_PIN') or str((cfg or {}).get('pin') or '')


def aktiv(cfg, heute=None):
    """True, wenn verschlüsselt werden soll: Abschnitt vorhanden, PIN da, Stichtag (falls gesetzt) noch nicht erreicht."""
    if not cfg or not pin_aus(cfg):
        return False
    bis = cfg.get('bis')
    return not bis or (heute or datetime.date.today()) < datetime.date.fromisoformat(bis)


def schuetzen(datei, pin):
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

    seite = open(datei, encoding='utf-8').read()
    notizen, nr = {}, [-1]

    def folie(m):
        nr[0] += 1
        kopf, inhalt, eintrag = m.group(1), m.group(2), {}
        for attr, kurz in (('data-zweck', 'z'), ('data-pointe', 'p')):
            a = re.search(r'\s%s="([^"]*)"' % attr, kopf)
            if a:
                eintrag[kurz] = html.unescape(a.group(1)); kopf = kopf.replace(a.group(0), '', 1)
        teile = re.findall(r'<aside class="notes">(.*?)</aside>', inhalt, flags=re.S)
        if teile:
            eintrag['n'] = '\n'.join(teile)
            inhalt = re.sub(r'\s*<aside class="notes">.*?</aside>', '', inhalt, flags=re.S)
        if eintrag:
            notizen[str(nr[0])] = eintrag
        return kopf + inhalt + '</section>'

    neu = re.sub(r'(<section class="slide[^"]*"[^>]*>)(.*?)</section>', folie, seite, flags=re.S)
    if not notizen:
        print('Notizschutz: keine Notizen gefunden'); return 0
    salz, iv = os.urandom(16), os.urandom(12)
    schluessel = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salz, iterations=RUNDEN).derive(pin.encode('utf-8'))
    daten = AESGCM(schluessel).encrypt(iv, json.dumps(notizen, ensure_ascii=False).encode('utf-8'), None)
    b64 = lambda b: base64.b64encode(b).decode('ascii')
    skript = SKRIPT.replace('__PAKET__', json.dumps({'salz': b64(salz), 'iv': b64(iv), 'runden': RUNDEN, 'daten': b64(daten)}))
    rest = len(re.findall(r'<aside class="notes"|\sdata-zweck=|\sdata-pointe=', neu))
    if rest:
        sys.exit('Notizschutz: %d Notizreste in %s – Abbruch, nichts veröffentlichen' % (rest, datei))
    ende = neu.rfind('</body>')          # das letzte – die Engine enthält '</body>' auch in Zeichenketten (Referentenfenster)
    neu = neu[:ende] + skript + neu[ende:] if ende >= 0 else neu + skript
    open(datei, 'w', encoding='utf-8').write(neu)
    print('Notizschutz: Notizen von %d Folien verschlüsselt (%s)' % (len(notizen), os.path.basename(datei)))
    return len(notizen)


if __name__ == '__main__':          # Einzelaufruf: python notizschutz.py <html-datei>   (PIN aus QP_NOTIZ_PIN)
    p = os.environ.get('QP_NOTIZ_PIN')
    if len(sys.argv) < 2 or not p:
        sys.exit('Aufruf: QP_NOTIZ_PIN=… python notizschutz.py <html-datei>')
    schuetzen(sys.argv[1], p)
