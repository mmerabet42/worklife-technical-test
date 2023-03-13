from uuid import UUID
from sqlalchemy.orm import Session 

class BaseRepository:
    def __init__(self, model):
        self.model = model

    def get_by_id(self, session: Session, id: UUID):
        return self.query(session, self.model.id == id).one_or_none()

    def _to_sa_filters(self, **kwargs):
        return [getattr(self.model, k) == v for k, v in kwargs.items()]

    def query(self, session: Session, *criterion, **kwargs):
        filters = self._to_sa_filters(**kwargs)
        return session.query(self.model).filter(*criterion, *filters)

    def get(self, session: Session, *criterion, **kwargs):
        return self.query(session, *criterion, **kwargs).one_or_none()

    def get_many(self, session: Session, *criterion, **kwargs):
        return self.query(session, *criterion, **kwargs).all()

    def create(self, session: Session, *_, **kwargs):
        instance = self.model()
        [setattr(instance, k, v) for k, v in kwargs.items()]
        session.add(instance)
        session.commit()
        return instance

    def delete(self, session: Session, *criterion, **kwargs):
        filters = self._to_sa_filters(**kwargs)
        if obj := session.query(self.model).filter(*criterion, *filters).first():
            session.delete(obj)
            session.commit()
        return obj
    
    def here_on_here(self):
        print("HELLO WORLD !")
    
    def delete_many(self, session: Session, *criterion, **kwargs):
        filters = self._to_sa_filters(**kwargs)
        return session.query(self.model).filter(*criterion, *filters).delete()
        