from mongoengine import Document, StringField, DictField, ListField


class ParsedCollection(Document):
    education = DictField()
    experience = DictField()
    languages = ListField()
    objectives = StringField()
    personal_information = DictField()
    projects = StringField()
    references = StringField()
    rewards = StringField()
    skills = DictField()
