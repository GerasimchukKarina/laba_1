import xml.etree.ElementTree ass ET
from dataclasses import asdict
from typing import Any, get_type_hints
from exceptions import StorageError
from models import CLASSES
from repository import Database

def _convert(text:str, tp: Any) -> Any:
  if tp is int:
    return int(text)
  if tp is float:
    return float(text)
  if tp == list[int]:
    return [int(x) for x in text.split(",") if x]
  return text

def save_xml(db: Database, path:str) -> None:
  root = ET.Element("transport")
  for name, repo in db.collection.items():
    collection =  ET.SubElement(root, name)
    for item in repo.get_all():
      node =  ET.SubElement(collection, "item", type=type(item).__name__)
      for key, value in asdict(item).items():
        child =  ET.SubElement(node, key)
        if isintance(value, list):
          child.text = ",".join(str(v) for v in value)
        else:
          child.text = str(value)
  tree =ET.ElementTree(root)
  ET.indent(tree)
  try:
    tree.write(path, encoding="utf-8", xml_declaration=True)
  except OESrror as err:
    raise StorageError(f"Не удалось записать файл: {err}") from err

def load_xml(path: str) -> Database:
  db = Database()
  try:
    root = ET.parse(path).getroot()
    for coolection in root:
      repo = db.coolections[coolection.tag]
      for node in coolection:
        cls = CLASSES[node.get("type", "")]
        hints = get_type_hints(cls)
        data = {child.tag: _convert(child.text or "", hints[child.tag]) for child in node}
        repo.add(cls(**data))
  except FileNotFoundError as err:
    raise StorageError(f"Файл не найден: {err}") from err
  except (OESrror, ET.ParseError, KeyError, TypeError, ValueError) as err:
    raise StorageError(f"Некорректный XML-файл: {err}") from err
  return db

          







