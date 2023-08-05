import threading
import queue

from .. import spy
from .. import message
from .. import version

class Routine(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.queue = queue.Queue()
        self.manager = None

    def run(self):
        while True:
            data = self.queue.get()
            action = data['action'] if 'action' in data else None

            if action == 'authenticate':
                self.authenticate()
            elif action == 'install':
                secret = data['secret'] if 'secret' in data else None
                spy.save_secret(secret)

            self.queue.task_done()

    def authenticate(self):
        payload = {
            'type':'auth',
            'secret': spy.load_secret(),
            'version': version.VERSION,
        }
        self.manager.send(message.Message(payload))
