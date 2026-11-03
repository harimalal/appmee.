// Parcourt chaque étape d'un diaporama et signale les éléments visibles qui se chevauchent ou sortent du cadre.
// Usage : NODE_PATH=$(npm root -g) node chevauchements.cjs /chemin/absolu/demo.html
// Faux positifs connus : un bloc titre pleine largeur, une image qui défile dans une fenêtre, les fonds floutés voulus.
const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1920,height:1080}});
await p.goto('file://'+process.argv[2]);await p.waitForTimeout(800);
const S=await p.evaluate(()=>window.__S);const out=[];
for(let i=0;i<S.length;i++){for(let st=0;st<=S[i][1];st++){
 await p.evaluate(([i,st])=>window.__go(i,st),[i,st]);await p.waitForTimeout(120);
 const r=await p.evaluate(()=>{
  const sl=document.querySelector('.slide.cur');const st=document.getElementById('stage').getBoundingClientRect();const k=st.width/1920;
  const vis=e=>{for(let x=e;x&&x!==sl;x=x.parentElement){const c=getComputedStyle(x);if(c.opacity<0.3||c.display==='none'||c.visibility==='hidden')return false;if(x.classList.contains('ghost')||x.classList.contains('covbg')||x.classList.contains('wall5')||x.classList.contains('wall4')||x.classList.contains('fanbg'))return false}return true};
  const els=[...sl.querySelectorAll('img,.title,.eyebrow,.prom,.ben,.card,.kpi,.hb,.vb,.igcard,.mc,.sc3,.pl,.fm,.mt,.mr,.vs2,.lb,.cb,.fl,.ba,.wish,.refi,.lp,.eb,.srcl,.bub,.ytc,.prof,.ctabar,.phone,.win,.nlbox,.tkz2,.lgi,.gl,.big,.tot')].filter(vis);
  const R=els.map(e=>{const b=e.getBoundingClientRect();return {e,x:(b.left-st.left)/k,y:(b.top-st.top)/k,w:b.width/k,h:b.height/k}}).filter(o=>o.w>4&&o.h>4);
  const res=[];const name=e=>e.tagName.toLowerCase()+(e.className&&typeof e.className==='string'?'.'+e.className.split(' ').slice(0,2).join('.'):'')+(e.getAttribute('data-img')?'['+e.getAttribute('data-img')+']':'')+(e.textContent?' «'+e.textContent.trim().slice(0,25)+'»':'');
  for(let a=0;a<R.length;a++)for(let c=a+1;c<R.length;c++){const A=R[a],C=R[c];if(A.e.contains(C.e)||C.e.contains(A.e))continue;
   const ix=Math.max(0,Math.min(A.x+A.w,C.x+C.w)-Math.max(A.x,C.x)),iy=Math.max(0,Math.min(A.y+A.h,C.y+C.h)-Math.max(A.y,C.y));const ar=ix*iy,m=Math.min(A.w*A.h,C.w*C.h);
   if(ar>0.04*m&&ar>400)res.push(name(A.e)+' × '+name(C.e)+' '+Math.round(100*ar/m)+'%')}
  // hors cadre
  R.forEach(o=>{if(o.x<-2||o.y<-2||o.x+o.w>1922||o.y+o.h>1082){if(!o.e.closest('#strip')&&!o.e.closest('.swp'))res.push('HORS CADRE '+name(o.e)+' '+[o.x,o.y,o.w,o.h].map(Math.round))}});
  return res});
 if(r.length)out.push(S[i][0]+':'+st+'\n  '+r.join('\n  '))}}
console.log(out.join('\n'));await b.close()})();
