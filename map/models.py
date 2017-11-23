from peewee import *
from datetime import datetime

db = SqliteDatabase("map.db", pragmas=(('foreign_keys', 'on'),))

class BaseModel(Model):
    class Meta:
        database = db

class MapModel(BaseModel):
    name = CharField(unique=True)
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        order_by = ('created_at',)

class NodeModel(BaseModel):
    node_id = CharField()
    map_name = ForeignKeyField(MapModel, related_name="nodes", to_field="name", on_delete="CASCADE")
    x = FloatField()
    y = FloatField()
    
    class Meta:
        indexes = (
            (('map_name', 'node_id'), True),
        )   

class EdgeModel(BaseModel):
    start_node = CharField()
    end_node = CharField()
    map_name = CharField()
    lanes_count = IntegerField()
    length = FloatField()

    class Meta:
        constraints = [SQL('FOREIGN KEY(map_name, start_node) '
                           'REFERENCES nodemodel(map_name_id, node_id) '
                           'ON DELETE CASCADE'),
                       SQL('FOREIGN KEY(map_name, end_node) '
                           'REFERENCES nodemodel(map_name_id, node_id) '
                           'ON DELETE CASCADE'),
                      ]
