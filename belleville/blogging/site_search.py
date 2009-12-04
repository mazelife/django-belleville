from pierre.site_search.base_mixins import SearchableMixin
from pierre import site_search
from models import BlogEntry, TumblelogEntry
from settings import BloggingSettings

class BlogEntrySearchMixin(SearchableMixin):
    """A mix-in for a blog entry"""

    fields_to_index  = ('headline', 'intro', 'body')

    def is_searchable(self):
        return self.status in BloggingSettings.PUBLISHED_ENTRY_STATES

    def get_search_result_title(self):
        return self.headline

    def get_search_result_description(self):
        return self.intro

    def get_search_result_date(self):
        return self.pub_date

site_search.register(BlogEntry, BlogEntrySearchMixin)

class TumblelogEntrySearchMixin(SearchableMixin):
    """A mix-in for a blog entry"""

    fields_to_index  = ('title', 'post')

    def is_searchable(self):
        return self.status in BloggingSettings.PUBLISHED_ENTRY_STATES

    def get_search_result_title(self):
        return self.title

    def get_search_result_description(self):
        return self.post

    def get_search_result_date(self):
        return self.pub_date

site_search.register(TumblelogEntry, TumblelogEntrySearchMixin)