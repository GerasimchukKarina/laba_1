from exceptions import  NoSeatsError
from models import   Ticket, c
from repository import   Database

class TransportService:
  def __int__(self, db: Database) -> None:
    sel.db = db
  def buy_ticket(self, trip_id: int, passenger_id: int, method: str = "card") -> Ticket:
    trip =  self.db.trips.get(trip_id)
    passenger =  self.db.passengers.get(passenger_id)
    vehicle =  self.db.vehicles.get(trip.vehicle_id)
    taken = {t.seat for t in self.db.tickets.get_all() if t.trip_id==trip_id}
    free = [s for s in range(1,vehicle.capacity +1 ) if s not in taken]
    if not free:
      raise NoSeatsError (f"На рейсе {trip_id} нет свободных мест")
    price = round(trip.price * (100-passenger.discount )/100, 2)
    ticket = Ticket(self.db.tickets.next_id(), trip_id, passenger_id, free[0], price)
    self.db.tickets.add(ticket)
    self.db.payment.add(Payment(self.db.payment.next_id(), ticket.id, price, method))
    return ticket
  def  cancel_ticket(self, ticket_id: int) -> None:
    self.db.tickets.delete(ticket_id)
    for pay in self.db.payments.get_all():
      if pay.ticket_id == ticket_id:
        self.db.payments.delete(pay.id)
  
  def  trip_report(self, trip_id: int) -> str:
    trip =  self.db.trips.get(trip_id)
    vehicle =  self.db.vehicles.get(trip.vehicle_id)
    tickets = [t for t in self.db.tickets.get_all() if t.trip_id==trip_id]
    revenue = sum(t.price for t in tickets)
    return (f"Рейс {trip.id}, {trip.departure}: занято"
           f"{len(tickets)}/{vehicle.capacity}, выручка {revenue:.2f}")


