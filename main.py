from exceptions import TransportjError
from json_storage import load_json, save_json
from models import Passenger, Driver, Vehicle, Bus, Tram, Stop, Route, Trip, Ticket, Payment
from service import TransportService
from repository import Database
from  xml_storage import load_xml, save_xml

MENU ="""
1 Добавить пассажира     2 Список пассажиров
3 Изменить скидку        4 Удаоить пассажира
5 Список рейсов          6 Купить билет
7 Отменить билет         8 Отчет по рейсу
9 Сохранить JSON         10 Загрузить JSON
11 Сохранить XML         12 Загрузить XML
0 Выход
"""

def seed(db:Database ) -> None:
  for i, name in enumerate(["Центр", "Вокзал", "Университет"], start=1):
    db.stops.add(Stop(i, name))
  db.routes.add(Route(1, "5", [1, 2, 3]))
  db.vehicles.add(Bus(1, "A123BC", 2, "diesel"))
  db.vehicles.add(Tram(2, "T-77", 100, 3))
  db.drivers.add(Driver(1, "Петр Сидоров", "+7911", "AB123"))
  db.passengers.add(Passenger(1, "Иван Петров", "+7900", 50))
  db.trips.add(Trip(1, 1, 1, 1, "2026-09-10 8:00", 60.0))

def handle(choice: str, db:Database, service:TransportService ) -> Database:
  if choice == "1":
    name = input("Имя: ")
    phone = input("Телефон:")
    discount = int(input("Скидка %: "))
    db.passengers.add(Passenger( db.passengers.next_id(), name,phone, discount ))
    print("Пассажир добавлен")
  elif choice == "2":
    for p in db.passengers.get_all():
      print(p)
  elif choice == "3":
    passenger = db.passengers.get(int(input("id пассажира: ")))
    passenger.discount = int(input("Новая скдка %: "))
    Passenger.__post_init_(passenger)
    db.passengers.update(passenger)
    print("Скидка изменена")
  elif choice == "4":
     db.passengers.delete(int(input("id пассажира: "))):
    print("Пассажир удален")
  elif choice == "5":
     for t in db.trips.get_all():
       print(t)
  elif choice == "6":
    ticket = service.buy_ticket(int(input("id рейса:")), int(input("id пассажира:")))
    print(f"Билет {ticket.id}: место {ticket.seat}, цена {ticket.price}")
  elif choice == "7":
    service.cancel_ticket(int(input("id билета:")))
    print("Билет отменен")
  elif choice == "8":
    print(service.trip_report(int(input("id рейса:"))))
  elif choice == "9":
    save_json(db, "data.json")
    print("Сохранено в data.json")
  elif choice == "10":
    db = load_json("data.json")
    print("Загружено из data.json")
  elif choice == "11":
    save_xml(db, "data.xml")
    print("Сохранено в data.xml")
  elif choice == "12":
    db = load_xml("data.xml")
    print("Загружено из data.xml")
  else:
    print("Неизвестная команда")
  return db


def main() -> None:
  db = Database()
  seed(db)
  service = TransportService(db)
  while True:
    print(MENU)
    choice = input("Выбор: ").strip()
    if choice== "0":
      break
    try:
      db = handle(choice, db, service)
      service.db = db
    except TransportjError as err:
      print(f"Ошибка: {err}")
    except ValueError as err:
      print("Ошибка: введено некорректное число")
if __name__ == "__main__":
  main()








