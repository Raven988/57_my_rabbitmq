import threading

import pika
import time


class WorkerThread(threading.Thread):
    def __init__(self):
        super(WorkerThread, self).__init__()
        self._is_interrupted = False
        self.daemon = True

    def stop(self):
        self._is_interrupted = True

    def run(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters())
        channel = connection.channel()
        channel.queue_declare("queue")
        for message in channel.consume("queue", inactivity_timeout=1):
            print(message)
            if self._is_interrupted:
                break
            if not all(message):
                continue
            method, properties, body = message
            print(body)

def main():
    thread = WorkerThread()
    thread.start()
    # some main thread activity .....
    time.sleep(20)
    thread.stop()
    thread.join()


if __name__ == "__main__":
    main()