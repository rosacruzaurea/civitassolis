#!/usr/bin/env python3
"""Generate static HTML. Python standard library only; no browser framework."""
import os,json,html,shutil,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'site'
BASE='/' + os.environ.get('BASE_PATH','/civitassolis').strip('/') if os.environ.get('BASE_PATH','/civitassolis').strip('/') else ''
NOINDEX=os.environ.get('SITE_NOINDEX','0')=='1'
ORIGIN=os.environ.get('SITE_ORIGIN','https://rosacruzaurea.github.io').rstrip('/')
LANGS={'pt':('Português','br'),'en':('English','us'),'es':('Español','es'),'fr':('Français','fr'),'de':('Deutsch','de'),'it':('Italiano','it')}
ROUTES=['','missao-visao-valores','publicacoes','youtube','instagram','contato','trabalho-global','livro']
def load(name):return json.loads((ROOT/'content'/name).read_text())
PAGES=load('pages.json');TRANS=load('translations.json');PUB=load('publications.json');PA=load('publication-assets.json');GLOBAL=load('global.json');VIDEOS=load('videos.json')
UI={
'pt':{'menu':'Menu','skip':'Ir para o conteúdo','play':'Reproduzir vídeo','close':'Fechar','previous':'Anterior','next':'Próxima','page':'Página','of':'de','search':'Buscar vídeos','clear':'Limpar busca','empty':'Nenhum vídeo encontrado.','load':'Carregar perfil do Instagram','external':'Ao carregar, seu navegador se conecta ao Instagram.','contact':'Fale com o Instituto pelos canais oficiais.','mail':'Abrir aplicativo de e-mail','email':'E-mail','subject':'Assunto','message':'Mensagem','mailNote':'O envio é feito no seu aplicativo de e-mail. Este site não armazena nem envia sua mensagem.','pause':'Pausar imagens','resume':'Retomar imagens'},
'en':{'menu':'Menu','skip':'Skip to content','play':'Play video','close':'Close','previous':'Previous','next':'Next','page':'Page','of':'of','search':'Search videos','clear':'Clear search','empty':'No videos found.','load':'Load Instagram profile','external':'Loading connects your browser to Instagram.','contact':'Contact the Institute through its official channels.','mail':'Open email application','email':'Email','subject':'Subject','message':'Message','mailNote':'Your email application handles sending. This website does not store or send your message.','pause':'Pause images','resume':'Resume images'},
'es':{'menu':'Menú','skip':'Ir al contenido','play':'Reproducir vídeo','close':'Cerrar','previous':'Anterior','next':'Siguiente','page':'Página','of':'de','search':'Buscar vídeos','clear':'Limpiar búsqueda','empty':'No se encontraron vídeos.','load':'Cargar contenido de Instagram','external':'Al cargar, el navegador se conecta al servicio externo.','contact':'Contacta con el Instituto por sus canales oficiales.','mail':'Abrir aplicación de correo','email':'Correo','subject':'Asunto','message':'Mensaje','mailNote':'El envío se realiza en tu aplicación de correo. Este sitio no almacena ni envía mensajes.','pause':'Pausar imágenes','resume':'Reanudar imágenes'},
'fr':{'menu':'Menu','skip':'Aller au contenu','play':'Lire la vidéo','close':'Fermer','previous':'Précédente','next':'Suivante','page':'Page','of':'sur','search':'Rechercher des vidéos','clear':'Effacer la recherche','empty':'Aucune vidéo trouvée.','load':'Charger le profil Instagram','external':'Le chargement connecte votre navigateur au service externe.','contact':'Contactez l’Institut par ses canaux officiels.','mail':'Ouvrir la messagerie','email':'E-mail','subject':'Objet','message':'Message','mailNote':'Votre messagerie assure l’envoi. Ce site ne conserve ni n’envoie votre message.','pause':'Mettre les images en pause','resume':'Reprendre les images'},
'de':{'menu':'Menü','skip':'Zum Inhalt','play':'Video abspielen','close':'Schließen','previous':'Zurück','next':'Weiter','page':'Seite','of':'von','search':'Videos suchen','clear':'Suche löschen','empty':'Keine Videos gefunden.','load':'Instagram-Profil laden','external':'Beim Laden verbindet sich Ihr Browser mit dem externen Dienst.','contact':'Kontaktieren Sie das Institut über seine offiziellen Kanäle.','mail':'E-Mail-Programm öffnen','email':'E-Mail','subject':'Betreff','message':'Nachricht','mailNote':'Der Versand erfolgt in Ihrem E-Mail-Programm. Diese Website speichert oder versendet Ihre Nachricht nicht.','pause':'Bilder pausieren','resume':'Bilder fortsetzen'},
'it':{'menu':'Menu','skip':'Vai al contenuto','play':'Riproduci video','close':'Chiudi','previous':'Precedente','next':'Successiva','page':'Pagina','of':'di','search':'Cerca video','clear':'Cancella ricerca','empty':'Nessun video trovato.','load':'Carica il profilo Instagram','external':'Il caricamento collega il browser al servizio esterno.','contact':'Contatta l’Istituto attraverso i canali ufficiali.','mail':'Apri l’applicazione email','email':'Email','subject':'Oggetto','message':'Messaggio','mailNote':'L’invio avviene nella tua applicazione email. Questo sito non conserva né invia il messaggio.','pause':'Pausa immagini','resume':'Riprendi immagini'} }
def esc(s):return html.escape(str(s),quote=True)
def asset(p):return BASE+'/'+p.lstrip('/')
def url(route='',lang='pt'):return BASE+'/' + (lang+'/' if lang!='pt' else '') + (route.strip('/')+'/' if route else '')
def tr(s,l):return TRANS.get(l,{}).get(s,s)
def para(s,l):return '<p>'+esc(tr(s,l))+'</p>'
def img(p,alt='',cls='',lazy=True):return f'<img src="{esc(asset(p))}" alt="{esc(alt)}" class="{cls}"'+(' loading="lazy"' if lazy else ' fetchpriority="high"')+' decoding="async">'
def link(href,text,cls='button',external=False):return f'<a class="{cls}" href="{esc(href)}"'+(' target="_blank" rel="noopener noreferrer"' if external else '')+'>'+esc(text)+('</a>')
def icon(name):
 paths={'art':'M5 20l14-14M12 5l7 7M4 20l4-1-3-3-1 4','spirit':'M12 3l3 6 6 3-6 3-3 6-3-6-6-3 6-3 3-6','science':'M9 3v7l-5 9a1 1 0 001 2h14a1 1 0 001-2l-5-9V3M8 3h8M7 15h10','book':'M3 4h7l2 2 2-2h7v16h-7l-2 1-2-1H3V4M12 6v15','chat':'M4 4h16v13H9l-5 4V4','globe':'M3 12h18M12 3a9 9 0 100 18 9 9 0 000-18M12 3c-6 5-6 13 0 18 6-5 6-13 0-18'}
 return f'<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="{paths[name]}"/></svg>'
