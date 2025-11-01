# ⚡ Quick Fix - Erro OAuth2 EVE Online

## 🎯 Problema
```
Error: "The callback URI doesn't match the value stored for this client"
```

## ✅ Solução Rápida (5 minutos)

### 1️⃣ EVE Developers Portal
1. Acesse: https://developers.eveonline.com/
2. **Manage Applications** → Sua aplicação
3. **Callback URL:** Adicione estas 3 URLs:

```
https://www.pulaleeroybrasil.com.br/eve-callback/
https://pulaleeroybrasil.com.br/eve-callback/
https://leeroy-market-9e6b5666aca1.herokuapp.com/eve-callback/
```

4. **Save/Update Application**

### 2️⃣ Deploy
```bash
git add eve_mkt/settings.py
git commit -m "Fix: Atualiza redirect URI para domínio customizado"
git push heroku main
heroku restart
```

### 3️⃣ Teste
1. Limpe cache do navegador (Ctrl+Shift+Delete)
2. Acesse: https://www.pulaleeroybrasil.com.br
3. Clique em "Login com EVE Online"
4. ✅ Deve funcionar!

---

## ⚠️ Importante
- ✅ Mantenha a **/** no final das URLs
- ✅ Use **https://**, não http://
- ✅ Adicione **TODOS** os 3 callbacks
- ⏱️ Aguarde 1-2 minutos após salvar no EVE Developers

---

## 🐛 Ainda Não Funciona?

### Verificar logs:
```bash
heroku logs --tail
```

### Limpar sessão:
- Use aba anônima/privada
- Ou limpe cookies do site

### Confirmar no EVE Developers:
- Volte ao portal
- Verifique se os 3 callbacks estão salvos
- Confirme que terminam com **/**

---

## 📚 Guia Completo
Para instruções detalhadas, veja: **CORRIGIR_EVE_OAUTH.md**

---

**Status:** settings.py já foi atualizado ✅  
**Próximo passo:** Atualizar EVE Developers Portal

