import sys
from flask import request
from flask_restful import Resource
from http import HTTPStatus

from models.gate import Gate
from models.flight import Flight

class GateListResource(Resource):

    #Gets all gates
    def get(self):
        gate = Gate.get_all()
        
        if gate == []:
            return {'message':'gate not found'}, HTTPStatus.NOT_FOUND
        
        return {'data':gate}, HTTPStatus.OK
    
    #Post gate
    def post(self):
        data = request.get_json()
        
        check_gate = Gate.get_by_number(data['number'])

        if check_gate:
            return {'message': 'gate already exists'}, HTTPStatus.BAD_REQUEST

        gate = Gate(
            number = data['number'],
            gate_status = data['gate_status']
        )

        gate.save()
        return gate.data, HTTPStatus.OK

class GateResource(Resource):

    #delete gate
    def delete(self, id):
        return Gate.delete_gate(id)
    
    #update gate status
    def put(self, id):
        data = request.get_json()

        return Gate.update_status(id, data['gate_status'])
    
    #gets by id
    def get(self, id):
        gate = Gate.get_by_id(id)
        if gate is None:
            return {'message':'gate not found'}, HTTPStatus.NOT_FOUND
        return gate.data, HTTPStatus.OK

class AssignGateResource(Resource):

    #assigns gate to flight
    def put(self, gid, fid):
        flight = Flight.get_by_id(fid)
        gate = Gate.get_by_id(gid)

        if flight is None:
            return{"message: flight not found", HTTPStatus.NOT_FOUND}
        
        if flight.gate_id is not None:
            Gate.update_status((flight.gate_id), 'available')

        if gate.gate_status.lower() != 'available':
            return {'message': 'gate in use'}, HTTPStatus.BAD_REQUEST
        
        Gate.update_status(gid, 'scheduled')
        flight.gate_id = gid
        flight.save()
        return{'data': flight.data}, HTTPStatus.OK
    
    #unassign gate to filght
    def delete(self, gid, fid):
        flight = Flight.get_by_id(fid)
        gate = Gate.get_by_id(gid)

        if flight is None:
            return{"message: flight not found", HTTPStatus.NOT_FOUND}

        if flight.gate_id != gid:
            return {'message': 'gate not assigned to flight'}, HTTPStatus.BAD_REQUEST
        
        gate.update_status(gid, 'available')
        flight.gate_id = None
        flight.save()
        return{'data': flight.data}, HTTPStatus.OK

class AvailableGatesResource(Resource):
    #gets available gates
    def get(self):
        gates = Gate.get_by_status('available')
        if gates is []:
            return {'message: no gates available'}, HTTPStatus.NOT_FOUND
        
        return{'data': gates}, HTTPStatus.OK


    


