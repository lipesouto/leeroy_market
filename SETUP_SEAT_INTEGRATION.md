# 🔗 Guia de Integração Híbrida - SeAT + Sistema de Pedidos

## 📊 Visão Geral

Esta integração permite:
- ✅ **Seu Sistema:** Gerencia pedidos de naves (já pronto e modernizado)
- ✅ **SeAT:** Fornece dados corporativos (wallet, assets, membros, etc)

---

## 🎯 Arquitetura da Solução

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│  pulaleeroybrasil.com.br (Seu Sistema)                 │
│  ┌──────────────────────────────────────────────────┐  │
│  │                                                  │  │
│  │  ┌──────────────┐      ┌──────────────┐        │  │
│  │  │  Pedidos de  │      │  Dashboard   │        │  │
│  │  │    Naves     │      │  Corporativo │        │  │
│  │  │  (Seu DB)    │      │  (SeAT API)  │        │  │
│  │  └──────────────┘      └──────┬───────┘        │  │
│  │                                │                │  │
│  └────────────────────────────────┼────────────────┘  │
│                                   │                   │
└───────────────────────────────────┼───────────────────┘
                                    │
                                    │ API Requests
                                    │
┌───────────────────────────────────▼───────────────────┐
│                                                        │
│  seat.sua-corporacao.com (SeAT Instance)              │
│  ┌──────────────────────────────────────────────┐    │
│  │                                              │    │
│  │  ┌──────┐  ┌────────┐  ┌─────────┐         │    │
│  │  │Wallet│  │ Assets │  │ Members │         │    │
│  │  └──────┘  └────────┘  └─────────┘         │    │
│  │                                              │    │
│  │           SeAT Database                      │    │
│  └──────────────────────────────────────────────┘    │
│                                                        │
└────────────────────────────────────────────────────────┘
```

---

## 📥 FASE 1: Instalar SeAT

### Opção A: Docker (Recomendado)

#### 1.1 Requisitos
- Servidor Linux (Ubuntu 20.04+ recomendado)
- 2GB RAM mínimo (4GB recomendado)
- Docker + Docker Compose instalados

#### 1.2 Instalação

```bash
# 1. Criar diretório
mkdir -p /opt/seat-docker
cd /opt/seat-docker

# 2. Baixar docker-compose
curl -L https://raw.githubusercontent.com/eveseat/seat-docker/master/docker-compose.yml -o docker-compose.yml
curl -L https://raw.githubusercontent.com/eveseat/seat-docker/master/.env.example -o .env

# 3. Configurar .env
nano .env
```

**Configurações importantes no .env:**
```bash
# Database
DB_HOST=mariadb
DB_PORT=3306
DB_DATABASE=seat
DB_USERNAME=seat
DB_PASSWORD=SuaSenhaForteAqui

# EVE SSO
EVE_CLIENT_ID=seu_client_id
EVE_CLIENT_SECRET=seu_client_secret
EVE_CALLBACK_URL=https://seat.sua-corporacao.com/auth/eve/callback

# App
APP_URL=https://seat.sua-corporacao.com
APP_KEY=base64:...gerado_automaticamente
```

```bash
# 4. Iniciar SeAT
docker-compose up -d

# 5. Gerar APP_KEY
docker-compose exec seat-web php artisan key:generate

# 6. Rodar migrations
docker-compose exec seat-web php artisan migrate

# 7. Criar usuário admin
docker-compose exec seat-web php artisan seat:admin:login
```

#### 1.3 Acessar SeAT
- Acesse: `https://seat.sua-corporacao.com`
- Faça login com EVE Online
- Configure permissões

### Opção B: VPS/Cloud

**Provedores Recomendados:**
- DigitalOcean (Droplet $12/mês)
- Linode ($10/mês)
- Vultr ($10/mês)
- AWS EC2 t3.small

**Tutorial Completo:** https://eveseat.github.io/docs/installation/docker_installation/

---

## 🔑 FASE 2: Configurar API Token no SeAT

### 2.1 Criar API Token

1. Acesse SeAT
2. Vá em **Settings** → **API Tokens**
3. Clique em **Create New Token**
4. Configure:
   - **Name:** "Sistema de Pedidos"
   - **Permissions:** 
     - ✅ `corporation.read`
     - ✅ `corporation.wallet`
     - ✅ `corporation.assets`
     - ✅ `character.read`

5. Copie o token gerado (será algo como):
   ```
   eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9...
   ```

### 2.2 Configurar no Heroku

```bash
# Adicionar token como variável de ambiente
heroku config:set SEAT_API_URL="https://seat.sua-corporacao.com/api/v2"
heroku config:set SEAT_API_TOKEN="seu_token_aqui"
heroku config:set SEAT_CORPORATION_ID="sua_corporation_id"
```

---

## 🔧 FASE 3: Integração no Código

### 3.1 Adicionar Biblioteca HTTP

Já temos `requests` no requirements.txt ✅

### 3.2 Estrutura de Código

```python
# core/seat_integration.py (SERÁ CRIADO)
"""
Integração com SeAT API
"""
import requests
from django.conf import settings

class SeATAPI:
    def __init__(self):
        self.base_url = settings.SEAT_API_URL
        self.token = settings.SEAT_API_TOKEN
        self.headers = {
            'Authorization': f'Bearer {self.token}',
            'Accept': 'application/json'
        }
    
    def get_corporation_wallet(self):
        """Busca saldo da corporação"""
        pass
    
    def get_corporation_assets(self):
        """Busca assets da corporação"""
        pass
    
    def get_members(self):
        """Busca membros da corporação"""
        pass
```

---

## 📊 FASE 4: Dashboard Híbrido

