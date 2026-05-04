from extensions import db
from http import HTTPStatus

class Gate(db.Model):
    __tablename__ = 'gate'

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(10), nullable=False)
    gate_status = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(), onupdate=db.func.now())


    flights = db.relationship('Flight', backref = 'gate')

    @property
    def data(self):
        return{
            'id': self.id,
            'number': self.number,
            'gate_status': self.gate_status
        }
    
    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter(cls.id==id).first()
    
    @classmethod
    def get_by_number(cls, number):
        return cls.query.filter(cls.number==number).first()

    @classmethod
    def get_status(cls, id):
        return cls.query.filter(cls.id==id).first().gate_status
      
    @classmethod
    def get_all(cls):
        data = cls.query.all()

        gates = []
        for i in data:
            gates.append(i.data)
        
        return gates

    @classmethod
    def get_by_status(cls, status):
        data = cls.query.filter(cls.gate_status==status).all()
        gates = []

        for i in data:
            gates.append(i.data)

        return gates
    
    @classmethod
    def update_status(cls, id, status):
        gate = cls.get_by_id(id)

        if gate is None:
            return {'message':'gate not found'}, HTTPStatus.NOT_FOUND

        gate.gate_status = status.lower()
        gate.save()

        return {'data':gate.data}, HTTPStatus.OK

    @classmethod
    def delete_gate(cls, id):
        gate = cls.query.filter(cls.id==id).first()

        if gate is None:
            return {'message': 'gate not found'}, HTTPStatus.NOT_FOUND
        
        db.session.delete(gate)
        db.session.commit()

        return HTTPStatus.NO_CONTENT


    def save(self):
        db.session.add(self)
        db.session.commit()
    