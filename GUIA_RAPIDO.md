# 🚀 Guia Rápido - EVE Market System

## 📖 Índice Rápido
1. [Acesso ao Sistema](#acesso-ao-sistema)
2. [Navegação](#navegação)
3. [Solicitar Nave](#solicitar-nave)
4. [Ver Pedidos](#ver-pedidos)
5. [Perfil](#perfil)
6. [Dicas e Atalhos](#dicas-e-atalhos)

---

## 🔐 Acesso ao Sistema

### Primeira Vez
1. Acesse a página inicial: `https://seu-dominio.com/`
2. Clique no botão **"Login com EVE Online"**
3. Você será redirecionado para o EVE Online SSO
4. Autorize o aplicativo
5. Você será redirecionado de volta ao sistema

### Login Subsequente
- O sistema mantém você logado por tempo determinado
- Se a sessão expirar, basta clicar em **"Login com EVE"** novamente

---

## 🧭 Navegação

### Menu Lateral (Sidebar)
O menu está sempre visível no lado esquerdo da tela:

```
📱 EVE Market
   👤 [Seu Nome]
   
   🏠 Home              → Dashboard principal
   🛒 Solicitar Nave    → Fazer novos pedidos
   👤 Perfil            → Suas informações
   🚪 Sair              → Fazer logout
```

### Indicador de Página Ativa
- A página atual fica **destacada em azul** no menu
- Facilita saber onde você está no sistema

---

## 🛒 Solicitar Nave

### Método 1: Busca Rápida (Recomendado)
1. Vá em **"Solicitar Nave"**
2. Digite o nome da nave no campo de busca
3. Aguarde o autocomplete aparecer
4. Clique na nave desejada
5. Verifique os detalhes no card azul
6. Clique em **"Solicitar"**

**Dica:** Digite pelo menos 2 letras para ativar o autocomplete

### Método 2: Menu de Categorias
1. Vá em **"Solicitar Nave"**
2. Role até a seção **"Navegação por Categoria"**
3. Clique no **ícone de foguete** da categoria desejada
4. O menu se expande mostrando as naves
5. Clique na nave desejada
6. Verifique os detalhes
7. Clique em **"Solicitar"**

**Dica:** O ícone muda de 🚀 para 🚀↗️ quando expandido

### Confirmação
Após solicitar, você verá:
- ✅ Mensagem verde de sucesso
- 📧 Confirmação de e-mail in-game (se disponível)
- O pedido aparece na lista lateral

---

## 📋 Ver Pedidos

### Dashboard (Home)
Acesse o **Dashboard** para ver:

#### Cards de Estatísticas
```
📊 Total de Pedidos    ⏳ Pendentes    🚀 Ação Rápida
       5                    3           [Nova Solicitação]
```

#### Tabela de Pedidos
Mostra todos os seus pedidos com:
- **#** - Número sequencial
- **🚀 Nave** - Nome e categoria
- **ℹ️ Status** - Badge colorido
  - 🟡 Amarelo = Pendente
  - 🟢 Verde = Aprovado
  - 🔴 Vermelho = Rejeitado
- **📅 Data** - Data e hora da solicitação

### Lista Lateral (Solicitar Nave)
Na página de solicitação, você vê os **10 pedidos mais recentes** na barra lateral direita.

---

## 👤 Perfil

### Informações Disponíveis

#### Coluna Esquerda
- **🖼️ Avatar** - Sua foto do EVE Online
- **🆔 Character ID** - Seu ID único
- **✅ Status da Conta** - Ativo/Inativo
- **⭐ Tipo de Conta** - Staff/Usuário

#### Coluna Direita
- **👤 Detalhes do Personagem**
  - Nome
  - Character ID
  
- **🔑 Autenticação**
  - Status do token
  - Data de expiração
  
- **🔌 Integrações**
  - ESI Mail - Envio de e-mails in-game
  - OAuth2 - Autenticação segura

---

## 💡 Dicas e Atalhos

### Navegação Rápida

#### No Dashboard
- **"Nova Solicitação"** → Vai direto para solicitar nave
- **"Ver Perfil"** → Acessa seu perfil

#### Na Solicitação de Nave
- **"Ver Todos"** → Volta ao dashboard com todos os pedidos
- **ESC** → Fecha o autocomplete

### Atalhos de Teclado
```
Tab       → Navega entre campos
Enter     → Submete formulário
Esc       → Fecha dropdowns
Setas     → Navega no autocomplete
```

### Funcionalidades Inteligentes

#### 1. Autocomplete Inteligente
- Busca por **qualquer parte** do nome
- **Case insensitive** (maiúsculas/minúsculas)
- Mostra **categoria** de cada resultado
- Máximo de **10 resultados**

Exemplos:
- "rav" → Encontra "**Rav**en"
- "drake" → Encontra "**Drake**"
- "hur" → Encontra "**Hur**ricane"

#### 2. Menu Inteligente
- Fecha automaticamente **outras categorias**
- Ícone animado indica **estado**
- **Badge** mostra quantidade de naves

#### 3. Validação de Formulário
- Não permite enviar **sem selecionar** nave
- Alerta visual se tentar submeter vazio
- Confirmação visual ao selecionar

### Mensagens do Sistema

#### Tipos de Mensagem
```
✅ SUCESSO (Verde)
   "Pedido criado com sucesso!"
   
⚠️ AVISO (Amarelo)
   "Pedido criado, mas sem notificação por e-mail."
   
❌ ERRO (Vermelho)
   "Por favor, selecione uma nave antes de solicitar."
   
ℹ️ INFO (Azul)
   "Notificação enviada por e-mail in-game!"
```

#### Como Fechar
- Clique no **X** no canto superior direito
- Ou aguarde **5 segundos** (auto-close)

---

## 📱 Uso em Mobile

### Layout Adaptativo
O sistema se adapta automaticamente ao tamanho da tela:

#### Desktop (> 768px)
- Sidebar fixa no lado esquerdo
- Layout de 2 colunas
- Menu sempre visível

#### Tablet (576px - 768px)
- Sidebar responsiva
- Layout adaptável
- Ícones maiores para toque

#### Mobile (< 576px)
- Sidebar colapsada
- Layout de 1 coluna
- Menu hambúrguer
- Botões grandes para toque

### Gestos
- **Swipe** → Navega entre páginas (browser nativo)
- **Tap** → Clica em elementos
- **Long Press** → Menu contextual

---

## 🔍 Solução de Problemas

### Não consigo fazer login
**Causa:** Você não pertence à corporação "PulaLeeroy BR"
**Solução:** Apenas membros da corporação podem acessar

### Autocomplete não funciona
**Causa:** JavaScript desabilitado ou conexão lenta
**Solução:** Use o menu de categorias

### Não vejo minhas naves
**Causa:** Banco de dados não sincronizado
**Solução:** Contate o administrador

### Página não carrega corretamente
**Causa:** Cache do browser ou CSS não carregado
**Solução:** 
1. Pressione `Ctrl + F5` (Windows) ou `Cmd + Shift + R` (Mac)
2. Limpe o cache do navegador
3. Verifique conexão com internet

### E-mail in-game não chega
**Causa:** Token expirado ou sem permissão
**Solução:** 
1. Faça logout
2. Faça login novamente
3. Autorize novamente as permissões

---

## 🎯 Melhores Práticas

### 1. Mantenha o Token Atualizado
- Faça login pelo menos **1x por semana**
- Isso mantém o token ativo
- Evita problemas com notificações

### 2. Use a Busca Rápida
- Mais rápido que navegar categorias
- Menos cliques
- Mais eficiente

### 3. Verifique Seus Pedidos
- Acesse o Dashboard regularmente
- Acompanhe o status
- Veja datas de solicitação

### 4. Mantenha Perfil Atualizado
- Verifique informações periodicamente
- Confirme status de autenticação
- Atualize se necessário

---

## 🆘 Precisa de Ajuda?

### Documentação Completa
- **ANALISE_TECNICA.md** - Análise detalhada do sistema
- **MELHORIAS_BOOTSTRAP.md** - Guia de componentes visuais
- **RESUMO_MELHORIAS.md** - Resumo das melhorias

### Contato
- **In-Game:** Envie mail para administrador
- **Discord:** Canal da corporação
- **GitHub:** Issues do repositório

---

## 📊 Atalhos Visuais

### Cores dos Badges
```
🟡 Amarelo    → Pendente (aguardando aprovação)
🟢 Verde      → Aprovado (nave em processo)
🔴 Vermelho   → Rejeitado (pedido negado)
⚪ Cinza      → Outros status
```

### Ícones Importantes
```
🏠 Home           → Página inicial
🛒 Bag Plus       → Solicitar nave
👤 Person         → Perfil
🚪 Box Arrow      → Sair
🚀 Rocket         → Nave/Categoria
📅 Calendar       → Data
⏰ Clock          → Hora
✅ Check          → Sucesso/Aprovado
❌ X              → Erro/Rejeitado
⚠️ Triangle       → Aviso
ℹ️ Info           → Informação
```

---

## 🎓 Dicas Avançadas

### 1. Atalhos de URL
```
/                     → Página inicial (pública)
/home-logada/         → Dashboard
/solicitar-nave/      → Solicitar nave
/perfil/              → Seu perfil
/logout/              → Fazer logout
```

### 2. Bookmarks Úteis
Salve nos favoritos:
- Dashboard: `https://seu-dominio.com/home-logada/`
- Solicitar: `https://seu-dominio.com/solicitar-nave/`

### 3. Múltiplas Solicitações
Para solicitar várias naves:
1. Faça a primeira solicitação
2. A página recarrega automaticamente
3. Faça a próxima solicitação
4. Repita o processo

---

## ✅ Checklist Diário

```
☐ Acessar o sistema
☐ Verificar pedidos no dashboard
☐ Fazer novas solicitações (se necessário)
☐ Verificar e-mails in-game
☐ Atualizar status mental do token
☐ Logout ao terminar (opcional)
```

---

## 🌟 Recursos Destacados

### 🎨 Interface Moderna
- Design inspirado em EVE Online
- Tema dark para conforto visual
- Animações suaves

### 📱 Responsivo
- Funciona em qualquer dispositivo
- Layout adaptável
- Touch-friendly

### ⚡ Rápido
- Busca instantânea
- Carregamento otimizado
- Feedback imediato

### 🔒 Seguro
- Autenticação OAuth2
- Integração oficial EVE
- Dados protegidos

---

**Última Atualização:** 01/11/2025  
**Versão:** 1.0  
**Para mais detalhes, consulte a documentação completa!**

