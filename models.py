from dataclasses import dataclass, field
from exceptions import ValidationError

@dataclass
class Person:
  id: int
  name: str
  phone: str = ""
  def __post_init__(self) -> None:
    if not self.name.strip():
      raise ValidationError("Имя не может быть пустым")

@dataclass
class Passenger(Person):
  discount: int=0
  
  def __post_init__(self) -> None:
    super().__post_init__()
    if not 0 <= self.discount <= 100:
      raise ValidationError(" ")

@dataclass
class Driver(Person):
  licence_number: str = ""

@dataclass
class Vehicle:
  id: int
  namber: str
  capacity: int
  
  def __post_init__(self) -> None:
    if self.capacity <= 0:
      raise ValidationError("")

@dataclass
class Bus(Vehicle):
  fuel: str = "diesel"

@dataclass
class Tram(Vehicle):
  wagons: int = 1

@dataclass
class Stop:
  id: int 
  name: str

@dataclass
class Route:
  id: int 
  namber: str
  stop_ids: list[int] = field(default_factory=list)


@dataclass
class Trip:
  route_id: int 
  vehicle_id: int 
  driver_id: int 
  departure: str
  price: float
  
  def __post_init__(self) -> None:
    if self.price < 0:
      raise ValidationError("")

@dataclass
class Ticket:
  id: int 
  trip_id: int 
  passenger_id: int 
  seat: int
  price: float
  
@dataclass
class Payment:
  id: int 
  ticket_id: int 
  amout: float
  method: str = "card"

CLASSES: dict[str, type] = {
  cls.__name__: cls
  for cls in (Passenger, Driver, Vehicle, Bus, Tram, Stop, Route, Trip, Ticket, Payment)
}


