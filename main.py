import websocket
import rel
import os
from dotenv import load_dotenv
from zoomer import (
  open_zoom_app,
  create_zoom_room,
  approve_remote_control,
  press_enter,
  share_screen,
  switch_tab,
  switch_window,
  focus_zoom_meeting,
  hide_window,
)

load_dotenv()

REMOTE_COMMAND_WSS_HOST = os.environ['REMOTE_COMMAND_WSS_HOST']
REMOTE_COMMAND_WSS_PORT = os.environ['REMOTE_COMMAND_WSS_PORT']
REMOTE_COMMAND_APP_NAME = os.environ['REMOTE_COMMAND_APP_NAME']

def on_message(ws, message):
    if message == 'open':
        open_zoom_app()
    elif message == 'create':
        create_zoom_room()
    elif message == 'approve' or message == "accept":
        approve_remote_control()
    elif message == 'enter':
        press_enter()
    elif message == 'share':
        share_screen()
    elif message == 'switchtab':
        switch_tab()
    elif message == 'switch':
        switch_window()
    elif message == 'focus':
        focus_zoom_meeting()
    elif message == 'hide':
        hide_window()

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    print("Opened connection")
    ws.send_text(REMOTE_COMMAND_APP_NAME)

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(f"ws://{REMOTE_COMMAND_WSS_HOST}:{REMOTE_COMMAND_WSS_PORT}",
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)

    ws.run_forever(dispatcher=rel, reconnect=5)  # Set dispatcher to automatic reconnection, 5 second reconnect delay if connection closed unexpectedly
    rel.signal(2, rel.abort)  # Keyboard Interrupt
    rel.dispatch()