from django.contrib.sites.models import Site
from django.db import models
from django.utils.translation import ugettext_lazy as _

class Preference(models.Model):
    site = models.OneToOneField(Site)
    site_title =  models.CharField(_(u"Site Title"), 
        help_text = _("The main title of your site"),
        max_length=255
    )
    blog_title =  models.CharField(_(u"Blog Title"),
        blank = True,
        help_text = _((
            "The title of your site's blog. May be left blank if your blog "
            "doesn't need a special title."
        )),
        max_length=255
    )
    blog_entries_per_page = models.IntegerField(_("Blog entries per page"),
        blank=True,
        help_text=_("If left blank, entries will not be paginated.")
    )
    tumblelog_title =  models.CharField(_(u"Tumblelog Title"), 
        blank = True,
        help_text = _((
            "The title of your site's tumblelog. May be left blank if your "
            "tumblelog doesn't need a special title."
        )),
        max_length=255
    )
    tumblelog_entries_per_page = models.IntegerField(
        _("Tumblelog entries per page"),
        blank = True,
        help_text=_("If left blank, entries will not be paginated.")
    )
