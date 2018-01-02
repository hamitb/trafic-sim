# In consumers.py
import json
from channels import Group
from util.server import rpc_service, rpc_call

# Connected to websocket.connect
def ws_connect(message):
    # Accept connection
    message.reply_channel.send({"accept": True, "text": "Hello from server"})
    # Parse the query string
    rpc_service(message.reply_channel, quick_start=True)

# Connected to websocket.receive
def ws_message(message):
    # message.reply_channel.send({
    #     "text": message["text"],
    # })
    rpc_call(message["text"], message.reply_channel)
