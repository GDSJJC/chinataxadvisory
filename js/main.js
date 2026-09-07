// Mobile nav + active link + footer year. No dependencies.
(function(){
  var btn = document.querySelector('.menu-btn');
  var nav = document.querySelector('.nav');
  if(btn && nav){
    btn.addEventListener('click', function(){
      var open = nav.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }
  // Active nav
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
  // Year
  var y = document.getElementById('year');
  if(y) y.textContent = new Date().getFullYear();
})();
