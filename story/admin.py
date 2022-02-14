from django.contrib import admin
from .models import Cerita, Gambar, Komentar
# Register your models here.


class AdminCerita(admin.ModelAdmin):
    readonly_fields = [
        'slug',
        'publish',
        'author',
        'stress'
    ]

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form,change)

class AdminKomentar(admin.ModelAdmin):
    readonly_fields = [
        'author',
        'publish'
    ]

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form,change)

admin.site.register(Cerita, AdminCerita)
admin.site.register(Gambar)
admin.site.register(Komentar, AdminKomentar)
