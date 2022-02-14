
const tambah = document.location.pathname + document.location.search
const menu = document.querySelectorAll('a[href="'+tambah+'"]')[0];
menu.style.color = '#1072aa';