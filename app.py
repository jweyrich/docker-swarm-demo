import socket
import uuid

from flask import Flask, render_template
from redis import Redis

# Create the flask application
app = Flask(__name__)

# Connect to redis and set num_requests to 0 if it doesn't exist
redis = Redis(host='redis')
redis.setnx('num_requests', 0)

# Get the id of the docker container we're running in (it's our hostname)
container_id = socket.gethostname()


@app.route('/')
def home():
    # Increment the number of requests
    redis.incr('num_requests')

    # Display process information to the user
    return render_template(
        'home.html',
        container_id=container_id,
        num_requests=int(redis.get('num_requests')),
    )

if __name__ == '__main__':
    # This will only run when using docker-compose.override.yml
    app.run(debug=True, host='0.0.0.0')
