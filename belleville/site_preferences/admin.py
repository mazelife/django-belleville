from django.contrib import admin

from models import Preference

class PreferenceAdmin(admin.ModelAdmin):
    list_display = ('site', 'site_title',)
    fieldsets = (
        (None, {
            'fields': ('site', 'site_title',),
            'classes': ['wide'],
        }),
        ('Blog settings', {
            'fields': ('blog_title', 'blog_entries_per_page',),
            'classes': ['wide'],            
        }),
        ('Tumblelog settings', {
            'fields': ('tumblelog_title', 'tumblelog_entries_per_page', ),
            'classes': ['wide'],
        })
    )    
    
admin.site.register(Preference, PreferenceAdmin)
