import zmq
import json


RATINGS_FILE = "artwork_ratings.json"


def load_ratings():
   try:
       with open(RATINGS_FILE, "r") as file:
           return json.load(file)
   except FileNotFoundError:
       return {}


def save_ratings(ratings):
   with open(RATINGS_FILE, "w") as file:
       json.dump(ratings, file)


def main():
   context = zmq.Context()
   socket = context.socket(zmq.REP)  # REP (reply) socket
   socket.bind("tcp://*:5555")


   print("Rating service running on port 5555...")


   while True:
       try:
           message = socket.recv_json()
           print("Received message:", message)  # Debugging log


           action = message.get("action")
           artwork_id = message.get("artwork_id")


           if action == "rate":
               # Handle rating action
               rating = message.get("rating")
               if not artwork_id or not (1 <= rating <= 5):
                   response = {"error": "Invalid artwork ID or rating. Rating must be between 1 and 5."}
                   print("Error:", response["error"])
               else:
                   # Save the rating
                   ratings = load_ratings()
                   ratings[artwork_id] = rating
                   save_ratings(ratings)
                   response = {"message": "Rating recorded successfully."}
                   print("Success:", response["message"])


           elif action == "retrieve":
               # Handle retrieve action
               ratings = load_ratings()
               rating = ratings.get(str(artwork_id))
               if rating is not None:
                   response = {"artwork_id": artwork_id, "rating": rating}
                   print(f"Retrieved rating for artwork ID {artwork_id}: {rating}")
               else:
                   response = {"error": f"No rating found for artwork ID {artwork_id}"}
                   print(response["error"])


           else:
               response = {"error": "Invalid action"}


           # Send response back to client
           socket.send_json(response)


       except Exception as e:
           error_message = f"An error occurred: {e}"
           print(error_message)
           socket.send_json({"error": error_message})


if __name__ == "__main__":
   main()