from thingy52.thingy52 import Thingy52
from thingy52.delegates import ThingyCharDelegate
import atexit
t = Thingy52("E2:D9:D5:C6:30:26")


atexit.register(t.disconnect)
t.setDelegate(ThingyCharDelegate(t.handles))
t.environment.toggle_notifications(characteristic="temperature", enable=True)
while True:
    t.waitForNotifications(1.0)
    print("Waiting...")
