/* オフライン用：一度開いた版を端末に覚えておき、電波がないときはそれを出す。
   ふだんは毎回ネットの最新版を取りに行く（4秒で返ってこなければ保存版）。 */
const V='mini-v2';
const CORE=['./','./index.html','./tools/list.json'];
self.addEventListener('install',e=>{e.waitUntil((async()=>{const c=await caches.open(V);
  await Promise.all(CORE.map(u=>c.add(new Request(u,{cache:'reload'})).catch(()=>{})));
  try{const l=await (await fetch('tools/list.json',{cache:'no-store'})).json();await Promise.all(l.map(t=>c.add(new Request('tools/'+encodeURIComponent(t.file),{cache:'reload'})).catch(()=>{})))}catch(_){}
})());self.skipWaiting()});
self.addEventListener('activate',e=>{e.waitUntil((async()=>{for(const k of await caches.keys())if(k.startsWith('mini-')&&k!==V)await caches.delete(k);await self.clients.claim()})())});
const FONT=/^https:\/\/fonts\.(googleapis|gstatic)\.com\//;
async function put(req,res){try{if(res&&(res.ok||res.type==='opaque')){const c=await caches.open(V);await c.put(req,res.clone())}}catch(_){}return res}
async function fromCache(req){return (await caches.match(req,{ignoreSearch:true}))||(req.mode==='navigate'?await caches.match('./',{ignoreSearch:true})||await caches.match('./index.html'):undefined)}
async function netFirst(req){
  const net=fetch(req,{cache:'no-store'}).then(r=>put(req,r));
  const timer=new Promise(ok=>setTimeout(ok,4000,'t'));
  try{const r=await Promise.race([net,timer]);if(r!=='t')return r;const c=await fromCache(req);return c||await net}
  catch(_){const c=await fromCache(req);if(c)return c;throw _}
}
async function cacheFirst(req){const c=await caches.match(req);if(c)return c;return put(req,await fetch(req))}
self.addEventListener('fetch',e=>{const r=e.request;if(r.method!=='GET')return;const u=new URL(r.url);
  if(FONT.test(r.url))return e.respondWith(cacheFirst(r));
  if(u.origin===location.origin)e.respondWith(netFirst(r));
});
