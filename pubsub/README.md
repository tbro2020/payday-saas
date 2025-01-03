This is a simle setup to demonstrate pub/sub using Redis, WebSockets and NodeJS.

## What exactly does this do?

You will end up with two simple docker instances. One for redis and one
with your pubsub service. 

## Getting Started


First clone the repo, build docker and start the instance 
```
git clone https://github.com/fbhdk/docker-redis-websockets.git
cd docker-redis-websockets
docker-compose build 
docker-compose up
```

Open `client.html` in a browser and open the inspector. 
Reload the page and you should see console output.

Run this to generate a new message: 
```
curl --request POST --url http://localhost:8000/in --header 'x-auth-token: PourSomeSugarOnMe' --header 'content-type: application/json' --data '{"channel": "my-awesome-channel", "payload": "This is a message!" }'
```

Voila! The message should now show in your browser window. 

