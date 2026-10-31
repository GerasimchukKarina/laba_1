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
      for key
