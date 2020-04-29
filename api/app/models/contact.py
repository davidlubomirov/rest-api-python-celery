import os

from app.db import db, ma
from marshmallow import fields, validate, ValidationError

# TODO(David): No validation for length of fields in both models


class Contact(db.Model):
    __tablename__ = "contact"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    emails = db.relationship(
        'Email',
        cascade='all,delete-orphan',
        single_parent=True
    )

    def __repr__(self):
        return "User: {} {}, username-{}".format(self.first_name, self.last_name, self.username)


# TODO(David): Add email type: personal or corporate
class Email(db.Model):
    __tablename__ = "email"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'))
    contact = db.relationship('Contact', backref='email')


class EmailSchema(ma.Schema):
    email = fields.Str()
    # created_at = fields.DateTime(format="%Y-%m-%d %H:%M:%S")


class ContactSchema(ma.Schema):
    username = fields.Str()
    first_name = fields.Str()
    last_name = fields.Str()
    emails = fields.Nested(EmailSchema, many=True)


contact_schema = ContactSchema()
contacts_schema = ContactSchema(many=True)
