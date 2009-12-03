import tagging
from models import BlogEntry

try:
    tagging.register(BlogEntry)
except tagging.AlreadyRegistered:
    pass
