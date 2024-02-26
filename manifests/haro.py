import asyncio
import os
from meross_iot.http_api import MerossHttpClient
from meross_iot.manager import MerossManager
import logging
from slack_sdk import WebClient
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

logging.basicConfig(level=logging.info, format='%(asctime)s %(message)s')

MEROSS_EMAIL = os.getenv('MEROSS_EMAIL')
MEROSS_PASSWORD = os.getenv('MEROSS_PASSWORD')
MEROSS_DEVICE_TYPE = os.getenv('MEROSS_DEVICE_TYPE')
MEROSS_DEVICE_NAME = os.getenv('MEROSS_DEVICE_NAME')
MEROSS_DEVICE_CHANNEL = os.getenv('MEROSS_DEVICE_CHANNEL')

ALERTMANAGERID = os.getenv("ALERTMANAGER_ID")

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")

app = App(token=SLACK_BOT_TOKEN)
loop = asyncio.get_event_loop()

async def _ntd(status):
    http_api_client = await MerossHttpClient.async_from_user_password(api_base_url='https://iotx-ap.meross.com',
                                                                      email=MEROSS_EMAIL, 
                                                                      password=MEROSS_PASSWORD)
    manager = MerossManager(http_client=http_api_client)
    await manager.async_init()
    await manager.async_device_discovery()
    device =manager.find_devices(device_type=MEROSS_DEVICE_TYPE, device_name=MEROSS_DEVICE_NAME)

    if len(device) == 1:
      if status :
        await device[0].async_turn_on(channel=MEROSS_DEVICE_CHANNEL)
      else: 
        await device[0].async_turn_off(channel=MEROSS_DEVICE_CHANNEL)
    else:
       print("Not found divice")
			 
    manager.close()
    await http_api_client.async_logout()

def ntd(status):
  loop.run_until_complete(_ntd(status))

# Event API
@app.event("message")
def handle_alert(event, say):
    logging.debug("Calling handle_alert()")
    logging.info("handle_alert(event): %s", str(event))

    thread_ts = event.get("thread_ts") or None
    bot_id = event.get("bot_id") or None
    channel = event["channel"]

    if thread_ts != None:
        logging.info("Ignore the message because it is tme message in a thread")
        return

    if bot_id is None:
        logging.info("Ignore the message because it is not a Bot")
        return

    if bot_id != ALERTMANAGERID:
        logging.info("Ignore the message because it is not an Alert message")
        return

    res = app.client.conversations_replies(channel=channel, ts=event["ts"])
    thread = res["messages"][0]["ts"]

    for attachment in event["attachments"]:
        title = attachment["title"]  
        if title.startswith('[FIRING'):
          say(text="NT-D発動", thread_ts=thread, channel=channel)
          ntd(1)
        elif title.startswith('[RESOLVED'): 
          say(text="NT-D停止", thread_ts=thread, channel=channel)
          ntd(0)

if __name__ == '__main__':
  # Start slack bot
  handler = SocketModeHandler(app, SLACK_APP_TOKEN)
  handler.start()
   
  loop.close() 
