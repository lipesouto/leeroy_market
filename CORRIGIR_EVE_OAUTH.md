# 🔐 Guia: Corrigir Erro de OAuth2 - EVE Online

## ❌ Erro Recebido
```json
{
  "error": "invalid_request",
  "error_description": "The callback URI doesn't match the value stored for this client"
}
```

---

## 🎯 Causa do Problema

O **redirect URI** (callback URL) configurado no EVE Developers não corresponde ao domínio que você está usando.

### Configuração Anterior
- **EVE Developers:** `https://leeroy-market-9e6b5666aca1.herokuapp.com/eve-callback/`
- **Domínio Atual:** `https://www.pulaleeroybrasil.com.br`

❌ **Não Corresponde!**

---

## ✅ Solução Completa

### **Passo 1: Atualizar no EVE Developers Portal**

#### 1.1. Acessar o Portal
1. Acesse: https://developers.eveonline.com/
2. Clique em **"Sign In"**
3. Faça login com sua conta EVE Online

#### 1.2. Localizar Sua Aplicação
1. No menu superior, clique em **"Manage Applications"**
2. Você verá sua aplicação listada
3. Clique no **nome da aplicação** ou em **"View"**

#### 1.3. Editar Callback URLs
1. Procure a seção **"Callback URL"** ou **"Redirect URIs"**
2. Você verá o callback atual:
   ```
   https://leeroy-market-9e6b5666aca1.herokuapp.com/eve-callback/
   ```

3. **ADICIONE** (não substitua, adicione!) os novos callbacks:
   ```
   https://www.pulaleeroybrasil.com.br/eve-callback/
   https://pulaleeroybrasil.com.br/eve-callback/
   https://leeroy-market-9e6b5666aca1.herokuapp.com/eve-callback/
   ```

   ⚠️ **IMPORTANTE:**
   - Mantenha a **barra** `/` no final de cada URL
   - Adicione **TODOS** os domínios possíveis
   - Use **https://**, não http://

#### 1.4. Atualizar Escopos (se necessário)
Certifique-se de que o escopo está configurado:
```
esi-mail.send_mail.v1
```

#### 1.5. Salvar
1. Role até o final da página
2. Clique em **"Update Application"** ou **"Save"**
3. Aguarde a mensagem de confirmação

---

### **Passo 2: Atualizar settings.py**

✅ **JÁ ATUALIZADO!**

O arquivo `settings.py` foi atualizado para:
```python
EVE_REDIRECT_URI = 'https://www.pulaleeroybrasil.com.br/eve-callback/'
```

---

### **Passo 3: Deploy no Heroku**

Execute no terminal:

```bash
# 1. Commit da mudança
git add eve_mkt/settings.py
git commit -m "Atualiza redirect URI para domínio customizado"

# 2. Deploy
git push heroku main

# 3. Reiniciar aplicação
heroku restart
```

Ou use o script automático:
```bash
.\deploy.bat
```

---

## 🧪 Testar a Correção

### 1. Limpar Cache do Navegador
- Pressione `Ctrl + Shift + Delete`
- Limpe cookies e cache
- Ou use aba anônima

### 2. Acessar a Aplicação
```
https://www.pulaleeroybrasil.com.br
```

### 3. Clicar em "Login com EVE Online"
- Você será redirecionado para o EVE SSO
- Autorize a aplicação
- Você deve ser redirecionado de volta **SEM ERRO**

---

## 🔍 Verificar Configuração

### No EVE Developers Portal

Sua aplicação deve ter:

**Application Name:** (seu nome de app)

**Callback URLs:**
```
https://www.pulaleeroybrasil.com.br/eve-callback/
https://pulaleeroybrasil.com.br/eve-callback/
https://leeroy-market-9e6b5666aca1.herokuapp.com/eve-callback/
```

**Scopes:**
```
esi-mail.send_mail.v1
```

**Client ID:**
```
995968f151a54fc5b0870da6c0ddb455
```

**Client Secret:**
```
lkrKmQEiYwFlLhc87aZLhshaoGj9mPnkhY82my6Z
```
⚠️ **Mantenha secreto!**

---

## 🐛 Se Ainda Não Funcionar

### Erro Persiste Após Configurar

#### 1. Verificar se salvou no EVE Developers
- Volte ao portal
- Confirme que os 3 callbacks estão listados

#### 2. Verificar o redirect URI exato
Adicione um print temporário em `views.py`:

