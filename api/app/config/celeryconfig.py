CELERY_IMPORTS = ("app.subtasks.contact")

CELERYBEAT_SCHEDULE = {
    "create-contacts": {
        "task": "app.subtasks.contact.create_random_contacts",
        "schedule": 15.0
    },
    "delete-contacts": {
        "task": "app.subtasks.contact.delete_contacts",
        "schedule": 60.0
    }
}
