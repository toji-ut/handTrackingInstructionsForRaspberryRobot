import mediapipe as mp
import cv2
import socket
import threading

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Server setup
host = '0.0.0.0'
port = 4444

# Global list to keep track of connected clients
clients = []

def handle_client(client_socket):
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
        except:
            break
    client_socket.close()

def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f'Server listening on port {port}...')

    while True:
        client_socket, addr = server_socket.accept()
        print(f'Connected by {addr}')
        clients.append(client_socket)
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

# Utility function to send commands to all connected clients
def send_command(command):
    print(f"Sending command: {command}")
    for client_socket in clients:
        try:
            client_socket.sendall(command.encode())
        except:
            clients.remove(client_socket)
            client_socket.close()

# Check if two points are touching
def are_fingers_touching(point1, point2, threshold=0.05):
    distance = ((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2 + (point1.z - point2.z) ** 2) ** 0.5
    return distance < threshold

# Start server in a separate thread
server_thread = threading.Thread(target=run_server)
server_thread.start()

# Start capturing video
cam = cv2.VideoCapture(0)

with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5) as hands:
    while cam.isOpened():
        ret, frame = cam.read()

        # BGR to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Flip on horizontal
        image = cv2.flip(image, 1)

        # Set flag
        image.flags.writeable = False

        # Detections
        results = hands.process(image)

        # Set flag to true
        image.flags.writeable = True

        # RGB to BGR
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Rendering results
        if results.multi_hand_landmarks:
            for num, hand in enumerate(results.multi_hand_landmarks):
                mp_drawing.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS,
                                          mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
                                          mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2, circle_radius=2),
                                          )

                # Extracting finger tips
                thumb_tip = hand.landmark[4]
                index_tip = hand.landmark[8]
                middle_tip = hand.landmark[12]
                ring_tip = hand.landmark[16]
                pinky_tip = hand.landmark[20]

                # Detect gestures
                if are_fingers_touching(thumb_tip, index_tip):
                    send_command('f')
                elif are_fingers_touching(thumb_tip, middle_tip):
                    send_command('b')
                elif are_fingers_touching(thumb_tip, ring_tip):
                    send_command('s')
                elif are_fingers_touching(thumb_tip, pinky_tip):
                    send_command('e')

        cv2.imshow('Hand Tracking', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cam.release()
cv2.destroyAllWindows()
