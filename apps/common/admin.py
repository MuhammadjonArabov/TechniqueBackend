from . import models
from datetime import timedelta
from django.contrib import admin
from django.db.models import Sum
from django.utils import timezone
from django.utils.html import format_html
from django.contrib.admin import AdminSite
from django.contrib.auth import get_user_model
from django.template.response import TemplateResponse
from django.utils.translation import gettext_lazy as _





