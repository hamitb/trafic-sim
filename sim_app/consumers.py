import json
from channels.sessions import http_session
from util.server import register_socket

# Connected to websocket.connect
@http_session
def ws_connect(message):
    # Accept connection
    data = {
        'type': 'message',
        'message': "Successfully bound.",
    }

    try:
        message.reply_channel.send({"accept": True, "text": json.dumps(data)})
        register_socket(message.http_session.session_key, message.reply_channel)
    except:
        message.reply_channel.send({"accept": False, "text": "Session error: key not found"})
    # Parse the query string


# Connected to websocket.receive
def ws_message(message):
    print(message['text'])
