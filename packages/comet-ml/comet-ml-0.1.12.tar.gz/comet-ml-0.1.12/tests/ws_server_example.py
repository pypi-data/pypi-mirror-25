from websocket_server import WebsocketServer


def my_websocket_server():
    # Called for every client connecting (after handshake)
    def new_client(client, server):
        pass

    # Called for every client disconnecting
    def client_left(client, server):
        pass

    # Called when a client sends a message
    def message_received(client, server, message):
        # echo
        with open("tmp/server.txt" ,'a') as f:
            f.write(message)

    PORT = 9005
    server = WebsocketServer(PORT)
    server.set_fn_new_client(new_client)
    server.set_fn_client_left(client_left)
    server.set_fn_message_received(message_received)
    server.run_forever()


print("server started")
my_websocket_server()