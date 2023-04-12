from mongoengine import Document, StringField, IntField, ListField


class Employee(Document):
    emp_id = IntField()
    name = StringField(max_length=100)
    age = IntField()
    teams = ListField()