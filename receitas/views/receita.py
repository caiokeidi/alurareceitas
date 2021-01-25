
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import HttpResponseNotFound
from receitas.models import Receita
from django.contrib.auth.models import User
from django.contrib import auth, messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def index(request):

    receitas = Receita.objects.order_by('-data_receita').filter(publicada=True)
    
    paginator = Paginator(receitas, 3)
    page = request.GET.get('page')
    receitas_por_pagina = paginator.get_page(page)


    dados = {
        'receitas' : receitas_por_pagina
    }

    return render(request,'receitas/index.html', dados)

def receita(request, receita_id):
    receita = get_object_or_404(Receita, pk=receita_id)    
    user_id = get_object_or_404(User, pk = request.user.id)

    if(receita.publicada == False and receita.pessoa != user_id):
        return HttpResponseNotFound('Página não encontrada')
    

    receita_a_exibir = {
        'receita' : receita
    }
    
    return render(request, 'receitas/receita.html', receita_a_exibir)



def cria_receita(request):
    if request.method == 'POST':
        nome_receita = request.POST['nome_receita']
        ingredientes = request.POST['ingredientes']
        modo_preparo = request.POST['modo_preparo']
        tempo_preparo = request.POST['tempo_preparo']
        rendimento = request.POST['rendimento']
        categoria = request.POST['categoria']
        foto_receita = request.FILES['foto_receita']


        ##Aqui eu quero pegar um objeto do tipo USER, que tem como referência
        ##A Primary Key ser igual ao user.id que veio na request.
        user = get_object_or_404(User, pk=request.user.id)

        receita = Receita.objects.create(pessoa=user, 
        nome_receita = nome_receita, ingredientes = ingredientes,
        modo_preparo = modo_preparo, tempo_preparo = tempo_preparo,
        rendimento = rendimento, categoria = categoria,
        foto_receita = foto_receita)
        receita.save()

        return redirect('dashboard')
    else:
        return render(request, 'receitas/cria_receita.html')

def deleta_receita(request, receita_id):
    receita = get_object_or_404(Receita, pk=receita_id)
    receita.delete()

    messages.success(request, 'Post apagado com sucesso')
    return redirect(dashboard)

def edita_receita(request, receita_id):
    receita = get_object_or_404(Receita, pk=receita_id)
    receita_a_editar = {'receita': receita}

    return render(request, 'receitas/edita_receita.html', receita_a_editar)

def atualiza_receita(request):
    if request.method == 'POST':
        receita_id = request.POST['receita_id']
        r = Receita.objects.get(pk=receita_id)

        r.nome_receita = request.POST['nome_receita']
        r.ingredientes = request.POST['ingredientes']
        r.modo_preparo = request.POST['modo_preparo']
        r.tempo_preparo = request.POST['tempo_preparo']
        r.rendimento = request.POST['rendimento']
        r.categoria = request.POST['categoria']
        ##r.publicada = request.POST['publicada']

        if 'publicada' in request.POST:
            r.publicada = True
        else:
            r.publicada = False
        
        
        if 'foto_receita' in request.FILES:
            r.foto_receita = request.FILES['foto_receita']

        r.save()
        messages.success(request, 'Post alterado com sucesso')
        return redirect('dashboard')
    else:
        messages.error(request, 'Erro ao alterar o Post')
        return redirect('dashboard')
