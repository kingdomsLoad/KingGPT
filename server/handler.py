import json
import traceback
from simulator.simulator import crawl_website

async def handle_data(data: bytes) -> str:
    try:
        obj = json.loads(data.decode())
        event = obj['event']
        room = obj['data']['room']
        content = obj['data']['content']
        print(event, room, content)

        response_content = await crawl_website(content)

        obj['event'] = 'response'
        obj['data']['rescon'] = response_content

    except:
        traceback.print_exc()
        obj = data.decode()

    return json.dumps(obj)