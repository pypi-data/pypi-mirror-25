from datetime import datetime


def get_model(DB):

    class Model(DB.Model):
        __abstract__ = True

        id = DB.Column(DB.Integer, primary_key=True)
        created_at = DB.Column(DB.DateTime, default=datetime.utcnow, nullable=False)
        updated_at = DB.Column(DB.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

        def __init__(self, **kwargs):
            DB.Model.__init__(self, **kwargs)

        @classmethod
        def create(cls, **kwargs):
            instance = cls(**kwargs)
            return instance.save()

        @classmethod
        def delete_all(cls):
            all_objs = cls.query.all()
            for obj in all_objs:
                obj.delete()

        @classmethod
        def all(cls):
            return cls.query.all()

        @classmethod
        def newest(cls, field_name):
            return cls.query.order_by('{field_name} desc'.format(field_name=field_name)).limit(1)

        @classmethod
        def oldest(cls, field_name):
            return cls.query.order_by('{field_name} asc'.format(field_name=field_name)).limit(1)

        def update(self, commit=True, **kwargs):
            for attr, value in kwargs.iteritems():
                setattr(self, attr, value)
            return commit and self.save() or self

        def save(self, commit=True):
            DB.session.add(self)
            if commit:
                DB.session.commit()
            return self

        def delete(self, commit=True):
            DB.session.delete(self)
            return commit and DB.session.commit()

    return Model
