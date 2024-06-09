#!env python

"""Chat client for CST311 Programming Assignment 3"""
__author__ = "Group 8"
__credits__ = [
  "Bradley",
  "Shannon",
  "Talia",
  "Triet"
]

# Import statements
import socket as s
import threading
import os

# Configure logging
import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

# Set global variables
server_ip = "10.0.1.2"
server_port = 12001

def receive_message(socket):
  # Enter an infinite loop to receive messages
  while True:
    # Errors/exceptions handling
    try:
      # Receive and decode the message using 'utf-8'
      message=socket.recv(1024).decode('utf-8')
      # Print non-empty message
      if message:
        print(message)
      else:
        break
    except:
      print("Error occured, closing.")
      break

def main():
  # Create socket
  client_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
  
  # Establish TCP connection
  try:
    client_socket.connect((server_ip,server_port))
    # specify username
    user_input = input("Specify username: ")
    client_socket.send(user_input.encode('utf-8'))
  except Exception as e:
    log.exception(e)
    log.error("***Advice:***")
    if isinstance(e, s.gaierror):
      log.error("\tCheck that server_name and server_port are set correctly.")
    elif isinstance(e, ConnectionRefusedError):
      log.error("\tCheck that server is running and the address is correct")
    else:
      log.error("\tNo specific advice, please contact teaching staff and include text of error and code.")
    exit(8)

  # Print welcome message
  print("Connected to chat server. To send a message, type the message and hit enter") 

  # Create and start a seperate thread for receiving messages
  threading.Thread(target=receive_message,args=(client_socket,)).start()

  # Wrap in a try-finally to ensure the socket is properly closed regardless of errors
  try:
    while True:
      # Set data across socket to server
      #  Note: encode() converts the string to UTF-8 for transmission
      user_input=input()
      client_socket.send(user_input.encode('utf-8'))
      if user_input.lower()=='bye':
        # clear terminal screen
        os.system('cls' if os.name == 'nt' else 'clear')
        break
  finally:
    # Close socket prior to exit
    client_socket.close()

# This helps shield code from running when we import the module
if __name__ == "__main__":
  main()