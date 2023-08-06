import time
import threading

class Spinner:
    """ CPU spinner class """

    def __init__(self, duration=10):
        """ Constructor
        :type duration: int
        :param duration: How long to spin
        """
        self.duration = duration 
        self.running = True

        thread = threading.Thread(target=self.run, args=())
        thread.setDaemon(True)
        thread.start()

    def isRunning(self):
        return self.running

    def run(self):
        """ Method that runs forever """
	start_time = time.time()
        while (time.time() - start_time) < self.duration:
            pass
        self.running = False
