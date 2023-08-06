from cpuspinner import Spinner
import time
spin = Spinner(10)
while spin.isRunning():
    print("Still running")
    time.sleep(1)

