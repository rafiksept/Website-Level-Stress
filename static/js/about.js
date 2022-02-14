const profil = document.querySelectorAll('.profil');



document.addEventListener('click', function(e){
    if (e.target.classList.contains('kanan')){
        profil.forEach(i => {
            if(i.classList.contains('kanan')){
                i.style.animation = 'kanan';
                i.style.animationDuration = '3s';
                i.style.animationFillMode = 'forwards';
                setTimeout(function(){
                    i.classList.remove('kanan');
                    i.classList.add('tengah');
                },2000)
            } else if (i.classList.contains('tengah')){
                i.style.animation = 'tengah';
                i.style.animationDelay = '1s';
                i.style.animationDuration = '3s';
                i.style.animationFillMode = 'forwards';
                setTimeout(function(){
                    i.classList.remove('tengah');
                    i.classList.add('kanan');
                },2000)

            }
        })
    } else if (e.target.classList.contains('kiri')){
        profil.forEach(i => {
            if(i.classList.contains('kiri')){
                i.style.animation = 'kiri';
                i.style.animationDuration = '3s';
                i.style.animationFillMode = 'forwards';
                setTimeout(function(){
                    i.classList.remove('kiri');
                    i.classList.add('tengah');
                },2000)
            } else if (i.classList.contains('tengah')){
                i.style.animation = 'tengah1';
                i.style.animationDelay = '1s';
                i.style.animationDuration = '3s';
                i.style.animationFillMode = 'forwards';
                setTimeout(function(){
                    i.classList.remove('tengah');
                    i.classList.add('kiri');
                },2000)

            }
        })
    }
})