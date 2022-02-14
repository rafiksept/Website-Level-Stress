var textarea = document.querySelector('textarea');

textarea.addEventListener('keydown', autosize);
             
function autosize(){
  var el = this;
  setTimeout(function(){
    el.style.cssText = 'height:auto; padding:0';
    // for box-sizing other than "content-box" use:
    el.style.cssText = '-moz-box-sizing:content-box';
    el.style.cssText = 'height:' + el.scrollHeight + 'px';
  },0);
}

const kotak = document.querySelector('.ajak-dalam');
const gambar = document.querySelector('.ajak img');

kotak.addEventListener('click', function geser(){
  kotak.style.animationName = "geser";
  kotak.style.animationDuration = "3s";
  kotak.style.animationFillMode = "forwards";
  gambar.style.animationName = "geserGambar";
  gambar.style.animationDuration = "3s";
  gambar.style.animationFillMode = "forwards";
  this.removeEventListener('click', geser);
})