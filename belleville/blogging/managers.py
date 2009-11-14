import datetime
from django.db import models

from settings import BloggingSettings

class BloggingEntryManager(models.Manager):
    """
    This manager can be used for blog and tumblelog entries becuase the 
    conditions for an entry being published in either are the same.
    """
    def published(self):
        """
        A tumblelog entry is published if its status is in the 
        PUBLISHED_ENTRY_STATES list in BloggingSettings (which can be overriden
        in the main settings file by setting BLOGGING_PUBLISHED_ENTRY_STATES).
        """
        return self.get_query_set().filter(
                status__in=BloggingSettings.PUBLISHED_ENTRY_STATES
            ).exclude(
                pub_date__gt=datetime.datetime.now()
            )

    def get_entry_dates(self):
        """
        Create a dictionary of published entries. Dictionary keys are years
        with published entries, values are lists of months in that year in which
        entries were published each month is represented by a tuple of month 
        name and number:    
            ("February", 2)
        """
        entries = self.published()
        dates = [getattr(entry, "pub_date") for entry in entries]
        archive = {}
        for date in dates:
            month_name = datetime.date(2008,date.month,1).strftime("%B")
            if date.year not in archive.keys():
                archive[date.year] = set()
            archive[date.year].add((month_name, date.month))
        return archive            