import requests
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
def enviar_mail_eve(character_id, access_token, subject, body, recipient_id):
    url = f"https://esi.evetech.net/latest/characters/{character_id}/mail/"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "approved_cost": 0,
        "body": body,
        "subject": subject,
        "recipients": [
            {
                "recipient_id": recipient_id,  # ID do personagem que receberá o mail
                "recipient_type": "character"
            }
        ]
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 201:
        print("Mail enviado com sucesso!")
        return True
    else:
        print("Falha ao enviar mail:", response.status_code, response.text)
        return False


def refresh_eve_token(eve_profile):
    if not eve_profile.refresh_token:
        return False  # não temos refresh_token salvo

    token_url = "https://login.eveonline.com/oauth/token"
    data = {
        "grant_type": "refresh_token",
        "refresh_token": eve_profile.refresh_token
    }
    auth = (settings.EVE_CLIENT_ID, settings.EVE_CLIENT_SECRET)

    resp = requests.post(token_url, data=data, auth=auth)
    if resp.status_code == 200:
        token_data = resp.json()
        new_access_token = token_data.get('access_token')
        new_refresh_token = token_data.get('refresh_token', eve_profile.refresh_token)
        expires_in = token_data.get('expires_in', 0)

        eve_profile.access_token = new_access_token
        eve_profile.refresh_token = new_refresh_token
        eve_profile.token_expires = timezone.now() + timedelta(seconds=expires_in)
        eve_profile.save()
        return True
    else:
        return False

def verify_eve_token(access_token):
    verify_url = "https://login.eveonline.com/oauth/verify"
    headers = {"Authorization": f"Bearer {access_token}"}
    resp = requests.get(verify_url, headers=headers)
    if resp.status_code == 200:
        return resp.json()  # ex: {"CharacterID": 123, "Scopes": "esi-mail.send_mail.v1 ...", ...}
    return None