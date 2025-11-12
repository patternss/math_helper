import sys
from pathlib import Path

parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir))

from assistant import Assistant


assistant = Assistant()

assistant.clear_msg_history()

resp = assistant.get_response('help me with this one!', '5+5*4', ['40'])
print(resp)