def nav(l,r):
 names=['Home','Missão, Visão e Valores','Publicações','YouTube','Instagram','Contato'];routes=ROUTES[:6]
 return ''.join(f'<a href="{url(p,l)}"'+(' aria-current="page"' if p==r else '')+'>'+esc(PUB[l]['eyebrow'].split(' Civitas')[0] if p=='publicacoes' else tr(n,l))+'</a>' for n,p in zip(names,routes))
def header(l,r):
 choices=''.join(f'<a href="{url(r,k)}" lang="{k}" hreflang="{k}"'+(' aria-current="true"' if k==l else '')+'>'+'<span class="language-code">'+v[1].upper()+'</span>'+esc(v[0])+'</a>' for k,v in LANGS.items())
 return f'''<a class="skip" href="#conteudo">{UI[l]['skip']}</a><header class="site-header"><div class="header-inner"><a class="brand" href="{url('',l)}">{img('assets/logo.png','',lazy=False)}<span><strong>{esc(tr('Instituto Civitas Solis',l))}</strong><small>{esc(tr('Arte • Espiritualidade • Ciência',l))}</small></span></a><button class="menu-toggle js-only" aria-expanded="false" aria-controls="menu-principal">☰ <span>{UI[l]['menu']}</span></button><nav id="menu-principal" class="main-nav" aria-label="{UI[l]['menu']}">{nav(l,r)}</nav><details class="language"><summary><span class="language-code">{LANGS[l][1].upper()}</span>{LANGS[l][0]} <span aria-hidden="true">⌄</span></summary><div>{choices}</div></details></div></header>'''
