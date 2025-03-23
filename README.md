# Projeto: EVE Online - Sistema de Solicitação de Naves

Este projeto é um **sistema web** desenvolvido em **Django** que permite aos usuários:

- **Fazer login** via API do EVE Online (OAuth2/ESI).  
- **Selecionar** e **solicitar naves** de uma lista categorizada (menu tree).  
- **Visualizar** seus pedidos e status.  
- **Enviar mails in-game** através da ESI (opcional), notificando o usuário ou outra pessoa após criar um pedido.

---

## Sumário

1. [Tecnologias Principais](#tecnologias-principais)  
2. [Funcionalidades](#funcionalidades)  
3. [Instalação](#instalação)  
4. [Configuração do Banco de Dados](#configuração-do-banco-de-dados)  
5. [Integração com EVE Online (OAuth2)](#integração-com-eve-online-oauth2)  
6. [Execução do Projeto](#execução-do-projeto)  
7. [Uso do Sistema](#uso-do-sistema)  
8. [Estrutura de Pastas](#estrutura-de-pastas)  
9. [Observações Finais](#observações-finais)  

---

## Tecnologias Principais

- **Python 3.12+**  
- **Django 4+**  
- **PostgreSQL** (ou outro banco de dados, se configurado)  
- **ESI (EVE Swagger Interface)** para login OAuth2 e envio de mails  
- **HTML/CSS/JS** (menu tree, jQuery UI para autocomplete, etc.)

---

## Funcionalidades

1. **Login via EVE**: O usuário se autentica usando a conta EVE Online (com os escopos necessários).  
2. **Solicitar Nave**:  
   - **Menu Tree** para navegar nas categorias e escolher uma nave.  
   - **Campo de Autocomplete** para buscar rapidamente pelo nome da nave.  
   - **Exibição de detalhes** (categoria, nome) antes de confirmar a solicitação.  
3. **Pedidos**:  
   - **Lista** dos pedidos do usuário, com status e data de solicitação.  
   - **Status** inicial “Pendente” (pode evoluir conforme sua lógica).  
4. **Envio de Mail In-Game**:  
   - Ao criar um pedido, é possível enviar um **mail in-game** via ESI (se o token tiver `esi-mail.send_mail.v1`).  
   - Notifica o jogador ou outro personagem sobre o pedido.

---

## Instalação

1. **Clonar** este repositório:
   ```bash
   git clone https://github.com/seu-usuario/eve-nave-solicitacao.git
   cd eve-nave-solicitacao

2. **Criar e ativar** um ambiente virtual (opcional, mas recomendado):
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    venv\Scripts\activate     # Windows

3. **Instalar** as dependências:
    ```bash
    pip install -r requirements.txt

---

## Configuração do Banco de Dados

1. Ajuste o arquivo `settings.py` no projeto Django para apontar para seu banco de dados PostgreSQL (ou outro):
    ```bash
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'eve_online',
            'USER': 'eve_user',
            'PASSWORD': 'eve_password',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }

2. Aplicar migrações:
    ```bash
    python manage.py makemigrations
    python manage.py migrate

---

## Integração com EVE Online (OAuth2)

1. Registre sua aplicação no EVE Developers.
2. Obtenha CLIENT_ID e CLIENT_SECRET.
3. Configure no settings.py
    ```bash
    EVE_CLIENT_ID = 'sua_client_id'
    EVE_CLIENT_SECRET = 'sua_client_secret'
    EVE_REDIRECT_URI = 'http://127.0.0.1:8000/eve-callback/'
---

## Execução do Projeto

1. Rodar o servidor de desenvolvimento:
    ```bash
    python manage.py runserver

2. Acesse http://127.0.0.1:8000/ para ver a página inicial.

3. Acesse /admin/ se quiser gerenciar modelos via Django Admin (necessário um superusuário)
    ```bash
    python manage.py createsuperuser

---

## Uso do Sistema
1. Home Pública: Caso exista uma home inicial, o usuário encontra o botão “Login com EVE”.
2. Login: Redireciona ao EVE SSO; após autorizar, o usuário retorna autenticado.
3. Home Logada: Exibe o menu lateral, opções de “Solicitar Nave”, “Perfil”, etc.
4. Solicitar Nave:
    - Selecione a nave no menu tree ou use autocomplete.
    - Clique em “Solicitar” para criar o pedido (status “Pendente”).
    - Opcionalmente, o sistema envia mail in-game ao personagem.

### Pedidos:
- Exibe a tabela com as naves solicitadas, status em vermelho e data.

---

## Estrutura de Pastas

    ```bash
        eve_mkt/
    ├── eve_mkt/
    │   ├── settings.py
    │   ├── urls.py
    │   └── ...
    ├── core/
    │   ├── models.py
    │   ├── views.py
    │   ├── utils.py            # Funções de envio de mail, refresh token, etc.
    │   ├── templates/
    │   │   ├── layout_logado.html
    │   │   ├── solicitar_nave.html
    │   │   └── ...
    │   ├── static/
    │   │   ├── css/
    │   │   │   └── style.css
    │   │   └── js/
    │   │       ├── jquery.min.js
    │   │       └── ...
    │   └── ...
    ├── manage.py
    └── requirements.txt

---
## Observações finais

- Token Expirado: Lembre-se de refresh tokens se quiser manter o usuário logado por mais tempo.
- Scopes: Para envio de mail, é obrigatório o escopo esi-mail.send_mail.v1.
- Menu Tree: Use CSS e JS para expandir/colapsar categorias com ícones de foguete.
- Contribuições: Sinta-se à vontade para abrir PRs e Issues se encontrar problemas ou tiver sugestões.
