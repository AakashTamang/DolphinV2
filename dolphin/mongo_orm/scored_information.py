from mongoengine import Document, StringField, DictField, ListField


class ScoredDocuments(Document):
    user_profile = DictField()
    job_description = DictField()
