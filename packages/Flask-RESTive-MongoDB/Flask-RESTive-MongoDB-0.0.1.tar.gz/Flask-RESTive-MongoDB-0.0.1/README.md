# flask-restive-mongodb
Flask-RESTive extension to work with mongodb.

[![Build Status](https://travis-ci.org/left-join/flask-restive-mongodb.svg?branch=master)](https://travis-ci.org/left-join/flask-restive-mongodb)
[![Coverage Status](https://coveralls.io/repos/github/left-join/flask-restive-mongodb/badge.svg?branch=master)](https://coveralls.io/github/left-join/flask-restive-mongodb?branch=master)
[![Code Health](https://landscape.io/github/left-join/flask-restive-mongodb/master/landscape.svg?style=flat)](https://landscape.io/github/left-join/flask-restive-mongodb/master)
[![PyPI Version](https://img.shields.io/pypi/v/Flask-RESTive-MongoDB.svg)](https://pypi.python.org/pypi/Flask-RESTive-MongoDB)


## Installation

```bash
pip install flask-restive-mongodb
```

## How to use

```python
from datetime import datetime

import mongoengine as me
from flask import Flask
from flask_restive import Api, StorageResource, UUIDSchema, fields
from marshmallow import pre_load
from flask_restive_mongodb import Model, Storage


app = Flask(__name__)

app.config['MONGODB_DATABASE_URI'] = 'mongodb://localhost/local'


def utc_time():
    return datetime.utcnow().replace(microsecond=0)


class ClientSchema(UUIDSchema):
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    created_on = fields.DateTime(
        required=True,
        missing=lambda: utc_time().isoformat())
    updated_on = fields.DateTime()

    class Meta(UUIDSchema.Meta):
        sortable_fields = ('id', 'created_on', 'updated_on')
        default_sorting = ('-updated_on', '-created_on', 'id')

    @pre_load(pass_many=False)
    def set_updated_on(self, data):
        # update time stamp on each create/update operation
        data['updated_on'] = utc_time().isoformat()
        return data


class ClientModel(Model):
    id = me.fields.UUIDField(primary_key=True)
    first_name = me.fields.StringField()
    last_name = me.fields.StringField()
    created_on = me.fields.DateTimeField()
    updated_on = me.fields.DateTimeField()


class ClientStorage(Storage):

    class Meta(Storage.Meta):
        model_cls = ClientModel
        primary_key_fields = ('id',)


class ClientResource(StorageResource):
    data_schema_cls = ClientSchema
    storage_cls = ClientStorage


api = Api(app, prefix='/api/v1', api_resources=[
    (ClientResource, ('/clients', '/clients/<uuid:id>')),
])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

```
