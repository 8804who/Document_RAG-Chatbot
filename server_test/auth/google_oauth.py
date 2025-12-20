import httpx

from core.config import settings


GOOGLE_CLIENT_ID = settings.GOOGLE_CLIENT_ID
GOOGLE_CLIENT_SECRET = settings.GOOGLE_CLIENT_SECRET
GOOGLE_REFRESH_TOKEN = settings.GOOGLE_REFRESH_TOKEN


def get_google_access_token() -> str:
    with httpx.Client() as client:
        response = client.post(
            "https://oauth2.googleapis.com/token",
            data={
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET.get_secret_value(),
                "refresh_token": GOOGLE_REFRESH_TOKEN.get_secret_value(),
                "grant_type": "refresh_token",
            },
        )
        if response.status_code == 200:
            return response.json()["access_token"]
        else:
            raise Exception("Failed to get Google access token")
