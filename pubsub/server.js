require('dotenv').config();
require('console-stamp')(console, 'yyyy-mm-dd HH:MM:ss.l');

const express = require('express');
const http = require('http');
const bodyParser = require('body-parser');
const redis = require('redis');
const ioredis = require('socket.io-redis');

// Load environment variables
const PUBLISHER_KEY = process.env.AUTH_TOKEN || '123456';
const SERVER_PORT = process.env.SERVER_PORT || 8001;
const REDIS_HOST = process.env.REDIS_HOST || 'redis';
const REDIS_PORT = process.env.REDIS_PORT || 6379;

const app = express();
const server = http.createServer(app);
const io = require('socket.io')(server);

io.adapter(ioredis({ host: REDIS_HOST, port: REDIS_PORT }));

const subscriber = redis.createClient(`redis://${REDIS_HOST}:${REDIS_PORT}`);
const publisher = redis.createClient(`redis://${REDIS_HOST}:${REDIS_PORT}`);

subscriber.on('error', (error) => {
    console.log('An error occurred: ' + error);
});

subscriber.on('subscribe', (channel, count) => {
    console.log('Subscribing to Redis channel: ' + channel + ' - Subscribers: ' + count);
});

subscriber.on('message', (channel, payload) => {
    console.log('Message received: ', channel, payload);
    io.sockets.in(channel).emit("messages.new", payload);
});

io.sockets.on('connection', (socket) => {
    console.log('Client connected..');

    socket.on('client-subscribe', (data) => {
        console.log('Subscribe to ' + data);
        subscriber.subscribe(data);
        socket.join(data);
    });

    socket.on('disconnect', () => {
        var ip = socket.handshake.address;
        console.log('Client disconnected ' + ip);
    });
});

// Middleware to parse JSON bodies
app.use(bodyParser.json());

// Handle JSON parsing errors
app.use((err, req, res, next) => {
    if (err instanceof SyntaxError && err.status === 400 && 'body' in err) {
        console.log("Received bad JSON");
        return res.status(400).send('JSON parse error');
    }
    next();
});

// Handle incoming requests to publish messages
app.post('/in', (req, res) => {
    const contype = req.headers['content-type'];
    if (!contype || contype.indexOf('application/json') !== 0) {
        return res.status(400).send("Bad Request. Content-Type must be application/json");
    }

    const authkey = req.get('X-Auth-Token');
    const body = req.body;

    if (authkey === PUBLISHER_KEY) {
        console.log("Publishing payload: " + body.payload);
        publisher.publish(body.channel, body.payload);
        res.send("Accepted");
    } else {
        res.status(401).send("Auth failed");
    }
});

// Start the server
server.listen(SERVER_PORT, () => {
    console.log(`Listening on port ${SERVER_PORT} with Auth key: ${PUBLISHER_KEY}`);
});