```python
def login_eve(request):
    client_id = settings.EVE_CLIENT_ID
    redirect_uri = settings.EVE_REDIRECT_URI
    
    # DEBUG: Imprimir redirect URI
    print(f"DEBUG - Redirect URI: {redirect_uri}")
    
    scope = "esi-mail.send_mail.v1"
    auth_url = (
        f"https://login.eveonline.com/oauth/authorize?response_type=code"
        f"&redirect_uri={redirect_uri}&client_id={client_id}"
        f"&scope={scope}"
    )
    return redirect(auth_url)
```

Verifique os logs:
```bash
heroku logs --tail
```

#### 3. Verificar URL de Callback
Copie a URL completa que aparece no erro e compare:
- URL no erro: `_____________________`
- URL no EVE Developers: `_____________________`

Elas devem ser **EXATAMENTE** iguais!

---

## 📋 Checklist de Configuração

```
☐ EVE Developers atualizado com todos os callbacks
☐ Callbacks incluem a barra / no final
☐ settings.py atualizado com o novo redirect URI
☐ Deploy feito no Heroku
☐ Aplicação reiniciada
☐ Cache do navegador limpo
☐ Teste realizado em aba anônima
```

---

## 💡 Dicas Importantes

### 1. Múltiplos Domínios
O EVE Developers **permite múltiplos callbacks**. Adicione todos:
- Domínio customizado (www)
- Domínio customizado (sem www)
- Domínio Heroku

### 2. Barra Final
A barra `/` no final é **obrigatória**:
- ✅ `https://dominio.com/eve-callback/`
- ❌ `https://dominio.com/eve-callback`

### 3. HTTPS vs HTTP
Use sempre **HTTPS** em produção:
- ✅ `https://dominio.com/eve-callback/`
- ❌ `http://dominio.com/eve-callback/`

### 4. Desenvolvimento Local
Para testar localmente, adicione também:
```
http://127.0.0.1:8000/eve-callback/
http://localhost:8000/eve-callback/
```

---

## 🔄 Para Ambiente de Desenvolvimento

Se quiser testar localmente, use variáveis de ambiente:

```python
# settings.py
import os

DEBUG = os.getenv('DEBUG', 'False') == 'True'

if DEBUG:
    EVE_REDIRECT_URI = 'http://127.0.0.1:8000/eve-callback/'
else:
    EVE_REDIRECT_URI = 'https://www.pulaleeroybrasil.com.br/eve-callback/'
```

E adicione no EVE Developers:
```
http://127.0.0.1:8000/eve-callback/
http://localhost:8000/eve-callback/
```

---

## 📸 Screenshots de Referência

### Como Deve Ficar no EVE Developers

```
┌─────────────────────────────────────────────────┐
│ Application Details                             │
├─────────────────────────────────────────────────┤
│                                                 │
│ Application Name: [EVE Market System]           │
│                                                 │
│ Description: [Sistema de solicitação de naves] │
│                                                 │
│ Callback URL:                                   │
│ https://www.pulaleeroybrasil.com.br/eve-callback/  │
│ https://pulaleeroybrasil.com.br/eve-callback/      │
│ https://leeroy-market-9e6b5666aca1.herokuapp... │
│                                                 │
│ Requested Scopes:                               │
│ ☑ esi-mail.send_mail.v1                        │
│                                                 │
│ [Update Application]                            │
└─────────────────────────────────────────────────┘
```

---

## ✅ Confirmação de Sucesso

Após configurar corretamente, você verá:

1. ✅ Redirecionamento para EVE SSO funciona
2. ✅ Página de autorização do EVE aparece
3. ✅ Após autorizar, retorna ao seu site
4. ✅ Login é concluído com sucesso
5. ✅ Dashboard é exibido com seu nome

---

## 📞 Suporte

Se o problema persistir:

1. **Verifique os logs:**
   ```bash
   heroku logs --tail
   ```

2. **Teste em diferentes navegadores:**
   - Chrome (aba anônima)
   - Firefox (janela privada)
   - Edge

3. **Aguarde alguns minutos:**
   - Mudanças no EVE Developers podem levar 1-2 minutos para propagar

4. **Revise a documentação oficial:**
   - https://developers.eveonline.com/blog/article/sso-to-authenticated-calls

---

**Data:** 01/11/2025  
**Status:** Configuração Atualizada ✅

