import os
from pathlib import Path

import dj_database_url
from dotenv import load_dotenv
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables
load_dotenv(BASE_DIR / ".env")

# Security and environment
SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]

DEBUG = os.getenv("DJANGO_DEBUG", "False").lower() in (
    "true",
    "1",
    "yes",
)

ALLOWED_HOSTS = [
    host.strip()
    for host in os.getenv(
        "DJANGO_ALLOWED_HOSTS",
        "localhost,127.0.0.1,testserver",
    ).split(",")
    if host.strip()
]

# Application definition
INSTALLED_APPS = [
    "unfold",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "pages",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.template.context_processors.media",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "pages.context_processors.portfolio_globals",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

# Database: Neon PostgreSQL or local SQLite
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": ("django.contrib.auth.password_validation.MinimumLengthValidator"),
    },
    {
        "NAME": ("django.contrib.auth.password_validation.CommonPasswordValidator"),
    },
    {
        "NAME": ("django.contrib.auth.password_validation.NumericPasswordValidator"),
    },
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = "/static/"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
STATIC_ROOT = BASE_DIR / "staticfiles"

# Media files
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Email
EMAIL_BACKEND = os.getenv(
    "DJANGO_EMAIL_BACKEND",
    (
        "django.core.mail.backends.console.EmailBackend"
        if DEBUG
        else "django.core.mail.backends.smtp.EmailBackend"
    ),
)

# Default primary key
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Unfold configuration
UNFOLD = {
    "SITE_TITLE": "Portfolio Admin",
    "SITE_HEADER": "Portfolio Studio",
    "SITE_SUBHEADER": "Content Management",
    "SITE_URL": "/",
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": True,
    "THEME": "light",
    "COLORS": {
        "primary": {
            "50": "255 247 237",
            "100": "255 237 213",
            "200": "254 215 170",
            "300": "253 186 116",
            "400": "251 146 60",
            "500": "249 115 22",
            "600": "234 88 12",
            "700": "194 65 12",
            "800": "154 52 18",
            "900": "124 45 18",
            "950": "67 20 7",
        },
    },
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": False,
        "navigation": [
            {
                "title": _("Overview"),
                "separator": False,
                "collapsible": False,
                "items": [
                    {
                        "title": _("Dashboard"),
                        "icon": "dashboard",
                        "link": reverse_lazy("admin:index"),
                    },
                ],
            },
            {
                "title": _("Portfolio Content"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Profile"),
                        "icon": "person",
                        "link": reverse_lazy("admin:pages_profile_changelist"),
                    },
                    {
                        "title": _("Projects"),
                        "icon": "work",
                        "link": reverse_lazy("admin:pages_project_changelist"),
                    },
                    {
                        "title": _("Skills"),
                        "icon": "psychology",
                        "link": reverse_lazy("admin:pages_skill_changelist"),
                    },
                    {
                        "title": _("Services"),
                        "icon": "design_services",
                        "link": reverse_lazy("admin:pages_service_changelist"),
                    },
                ],
            },
            {
                "title": _("Career & Social Proof"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Experience"),
                        "icon": "work_history",
                        "link": reverse_lazy("admin:pages_experience_changelist"),
                    },
                    {
                        "title": _("Education"),
                        "icon": "school",
                        "link": reverse_lazy("admin:pages_education_changelist"),
                    },
                    {
                        "title": _("Testimonials"),
                        "icon": "reviews",
                        "link": reverse_lazy("admin:pages_testimonial_changelist"),
                    },
                ],
            },
            {
                "title": _("Website Management"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Hero Section"),
                        "icon": "web",
                        "link": reverse_lazy("admin:pages_hero_changelist"),
                    },
                    {
                        "title": _("FAQs"),
                        "icon": "quiz",
                        "link": reverse_lazy("admin:pages_faq_changelist"),
                    },
                    {
                        "title": _("Links"),
                        "icon": "link",
                        "link": reverse_lazy("admin:pages_links_changelist"),
                    },
                    {
                        "title": _("Social Links"),
                        "icon": "share",
                        "link": reverse_lazy("admin:pages_sociallinks_changelist"),
                    },
                    {
                        "title": _("Contact Messages"),
                        "icon": "mail",
                        "link": reverse_lazy("admin:pages_contactmessage_changelist"),
                    },
                ],
            },
        ],
    },
}

# Production security settings
if not DEBUG:
    SECURE_SSL_REDIRECT = os.getenv(
        "DJANGO_SECURE_SSL_REDIRECT",
        "True",
    ).lower() in ("true", "1", "yes")

    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = "DENY"

    SECURE_HSTS_SECONDS = int(os.getenv("DJANGO_SECURE_HSTS_SECONDS", "31536000"))

    SECURE_HSTS_INCLUDE_SUBDOMAINS = os.getenv(
        "DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS",
        "True",
    ).lower() in ("true", "1", "yes")

    SECURE_HSTS_PRELOAD = os.getenv(
        "DJANGO_SECURE_HSTS_PRELOAD",
        "True",
    ).lower() in ("true", "1", "yes")
