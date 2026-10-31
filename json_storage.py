import json
from dataclasses import asdict
from exceptions import StorageError
from models import CLASSES
from repository import Database

def save_json(db: Database, path: str) -> None:
  data = {
    name: [{"type": type(itrm).__name__, **asdict(item)} for item in repo.get_all()]
    for name, repo in db.collection.items()
  }
  try:
    with open(path, "w", encoding="utf-8") as file:
      json.dump(data, file, ensure_ascii=False, indent=4)
  except OSError as err:
    raise StorageError(f"Не удалось записать файл: {err}") from err
def load_json(path: str) -> Database:
  db = Database
  try:
    with open(path, "r", encoding="utf-8") as file:
      data = json.load( file)
    for name, items in data.items():
      repo =  db.collection[name]
      for raw in items:
        cls = CLASSES[raw.pop("type")]
        repo.add(cls(**raw))
  except FileNotFoundError as err:
    raise StorageError(f"Файл не найден: {err}") from err
  except (OSError, json.JSONDecodeError, KeyError, TypeError, AttributeError) as err:
    raise StorageError(f"Некорректный JSON-файл: {err}") from err
  return db




     
