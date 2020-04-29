import random
import string

from sqlalchemy import text


from app import celery

from app.db import db
from app.models.contact import Contact, Email

EMAILS = [
    "first_test_email@test-mail.com",
    "second_test_email@test-mail.com",
    "third_test_email@test-mail.com",
    "fourth_test_email@test-mail.com",
    "fifth_test_email@test-mail.com",
]


@celery.task()
def create_random_contacts():
    # TODO(David): username is set to unique. Therefore if a username already exists it'll get 500 db exception
    username = ''.join(random.choice(string.ascii_lowercase)
                       for _ in range(40))
    first_name = ''.join(random.choice(string.ascii_lowercase)
                         for _ in range(40))
    last_name = ''.join(random.choice(string.ascii_lowercase)
                        for _ in range(40))

    curr_contact = Contact(
        username=username,
        first_name=first_name,
        last_name=last_name
    )

    db.session.add(curr_contact)
    db.session.commit()

    selected_emails = random.sample(EMAILS, random.randint(0, len(EMAILS)))
    if len(selected_emails) is not 0:
        for each_email in selected_emails:
            curr_email = Email(email=each_email, contact=curr_contact)
            db.session.add(curr_email)

        db.session.commit()


@celery.task()
def delete_contacts():
    """Delete all contact that were created in the last 1 min
    """
    time_filter = text("created_at > datetime('now', '-1 minute')")

    all_contacts = Contact.query.filter(time_filter).all()

    if len(all_contacts) is not 0:
        for each_contact in all_contacts:
            db.session.delete(each_contact)

        db.session.commit()