### 4.1 Layout

```
┌─────────────────────────────────────────────┐
│         Dashboard Corporativo               │
├─────────────────────────────────────────────┤
│                                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐ │
│  │ Wallet   │  │ Membros  │  │ Assets   │ │
│  │ (SeAT)   │  │ (SeAT)   │  │ (SeAT)   │ │
│  └──────────┘  └──────────┘  └──────────┘ │
│                                             │
│  ┌─────────────────────────────────────┐   │
│  │  Pedidos de Naves (Seu Sistema)     │   │
│  │  ┌───┬──────┬────────┬──────────┐   │   │
│  │  │ # │ Nave │ Status │ Data     │   │   │
│  │  ├───┼──────┼────────┼──────────┤   │   │
│  │  │ 1 │Raven │Pendente│01/11/25  │   │   │
│  │  └───┴──────┴────────┴──────────┘   │   │
│  └─────────────────────────────────────┘   │
│                                             │
└─────────────────────────────────────────────┘
```

---

## 🎯 Endpoints da API SeAT

### Principais Endpoints

```bash
# Corporation
GET /api/v2/corporation/{id}/wallet
GET /api/v2/corporation/{id}/assets
GET /api/v2/corporation/{id}/members
GET /api/v2/corporation/{id}/structures

# Character
GET /api/v2/character/{id}/wallet
GET /api/v2/character/{id}/skills
GET /api/v2/character/{id}/assets
```

### Exemplo de Resposta

```json
// GET /api/v2/corporation/{id}/wallet
{
  "data": [
    {
      "division": 1,
      "balance": 1234567890.50
    }
  ]
}
```

---

## 🔐 Segurança

### Variáveis de Ambiente

```bash
# settings.py
SEAT_API_URL = os.getenv('SEAT_API_URL', '')
SEAT_API_TOKEN = os.getenv('SEAT_API_TOKEN', '')
SEAT_CORPORATION_ID = os.getenv('SEAT_CORPORATION_ID', '')
```

### Proteção de Rotas

```python
from functools import wraps
from django.http import HttpResponseForbidden

def require_director(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Verificar se usuário é diretor
        if not request.user.eve_profile:
            return HttpResponseForbidden()
        
        # Aqui você pode verificar roles no SeAT
        return view_func(request, *args, **kwargs)
    return wrapper

@require_director
def corporation_dashboard(request):
    # Apenas diretores podem ver
    pass
```

---

## 📈 Benefícios da Integração

### Seu Sistema
- ✅ Gerencia pedidos de naves
- ✅ Interface moderna Bootstrap 5
- ✅ Específico e focado
- ✅ Fácil de manter

### SeAT
- ✅ Wallet tracking completo
- ✅ Asset management
- ✅ Member tracking
- ✅ Structure management
- ✅ Industry jobs
- ✅ Contract tracking

### Juntos
- 🎯 Sistema completo de gestão
- 🎯 Melhor dos dois mundos
- 🎯 Cada um faz o que faz de melhor

---

## 🧪 Testes

### 1. Testar Conexão SeAT

```python
# teste_seat.py
import requests

SEAT_API_URL = "https://seat.sua-corporacao.com/api/v2"
SEAT_API_TOKEN = "seu_token"

headers = {
    'Authorization': f'Bearer {SEAT_API_TOKEN}',
    'Accept': 'application/json'
}

# Testar conexão
response = requests.get(f"{SEAT_API_URL}/corporation/123456/wallet", headers=headers)
print(response.status_code)
print(response.json())
```

### 2. Testar em Ambiente Local

```bash
# .env.local
SEAT_API_URL=https://seat.sua-corporacao.com/api/v2
SEAT_API_TOKEN=seu_token_de_teste
SEAT_CORPORATION_ID=123456
```

---

## 📋 Checklist de Implementação

### Setup SeAT
```
☐ Servidor provisionado
☐ Docker instalado
☐ SeAT instalado e rodando
☐ Domínio configurado (seat.sua-corporacao.com)
☐ SSL/HTTPS configurado
☐ Login EVE configurado no SeAT
☐ Personagens e corp adicionados
☐ API Token criado
```

### Configuração Sistema
```
☐ Variáveis de ambiente configuradas no Heroku
☐ Módulo seat_integration.py criado
☐ Views atualizadas
☐ Templates do dashboard criados
☐ Testes de conexão realizados
☐ Deploy feito
```

### Funcionalidades
```
☐ Dashboard mostra wallet
☐ Dashboard mostra assets
☐ Dashboard mostra membros
☐ Pedidos de naves integrados
☐ Permissões configuradas
```

---

## 💰 Custos Estimados

### SeAT (mensal)
- **VPS:** $10-12/mês
- **Domínio:** $1-2/mês
- **SSL:** Grátis (Let's Encrypt)
- **Total:** ~$12/mês

### Seu Sistema (atual)
- **Heroku Free:** $0/mês
- **Domínio:** Já tem
- **Total:** $0/mês

**Custo Total:** ~$12/mês

---

## 🔄 Próximos Passos

1. **Você:** Instalar SeAT em um servidor
2. **Você:** Criar API token no SeAT
3. **Eu:** Implementar integração no código
4. **Eu:** Criar dashboard híbrido
5. **Juntos:** Testar e ajustar

---

## 📚 Recursos

- [SeAT Documentation](https://eveseat.github.io/docs/)
- [SeAT API Reference](https://eveseat.github.io/docs/developer_guides/api/)
- [SeAT Discord](https://discord.gg/fKnFjz7)

---

**Pronto para começar?** 

Quando você tiver o SeAT instalado e o token da API, me avise que implemento a integração completa! 🚀

