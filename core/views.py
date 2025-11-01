from django.shortcuts import render

# core/views.py
from django.conf import settings
import requests
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .models import EveProfile
import json
from .utils import enviar_mail_eve
from .utils import verify_eve_token
from .utils import refresh_eve_token
from django.utils import timezone

def home(request):
    return render(request, 'home.html')

def login_eve(request):
    client_id = settings.EVE_CLIENT_ID
    redirect_uri = settings.EVE_REDIRECT_URI
    scope = "esi-mail.send_mail.v1"  # Adicione outros scopes se precisar
    auth_url = (
        f"https://login.eveonline.com/oauth/authorize?response_type=code"
        f"&redirect_uri={redirect_uri}&client_id={client_id}"
        f"&scope={scope}"
    )
    return redirect(auth_url)


def eve_callback(request):
    code = request.GET.get('code')
    token_url = "https://login.eveonline.com/oauth/token"
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": settings.EVE_REDIRECT_URI,
    }
    auth = (settings.EVE_CLIENT_ID, settings.EVE_CLIENT_SECRET)

    # 1. Trocar 'code' por 'access_token'
    token_response = requests.post(token_url, data=data, auth=auth)
    token_data = token_response.json()
    access_token = token_data.get('access_token')

    # 2. Verificar dados do personagem (CharacterID, CharacterName)
    verify_url = "https://login.eveonline.com/oauth/verify"
    headers = {"Authorization": f"Bearer {access_token}"}
    verify_response = requests.get(verify_url, headers=headers)
    verify_data = verify_response.json()

    # Print dos dados obtidos via /oauth/verify
    print("=== Dados de verificação (verify_data) ===")
    print(json.dumps(verify_data, indent=2))  # imprime formatado no console

    character_id = verify_data.get("CharacterID", "0")
    character_name = verify_data.get("CharacterName", f"eve_{character_id}")
    portrait_url = f"https://images.evetech.net/characters/{character_id}/portrait?size=64"

    # 3. Dados do personagem pela ESI (corporation_id, etc.)
    char_info_url = f"https://esi.evetech.net/latest/characters/{character_id}/"
    char_info_resp = requests.get(char_info_url)
    char_info = char_info_resp.json()

    # Print dos dados do personagem
    print("=== Dados do personagem (char_info) ===")
    print(json.dumps(char_info, indent=2))

    corporation_id = char_info.get("corporation_id")

    # 4. Dados da corporação
    corp_info_url = f"https://esi.evetech.net/latest/corporations/{corporation_id}/"
    corp_info_resp = requests.get(corp_info_url)
    corp_info = corp_info_resp.json()

    # Print dos dados da corporação
    print("=== Dados da corporação (corp_info) ===")
    print(json.dumps(corp_info, indent=2))

    # Exemplo de checagem de corp
    corp_name = corp_info.get("name", "")
    if corp_name != "PulaLeeroy Br":
        return render(request, 'erro.html', {"mensagem": "Você não pertence à corporação PulaLeeroy Br."})

    # 5. Cria ou atualiza o usuário e EveProfile (exemplo)
    User = get_user_model()
    user, _ = User.objects.get_or_create(username=character_name)
    user.is_active = True
    user.save()

    profile, created = EveProfile.objects.get_or_create(
        user=user,
        defaults={
            'character_id': character_id,
            'character_name': character_name,
            'portrait_url': portrait_url
        }
    )
    if not created:
        profile.character_id = character_id
        profile.character_name = character_name
        profile.portrait_url = portrait_url
        profile.save()

    # 6. Login e redireciona
    login(request, user)
    messages.success(request, f'Bem-vindo(a), {character_name}! Login realizado com sucesso.')
    return redirect('home_logada')


from django.contrib.auth.decorators import login_required
from .models import ShipCategory, Ship, Pedido
from django.contrib import messages


