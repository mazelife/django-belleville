import tagging
from models import Project

try:
    tagging.register(Project)
except tagging.AlreadyRegistered:
    pass