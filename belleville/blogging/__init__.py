import tagging
from models import BlogEntry, TumblelogEntry

try:
    tagging.register(BlogEntry)
except tagging.AlreadyRegistered:
    pass

try:
    tagging.register(TumblelogEntry)
except tagging.AlreadyRegistered:
    pass
