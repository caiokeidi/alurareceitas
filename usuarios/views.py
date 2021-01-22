
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth

def cadastro(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    else:
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
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    else:
        if request.method == 'POST':
            email = request.POST['email']
            senha = request.POST['senha']

            if email == "" or senha == "":
                print('Os campos de email e senha não devem ficar em branco')
                return redirect('login')

            if User.objects.filter(email=email).exists:
                try:
                    nome = User.objects.filter(email=email).values_list('username', flat=True).get()

                    user = auth.authenticate(request, username = nome, password = senha)
                except:
                    user = None

                if user is not None:
                    auth.login(request, user)
                    print('login realizado com sucesso')
                    return redirect('dashboard')
                else:
                    print('Senha ou Usuário incorretos')
                    return redirect('login')
            else:
                print('Email não cadastrado')
                return redirect('login')

        return render(request, 'usuarios/login.html')

def logout(request):
    auth.logout(request)
    return redirect('index')

def dashboard(request):
    if request.user.is_authenticated:
        return render(request, 'usuarios/dashboard.html')
    else:
        return redirect('login')




