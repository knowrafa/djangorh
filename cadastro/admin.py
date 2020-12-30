from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from cadastro.models import Curriculum, Vagas

# Register your models here.

# admin.site.register(Cadastro)
admin.site.register(Curriculum)
admin.site.register(Vagas)
