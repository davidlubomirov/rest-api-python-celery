from flask import Blueprint, jsonify, request

from app.db import db
from marshmallow import ValidationError
from app.models.contact import Contact, Email, contact_schema, contacts_schema
from app.middleware.auth import token_required

contact_api = Blueprint("contact", __name__)

# TODO(David): Move all response codes in globals for reuse in test cases


def _add_emails_to_contact(contact=None, emails=None):
    """Create new emails defined in JSON 'emails' array of objects to contact.

        Parameters
        ----------
        contact: Contact, required
        emails: json_array, required

        Raises
        ------
        ValueError
            In case of wrong usage it'll
    """
    if contact is None or emails is None:
        raise ValueError(
            "Invalid input. Please specify contact and emails from JSON")

    if len(emails) is 0:
        return

    for each_email in emails:
        email_to_add = Email(
            email=each_email["email"], contact=contact)


def _remove_emails_from_contact(contact=None):
    """Remove all emails associated to contact from the DB

        Parameters
        ----------
        contact: Contact, required

        Raises
        ------
        ValueError
            In case of wrong usage it'll
    """
    if contact is None:
        raise ValueError("Invalid input. Please specify correct contact value")

    all_emails = Email.query.filter_by(contact=contact).all()

    if all_emails is None:
        return

    for each_email in all_emails:
        db.session.delete(each_email)

    db.session.commit()


@contact_api.route("/api/contact", methods=["GET", "POST", "PUT", "DELETE"])
@token_required
def contact():
    if request.method == "GET":
        if 'username' in request.args:
            username_to_query = request.args.get('username')

            contact = Contact.query.filter_by(
                username=username_to_query).first()
            if not contact:
                return jsonify(
                    {
                        "msg": "contact does not exist"
                    }
                ), 404

            return jsonify(contact_schema.dump(contact))

        all_contacts = Contact.query.all()
        return jsonify(contacts_schema.dump(all_contacts))

    if request.method == "POST":
        json_data = request.get_json(silent=True)
        if not json_data:
            return jsonify(
                {
                    "msg": "invalid request"
                }
            ), 400

        try:
            data = contact_schema.load(json_data)
        except ValidationError as err:
            return err.messages, 422

        contact = Contact.query.filter_by(username=data["username"]).first()
        if contact:
            return jsonify(
                {
                    "msg": "username already exist"
                }
            ), 409

        new_contact = Contact(
            username=json_data["username"],
            first_name=json_data["first_name"],
            last_name=json_data["last_name"]
        )

        db.session.add(new_contact)
        db.session.commit()

        if "emails" in json_data.keys():
            _add_emails_to_contact(contact=new_contact,
                                   emails=json_data["emails"])

        db.session.commit()

        return jsonify(
            {
                "msg": "successfully created user: {}".format(new_contact.username)
            }
        ), 200

    if request.method == "PUT":
        json_data = request.get_json(silent=True)
        if not json_data:
            return jsonify(
                {
                    "msg": "invalid request"
                }
            ), 400

        try:
            data = contact_schema.load(json_data)
        except ValidationError as err:
            return err.messages, 422

        contact = Contact.query.filter_by(username=data["username"]).first()
        if not contact:
            return jsonify(
                {
                    "msg": "contact with this username does not exist"
                }
            ), 404

        contact.first_name = data["first_name"]
        contact.last_name = data["last_name"]

        db.session.commit()

        _remove_emails_from_contact(contact=contact)
        if "emails" in data.keys():
            _add_emails_to_contact(contact=contact, emails=data["emails"])

        return jsonify(
            {
                "msg": "contact was succefully updated",
                "contact": contact_schema.dump(contact)
            }
        )

    if request.method == "DELETE":
        if 'username' in request.args:
            username_to_query = request.args.get('username')

            contact = Contact.query.filter_by(
                username=username_to_query).first()
            if not contact:
                return jsonify(
                    {
                        "msg": "contact doesn't exist"
                    }
                ), 404

            db.session.delete(contact)
            db.session.commit()

            return jsonify(
                {
                    "msg": "contact deleted"
                }
            ), 200

        return jsonify(
            {
                "msg": "invalid request"
            }
        ), 400
