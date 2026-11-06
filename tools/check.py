#!/usr/bin/env python3
"""Validate public artifact and editorial inventory without network access."""
import json,re,hashlib
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
ROOT=Path(__file__).resolve().parents[1];SITE=ROOT/'site';manifest=json.loads((SITE/'build-manifest.json').read_text());base=manifest['base_path'];errors=[];refs=0
class Parser(HTMLParser):
 def __init__(self):super().__init__();self.refs=[];self.ids=set();self.h1=0;self.lang=None
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:
   if a['id'] in self.ids:errors.append('duplicate id '+a['id'])
   self.ids.add(a['id'])
  if tag=='h1':self.h1+=1
  if tag=='html':self.lang=a.get('lang')
  for key in ('href','src','poster'):
   if a.get(key):self.refs.append((tag,key,a[key]))
parsers={}
for rel in manifest['pages']:
 f=SITE/rel;s=f.read_text();p=Parser();p.feed(s);parsers[rel]=p
 if p.h1!=1:errors.append(f'{rel}: expected one h1, got {p.h1}')
 if not p.lang:errors.append(f'{rel}: missing language')
 if re.search(r'<script[^>]+src="https?://',s):errors.append(f'{rel}: automatic third-party script')
 if '<iframe' in s:errors.append(f'{rel}: automatic iframe')
 if manifest['noindex'] and rel!='404.html' and 'noindex, nofollow' not in s:errors.append(f'{rel}: noindex missing')
 for tag,key,v in p.refs:
  u=urlsplit(v)
  if u.scheme or u.netloc:continue
  if not u.path:dest=f
  elif base and not u.path.startswith(base+'/'):errors.append(f'{rel}: wrong base {v}');continue
  else:dest=SITE/unquote(u.path[len(base):].lstrip('/'))
  if dest.is_dir():dest=dest/'index.html'
  if not dest.is_file():errors.append(f'{rel}: missing {v}')
  refs+=1
for rel,p in parsers.items():
 for tag,key,v in p.refs:
  u=urlsplit(v)
  if u.scheme or u.netloc or not u.fragment:continue
  dest=rel if not u.path else (unquote(u.path[len(base):].lstrip('/')).rstrip('/')+'/index.html').lstrip('/')
  if dest in parsers and unquote(u.fragment) not in parsers[dest].ids:errors.append(f'{rel}: missing anchor {v}')
vid=json.loads((ROOT/'content/videos.json').read_text())
assert len(vid)>0 and len({v['id'] for v in vid})==len(vid)==manifest['videos']
assert all(re.fullmatch(r'[A-Za-z0-9_-]{11}',v['id']) and v['position']==i+1 for i,v in enumerate(vid))
assert len(manifest['pages'])==49
publications=json.loads((ROOT/'content/publication-assets.json').read_text())
assert len(publications)==manifest['publications']==6
assert all(len(d['books'])==len(publications) for d in json.loads((ROOT/'content/publications.json').read_text()).values())
for f in SITE.rglob('*'):
 if f.is_file() and f.suffix in {'.html','.js','.json','.css'}:
  s=f.read_text()
  if re.search(r'gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}|sk-proj-[A-Za-z0-9_-]+|BEGIN [A-Z ]*PRIVATE KEY|/root/\.openclaw|libfile_[a-f0-9]+',s):errors.append(f'sensitive pattern {f.relative_to(SITE)}')
assert not (SITE/'CNAME').exists()
assert not (SITE/'content').exists()
if errors:raise SystemExit('\n'.join(errors[:30]))
files=[f for f in SITE.rglob('*') if f.is_file()]
print(json.dumps({'pages':len(parsers),'local_refs':refs,'files':len(files),'bytes':sum(f.stat().st_size for f in files),'video_records':len(vid),'ok':True}))