def footer(l,r):
 return f'''<footer><div class="footer-grid wrap"><div><a class="brand" href="{url('',l)}">{img('assets/logo.png')}<strong>{esc(tr('Instituto Civitas Solis',l))}</strong></a>{para('Arte, Espiritualidade e Ciência para uma Nova Consciência.',l)}</div><div><h2>{UI[l]['menu']}</h2><nav>{nav(l,r)}</nav></div><div><h2>{esc(tr('Siga-nos',l))}</h2><nav>{link('https://www.instagram.com/institutocivitassolis/','Instagram','',True)}{link('https://www.youtube.com/@institutocivitassolis5117','YouTube','',True)}{link('https://www.facebook.com/institutocivitassolis','Facebook','',True)}</nav></div></div><p class="copyright">© 2026 {esc(tr('Instituto Civitas Solis',l))}</p></footer>'''
def hero(title,desc,l,tone='warm',extra=''):
 return f'<section class="page-hero {tone}"><div class="wrap narrow"><h1>{esc(tr(title,l))}</h1>{para(desc,l) if desc else ""}{extra}</div></section>'
def globals_section(l):
 data=GLOBAL[l];base=GLOBAL['pt']['items'];cards=[];panels=[]
 for i,item in enumerate(data['items']):
  cards.append(f'<article class="global-card">{icon(["book","chat","globe"][i])}<h3>{esc(item["title"])}</h3><p>{esc(item["body"])}</p><button class="text-button js-only" data-panel="panel-{i}" aria-controls="panel-{i}" aria-expanded="false">{esc(data["more"])}</button></article>')
  media=''.join(img(p,item['title']+' '+str(n+1)).replace('<img ', '<img tabindex="0" ') for n,p in enumerate(base[i]['images']))
  panels.append(f'<section class="global-panel" id="panel-{i}" data-global-panel><div class="panel-media count-{len(base[i]["images"])}">{media}</div><div><h3>{esc(item["title"])}</h3><p>{esc(item["detail"])}</p>'+ (link(url('publicacoes',l),PUB[l]['title'],'text-link') if i==0 else '')+'</div></section>')
 return f'<section id="trabalho-global" class="section soft"><div class="wrap"><h2 class="center">{esc(tr("Trabalho Global",l))}</h2><div class="grid three">'+''.join(cards)+'</div>'+''.join(panels)+'</div></section>'
def video_card(v,l):
 return f'''<article class="video-card" data-video-card data-title="{esc(v['title'])}"><div class="video-thumb">{link(v['url'],'','video-image',True)[:-4]}{img('assets/videos/'+v['id']+'.jpg',v['title'])}</a><button class="play js-only" data-video="{v['id']}" data-video-title="{esc(v['title'])}" aria-label="{UI[l]['play']}: {esc(v['title'])}">▶</button><span class="duration">{esc(v['duration'])}</span></div><h3>{link(v['url'],v['title'],'',True)}</h3></article>'''
