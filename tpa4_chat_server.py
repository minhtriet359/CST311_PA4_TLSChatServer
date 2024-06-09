#!env python

"""Chat server for CST311 Programming Assignment 3"""
__author__ = "Group 8"
__credits__ = [
  "Bradley",
  "Shannon",
  "Talia",
  "Triet"
]


import socket as s
import threading

# Configure logging
import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

server_port = 12001
clients = []
client_ids = {}
messages=[]

def client_handler(client_socket, address):
    # Handle client socket and send/receive messages
    # Surround with a try-finally to ensure we clean up the socket after we're done
    try:
        # Get client ID from client_socket
        client_id = client_ids.get(address[0])
        # Attempt to send offline messages to non-sender users
        messages_sent=0
        for m in messages[:]:
            if(str(client_id) not in m):
                messages_sent += 1
                messages.remove(m)
                if messages_sent>1:
                    m ='\n'+m
                m = m.encode("utf-8")
                client_socket.send(m)
        # Enter a forever loop to send and receive messages
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                log.info(f"\nReceived message from {client_id}: {message}")
                if message.lower() == 'bye':
                    bye_message = f"{client_id} has left the chat."
                    log.info(bye_message)
                    message_handler(bye_message, client_socket)
                    break
                else:
                    message_handler(f"{client_id}: {message}", client_socket)
            else:
                break
    except Exception as e:
        log.error(f"Error handling {client_id}: {e}")
    finally:
        # Disconnect client and close socket
        log.info(f"Closing connection to {client_id}")
        client_socket.close()
        clients.remove(client_socket)
        message_handler(f"{client_id} has disconnected.", client_socket)

def message_handler(message, sender_socket):
    # Check number of connected clients
    if len(clients)<2:
        # Store the message for offline clients
        messages.append(message)
    else:
        # Forward messages to other online client
        for client_socket in clients:
            if client_socket != sender_socket:
                try:
                    client_socket.send(message.encode('utf-8'))
                except:
                    client_socket.close()
                    if client_socket in clients:
                        clients.remove(client_socket)

def main():
    # Create a TCP socket
    # Notice the use of SOCK_STREAM for TCP packets
    server_socket = s.socket(s.AF_INET, s.SOCK_STREAM)

    # Assign port number to socket, and bind to chosen port
    server_socket.bind(('', server_port))

    # Configure how many requests can be queued on the server at once
    server_socket.listen(3)

    # Alert user(s) we are now online
    log.info("The server is ready to receive on port " + str(server_port))
    
    # Surround with a try-finally to ensure we clean up the socket after we're done
    try:
        # Enter forever loop to listen for requests
        while True:
            # When a client connects, create a new socket and record their address
            connection_socket, address = server_socket.accept()
            # Get username from client 
            client_id = connection_socket.recv(1024).decode('utf-8')
            # Create new if user has not been registered
            if client_id not in client_ids:
                # Clients connect for the first time, receive and save client ID to IP addressd
                client_ids[address[0]] = client_id
            clients.append(connection_socket)
            log.info(f"Connected to client {client_id} at {address}")
            # Create a thread for each client and pass the new socket and address off to a connection handler function
            threading.Thread(target=client_handler, args=(connection_socket, address)).start()
    finally:
        # Close all sockets
        for client_socket in clients:
            client_socket.close()
        server_socket.close()

if __name__ == "__main__":
    main()
