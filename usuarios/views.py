
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

def cadastro(request):
    erros = {
        'err' : True,
        'erros' : []
    }

    #Abaixo, se tiver algum erro nas condições, ele vai e coloca dentro da array erros.
    if request.method == 'POST':
        nome = request.POST['nome']
        email = request.POST['email']
        senha = request.POST['password']
        senha2 = request.POST['password2']

        

        if not nome.strip():
            print('Erro: O espaço de nome não pode ficar em branco')
            erros['erros'].append('Erro: O espaço de nome não pode ficar em branco')

        if not email.strip():
            print('Erro: O espaço de email não pode ficar em branco')
            erros['erros'].append('Erro: O espaço de email não pode ficar em branco')

        if senha != senha2:
            print('As senhas devem ser iguais.')
            erros['erros'].append('Erro: As senhas devem ser iguais')

        if User.objects.filter(email = email).exists():
            print('Usuário já cadastrado')
            erros['erros'].append('Erro: Usuário já cadastrado')
        
        ## Aqui vemos se erros está ou não vazio, se não tiver ele envia o erros, se estiver vazio, ele vai para o else.
        if erros['erros'] != []:
            return render(request, 'usuarios/cadastro.html', erros)
        ##Aqui ele executa o bloco de save.
        else:
            user = User.objects.create_user(username = nome, email = email, password = senha)
            user.save()
            
            print('Usuário cadastrado com sucesso')
            return redirect('login')

    else:
        print('aqui')
        return render(request, 'usuarios/cadastro.html')



def login(request):
    return render(request, 'usuarios/login.html')

def logout(request):
    pass

def dashboard(request):
    pass




