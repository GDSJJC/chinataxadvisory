// Mobile nav, active link, footer year, credentials lightbox. No dependencies.
(function(){
  var btn = document.querySelector('.menu-btn');
  var nav = document.querySelector('.nav');
  if(btn && nav){
    btn.addEventListener('click', function(){
      var open = nav.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      btn.textContent = open ? 'Close' : 'Menu';
    });
  }

  try{
    var path = location.pathname.replace(/\/index\.html?$/,'/').toLowerCase();
    document.querySelectorAll('.nav a').forEach(function(a){
      var href = (a.getAttribute('href')||'').toLowerCase();
      if(!href) return;
      var norm = href.replace(/\/index\.html?$/,'/');
      if(path === norm || (path.startsWith('/blog') && norm === '/' )) {
        a.classList.add('active');
      }
    });
  }catch(e){}

  var y = document.getElementById('year');
  if(y) y.textContent = new Date().getFullYear();

  var grid = document.querySelector('.cred-grid');
  if(!grid) return;
  var lb = document.createElement('div');
  lb.className = 'lightbox';
  lb.setAttribute('hidden','');
  lb.setAttribute('role','dialog');
  lb.setAttribute('aria-modal','true');
  lb.setAttribute('aria-label','Case study');
  lb.innerHTML = '<button type="button" class="lightbox-close" aria-label="Close">Close</button><img alt="">';
  document.body.appendChild(lb);
  var img = lb.querySelector('img');
  var closeBtn = lb.querySelector('.lightbox-close');
  var lastFocus = null;

  function close(){
    lb.setAttribute('hidden','');
    document.body.style.overflow = '';
    img.removeAttribute('src');
    if(lastFocus) lastFocus.focus();
  }
  function open(src, alt, from){
    lastFocus = from || document.activeElement;
    img.src = src;
    img.alt = alt || '';
    lb.removeAttribute('hidden');
    document.body.style.overflow = 'hidden';
    closeBtn.focus();
  }

  grid.addEventListener('click', function(e){
    var openBtn = e.target.closest('.cred-open');
    if(!openBtn) return;
    var pic = openBtn.querySelector('img');
    if(!pic) return;
    open(pic.currentSrc || pic.src, pic.alt, openBtn);
  });
  lb.addEventListener('click', function(e){
    if(e.target === lb || e.target === closeBtn) close();
  });
  document.addEventListener('keydown', function(e){
    if(e.key === 'Escape' && !lb.hasAttribute('hidden')) close();
  });
})();
