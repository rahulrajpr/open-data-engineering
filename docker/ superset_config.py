import os
import secrets

# ------------------------------
# SECURITY
# ------------------------------

# Generate a strong random secret key for production

SECRET_KEY = os.environ.get("SUPERSET_SECRET_KEY", secrets.token_urlsafe(64))

# Use secure session cookies

SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"

# ------------------------------
# DATABASE CONNECTION
# ------------------------------
# Superset metadata DB connection string
# (you’re already setting it via environment: SUPERSET_DATABASE_URI)

# ------------------------------
# CORS & CSRF
# ------------------------------

ENABLE_CORS = True

CORS_OPTIONS = {
    "supports_credentials": True,
    "origins": ["http://localhost:8088"],
    "methods": ["GET", "POST", "OPTIONS", "PUT", "DELETE"],
    "allow_headers": ["*"],
}


WTF_CSRF_ENABLED = True
WTF_CSRF_TIME_LIMIT = None  # Optional: disables CSRF token expiration

# ------------------------------
# EMAIL CONFIG (Optional)
# ------------------------------

EMAIL_NOTIFICATIONS = False

# ------------------------------
# FEATURE FLAGS
# ------------------------------

FEATURE_FLAGS = {
    "DASHBOARD_NATIVE_FILTERS": True,
    "ENABLE_TEMPLATE_PROCESSING": True,
    "ALERTS_ATTACH_REPORTS": True,
    "DYNAMIC_PLUGINS": True,
    "SCHEDULED_QUERIES": True,
    "TAGGING_SYSTEM": True,
}

# ------------------------------
# LOGGING (Optional, adjust if needed)
# ------------------------------

LOG_LEVEL = "INFO"