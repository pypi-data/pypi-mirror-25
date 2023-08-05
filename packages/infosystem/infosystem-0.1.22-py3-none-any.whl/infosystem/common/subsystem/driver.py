from sqlalchemy.orm import exc
from infosystem.common import exception


class Driver(object):

    def __init__(self, resource):
        self.resource = resource

    def instantiate(self, **kwargs):
        try:
            instance = self.resource(**kwargs)
        except Exception:
            # TODO(samueldmq): replace with specific exception
            raise exception.BadRequest()

        return instance

    def create(self, entity, session):
        session.add(entity)
        session.flush()

    def update(self, id, data, session):
        try:
            entity = self.get(id, session)
        except exc.NoResultFound:
            raise exception.NotFound()

        for key, value in data.items():
            if hasattr(entity, key):
                setattr(entity, key, value)
            else:
                raise exception.BadRequest()
        session.flush()
        return entity

    def delete(self, entity, session):
        session.delete(entity)
        session.flush()

    def get(self, id, session):
        try:
            query = session.query(self.resource).filter_by(id=id)
            result = query.one()
        except exc.NoResultFound:
            raise exception.NotFound()

        return result

    def list(self, session, **kwargs):
        query = session.query(self.resource)
        for k, v in kwargs.items():
            if hasattr(self.resource, k):
                if isinstance(v, str) and '%' in v:
                    query = query.filter(getattr(self.resource, k).like(v))
                else:
                    query = query.filter(getattr(self.resource, k) == v)

        result = query.all()
        return result

    def count(self, session):
        try:
            rows = session.query(self.resource.id).count()
            result = rows
        except exc.NoResultFound:
            raise exception.NotFound()

        return result
