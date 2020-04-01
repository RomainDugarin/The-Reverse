__import__('pkg_resources').declare_namespace(__name__)

from .sqlite import SqliteService
from .task import TaskService, loop