'use strict';
document.documentElement.classList.add('js');
const menu=document.querySelector('.menu-toggle');
menu?.addEventListener('click',()=>{const open=menu.getAttribute('aria-expanded')!=='true';menu.setAttribute('aria-expanded',String(open));document.getElementById('menu-principal').classList.toggle('is-open',open);});
document.addEventListener('keydown',e=>{if(e.key==='Escape'){document.querySelectorAll('.language[open]').forEach(d=>d.open=false);if(menu?.getAttribute('aria-expanded')==='true'){menu.click();menu.focus();}}});
document.addEventListener('click',e=>{document.querySelectorAll('.language[open]').forEach(d=>{if(!d.contains(e.target))d.open=false;});});
// Preserve the original expandable panels without a framework or hidden-only content.
document.querySelectorAll('[data-panel]').forEach(button=>button.addEventListener('click',()=>{
 const open=button.getAttribute('aria-expanded')!=='true';
 const section=button.closest('#trabalho-global');
 section.querySelectorAll('[data-panel]').forEach(b=>{b.setAttribute('aria-expanded','false');b.closest('.global-card').classList.remove('selected');});
 section.querySelectorAll('[data-global-panel]').forEach(p=>p.classList.remove('is-open'));
 if(open){button.setAttribute('aria-expanded','true');button.closest('.global-card').classList.add('selected');const panel=document.getElementById(button.dataset.panel);panel.classList.add('is-open');if(matchMedia('(max-width:640px)').matches)button.closest('.global-card').after(panel);else section.querySelector('.grid').after(panel);}
}));
const slides=[...document.querySelectorAll('.hero-image')],dots=[...document.querySelectorAll('[data-slide]')];let active=0,timer=null,paused=matchMedia('(prefers-reduced-motion:reduce)').matches;
function showSlide(index){active=(index+slides.length)%slides.length;slides.forEach((s,i)=>s.classList.toggle('active',i===active));dots.forEach((b,i)=>b.setAttribute('aria-pressed',String(i===active)));}
function clock(){clearInterval(timer);if(!paused&&slides.length&&!document.hidden)timer=setInterval(()=>showSlide(active+1),7000);}
dots.forEach(b=>b.addEventListener('click',()=>{showSlide(Number(b.dataset.slide));clock();}));
const pause=document.querySelector('[data-pause]');function labelPause(){if(pause)pause.textContent=paused?pause.dataset.resume:pause.dataset.pauseLabel;}
pause?.addEventListener('click',()=>{paused=!paused;labelPause();clock();});labelPause();clock();document.addEventListener('visibilitychange',clock);
const normalize=s=>s.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLocaleLowerCase();
document.querySelectorAll('[data-gallery]').forEach(gallery=>{
 const cards=[...gallery.querySelectorAll('[data-video-card]')];const search=gallery.querySelector('[data-video-search]');const prev=gallery.querySelector('[data-prev]'),next=gallery.querySelector('[data-next]');let page=0;const size=3;
 function render(){const query=normalize(search.value.trim());const found=cards.filter(c=>normalize(c.dataset.title).includes(query));const total=Math.ceil(found.length/size);page=Math.max(0,Math.min(page,total-1));const visible=new Set(found.slice(page*size,(page+1)*size));cards.forEach(c=>c.hidden=!visible.has(c));prev.disabled=page===0;next.disabled=page>=total-1;gallery.querySelector('.gallery-empty').hidden=found.length!==0;gallery.querySelector('[data-page-status]').textContent=`${gallery.dataset.pageLabel} ${total?page+1:0} ${gallery.dataset.ofLabel} ${total}`;}
 search.addEventListener('input',()=>{page=0;render();});gallery.querySelector('[data-video-clear]').addEventListener('click',()=>{search.value='';page=0;render();search.focus();});prev.addEventListener('click',()=>{page--;render();});next.addEventListener('click',()=>{page++;render();});render();
});
const dialog=document.querySelector('.video-dialog');let trigger=null;
function closeVideo(){dialog?.close();dialog?.querySelector('.player').replaceChildren();trigger?.focus();}
document.querySelectorAll('[data-video]').forEach(button=>button.addEventListener('click',()=>{
 const id=button.dataset.video;if(!/^[a-zA-Z0-9_-]{11}$/.test(id))return;trigger=button;
 const frame=document.createElement('iframe');frame.src=`https://www.youtube-nocookie.com/embed/${id}?rel=0`;frame.title=button.dataset.videoTitle||'YouTube';frame.allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';frame.allowFullscreen=true;frame.referrerPolicy='strict-origin-when-cross-origin';dialog.querySelector('.player').replaceChildren(frame);dialog.querySelector('[data-watch]').href=`https://www.youtube.com/watch?v=${id}`;dialog.showModal();
}));
dialog?.querySelector('[data-close]').addEventListener('click',closeVideo);dialog?.addEventListener('cancel',e=>{e.preventDefault();closeVideo();});dialog?.addEventListener('click',e=>{if(e.target===dialog)closeVideo();});
// Official Instagram profile embed; no credentials and no third-party widget vendor.
// The browser contacts Instagram only after an explicit visitor action.
document.querySelector('[data-instagram]')?.addEventListener('click',event=>{
 const button=event.currentTarget;if(button.disabled)return;button.disabled=true;
 const host=document.querySelector('[data-instagram-host]');const widget=document.createElement('blockquote');widget.className='instagram-media';widget.dataset.instgrmPermalink='https://www.instagram.com/institutocivitassolis/';widget.dataset.instgrmVersion='14';
 const link=document.createElement('a');link.href=widget.dataset.instgrmPermalink;link.textContent='@institutocivitassolis';link.target='_blank';link.rel='noopener noreferrer';widget.append(link);host.append(widget);
 const script=document.createElement('script');script.src='https://www.instagram.com/embed.js';script.async=true;script.onload=()=>window.instgrm?.Embeds?.process();script.onerror=()=>{button.disabled=false;script.remove();widget.remove();};document.head.append(script);
});
