from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Request
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from datetime import datetime
import logging
import httpx
import json
import os
from celery import Celery

# Load environment variables
load_dotenv()

# Configuration
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "https://webhook-test.com/72789d7d81fbbce5e2e54c51cc7f0303")
BROKER_URL = os.getenv("BROKER_URL", "redis://localhost:6379/0")
AUTHORIZATION_TOKEN = os.getenv("AUTHORIZATION_TOKEN")

# FastAPI App Initialization
app = FastAPI()

# Initialize Celery
celery_app = Celery("payday", broker=BROKER_URL, backend=BROKER_URL)

# Logger Configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("WebSocketApp")

# Tracks connected devices by serial number (sn)
connected_clients = {}

# Helper Functions
@celery_app.task(bind=True, default_retry_delay=300)
def send_to_webhook(self, data: dict):
    """
    Celery task to send data to a webhook. Retries on failure.

    :param self: Reference to the Celery task instance
    :param data: The data to send to the webhook
    """
    headers = {"Content-Type": "application/json"}
    if AUTHORIZATION_TOKEN:
        headers["Authorization"] = AUTHORIZATION_TOKEN

    response = httpx.post(WEBHOOK_URL, json=data, headers=headers)
    logger.info(f"Webhook success: {response.status_code} | Data: {data}")
    response.raise_for_status()


async def forward_command_to_device(sn: str, command: dict):
    """
    Forwards a command to a connected WebSocket device.

    :param sn: Serial number of the target device
    :param command: Command data to send
    :raises HTTPException: If the device is not connected
    """
    if sn in connected_clients:
        websocket = connected_clients[sn]
        await websocket.send_text(json.dumps(command))
        logger.info(f"Command sent to {sn}: {command}")
    else:
        logger.warning(f"Device {sn} not connected.")
        raise HTTPException(status_code=404, detail=f"Device {sn} not connected.")


async def handle_message_from_device(sn: str, message: str):
    """
    Processes messages received from a WebSocket device.

    :param sn: Serial number of the device
    :param message: JSON-formatted message string
    """
    try:
        data = json.loads(message)
        send_to_webhook.delay(data)  # Enqueue the task for Celery
        logger.info(f"Message received from {sn}: {data}")
    except json.JSONDecodeError:
        logger.warning(f"Invalid JSON received from {sn}: {message}")


# HTTP Endpoints
@app.post("/send-command/")
async def send_command(request: Request):
    """
    Accepts a command via HTTP and forwards it to a WebSocket device.

    :param request: HTTP request containing command data
    :return: JSON response indicating success or failure
    """
    data = await request.json()
    sn = data.get("sn")
    cmd = data.get("cmd")

    if not sn or not cmd:
        raise HTTPException(status_code=400, detail="Missing 'sn' or 'cmd' in request.")

    try:
        await forward_command_to_device(sn, data)
        return JSONResponse(content={"status": "success", "message": "Command sent"})
    except Exception as e:
        logger.error(f"Error sending command: {e}")
        raise HTTPException(status_code=500, detail=f"Error sending command: {str(e)}")


# WebSocket Endpoint
@app.websocket("/pub/chat")
async def websocket_endpoint(websocket: WebSocket):
    """
    Handles WebSocket connections from devices.

    :param websocket: The WebSocket connection object
    """
    logger.info("WebSocket connection initiated.")
    await websocket.accept()

    try:
        # Perform handshake: Device sends a registration message
        register_message = await websocket.receive_text()
        register_data = json.loads(register_message)

        if register_data.get("cmd") != "reg" or "sn" not in register_data:
            logger.warning("Invalid handshake message.")
            await websocket.close(code=4000, reason="Invalid handshake message")
            return

        sn = register_data["sn"]
        logger.info(f"Device {sn} registered.")
        connected_clients[sn] = websocket

        # Acknowledge registration
        response = {
            "ret": "reg",
            "result": True,
            "cloudtime": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        }
        await websocket.send_text(json.dumps(response))
        send_to_webhook.delay(register_data)  # Enqueue the registration data for webhook processing

        # Handle incoming messages
        while True:
            try:
                message = await websocket.receive_text()
                await handle_message_from_device(sn, message)
            except WebSocketDisconnect:
                logger.info(f"Device {sn} disconnected.")
                connected_clients.pop(sn, None)
                break
            except Exception as e:
                logger.error(f"Error handling message from {sn}: {e}")
                break
    except Exception as e:
        logger.error(f"WebSocket connection error: {e}")