def gallery(l):
 controls=f'<div class="gallery-tools js-only"><label>{UI[l]["search"]}<input type="search" data-video-search></label><button class="button secondary" data-video-clear>{UI[l]["clear"]}</button></div>'
 return f'''<div class="gallery" data-gallery data-page-label="{UI[l]['page']}" data-of-label="{UI[l]['of']}">{img('assets/channel-cover.jpg','','channel-cover')}<div class="channel">{img('assets/logo.png')}<div><h3>Instituto Civitas Solis</h3><p>@institutocivitassolis5117</p></div>{link('https://www.youtube.com/@institutocivitassolis5117/videos','YouTube ↗','text-link',True)}</div>{controls}<div class="video-grid">{''.join(video_card(v,l) for v in VIDEOS)}</div><p class="gallery-empty" hidden>{UI[l]['empty']}</p><nav class="gallery-pagination js-only" aria-label="{UI[l]['page']}"><button class="button secondary" data-prev>{UI[l]['previous']}</button><span role="status" data-page-status></span><button class="button secondary" data-next>{UI[l]['next']}</button></nav></div>'''
def contact(l,compact=False):
 # The reference form has no send backend. This preserves contact intent via public official profiles.
 return f'''<section class="section soft"><div class="wrap narrow"><div class="contact-card"><h2>{esc(tr('Entre em Contato',l))}</h2><p>{UI[l]['contact']}</p><div class="actions">{link('https://www.instagram.com/institutocivitassolis/','Instagram','button',True)}{link('https://www.facebook.com/institutocivitassolis','Facebook','button secondary',True)}{link('https://www.youtube.com/@institutocivitassolis5117','YouTube','button secondary',True)}</div></div></div></section>'''
def home(l):
 s=PAGES['gy']['text'];slides=''.join(img('assets/hero-'+str(i)+'.jpg','','hero-image'+(' active' if i==1 else '')) for i in range(1,6))
 controls=''.join(f'<button data-slide="{i}" aria-label="{i+1}" aria-pressed="{str(i==0).lower()}"></button>' for i in range(5))
 h=f'''<section class="home-hero">{slides}<div class="hero-shade"></div><div class="hero-copy wrap"><h1>{esc(tr(s[0],l))}</h1><p>{esc(tr(s[1],l))}</p><div class="actions">{link(url('missao-visao-valores',l),tr(s[2],l))}{link('#trabalho-global',tr(s[3],l),'button secondary')}</div></div><div class="slide-controls js-only">{controls}<button class="pause" data-pause data-resume="{UI[l]['resume']}" data-pause-label="{UI[l]['pause']}">{UI[l]['pause']}</button></div></section>'''
 org=f'<section class="section"><div class="wrap narrow center"><h2>{esc(tr(s[4],l))}</h2>'+''.join(para(t,l) for t in s[5:8])+f'<div class="organization-video"><button class="video-poster js-only" data-video="-nEZsZAjCrk" data-video-title="Instituto Civitas Solis - Objetivos Institucionais">{img("assets/channel-cover.jpg")}<span>▶ {UI[l]["play"]}</span></button>{link("https://www.youtube.com/watch?v=-nEZsZAjCrk","Instituto Civitas Solis - Objetivos Institucionais ↗","text-link",True)}</div></div></section>'
 pillars='<section class="section soft"><div class="wrap"><h2 class="center">'+esc(tr(s[8],l))+'</h2><div class="grid three">'+''.join(f'<article class="pillar">{icon(ic)}<h3>{esc(tr(s[i],l))}</h3>{para(s[i+1],l)}</article>' for i,ic in [(9,'art'),(11,'spirit'),(13,'science')])+'</div></div></section>'
 return h+org+pillars+globals_section(l)+f'<section class="section"><div class="wrap"><h2 class="center">{esc(tr("Nosso YouTube",l))}</h2>{gallery(l)}</div></section>'+contact(l,True)
