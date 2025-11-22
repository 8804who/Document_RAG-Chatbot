"""
Application-wide constants.
"""


class APIEndpoints:
    """API endpoint paths."""

    CHAT = "/api/v1/chatbot/chat"
    CHAT_HEALTH = "/api/v1/chatbot/health"
    AUTH_VERIFY = "/api/v1/auth/verify"
    AUTH_REFRESH = "/api/v1/auth/refresh"
    AUTH_LOGOUT = "/api/v1/auth/logout"
    AUTH_LOGIN = "/api/v1/auth/login"
    AUTH_CALLBACK = "/api/v1/auth/login/callback"
    DOCUMENTS_UPLOAD = "/api/v1/documents/user"
    DOCUMENTS_LIST = "/api/v1/documents/user"
    DOCUMENTS_DELETE = "/api/v1/documents/{document_id}"


class LogMessages:
    """Standard log messages."""

    SERVER_STARTING = "Server is starting..."
    SERVER_STOPPING = "Server is stopping..."
    AUTH_FAILED = "Authentication failed"
    TOKEN_REFRESH_FAILED = "Token refresh failed"
    TOKEN_REVOCATION_FAILED = "Token revocation failed"
    DOCUMENT_UPLOADED = "Document uploaded successfully"
    DOCUMENT_DELETED = "Document deleted successfully"


class ErrorMessages:
    """Standard error messages."""

    INVALID_TOKEN = "Invalid token"
    TOKEN_REQUIRED = "Token is required"
    REFRESH_TOKEN_REQUIRED = "Refresh token is required"
    ACCESS_TOKEN_REQUIRED = "Access token is required"
    DOCUMENT_NOT_FOUND = "Document not found"
    DATABASE_ERROR = "Database operation failed"
    VECTOR_STORE_ERROR = "Vector store operation failed"


class GoogleOAuth:
    """Google OAuth related constants."""

    TOKENINFO_URL = "https://oauth2.googleapis.com/tokeninfo"
    TOKEN_URL = "https://oauth2.googleapis.com/token"
    REVOKE_URL = "https://oauth2.googleapis.com/revoke"
    METADATA_URL = "https://accounts.google.com/.well-known/openid-configuration"
    SCOPE = "openid email profile"


class FrontendConfig:
    """Frontend configuration constants."""

    DEFAULT_ORIGIN = "http://localhost:10002"
    CALLBACK_ORIGIN = "http://localhost:10002"
