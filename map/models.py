from peewee import *
from datetime import datetime

db = SqliteDatabase("map.db")

class BaseModel(Model):
    class Meta:
        database = db

class MapModel(BaseModel):
    name = CharField(unique=True)
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        order_by = ('created_at',)

class NodeModel(BaseModel):
    node_id = CharField(unique=True)
    map_name = ForeignKeyField(MapModel, related_name="nodes", to_field="name")
    x = FloatField()
    y = FloatField()

class EdgeModel(BaseModel):
    start_node = ForeignKeyField(NodeModel, related_name="routes_going", to_field="node_id")
    end_node = ForeignKeyField(NodeModel, related_name="routes_coming", to_field="node_id")
    map_name = ForeignKeyField(MapModel, related_name="edges", to_field="name")
    lanes_count = IntegerField()
    length = FloatField()

    class Meta:
        indexes = (
            (('start_node', 'end_node'), True),
        )
