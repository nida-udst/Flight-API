import sys
from flask import request
from flask_restful import Resource
from http import HTTPStatus

from models.flight_status import Flight_Status

class StatusListResource(Resource):
    def get(self):
        status = Flight_Status.get_all()

        if status == []:
            return {'message':'no flight status'}, HTTPStatus.NOT_FOUND
        
        return {'data': status}, HTTPStatus.OK
    
    def post(self):
        data = request.get_json()

        status = data['flight_status']
        flight = Flight_Status.get_id_by_status(status)

        if flight:
            return {'message': 'status already exists'}, HTTPStatus.BAD_REQUEST

        status = Flight_Status(
            flight_status=data['flight_status'],
        )

        status.save()

        return status.data, HTTPStatus.OK

class StatusResource(Resource):
    def put(self,id):
        data = request.get_json()

        return Flight_Status.update_status(id, data['flight_status'])
    
    def get(self,id):
        flight_status = Flight_Status.get_by_id(id).data
        if flight_status is None:
            return{'message':'flight status not found'}
        return flight_status, HTTPStatus.OK

    def delete(self, id):
        return Flight_Status.delete(id)


