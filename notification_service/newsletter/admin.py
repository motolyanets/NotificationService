from django.contrib import admin
from .models import Newsletter


class NewsletterAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Newsletter._meta.fields]

    class Meta:
        model = Newsletter


admin.site.register(Newsletter, NewsletterAdmin)