@login_required
def solicitar_nave(request):
    if request.method == 'POST':
        ship_id = request.POST.get('ship_id')
        if ship_id:
            ship = Ship.objects.get(id=ship_id)
            pedido = Pedido.objects.create(usuario=request.user, nave=ship)
            messages.success(request, f'Pedido de "{ship.ship_name}" criado com sucesso!')

            # 1) Verificar se existe eve_profile
            eve_profile = getattr(request.user, 'eve_profile', None)
            if eve_profile:
                # 2) Checar se token expirou ou está próximo de expirar
                if eve_profile.token_expires and eve_profile.token_expires < timezone.now():
                    # Tentar refresh
                    refresh_ok = refresh_eve_token(eve_profile)
                    if not refresh_ok:
                        print("Falha ao renovar token. Não será possível enviar mail.")
                        return redirect('solicitar_nave')

                # 3) (Opcional) Verificar se o token ainda é válido e se possui escopo
                verify_data = verify_eve_token(eve_profile.access_token)
                if not verify_data:
                    print("Token inválido ou expirado, não foi possível enviar mail.")
                    return redirect('solicitar_nave')

                # Checar se "esi-mail.send_mail.v1" está em Scopes
                scopes_str = verify_data.get("Scopes", "")
                if "esi-mail.send_mail.v1" not in scopes_str:
                    print("Token não possui scope de mail. Não será possível enviar mail.")
                    return redirect('solicitar_nave')

                # 4) Enviar mail
                # Precisamos usar o CharacterID retornado em verify ou do eve_profile
                # e deve bater com o token
                sender_id = verify_data.get("CharacterID", eve_profile.character_id)

                subject = "Novo pedido de nave"
                body = (
                    f"Olá!\n\n"
                    f"O capsuler {request.user.username} criou um novo pedido de nave: {ship.ship_name}.\n"
                    f"Data: {pedido.data_solicitacao}\n"
                    f"Att,\nSistema de Pedidos"
                )

                # Exemplo: enviar mail para o próprio usuário
                # (ou outro ID, se for notificar um gerente)
                recipient_id = sender_id

                response = enviar_mail_eve(
                    character_id=sender_id,
                    access_token=eve_profile.access_token,
                    subject=subject,
                    body=body,
                    recipient_id=recipient_id
                )

                if response.status_code == 201:
                    print("Mail enviado com sucesso!")
                    messages.info(request, 'Notificação enviada por e-mail in-game!')
                else:
                    print("Falha ao enviar mail:", response.status_code, response.text)
                    messages.warning(request, 'Pedido criado, mas não foi possível enviar notificação por e-mail.')

            else:
                print("Usuário não possui eve_profile. Não é possível enviar mail.")
                messages.warning(request, 'Pedido criado, mas perfil EVE não encontrado.')
        else:
            messages.error(request, 'Por favor, selecione uma nave antes de solicitar.')
        return redirect('solicitar_nave')

    # GET
    categories = ShipCategory.objects.all()
    pedidos = Pedido.objects.filter(usuario=request.user)
    return render(request, 'solicitar_nave.html', {
        'categories': categories,
        'pedidos': pedidos,
    })

def nave_detail(request):
    ship_id = request.GET.get('ship_id')
    if not ship_id:
        return JsonResponse({'error': 'No ship_id provided'}, status=400)
    try:
        ship = Ship.objects.select_related('category').get(id=ship_id)
    except Ship.DoesNotExist:
        return JsonResponse({'error': 'Ship not found'}, status=404)

    data = {
        'category_name': ship.category.category_name,
        'ship_name': ship.ship_name,
    }
    return JsonResponse(data)


def nave_autocomplete(request):
    term = request.GET.get('term', '')
    ships = Ship.objects.filter(ship_name__icontains=term)[:10]

    results = []
    for s in ships:
        results.append({
            'id': s.id,
            'label': s.ship_name,       # O que aparece na lista
            'value': s.ship_name,       # O que vai pro input
            'category_name': s.category.category_name,  # Adiciona a categoria
        })
    return JsonResponse(results, safe=False)


# core/views.py
def perfil(request):
    if not request.user.is_authenticated:
        return redirect('eve_login')
    return render(request, 'perfil.html')


@login_required
def home_logada(request):
    if not request.user.is_authenticated:
        return redirect('home')  # Redireciona à home pública se não logado

    # Carrega todos os pedidos do usuário logado
    pedidos = Pedido.objects.filter(usuario=request.user)

    return render(request, 'home_logada.html', {
        'pedidos': pedidos
    })

def logout_view(request):
    logout(request)
    return redirect('home')  # Ajuste para a rota desejada após o logout




