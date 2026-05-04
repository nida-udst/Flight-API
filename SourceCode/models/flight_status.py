from extensions import db
from http import HTTPStatus

class Flight_Status(db.Model):
    __tablename__ = 'flight_status'

    id = db.Column(db.Integer, primary_key = True)
    flight_status = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(), onupdate=db.func.now())

    flights = db.relationship('Flight', backref = 'flight_status')

    @property
    def data(self):
        return{
            'id': self.id,
            'flight_status': self.flight_status,
        }
    
    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter(cls.id==id).first()
    
    @classmethod
    def get_id_by_status(cls, status):
        status = cls.query.filter(cls.flight_status==status).first()
        if status:
            return status.id
        
        return status
    
    
    @classmethod
    def get_all(cls):
        data = cls.query.all()
        status = []

        for i in data:
            status.append(i.data)

        return status
    
    @classmethod
    def update_status(cls, id, status):
        flight = cls.get_by_id(id)

        if flight is None:
            return{'message':'flight not found'}, HTTPStatus.NOT_FOUND
        
        flight.flight_status = status
        flight.save()
        return flight.data
    
    @classmethod
    def delete(cls, id):
        status = Flight_Status.get_by_id(id)

        if status is None:
            return{"message":"flight status not found"}, HTTPStatus.NOT_FOUND

        basic_status = ['on time', 'in flight', 'arrived', 'departed', 'boarding']
        
        if status.flight_status in basic_status:
            return {"message": f"Cannot delete flight status '{status.flight_status}' because it is restricted."}, HTTPStatus.FORBIDDEN


        db.session.delete(status)
        db.session.commit()
        return {"message":"flight record deleted"}, HTTPStatus.NO_CONTENT

    

        return flight.data
    
    def save(self):
        db.session.add(self), HTTPStatus.OK
        db.session.commit()

