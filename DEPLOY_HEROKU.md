# 🚀 Guia de Deploy no Heroku - EVE Market

## 🔧 Arquivos Criados/Corrigidos

### ✅ Arquivos Necessários para Deploy
1. **`Procfile`** - Criado ✅
2. **`runtime.txt`** - Criado ✅
3. **`requirements.txt`** - Já existe ✅
4. **`settings.py`** - Atualizado ✅

---

## 📋 Passos para Deploy

### 1️⃣ **Commit das Mudanças**

Primeiro, adicione todos os novos arquivos e mudanças ao Git:

```bash
git add .
git commit -m "Adiciona Procfile, runtime.txt e melhorias Bootstrap 5"
```

### 2️⃣ **Push para o Heroku**

```bash
git push heroku main
```

Se você usa `master` ao invés de `main`:
```bash
git push heroku master
```

### 3️⃣ **Escalar o Dyno Web**

O erro H14 acontece porque o dyno web não está rodando. Execute:

```bash
heroku ps:scale web=1
```

Este comando inicia 1 instância do processo web.

### 4️⃣ **Verificar Status**

```bash
heroku ps
```

Você deve ver algo como:
```
=== web (Free): gunicorn eve_mkt.wsgi --log-file - (1)
web.1: up 2024/11/01 15:10:00 -0300 (~ 1m ago)
```

### 5️⃣ **Coletar Arquivos Estáticos**

```bash
heroku run python manage.py collectstatic --noinput
```

### 6️⃣ **Verificar Logs**

```bash
heroku logs --tail
```

---

## 🔍 Comandos Úteis de Diagnóstico

### Ver Processos Rodando
```bash
heroku ps
```

### Ver Logs em Tempo Real
```bash
heroku logs --tail
```

### Ver Configuração do App
```bash
heroku config
```

### Reiniciar a Aplicação
```bash
heroku restart
```

### Abrir a Aplicação
```bash
heroku open
```

### Executar Comandos Django
```bash
heroku run python manage.py <comando>
```

---

## 🐛 Resolução de Problemas

### Problema: "No web processes running"
**Causa:** Dyno web não está escalado

**Solução:**
```bash
heroku ps:scale web=1
```

### Problema: "Application error"
**Causa:** Erro no código ou configuração

**Solução:**
```bash
heroku logs --tail
```
Verifique o erro específico nos logs.

### Problema: "Static files not found"
**Causa:** Arquivos estáticos não coletados

**Solução:**
```bash
heroku run python manage.py collectstatic --noinput
```

### Problema: "Database connection error"
**Causa:** Configuração do banco incorreta

**Solução:** Verifique as credenciais em `settings.py`

---

## 📁 Arquivos Criados

### `Procfile`
```
web: gunicorn eve_mkt.wsgi --log-file -
```

**Explicação:**
- `web:` - Define um processo web
- `gunicorn` - Servidor WSGI para Python
- `eve_mkt.wsgi` - Módulo WSGI do Django
- `--log-file -` - Envia logs para stdout

### `runtime.txt`
```
python-3.12.7
```

**Explicação:**
- Especifica a versão exata do Python a ser usada
- Heroku instalará automaticamente esta versão

---

## ⚙️ Configurações Atualizadas

### `settings.py`

#### ALLOWED_HOSTS
```python
ALLOWED_HOSTS = [
    'leeroy-market-9e6b5666aca1.herokuapp.com',
    'www.pulaleeroybrasil.com.br',
    'pulaleeroybrasil.com.br',
]
```

**Por que?**
- Django bloqueia requisições de domínios não listados
- Adicionados os domínios customizados

---

## 🔐 Segurança - Próximos Passos

### ⚠️ IMPORTANTE: Mover Credenciais para Variáveis de Ambiente

Atualmente, as credenciais estão hardcoded no código. Isso é **INSEGURO**.

### Configurar no Heroku

```bash
# Secret Key
heroku config:set SECRET_KEY="sua-secret-key-aqui"

# EVE Online
heroku config:set EVE_CLIENT_ID="995968f151a54fc5b0870da6c0ddb455"
heroku config:set EVE_CLIENT_SECRET="lkrKmQEiYwFlLhc87aZLhshaoGj9mPnkhY82my6Z"

# Database (já configurado automaticamente pelo Heroku)
heroku config:set DATABASE_URL="sua-database-url"
```

### Atualizar `settings.py`

```python
import os

# Secret Key
SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback-key-for-dev')

# EVE Online
EVE_CLIENT_ID = os.environ.get('EVE_CLIENT_ID')
EVE_CLIENT_SECRET = os.environ.get('EVE_CLIENT_SECRET')

# Database
import dj_database_url
DATABASES = {
    'default': dj_database_url.config(
        default='postgresql://...',
        conn_max_age=600
    )
}
```

**Nota:** Você precisará adicionar `dj-database-url` ao `requirements.txt`

---

## 📊 Checklist de Deploy

```
☐ Procfile criado
☐ runtime.txt criado
☐ requirements.txt atualizado
☐ ALLOWED_HOSTS configurado
☐ Git commit feito
☐ Push para Heroku
☐ Dyno web escalado (heroku ps:scale web=1)
☐ Collectstatic executado
☐ Logs verificados
☐ Aplicação testada
☐ Variáveis de ambiente configuradas (recomendado)
```

---

## 🎯 Sequência Completa de Deploy

Execute estes comandos na ordem:

```bash
# 1. Commit
git add .
git commit -m "Deploy com Bootstrap 5 e correções"

# 2. Push
git push heroku main

# 3. Escalar dyno
heroku ps:scale web=1

# 4. Collectstatic
heroku run python manage.py collectstatic --noinput

# 5. Verificar
heroku ps
heroku logs --tail

# 6. Abrir aplicação
heroku open
```

---

## 🌐 Domínio Customizado

Se você ainda não configurou o domínio customizado:

```bash
# Adicionar domínio
heroku domains:add www.pulaleeroybrasil.com.br
heroku domains:add pulaleeroybrasil.com.br

# Ver domínios configurados
heroku domains
```

Configure os registros DNS no seu provedor:
- **CNAME:** www → seu-app.herokuapp.com
- **ALIAS/ANAME:** @ → seu-app.herokuapp.com

---

## 🔄 Atualizações Futuras

Sempre que fizer mudanças:

```bash
git add .
git commit -m "Descrição da mudança"
git push heroku main
heroku restart  # Se necessário
```

---

## 📞 Suporte

### Heroku CLI
```bash
heroku help
heroku help <comando>
```

### Documentação
- [Heroku Python](https://devcenter.heroku.com/categories/python)
- [Django on Heroku](https://devcenter.heroku.com/articles/django-app-configuration)
- [Heroku Logs](https://devcenter.heroku.com/articles/logging)

---

## ✅ Resultado Esperado

Após seguir todos os passos:

1. ✅ Aplicação rodando em `https://www.pulaleeroybrasil.com.br`
2. ✅ Interface Bootstrap 5 visível
3. ✅ Login EVE Online funcionando
4. ✅ Todas as páginas acessíveis
5. ✅ Arquivos estáticos carregando

---

**Data:** 01/11/2025  
**Status:** Pronto para Deploy 🚀

