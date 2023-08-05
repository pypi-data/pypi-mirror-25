from datetime import datetime

from database import session
from filtering import Filter
from settings import *
from simplyrestful.models import get_class_by_table_name
from util import instantiate


class Serializer(object):
    authenticators = []
    authorizers = []
    validators = []
    fields = None

    methods = {
        datetime: lambda x: x.strftime(DATE_FORMAT)
    }

    @property
    def model(self):
        raise NotImplementedError

    def __init__(self):
        self.query = session.query(self.model)
        if not self.authenticators:
            self.authenticators = [
                instantiate(a) for a in DEFAULT_AUTHENTICATION
            ]
        if not self.authorizers:
            self.authorizers = [
                instantiate(a) for a in DEFAULT_AUTHORIZATION
            ]
        self.user = self._authenticate()

    def create(self, data):
        instance = self.model()
        self.deserialize(data, instance)
        session.add(instance)
        session.flush()
        serial = self.serialize(instance)
        session.commit()
        return serial

    def update(self, id, data):
        instance = self.query.get(id)
        self.deserialize(data, instance)
        session.flush()
        serial = self.serialize(instance)
        session.commit()
        return serial

    def read(self, id):
        return self.serialize(self.query.get(id))

    def list(self, filtering):
        filters = Filter(self.model, filtering)

        query = self.query.join(
            * filters.joins
        ).filter(
            filters.orm_filters
        ).order_by(
            * filters.order_by
        )

        return dict(
            results=[
                self.serialize(m)
                for m in query.limit(filters.limit).offset(filters.offset).all()
            ],
            count=query.count()
        )

    def delete(self, id):
        self.query.filter_by(id=id).delete()
        session.commit()

    def serialize(self, instance):
        serialized = dict()
        for prop in instance.__table__.columns:
            name = prop.name
            if not self.fields or name in self.fields:
                value = getattr(instance, name)
                value_type = type(value)

                if value_type in self.methods:
                    value = self.methods[value_type](value)

                relationships = instance.relationships
                if name in relationships and getattr(self, relationships[name], None):
                    # Consider that it may be not set
                    value = getattr(self, relationships[name])().serialize(
                        getattr(instance, relationships[name])
                    )
                    name = relationships[name]

                serialized[name] = value
        return serialized

    def deserialize(self, data, instance):
        data.update(
            self._deserialize_relationsips(data, instance)
        )
        for prop in data:
            if prop not in instance.primary_keys:
                setattr(instance, prop, data.get(prop))

    def _deserialize_relationsips(self, data, instance):
        for relationship in instance.__mapper__.relationships:
            target = relationship.local_remote_pairs[0][1]
            key = relationship.key
            if data.get(key):
                fields = data.get(key)
                target_class = get_class_by_table_name(target.table.name)

                # TODO: Remove
                fields = {k: v for k, v in fields.iteritems() if type(v) is not dict}

                value = session.query(target_class).filter_by(**fields).one()
                data[key] = value
        return data

    def _authenticate(self):
        for authenticator in self.authenticators:
            user = authenticator.authenticate()
            if user:
                return user
        raise Exception('Authentication error')

    def _authorize(self):
        for authorizer in self.authorizers:
            authorizer.authorize()

    def _validate(self):
        for validator in self.validators:
            validator.validate()
