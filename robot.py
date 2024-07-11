import sys
import time
import socket
import RPi.GPIO as GPIO

# GPIO pin setup
in1 = 24
in2 = 26
sleeptime = 1

GPIO.setmode(GPIO.BOARD)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)

def forward():
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)

def backward():
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.HIGH)

def stop():
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)

stop()

print("Connecting to the server...")

# Socket client setup
host = 'your-mac-ip-address'  # Replace with your Mac's IP address
port = 4444

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))
        print("Connected to the server.")
        
        while True:
            data = sock.recv(1024).decode()
            if not data:
                break

            print(f"Received command: {data}")
            if data == 'f':
                print("Forward")
                forward()
            elif data == 'b':
                print("Backward")
                backward()
            elif data == 's':
                print("Stopping...")
                stop()
            elif data == 'e':
                print("Exiting...")
                stop()
                GPIO.cleanup()
                break

except ConnectionRefusedError:
    print("Could not connect to the server. Make sure the server is running.")

except KeyboardInterrupt:
    print("Program interrupted by the user. Cleaning up...")
    stop()
    GPIO.cleanup()
