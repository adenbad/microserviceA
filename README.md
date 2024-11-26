Overview
    This microservice allows users to store and retrieve ratings for artwork using ZeroMQ for communication. The ratings are saved in a JSON file (artwork_ratings.json) for persistence.
    The microservice can:
    1. Store a rating for an artwork based on its ID.
    2. Retrieve a rating for an artwork by its ID.

Prerequisites
    Python 3.x
    pyzmq Python Library(pip3 install pyzmq)

How to Use the Microservice
    Run the Microservice
    Start the microservice by running:
        python rating_service_zmq.py
        The service will bind to tcp://*:5555 and wait for requests.

Communication Contract
    The microservice communicates via JSON objects. The client must follow these structures to interact with the service.

    1. Send a Rating
        To store a rating for an artwork, send a JSON object with the following structure:
        {
            "action": "rate",
            "artwork_id": "<ARTWORK_ID>",
            "rating": <RATING>
        }
        <ARTWORK_ID>: A unique identifier for the artwork (string or number).
        <RATING>: A value between 1 and 5 (inclusive).
    
    Example Call (Python):
        socket.send_json({
            "action": "rate",
            "artwork_id": "123456",
            "rating": 4
        })
        response = socket.recv_json()
        print(response)  # Expected: {"message": "Rating recorded successfully."}
   
    2. Retrieve a Rating
        To retrieve a rating for an artwork, send a JSON object with the following structure:
        {
            "action": "retrieve",
            "artwork_id": "<ARTWORK_ID>"
        }
        <ARTWORK_ID>: The unique identifier for the artwork whose rating is being retrieved.
        
    Example Call (Python):
        socket.send_json({
            "action": "retrieve",
            "artwork_id": "123456"
        })
    response = socket.recv_json()
    print(response)  # Expected: {"artwork_id": "123456", "rating": 4}
    
    Error Handling
    If the artwork_id is not provided or invalid, the server responds with:
        {"error": "Invalid artwork ID or rating. Rating must be between 1 and 5."}

    If no rating exists for the given artwork_id, the server responds with:
        {"error": "No rating found for artwork ID <ARTWORK_ID>"}

    If an unsupported action is sent, the server responds with:
        {"error": "Invalid action"}