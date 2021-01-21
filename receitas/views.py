
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponseNotFound
from .models import Receita

def index(request):

    receitas = Receita.objects.order_by('-data_receita').filter(publicada=True)

    dados = {
        'receitas' : receitas
    }

    return render(request,'index.html', dados)

def receita(request, receita_id):
    receita = get_object_or_404(Receita, pk=receita_id)    

    if(receita.publicada == False):
        return HttpResponseNotFound('Página não encontrada')
    

    receita_a_exibir = {
        'receita' : receita
    }
    
    return render(request, 'receita.html', receita_a_exibir)

def buscar(request):
    lista_receitas = Receita.objects.order_by('-data_receita').filter(publicada=True)
    dados = {}
    
    if 'buscar' in request.GET:
        nome_a_buscar = request.GET['buscar']
        if nome_a_buscar != '':
            lista_receitas = lista_receitas.filter(nome_receita__icontains = nome_a_buscar)
        
            dados ={
                'receitas' : lista_receitas
            }


    return render(request, 'buscar.html', dados)