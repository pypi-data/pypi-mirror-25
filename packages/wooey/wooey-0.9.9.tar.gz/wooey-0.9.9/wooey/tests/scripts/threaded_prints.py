import argparse
import random
import sys
import threading
import time

parser = argparse.ArgumentParser(description="Threaded print statements")
blah = parser.add_argument('--something', required=False)

class Thread(threading.Thread):
    def run(self):
        t = time.time()
        time.sleep(random.randint(3,6))
        print("{} Time in sleep: {}\n".format(threading.current_thread().name, time.time()-t))

def main():
    for i in range(10):
        t = Thread()
        t.start()
    return 0

if __name__ == "__main__":
    parser.parse_args()
    sys.exit(main())
