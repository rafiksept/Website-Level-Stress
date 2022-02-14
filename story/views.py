from xmlrpc.client import boolean
import warnings
warnings.filterwarnings("ignore")
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from .forms import FormCerita
from django.views.generic import DetailView, ListView, DeleteView
# Create your views here.
from .models import Cerita, Gambar
from django.core.paginator import Paginator
from .predict import predict
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


def linkGambar(user):
    if len(Gambar.objects.filter(author= user)) == 0:
        gambar = Gambar.objects.filter(author= "admin")[0]
    else:
        gambar = Gambar.objects.filter(author= user)[0]
    
    return gambar



class CeritaDeleteView(LoginRequiredMixin,DeleteView):
    model = Cerita
    template_name = 'cerita/konfirmasi_delete.html'
    success_url = reverse_lazy('cerita:riwayat', kwargs = {'page':'1'})
    context_object_name = 'cerita_delete'


class CeritaListView(LoginRequiredMixin,ListView):
    model = Cerita
    ordering = ['-publish']
    paginate_by = 9
    template_name = 'cerita/cerita_list.html'
    context_object_name = 'cerita_list'

    def get_context_data(self, *args, **kwargs):
        paginator  = Paginator(self.queryset.order_by('-publish'), self.paginate_by)
        batas = paginator.num_pages <= 3
        sebelum = int(self.kwargs['page']) - 2
        sesudah = int(self.kwargs['page']) + 2
        ada = boolean(len(self.queryset))
        gambar = linkGambar(self.request.user.username)
        self.kwargs.update({
            'batas':batas,
            'sebelum': sebelum,
            'sesudah':sesudah,
            'ada':ada,
            'gambar':gambar
        })
        kwargs = self.kwargs
        return super().get_context_data(*args, **kwargs)



    def get_queryset(self) :
        self.queryset = self.model.objects.filter(author__iexact = self.request.user.username)
        return super().get_queryset()


class CeritaDetailView(LoginRequiredMixin,UserPassesTestMixin,DetailView):
    model = Cerita
    template_name = 'cerita/cerita_detail.html' 

    def get_context_data(self, *args, **kwargs):
        gambar = linkGambar(self.request.user.username)
        self.kwargs.update({
            'gambar':gambar
        })
        kwargs = self.kwargs

        return super().get_context_data(*args, **kwargs)

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user.username

@login_required
def ceritaView(request):
    formulir = FormCerita(request.POST or None)
    gambar = linkGambar(request.user.username)
    


    if request.method == 'POST':
        if formulir.is_valid():
            formulir.save()
            instance = formulir.save(commit= False)
            instance.stress = predict(formulir.cleaned_data['isi'])
            instance.author = request.user.username
            instance.user = User.objects.get(id=request.user.id)
            if len(Gambar.objects.filter(author= request.user.username)) == 0:
                instance.save()
            else:
                instance.gambar = Gambar.objects.get(author= request.user.username)
                instance.save()
            
            
            return HttpResponseRedirect(reverse('cerita:detail', args=(instance.pk,)))

    context = {
        'page_title':'Buat Cerita',
        'formulir':formulir,
        'gambar':gambar

    }

    return render(request, 'cerita/tambah.html', context)