import sys
from flask import request
from flask_restful import Resource
from http import HTTPStatus

from models.flight import Flight
from models.flight_status import Flight_Status
from datetime import datetime
from models.gate import Gate

class FlightListResource(Resource):
    #gets all flights
    def get(self):
        data = Flight.get_all()

        if data == []:
            return{'message:':'no flights found'}, HTTPStatus.NOT_FOUND
        return {'data': data}, HTTPStatus.OK
    
    #post flight
    def post(self):
        data = request.get_json()

        flight = Flight(
            airline=data['airline'],
            origin = data['origin'],
            destination = data['destination'],
            est_departure = data['est_departure'],
            est_arrival = data['est_arrival'],
            act_departure = data.get('act_departure', None),
            act_arrival = data.get('act_arrival', None),
            status_id = data['status_id']

        )

        if 'gate_id' in data:

            if data['gate_id'] is not None:
                gate = Gate.get_by_id(data['gate_id'])

                if gate is None:
                    return {'message': 'gate not found'}, HTTPStatus.NOT_FOUND
                
                if gate.gate_status.lower() != 'available':
                    return {'message': 'gate in use'}, HTTPStatus.BAD_REQUEST
                
                Gate.update_status(data['gate_id'], 'scheduled')
            
            flight.gate_id = data['gate_id']
            
        

        flight.save()
        return flight.data, HTTPStatus.CREATED

class FlightResource(Resource):

    #gets flight by id
    def get(self, id):
        flight = Flight.get_by_id(id)
        if flight:
            return{'data': flight.data}, HTTPStatus.OK
        return{'message': 'flight not found'}, HTTPStatus.NOT_FOUND

    def put(self, id):
        data = request.get_json()
        return Flight.update_flight(id, data)

    #deletes flight
    def delete(self, id):
        return Flight.delete(id)



class FlightBoardResource(Resource):

    #changes status to boarding and gate to open
    def put(self, id):
        flight = Flight.get_by_id(id)

        gate_id = flight.gate_id
        if gate_id is None:
            return{"message":" gate not assigned"}, HTTPStatus.NOT_FOUND
        
        gate = Gate.get_by_id(gate_id)

        flight.update_status(id, 'boarding')
        gate.update_status(gate_id,'open')
        return{"data":flight.data}, HTTPStatus.OK

    #changes status to departed and gate to closed
    def delete(self, id):

        flight = Flight.get_by_id(id)
        if flight is None:
            return{"message":" flight not found"}, HTTPStatus.NOT_FOUND
        
        gate_id = flight.gate_id
        if gate_id is None:
            return{"message":" gate not assigned"}, HTTPStatus.NOT_FOUND
        
        
        gate = Gate.get_by_id(gate_id)

        flight.update_status(id, 'departed')
        gate.update_status(gate_id,'closed')
        flight.act_departure = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        flight.save()
        return{"data":flight.data}, HTTPStatus.OK


class FlightAirborneResource(Resource):

    #changes status to in flight and gate to available
    def put(self, id):
        flight = Flight.get_by_id(id)
        

        if flight is None:
            return{"message":" flight not found"}, HTTPStatus.NOT_FOUND

        if flight.act_departure is None:
            return{"message":" Flight has not departed"}, HTTPStatus.BAD_REQUEST

        gate_id = flight.gate_id
        gate = Gate.get_by_id(gate_id)

        flight.update_status(id, 'in flight')
        gate.update_status(gate_id,'available')
        return{"data":flight.data}, HTTPStatus.OK

    #changes status to arrived and gate to null
    def delete(self, id):

        flight = Flight.get_by_id(id)
        if flight is None:
            return{"message":" flight not found"}, HTTPStatus.NOT_FOUND
        
        status = Flight_Status.get_by_id(flight.status_id)
    
        if status.flight_status != 'in flight':
            return{"message":" flight is not airborne"}, HTTPStatus.BAD_REQUEST

        flight.update_status(id, 'arrived')
        flight.gate_id = None
        flight.act_arrival = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        flight.save()

        return{"data":flight.data}, HTTPStatus.OK
    
    
        
