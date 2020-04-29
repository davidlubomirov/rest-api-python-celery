### TODOs
| Filename | line # | TODO
|:------|:------:|:------
| [api/app/models/contact.py](api/app/models/contact.py#L6) | 6 | @David No validation for length of fields in both models
| [api/app/models/contact.py](api/app/models/contact.py#L27) | 27 | @David Add email type: personal or corporate
| [api/app/routes/contact.py](api/app/routes/contact.py#L10) | 10 | @David Move all response codes in globals for reuse in test cases
| [api/app/subtasks/contact.py](api/app/subtasks/contact.py#L23) | 23 | @David username is set to unique. Therefore if a username already exists it'll get 500 db exception
| [api/app/tests/test_contact.py](api/app/tests/test_contact.py#L23) | 23 | @David Move this in the global file when move then one package requires it's usage.
