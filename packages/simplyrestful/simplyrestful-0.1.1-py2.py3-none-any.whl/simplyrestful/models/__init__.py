from geometry import Geometry
from model import Model
from simplyrestful.database import Base


def get_class_by_table_name(table_name):
  for c in Base._decl_class_registry.values():
    if hasattr(c, '__tablename__') and c.__tablename__ == table_name:
      return c
