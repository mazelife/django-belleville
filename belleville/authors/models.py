from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

class Author(models.Model):
    """A model of an author (extends contrib.auth.models.User)."""
    user = models.ForeignKey(User, unique=True)
    slug = models.SlugField(_("Slug"),
        help_text=_("Slug for the public Author profile url")
    )
    bio = models.TextField(_("Bio"), blank=True)    
    photo = models.ImageField(_("Photo"),
        blank=True,
        upload_to="uploads/author_photos"
    )
    
    def __unicode__(self):
        name = self.user.get_full_name()
        # If name fields are empty, fallback to username, which is required:
        if name == '':
            return self.user.username
        return name

    @models.permalink
    def get_absolute_url(self):
        return ("authors:detail", (), {'slug': self.slug})        