def mission(l):
 s=PAGES['vy']['text'];v=PAGES['vy']['arrays'][0]
 cards=''.join(f'<article class="value value-{x["key"]}"><h3>{esc(tr(x["title"],l))}</h3>{para(x["description"],l)}</article>' for x in v)
 return hero(s[0],'',l)+f'<section class="section"><div class="wrap narrow mission-card"><h2>{esc(tr(s[2],l))}</h2>{para(s[3],l)}</div></section><section class="section soft"><div class="wrap narrow mission-card"><h2>{esc(tr(s[4],l))}</h2>{para(s[5],l)}</div></section><section class="section"><div class="wrap"><h2 class="center">{esc(tr(s[6],l))}</h2><p class="center">{esc(tr(s[7],l))}</p><div class="values">{img("assets/fundo-valores-geometria.png","","values-geometry")}{cards}</div></div></section>'
def publications(l,only=None):
 d=PUB[l];cards=[]
 for i,(title,subtitle,author,meta,desc) in enumerate(d['books']):
  if only is not None and i!=only:continue
  a=PA[i]
  cards.append(f'<article class="publication-card"'+(f' lang="{a["contentLang"]}"' if a.get('contentLang') else '')+f'><div class="publication-cover">{img(a["image"],d["cover"]+": "+title)}</div><div class="publication-copy"><p class="kicker">{esc(meta)}</p><h2>{esc(title)}</h2><h3>{esc(subtitle)}</h3><p class="author">{esc(author)}</p><p>{esc(desc)}</p><div class="publication-actions">{link(a["url"],d["amazon"],"button store",True)[:-4]}{img('assets/amazon-icon.png')}</a></div></div></article>')
 title=d['title'] if only is None else d['books'][only][0]
 return '<div class="publications-page"><section class="publications-hero"><div class="wrap narrow"><p class="publications-eyebrow">'+esc(d['eyebrow'])+'</p><h1>'+esc(title)+'</h1><p>'+esc(d['hero'] if only is None else d['books'][only][1])+'</p></div></section><section class="publication-list wrap">'+''.join(cards)+'</section></div>'
def youtube(l):
 s=PAGES['jy']['text']
 return hero(s[0],s[1],l,'red',link('https://www.youtube.com/@institutocivitassolis5117',tr(s[2],l),'button youtube-button',True))+f'<section class="section"><div class="wrap">{gallery(l)}</div></section><section class="section soft"><div class="wrap narrow"><h2>{esc(tr(s[3],l))}</h2>{para(s[4],l)}{para(s[5],l)}</div><div class="wrap grid four topics">'+''.join(f'<article><h3>{esc(tr(s[i],l))}</h3>{para(s[i+1],l)}</article>' for i in [6,8,10,12])+'</div></section>'+f'<section class="section center"><div class="wrap narrow"><h2>{esc(tr(s[14],l))}</h2>{para(s[15],l)}{link("https://www.youtube.com/@institutocivitassolis5117",tr(s[16],l),"button youtube-button",True)}</div></section>'
def instagram(l):
 s=PAGES['xy']['text'];return hero(s[0],s[1],l,'pink',link('https://www.instagram.com/institutocivitassolis/',tr(s[2],l),'button',True))+f'<section class="section"><div class="wrap narrow center instagram-card"><strong>@institutocivitassolis</strong><p>{UI[l]["external"]}</p><button class="button js-only" data-instagram>{UI[l]["load"]}</button><div data-instagram-host></div><p>{link("https://www.instagram.com/institutocivitassolis/",tr(s[5],l),"text-link",True)}</p></div></section>'
def global_page(l):
 s=PAGES['yy']['text'];body=hero(s[0],s[1],l)+f'<section class="section"><div class="wrap narrow"><h2>{esc(tr(s[2],l))}</h2>{para(s[3],l)}{para(s[4],l)}</div></section>'+globals_section(l)
 body+=f'<section class="section"><div class="wrap narrow"><h2>{esc(tr(s[9],l))}</h2>{para(s[10],l)}<h3>{esc(tr(s[11],l))}</h3>{para(s[12],l)}{para(s[14],l)}{para(s[15],l)}<h2>{esc(tr(s[16],l))}</h2>{para(s[17],l)}{para(s[18],l)}{link(url("contato",l),tr(s[19],l))}</div></section>'
 return body
