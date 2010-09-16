from django.contrib import admin
from django.contrib.contenttypes import generic
from django.db import models
from django.utils.encoding import force_unicode

from project_utils import CKEditor

from models import Project

from tagging.models import TaggedItem

class TaggingInline(generic.GenericTabularInline):
    model = TaggedItem
    extra = 3
    verbose_name_plural = "Tags for this item:"
    max_num = 10

class ProjectAdmin(admin.ModelAdmin):
    """
    An admin site object for Blog entries.
    """
    date_hierarchy = 'start_date'
    list_display = ('title', 'start_date', 'status', 'published')
    list_filter = ('status',)
    formfield_overrides = {
        models.TextField: {
            'widget' : CKEditor(ck_attrs={'height': '500px'})
        }
    }
    inlines = [TaggingInline]
    
    class Media:
        css = {"all": ("styles/admin.css",)}

admin.site.register(Project, ProjectAdmin)