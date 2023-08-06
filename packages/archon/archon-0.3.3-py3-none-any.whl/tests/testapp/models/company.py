from archon.models import db, Base
from archon.controller import Controller, model_route, http_route
import enum


class CompanyType(enum.Enum):
    IT = 'IT'
    notIT = 'notIT'


class CompanyController(Controller):
    @model_route
    def ask_for_raise(self, cls):
        return {
            'answer': 'no',
            'code': 'error',
        }

    @model_route
    def list_employees(self, cls):
        data = self.body['data']
        company = cls.query.get(data['id'])
        return {
            'code': 'success',
            'type': self.body['type'],
            'data': [e.name for e in company.employees],
        }

    @model_route
    def list_employees_error(self, cls):
        # A controller has no type, so this should error
        return {'type': self.type}

    @http_route(methods=['GET'])
    def foo(self, cls):
        return {'foo': 'bar'}

    @http_route(methods=['GET'])
    def foo_error(self, cls):
        # A controller has no type, so this should error
        return {'type': self.type}


class Company(Base):
    Controller = CompanyController

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    type = db.Column(db.Enum(CompanyType), default='notIT')
