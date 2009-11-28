class BloggingSettings:
    """ 
    This class contains settings for blog or tumblelog entries. Any property
     here can be overriden with a value of the same name beging set in the 
     main django project settings.py file (Just perface it with BLOGGING_).
     
     To override the COMMENTS_ALLOWED perference here, place the following
     in your setting.py:
     
     BLOGGING_COMMENTS_ALLOWED = True
    """

    # Workflow states:
    PUB_STATES = (
        ('draft', "Draft"),
        ('published', "Published")
    )    
    DEFAULT_PUB_STATE = 'draft'
    PUBLISHED_ENTRY_STATES = ('published',)    
    #TTL used for convinenece functions which allow model single-property lookups by key
    SPEEDY_LOOKUP_TTL = 60 * 20 #...in seconds
    
    # Boolean indicating whether comments are allowed on all blog posts by default
    COMMENTS_ALLOWED = False
    # Number of days a blog entry should allow comments to remain open:
    DAYS_COMMENTS_OPEN = 60
    
    TWITTER_EMAIL = None
    TWITTER_PASSWORD = None

# Import global project settings:
from django.conf import settings as _settings

# If a BloggingSettings propoerty is set in global project settings, override 
#the default setting in this file with it:
props = [("BLOGGING_" + p, p) for p in BloggingSettings.__dict__.keys() if not \
    p.startswith("__") and not callable(getattr(BloggingSettings, p)) and \
    type(getattr(BloggingSettings, p)) != property]
for global_prop, local_prop in props:
    if hasattr(_settings, global_prop):
        setattr(BloggingSettings, local_prop, getattr(_settings, global_prop))
        

