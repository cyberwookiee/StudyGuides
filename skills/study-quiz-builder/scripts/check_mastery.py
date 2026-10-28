#!/usr/bin/env python3
"""Check a mastery-mode quiz page before publishing.

Usage: python3 check_mastery.py path/to/index.html [--variants 400]

1. Answer keys: builds every fixed question and many variants of every generator, and confirms
   the answer key grades as correct, an obvious wrong answer grades as wrong, every accepted
   interval form passes, multiple choice has 3+ distinct options, and no text shows
   undefined/NaN/sign glitches.
2. Flow: plays the quiz as a student who is always right (each topic mastered after RULES.streak
   questions), always wrong (each topic stops at RULES.max and is marked for practice), then
   practices the missed topics; checks a draft and a checked answer survive a reload.
3. Layout: no sideways scrolling at 320, 390 and 768 px wide; no script errors.

Needs Playwright with Chromium. Exits non-zero on any failure.
"""
import argparse, functools, http.server, os, sys, threading
from playwright.sync_api import sync_playwright

ap = argparse.ArgumentParser(); ap.add_argument('page'); ap.add_argument('--variants', type=int, default=400)
args = ap.parse_args()
page_path = os.path.abspath(args.page)
class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
handler = functools.partial(Quiet, directory=os.path.dirname(page_path))
srv = http.server.ThreadingHTTPServer(('127.0.0.1', 0), handler)
threading.Thread(target=srv.serve_forever, daemon=True).start()
URL = f'http://127.0.0.1:{srv.server_port}/{os.path.basename(page_path)}'
fails = []

KEYS_JS = '''(V)=>{const {make,grade,TOPICS}=window.quiz;const bad=[];let count=0;
  const key=q=>q.t==='mc'?String(q.a):q.t==='tf'?(q.a?'0':'1'):q.ans;
  const wrong=q=>q.t==='mc'?String((q.a+1)%q.o.length):q.t==='tf'?(q.a?'1':'0'):q.t==='num'?String(q.a+1)
    :q.t==='nums'?q.a.map(x=>x+1).join(','):q.t==='interval'?'(0,0)':q.t==='expr'?'y=x+1000':'zzzz';
  TOPICS.forEach((T,ti)=>{const refs=[];
    (T.qs||[]).forEach((_,i)=>{for(let s=1;s<=10;s++)refs.push({ti,src:'s',idx:i,seed:s*977});});
    (T.gen||[]).forEach((_,i)=>{for(let s=1;s<=V;s++)refs.push({ti,src:'g',idx:i,seed:(s*2654435761)>>>0});});
    if(!refs.length)bad.push([T.name,'topic has no questions']);
    refs.forEach(ref=>{count++;let q;const tag=`${T.name} / ${ref.src==='s'?'fixed':'generator'} #${ref.idx} (seed ${ref.seed})`;
      try{q=make(ref);}catch(e){bad.push([tag,'throws: '+e.message]);return;}
      if(!grade(q,key(q)))bad.push([tag,'answer key grades wrong',key(q)]);
      if(grade(q,wrong(q)))bad.push([tag,'wrong answer grades right',wrong(q)]);
      if(q.t==='interval'&&!q.acc.every(a=>grade(q,a)))bad.push([tag,'an accepted form fails',q.acc]);
      if(q.t==='mc'){if(q.o.length<3)bad.push([tag,'fewer than 3 options']);if(new Set(q.o).size!==q.o.length)bad.push([tag,'duplicate options']);}
      const txt=[q.q,...(q.o||[]),q.ex,q.ans||''].join(' | ').replace(/<[^>]+>/g,' ');
      if(/undefined|NaN|\\+ −|− −|\\+ -|(^|[^0-9.])1x|(^|[^0-9.])1\\(|−1x|−1\\(/.test(txt))bad.push([tag,'formatting glitch',txt.slice(0,200)]);
      if(!q.ex)bad.push([tag,'missing explanation']);});});
  const gens=TOPICS.map(T=>(T.gen||[]).length),fixed=TOPICS.map(T=>(T.qs||[]).length);
  return {count,bad,gens,fixed,rules:RULES};}'''

