from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

class Author(models.Model):
    """A model of an author (extends contrib.auth.models.User)."""
    user = models.ForeignKey(User, unique=True)
    slug = models.SlugField(_("Slug"),
        help_text=_("Slug for public Author profile url")
    )
    bio = models.TextField(_("Bio"), blank=True)    
    photo = models.ImageField(_("Photo"),
        upload_to="uploads/author_photos"
    )
