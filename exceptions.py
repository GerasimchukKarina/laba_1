class TransportError(Exception):
  pass
class ValidationError(TransportError):
  pass
class NotFoundError(TransportError):
  pass
class DuplicateError(TransportError):
  pass
class NoSeatsError(TransportError):
  pass
class StorageError(TransportError):
  pass
