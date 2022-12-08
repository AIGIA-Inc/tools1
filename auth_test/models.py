from peewee import SqliteDatabase, Model, AutoField, CharField, TextField

db = SqliteDatabase('db.sqlite3')

class User(Model):
    id = AutoField(primary_key=True)
    name = CharField(100)
    password = CharField(100)
    refresh_token = TextField(null=True)

    class Meta:
        database = db

db.create_tables([User])

# ユーザーデータ挿入
User.create(name='aigia', password='1terabyte')
