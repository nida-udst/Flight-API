from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api

from config import Config
from extensions import db

from resources.flight import FlightListResource, FlightResource, FlightBoardResource, FlightAirborneResource
from resources.gate import GateListResource, GateResource, AssignGateResource, AvailableGatesResource
from resources.flight_status import StatusListResource, StatusResource

def create_app():
    
    app = Flask(__name__)
    app.config.from_object(Config)

    register_extensions(app)
    register_resources(app)

    return app

def register_extensions(app):
    db.init_app(app)
    migrate = Migrate(app, db)


def register_resources(app):
    api = Api(app)

    api.add_resource(FlightListResource, '/flights')
    api.add_resource(GateListResource, '/gates')
    api.add_resource(StatusListResource, '/status')

    api.add_resource(FlightResource, '/flights/<int:id>')
    api.add_resource(GateResource, '/gates/<int:id>')
    api.add_resource(StatusResource, '/status/<int:id>')

    api.add_resource(AssignGateResource, '/gates/<int:gid>/assign/<int:fid>')
    api.add_resource(FlightBoardResource, '/flights/<int:id>/board')
    api.add_resource(AvailableGatesResource, '/gates/available')
    api.add_resource(FlightAirborneResource, '/flights/<int:id>/airborne')

    
    
    

if __name__ == '__main__':
    app = create_app()
    app.run('127.0.0.1', 5000)

