from extensions import db
from models.gate import Gate
from models.flight_status import Flight_Status
from http import HTTPStatus
from datetime import datetime

class Flight(db.Model):
    __tablename__ = "flight"

    id = db.Column(db.Integer, primary_key = True)
    airline = db.Column(db.String(100), nullable=False)
    origin = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    est_departure = db.Column(db.DateTime(), nullable=False)
    est_arrival = db.Column(db.DateTime(), nullable=False)
    act_departure = db.Column(db.DateTime(), nullable=True)
    act_arrival = db.Column(db.DateTime(), nullable=True)
    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(), onupdate=db.func.now())


    gate_id = db.Column(db.Integer, db.ForeignKey('gate.id'), nullable=True)
    status_id = db.Column(db.Integer, db.ForeignKey('flight_status.id'), nullable=False)

    def format_date(date):
        if date:
            return date.strftime('%d-%m-%Y %H:%M:%S')
        else:
            return None

    @property
    def data(self):

        return{
            'id' : self.id,
            'airline': self.airline,
            'origin': self.origin,
            'destination': self.destination,
            'est_departure': Flight.format_date(self.est_departure),
            'est_arrival': Flight.format_date(self.est_arrival),
            'act_departure': Flight.format_date(self.act_departure),
            'act_arrival': Flight.format_date(self.act_arrival),
            'gate': Gate.get_by_id(self.gate_id).data if self.gate_id is not None else None,
            'status': Flight_Status.get_by_id(self.status_id).data

        }
   
    @classmethod
    def update_flight(cls, flight_id, data):
        flight = cls.query.get(flight_id)

        if not flight:
            return {"message": "Flight not found."}, HTTPStatus.NOT_FOUND

        # Only update each field if it actually exists in the data
        if "airline" in data:
            flight.airline = data["airline"]

        if "origin" in data:
            flight.origin = data["origin"]

        if "destination" in data:
            flight.destination = data["destination"]

        if "est_departure" in data:
            flight.est_departure = data["est_departure"]

        if "est_arrival" in data:
            flight.est_arrival = data["est_arrival"]

        if "act_departure" in data:
            flight.act_departure = data["act_departure"]

        if "act_arrival" in data:
            flight.act_arrival = data["act_arrival"]

        if "status_id" in data:
            flight.status_id = data["status_id"]

        if "gate_id" in data:
            flight.gate_id = data["gate_id"]

        flight.save()
        return flight.data, HTTPStatus.OK


    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter(cls.id==id).first()
    

    @classmethod
    def get_all(cls):
        data = cls.query.all()

        flights = []
        for i in data:
            flights.append(i.data)
        
        return flights
    
    @classmethod
    def update_status(cls, id, status):
        flight = Flight.get_by_id(id)

        if flight is None:
            return {'message': 'flight not found'}, HTTPStatus.NOT_FOUND
        
        new_status = Flight_Status.get_id_by_status(status)

        if status is None:
            return {'message': 'status not found'}, HTTPStatus.NOT_FOUND

        flight.status_id = new_status
        flight.save()

        return flight.data, HTTPStatus.OK
    
    @classmethod
    def cancel_flight(cls, id):
        flight = Flight.get_by_id(id)

        if flight is None:
            return {'message': 'flight not found'}, HTTPStatus.NOT_FOUND
        
        status = Flight_Status.get_id_by_status('Cancelled')

        flight.status_id = status
        flight.save()

        return flight.data, HTTPStatus.OK
    
    @classmethod
    def delete(cls, id):
        flight = Flight.get_by_id(id)

        if flight is None:
            return{"message":"flight not found"}, HTTPStatus.NOT_FOUND
        
        db.session.delete(flight)
        db.session.commit()
        return {"message":"flight record deleted"}, HTTPStatus.NO_CONTENT

    
    def save(self):
        db.session.add(self)
        db.session.commit()