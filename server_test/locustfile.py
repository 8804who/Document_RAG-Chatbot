from users.google_oauth_user import GoogleOAuthUser
from users.unauthenticated_user import UnauthenticatedUser

from core.config import settings

if settings.TEST_SCENARIO == "authenticated_user_chat":
    users = [GoogleOAuthUser]
elif settings.TEST_SCENARIO == "all":
    users = [GoogleOAuthUser, UnauthenticatedUser]
else:
    raise ValueError(f"Invalid test scenario: {settings.TEST_SCENARIO}")