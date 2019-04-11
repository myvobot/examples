import uasyncio as asyncio
import json
from core.params import *

class App:
    """App for periodic update of weather station

    - Request for latest weather over HTTP GET every hour
    - Analysis the weather condition
    - Generate a layout template and send to wireless display
    """

    def __init__(self, mgr, loop, pan):
        self.pan = pan
        loop.create_task(self.task()) # run a asyncio task
        self.targetNodeId = None
        mgr.setPanCallback(self.onPanEvent);

    async def task(self):
        """Main task of App Class
        This coro task() was brought up by __init__().
        """
        # waiting for at least one display node becomes online
        while self.targetNodeId is None:
            await asyncio.sleep(1)
        await self.printHello()

    def onPanEvent(self, event, data):
        if event == EVT_NODE_PRESENCE:
            if data['isOnline']:
                self.targetNodeId = data['nodeId']
                print('node:', self.targetNodeId, 'online.')

    async def printHello(self):
        """Create layout render template and send to display"""
        try:
            layout = '''
            {
                "background": {
                    "bgColor": "WHITE",
                    "enableButtonZone": false,
                    "rectangle": {
                        "strokeSize": 2,
                        "fgColor": "BLACK",
                        "block": { "x_percent": 10, "y_percent": 30, "w_percent": 80, "h_percent": 40,
                        }
                    }
                },
                "items": [
                    { "type": "TEXT",
                      "data": {
                        "caption": "HELLO WORLD",
                        "font": "YKSZ_BOLD_44",
                        "color": "BLACK",
                        "block": { "x": 120, "y": 125, "w": 200, "h": 56 },
                        "offset": { "x": 0, "y": 0 },
                      }
                    }
                ]
            }
            '''
            return await self.pan.updateDisplay(self.targetNodeId, json.loads(layout))
        except Exception as e:
            self.log.exception(e, 'unable to process')
        return False