import time

import network
from XIAO import *
from machine import Pin
from time import sleep
from wifi_connect import connect_to_network
from umqtt.simple import MQTTClient
import json
import _thread

THIS_BOX = 0  # "JIN"
# THIS_BOX = 1  # "MU"
# THIS_BOX = 2  # "SHUI"
# THIS_BOX = 3  # "HUO"
# THIS_BOX = 4  # "TU"

ssid = "EVERYWHERE-YZP"
password = "love4yzp"

broker = "47.119.176.136" # your server address
client_id = "jin"
client_password = "jin123"


board = BoardConfig()
pin_IN1 = Pin(board.D5, Pin.OUT)  # left
pin_IN2 = Pin(board.D4, Pin.OUT)  # center


class Motor:
    def __init__(self, IN1: Pin, IN2: Pin) -> None:
        self.IN1 = IN1
        self.IN2 = IN2

    def stop(self):
        self.IN1.off()
        self.IN2.off()

    def brake(self):
        self.IN1.on()
        self.IN2.on()

    def foreward(self, time=1):  # 1s
        self.IN1.on()
        self.IN2.off()
        sleep(time)
        self.stop()

    def backward(self, time=1):  # 1s
        self.IN1.off()
        self.IN2.on()
        sleep(time)
        self.stop()


motor = Motor(pin_IN1, pin_IN2)


def motor_redeem():
    motor.foreward(1)
    motor.backward(1)


class Maker_mqtt:
    def __init__(
        self, ssid, password, client_id, client_password, broker, username=None
    ):
        self.online_status = connect_to_network(ssid, password)

        if self.online_status:
            print("Trying connecting to MQTT broker")
            self.client = MQTTClient(
                client_id, broker, user=username, password=client_password
            )
            self.client.connect()  # Connect to the MQTT broker
            print("Connected to MQTT Broker")
        else:
            print("Wi-Fi connection failed.")

    def subscribe(self, topic, callback, qos=1):
        self.client.set_callback(callback)
        self.client.subscribe(topic, qos=qos)  # Set QoS level
        print(f"Subscribed to topic: {topic}")

    def publish(self, topic, message, qos=1):
        # """Publish a message to a specified topic with specified QoS."""
        self.client.publish(topic, message, qos=qos)  # Set QoS level
        print(f"Published message: '{message}' to topic: '{topic}'")

    def check_msg(self):
        # """Check for incoming messages and handle callbacks."""
        self.client.check_msg()

    def disconnect(self):
        # """Disconnect the MQTT client."""
        self.client.disconnect()
        print("Disconnected from MQTT Broker")


def message_callback(topic, msg):
    # print(f"Received message: {msg} on topic: {topic}")

    # Step 1: Decode the message from bytes to a UTF-8 string
    try:
        msg_str = msg.decode("utf-8")
        # print("Decoded message:", msg_str)  # Check the decoded message
    except UnicodeDecodeError as e:
        print(f"Failed to decode message as UTF-8: {e}")
        return

    # Step 2: Parse the JSON string into a dictionary
    try:
        data = json.loads(msg_str)

        # Access specific fields in the JSON data
        box = data.get("box")
        user_id = data.get("user_id")

        if box == THIS_BOX:
            _thread.start_new_thread(motor_redeem, ())
            response = {
                "box": THIS_BOX,
                "user_id": str(user_id),
            }
            # Convert the response dictionary to a JSON string
            response_str = json.dumps(response)
            maker_mqtt.publish("redeem/response", response_str)
            print("Response sent:", response_str)

    except json.JSONDecodeError as e:
        pass
        print(f"Failed to decode JSON: {e}")


if __name__ == "__main__":    maker_mqtt = Maker_mqtt(ssid, password, client_id, client_password, broker)

    try:
        if maker_mqtt.online_status:
            maker_mqtt.subscribe("redeem/request", message_callback)
            maker_mqtt.publish("redeem/response", f"Hello from {THIS_BOX}!")

            # 检查消息的主循环
            while True:
                maker_mqtt.check_msg()
                time.sleep(1)

    except KeyboardInterrupt:
        print("Program interrupted!")

    finally:
        maker_mqtt.disconnect()  # 保证客户端在脚本终止时断开连接