def answer(pg, correct):
    q = pg.evaluate('()=>{const q=window.quiz.question();return {t:q.t,a:q.a,ans:q.ans,n:(q.o||[]).length}}')
    if q['t'] in ('mc', 'tf'):
        right = q['a'] if q['t'] == 'mc' else (0 if q['a'] else 1)
        pg.click(f'label[data-j="{right if correct else (right + 1) % (q["n"] or 2)}"]')
    else:
        pg.fill('#ans', q['ans'] if correct else '999999')
    pg.click('#checkBtn')

def play(pg, correct, limit=2000):
    k = 0
    while k < limit and pg.locator('#nextBtn, #checkBtn').count():
        if pg.locator('#checkBtn').count():
            answer(pg, correct); k += 1
        pg.click('#nextBtn')
    return k

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': 390, 'height': 844}); errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto(URL); pg.wait_for_selector('#checkBtn')
    pg.evaluate('localStorage.clear()'); pg.reload(); pg.wait_for_selector('#checkBtn')

    r = pg.evaluate(KEYS_JS, args.variants)
    print(f"Answer keys: {r['count']} questions checked; generators per topic {r['gens']}, fixed per topic {r['fixed']}; rules {r['rules']}")
    for x in r['bad'][:25]: print('  FAIL', x)
    if r['bad']: fails.append(f"{len(r['bad'])} answer-key problems")
    for i, (g, f) in enumerate(zip(r['gens'], r['fixed'])):
        if g == 0 and f < 8: print(f'  WARN topic {i + 1} has only {f} fixed questions and no generator; misses will repeat often')

    T, streak, mx = len(r['gens']), r['rules']['streak'], r['rules']['max']
    n = play(pg, True); st = pg.evaluate('window.quiz.state()')
    ok = n == T * streak and all(t['status'] == 'mastered' for t in st['topics'])
    print(f'Always right: {n} questions (expected {T * streak}) -> {"ok" if ok else "FAIL"}')
    if not ok: fails.append('always-right flow')
    pg.click('#restartBtn'); n = play(pg, False); st = pg.evaluate('window.quiz.state()')
    asked = [t['asked'] for t in st['topics']]
    ok = all(t['status'] == 'review' for t in st['topics']) and pg.locator('#againBtn').count() == 1
    print(f'Always wrong: {n} questions, per topic {asked} (cap {mx}) -> {"ok" if ok else "FAIL"}')
    if any(a < mx for a in asked): print(f'  WARN some topics ran out of questions before {mx}; add a generator or more fixed questions')
    if not ok: fails.append('always-wrong flow')
    pg.click('#againBtn'); n = play(pg, True); st = pg.evaluate('window.quiz.state()')
    ok = all(t['status'] == 'mastered' for t in st['topics'])
    print(f'Practice round: {n} questions -> {"ok" if ok else "FAIL"}')
    if not ok: fails.append('practice-again flow')

    pg.click('#restartBtn'); q = pg.evaluate('window.quiz.question().q')
    if pg.locator('#ans').count(): pg.fill('#ans', '12')
    else: pg.click('label[data-j="0"]')
    pg.reload(); pg.wait_for_selector('#checkBtn')
    kept = pg.input_value('#ans') == '12' if pg.locator('#ans').count() else pg.locator('input[name=ans]:checked').count() == 1
    ok1 = pg.evaluate('window.quiz.question().q') == q and kept
    answer(pg, False); pg.reload(); pg.wait_for_selector('#nextBtn')
    ok2 = pg.locator('.q.done').count() == 1
    print(f'Resume after reload: draft {"ok" if ok1 else "FAIL"}, checked answer {"ok" if ok2 else "FAIL"}')
    if not (ok1 and ok2): fails.append('resume')

    for w in (320, 390, 768):
        pg.set_viewport_size({'width': w, 'height': 844}); pg.wait_for_timeout(100)
        if pg.evaluate('document.documentElement.scrollWidth>innerWidth'):
            fails.append(f'sideways scroll at {w}px'); print(f'Layout: sideways scroll at {w}px -> FAIL')
    if errs: fails.append('script errors'); print('Script errors:', errs[:5])
    pg.evaluate('localStorage.clear()')
    b.close()

srv.shutdown()
print('\nRESULT:', 'PASS' if not fails else 'FAIL: ' + '; '.join(fails))
sys.exit(1 if fails else 0)
