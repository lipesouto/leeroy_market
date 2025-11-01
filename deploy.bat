@echo off
REM Script de Deploy Rapido para Heroku
REM EVE Market System

echo.
echo ========================================
echo   DEPLOY HEROKU - EVE Market System
echo ========================================
echo.

echo [1/6] Adicionando arquivos ao Git...
git add .

echo.
set /p commit_msg="Digite a mensagem do commit: "
echo.

echo [2/6] Fazendo commit...
git commit -m "%commit_msg%"

echo.
echo [3/6] Fazendo push para o Heroku...
git push heroku main

echo.
echo [4/6] Escalando dyno web...
heroku ps:scale web=1

echo.
echo [5/6] Coletando arquivos estaticos...
heroku run python manage.py collectstatic --noinput

echo.
echo [6/6] Verificando status...
heroku ps

echo.
echo ========================================
echo   DEPLOY CONCLUIDO!
echo ========================================
echo.
echo Para ver os logs, execute:
echo    heroku logs --tail
echo.
echo Abrindo aplicacao no navegador...
heroku open

pause

