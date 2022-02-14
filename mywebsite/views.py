import os
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import NewUserForm, ProfileForm, KomentarForm
from django.contrib.auth.models import User
from django.views.generic import ListView, UpdateView, DeleteView
from story.models import Cerita,Gambar, Komentar
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from story.views import linkGambar
from story.gambar import ambil




def AboutView(request):
    gambar = linkGambar(request.user.username)
    context = {
        'gambar':gambar
    }
    return render(request, 'about.html',context)




@login_required
def deleteView(request, page, pk1, pk):
    komentar = Komentar.objects.get(id=pk)
    if komentar.author == request.user.username:
        komentar.delete()
        link = '/komentar/'+page+'/'+pk1
        return HttpResponseRedirect(link)
    else:
        return HttpResponse('FORBIDDEN')

@login_required
def komentarView(request,page,pk1):
    isi = Cerita.objects.get(id=pk1)
    gambar = linkGambar(request.user.username)
    form = KomentarForm(request.POST or None)
    gambar = linkGambar(request.user.username)
    komentar = isi.komentar_set.all().order_by('-publish')
    komentar_author = isi.komentar_set.filter(author=request.user.username)
    
    

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            instance = form.save(commit= False)
            instance.author = request.user.username
            instance.user   = User.objects.get(id=request.user.id)
            instance.gambar = Gambar.objects.get(author = request.user.username)
            instance.postingan = Cerita.objects.get(id=pk1)
            instance.save()
            return HttpResponseRedirect(reverse('komentar', args=[page,pk1]))

    if request.method == 'GET':
        if isi.is_publish == True:
            context={
                'isi':isi,
                'gambar':gambar,
                'form'  :form,
                'gambar':gambar,
                'komentar':komentar,
                'ada':komentar_author,
                'page':page
            }

            return render(request, 'komentar.html',context)

        else:
            return HttpResponse('FORBIDDEN')


class HomeListView(LoginRequiredMixin,ListView):
    model = Cerita
    paginate_by = 5
    template_name = 'index.html'
    context_object_name = 'cerita_list'
   

    def get_context_data(self, *args, **kwargs):
        order = self.request.GET['order']
        paginator  = Paginator(self.queryset.order_by(order), self.paginate_by)
        batas = paginator.num_pages <= 3
        sebelum = int(self.kwargs['page']) - 2
        sesudah = int(self.kwargs['page']) + 2
        gambar = linkGambar(self.request.user.username)
        get_gambar = []
        for i in self.object_list:
            keren = self.model.objects.get(id=i.id)
            get_gambar.append(keren)

        self.kwargs.update({
            'batas':batas,
            'sebelum': sebelum,
            'sesudah':sesudah,
            'order':order,
            'gambar':gambar,
            'foto':get_gambar
        })
        kwargs = self.kwargs
        return super().get_context_data(*args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        order = self.request.GET['order']
        self.queryset = self.model.objects.filter(is_publish = True).order_by(order)
        return super().get_queryset()

def register_request(request):
    form = NewUserForm(request.POST or None)
    context = {
        'register_form':form
    }
    if request.method == 'POST':
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password1']
            email = request.POST['email']
            user = User.objects.create_user(username, email, password)
            user.save()
            return redirect('login')
        
        else: 
            return render(request,'register.html', context)
            
            
    if request.method == 'GET':
        if not request.user.is_authenticated():
             return render(request,'register.html', context)
        
        else:
            return HttpResponse('<b>Forbidden<b>')

    
class fotoUpdateView(LoginRequiredMixin,UpdateView):
    form_class = ProfileForm
    model = Gambar
    template_name = 'profile.html'
    
    def get_success_url(self):
        url = reverse('home')
        return url
    
    def get_context_data(self, *args, **kwargs):
        postingan = Cerita.objects.filter(author = self.request.user.username, is_publish=True).count()
        stress = Cerita.objects.filter(author=self.request.user.username)
        level = []
        for i in stress:
            tambah = i.stress
            level.append(tambah)
        
        if len(stress) != 0 :
            ratarata = int(sum(level)/len(stress))
        else:
            ratarata = 0
        self.kwargs.update({
            'postingan':postingan,
            'mean':ratarata
        })
        kwargs = self.kwargs
        return super().get_context_data(*args, **kwargs)


@login_required
def index(request):
    form = ProfileForm(request.POST or None, request.FILES)
    gambar = linkGambar(request.user.username)
    prof = len(Gambar.objects.filter(author=request.user.username))
    val = bool(prof)
    postingan = Cerita.objects.filter(author = request.user.username, is_publish=True).count()
    stress = Cerita.objects.filter(author=request.user.username)
    level = []
    for i in stress:
        tambah = i.stress
        level.append(tambah)

    if len(stress) != 0 :
        ratarata = int(sum(level)/len(stress))
    else:
        ratarata = 0

    context = {
        'page_title':'Home',
        'form':form,
        'gambar':gambar,
        'val':val,
        'postingan':postingan,
        'mean':ratarata
    }

    if request.method == 'POST':
        if form.is_valid():
            form.foto = request.FILES['foto']
            form.save()
            instance = form.save(commit= False)
            instance.author = request.user.username
            instance.user   = User.objects.get(id=request.user.id)
            instance.save()
            ambil(request.user.username)
            return HttpResponseRedirect(reverse('home'))
            
    return render(request, 'profile.html', context)

@login_required
def profile(request):
    prof = len(Gambar.objects.filter(author=request.user.username))
    gambar = linkGambar(request.user.username)
    last_login  = User.objects.get(username=request.user.username).last_login
    postingan = Cerita.objects.filter(author = request.user.username, is_publish=True).count()
    stress = Cerita.objects.filter(author=request.user.username)
    level = []
    for i in stress:
        tambah = i.stress
        level.append(tambah)
    if len(level) != 0 :
        ratarata = int(sum(level)/len(stress))
    else:
        ratarata = 0
    val = bool(prof)
    context = {
        'val':val,
        'gambar':gambar,
        'login':last_login,
        'postingan':postingan,
        'mean':ratarata
    }
    
    return render(request, 'profile_semua.html',context)

def loginView(request):

    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username= username, password = password)

        if user is not None:
            login(request, user)
            return redirect('cerita:tambah')

        else:
            salah = True
            context = {
                'salah':salah
            }
            return render(request, 'login.html',context)

    return render(request, 'login.html')

@login_required
def logoutView(request):
    context = {
        'page_title':'Logout'
    }

    if request.method == 'POST':
        if request.POST['logout'] == 'Logout':
            logout(request)

            return redirect('login')

    return render(request, 'logout.html', context)



