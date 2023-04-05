from enum import Enum
import jsonpickle

@jsonpickle.handlers.register(Enum, base=True)
class EnumHandler(jsonpickle.handlers.BaseHandler):
  def flatten(self, obj, data):
    return obj.value  # Convert to json friendly format