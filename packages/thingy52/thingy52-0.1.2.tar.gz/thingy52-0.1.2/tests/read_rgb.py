from thingy52.thingy52 import Thingy52
import atexit
t = Thingy52("E2:D9:D5:C6:30:26")

atexit.register(t.disconnect)
t.ui.rgb_constant(0, 255, 0)
before = t.ui.rgb_read()
t.ui.rgb_off()
after = t.ui.rgb_read()
b=1
