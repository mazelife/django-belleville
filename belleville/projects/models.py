from  datetime import datetime
from django.db import models
from django.utils.html import strip_tags
from django.utils.translation import ugettext_lazy as _

from blogging.settings import BloggingSettings

class ProjectManager(models.Manager):
    """
    This manager can be used for blog and tumblelog entries becuase the 
    conditions for an entry being published in either are the same.
    """
    def published(self):
        """
        A project entry is published if its status is in the 
        PUBLISHED_ENTRY_STATES list in BloggingSettings (which can be overriden
        in the main settings file by setting BLOGGING_PUBLISHED_ENTRY_STATES) 
        the pub_date attribute is not in the future.
        """
        return self.get_query_set().filter(
                status__in=BloggingSettings.PUBLISHED_ENTRY_STATES
            ).exclude(
                start_date__gt=datetime.now()
            )

class Project(models.Model):
    """
    A model of a project
        
    """
    slug = models.SlugField(_("Slug"))
    title = models.CharField(_("Title"), max_length=255)
    summary = models.TextField(_("Summary"))
    description = models.TextField(_("Description"), blank=True)
    url = models.URLField(_("URL"), blank=True, verify_exists=False)
    author = models.ForeignKey('authors.Author')
    status = models.CharField(_("Status"),
        max_length=25, 
        choices=BloggingSettings.PUB_STATES,
        default=BloggingSettings.DEFAULT_PUB_STATE
    )
    start_date = models.DateTimeField(_(u"Start date"), 
        help_text=_((
            "Dates in the future will not appear on the "
            "site until the date is reached"
        )),
        default=datetime.now()
    )
    
    objects = ProjectManager()
    
    class Meta:
        verbose_name = "project"
        verbose_name_plural = 'projects'
        ordering = ('-start_date',)
        get_latest_by = 'start_date'

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ("projects:detail", (), {'slug': self.slug})
    
    def published(self):
        return self.status in BloggingSettings.PUBLISHED_ENTRY_STATES \
            and self.start_date <= datetime.now()
    published.boolean = True
        