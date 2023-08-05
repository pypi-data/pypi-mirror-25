from __future__ import unicode_literals

from django.contrib import admin

from modeltranslation.admin import TranslationAdmin

from .forms import TextBlockAdminForm
from .models import TextBlock


class TextBlockAdmin(TranslationAdmin):
    list_display = ['key', 'type', 'shortened_content']
    list_filter = ['type', ]
    fields = ['key', 'content', 'type', ]
    search_fields = ['key', 'content', ]
    readonly_fields = ['key', 'type', ]
    form = TextBlockAdminForm
    ordering = ['key', ]

    def shortened_content(self, instance):
        return (
            instance.content[:100] + '...'
            if len(instance.content) > 100
            else instance.content
        )


admin.site.register(TextBlock, TextBlockAdmin)
