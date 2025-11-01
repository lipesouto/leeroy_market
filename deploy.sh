#!/bin/bash

# Script de Deploy Rápido para Heroku
# EVE Market System

echo "🚀 Iniciando Deploy no Heroku..."
echo ""

# 1. Adicionar arquivos ao Git
echo "📦 Adicionando arquivos ao Git..."
git add .

# 2. Commit
echo "💾 Fazendo commit..."
read -p "Digite a mensagem do commit: " commit_msg
git commit -m "$commit_msg"

# 3. Push para Heroku
echo "⬆️  Fazendo push para o Heroku..."
git push heroku main

# 4. Escalar Dyno
echo "🔄 Escalando dyno web..."
heroku ps:scale web=1

# 5. Collectstatic
echo "📁 Coletando arquivos estáticos..."
heroku run python manage.py collectstatic --noinput

# 6. Verificar status
echo ""
echo "✅ Deploy concluído!"
echo ""
echo "📊 Status dos processos:"
heroku ps

echo ""
echo "🌐 Abrindo aplicação..."
heroku open

echo ""
echo "📋 Para ver os logs, execute:"
echo "   heroku logs --tail"

