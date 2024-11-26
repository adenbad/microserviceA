import zmq

def test_microservice():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)  # REQ (request) socket
    socket.connect("tcp://localhost:5555")

    # Test sending a rating
    print("Sending a rating...")
    rating_request = {
        "action": "rate",
        "artwork_id": "123456",
        "rating": 4
    }
    socket.send_json(rating_request)
    response = socket.recv_json()
    print("Received response:", response)

    # Test retrieving the rating
    print("\nRetrieving the rating...")
    retrieve_request = {
        "action": "retrieve",
        "artwork_id": "123456"
    }
    socket.send_json(retrieve_request)
    response = socket.recv_json()
    print("Received response:", response)

if __name__ == "__main__":
    test_microservice()