BUILDERS={'':home,'missao-visao-valores':mission,'publicacoes':publications,'youtube':youtube,'instagram':instagram,'contato':lambda l:hero(PAGES['wy']['text'][0],PAGES['wy']['text'][1],l,'blue')+contact(l),'trabalho-global':global_page,'livro':lambda l:publications(l,3)}
def document(l,r):
 title={'':'Instituto Civitas Solis','missao-visao-valores':'Missão, Visão e Valores','publicacoes':PUB[l]['title'],'youtube':'YouTube Civitas Solis','instagram':'Instagram Civitas Solis','contato':'Entre em Contato','trabalho-global':'Trabalho Global','livro':PUB[l]['books'][3][0]}[r]
 desc=tr('Arte, Espiritualidade e Ciência para uma Nova Consciência.',l)
 canonical=ORIGIN+url(r,l)
 alternates=''.join(f'<link rel="alternate" hreflang="{k}" href="{ORIGIN+url(r,k)}">' for k in LANGS)
 return f'''<!doctype html><html lang="{'pt-BR' if l=='pt' else l}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(tr(title,l))} | Civitas Solis</title><meta name="description" content="{esc(desc)}"><meta name="referrer" content="strict-origin-when-cross-origin"><meta name="robots" content="{'noindex, nofollow' if NOINDEX else 'index, follow'}"><link rel="canonical" href="{canonical}">{alternates}<link rel="icon" href="{asset('assets/logo.png')}"><link rel="stylesheet" href="{asset('assets/styles.css')}"><script src="{asset('assets/app.js')}" defer></script></head><body>{header(l,r)}<main id="conteudo">{BUILDERS[r](l)}</main>{footer(l,r)}<dialog class="video-dialog" aria-label="{UI[l]['play']}"><button class="dialog-close" data-close>{UI[l]['close']} ×</button><div class="player"></div><p><a data-watch target="_blank" rel="noopener noreferrer">YouTube ↗</a></p></dialog></body></html>'''
def main():
 OUT.mkdir(exist_ok=True)
 # Remove only generated HTML recorded by the previous build, within this artifact.
 old=OUT/'build-manifest.json'
 if old.exists():
  for rel in json.loads(old.read_text()).get('pages',[]):
   p=(OUT/rel).resolve()
   if p.is_relative_to(OUT.resolve()) and p.suffix=='.html' and p.is_file():p.unlink()
 shutil.copytree(ROOT/'static',OUT,dirs_exist_ok=True)
 pages=[]
 for lang in LANGS:
  for route in ROUTES:
   rel=('/'.join(x for x in [lang if lang!='pt' else '',route,'index.html'] if x))
   p=OUT/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(document(lang,route));pages.append(rel)
 (OUT/'404.html').write_text(f'<!doctype html><html lang="pt-BR"><meta charset="utf-8"><title>Página não encontrada</title><h1>Página não encontrada</h1><a href="{url()}">Instituto Civitas Solis</a></html>');pages.append('404.html')
 (OUT/'.nojekyll').write_text('')
 (OUT/'robots.txt').write_text('User-agent: *\nDisallow: /\n' if NOINDEX else f'User-agent: *\nAllow: /\nSitemap: {ORIGIN}{BASE}/sitemap.xml\n')
 entries=''.join('<url><loc>'+ORIGIN+url(r,l)+'</loc></url>' for l in LANGS for r in ROUTES)
 (OUT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+entries+'</urlset>')
 sha=os.environ.get('SOURCE_COMMIT') or subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
 manifest={'source_commit':sha,'base_path':BASE,'noindex':NOINDEX,'pages':pages,'languages':list(LANGS),'videos':len(VIDEOS),'publications':len(PA)}
 (OUT/'build-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'pages':len(pages),'videos':len(VIDEOS),'publications':len(PA),'base':BASE,'noindex':NOINDEX}))
if __name__=='__main__':main()
