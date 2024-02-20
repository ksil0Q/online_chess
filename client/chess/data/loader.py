import os
from dotenv import load_dotenv


load_dotenv()

WEBSOCKET_URI=os.environ.get('WEBSOCKET_URI')

WINDOW_HEIGHT=int(os.environ.get('WINDOW_HEIGHT'))
WINDOW_WIDTH=int(os.environ.get('WINDOW_WIDTH'))

WINDOW_SIZE = (WINDOW_HEIGHT, WINDOW_WIDTH)

SESSION_ID_SIZE=int(os.environ.get('SESSION_ID_SIZE'))

MESSAGE_ID_SIZE=int(os.environ.get('MESSAGE_ID_SIZE'))
