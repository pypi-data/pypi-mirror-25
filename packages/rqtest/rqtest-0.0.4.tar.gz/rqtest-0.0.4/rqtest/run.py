import sys
import requests
import time


def main():
    args = sys.argv[1:]
    if len(args) != 2:
        print("rqtest timelimit url")
        exit(1)
    timelimit, url = args
    timelimit = int(timelimit)
    start_at = time.time()
    while True:
        try:
            ret = requests.get(url, timeout=3)
            if 200 <= ret.status_code < 210:
                print("Ping Succeed")
                exit(0)
        except Exception as e:
            pass
        if time.time() - start_at > timelimit:
            print("Ping Failed")
            exit(1)
        time.sleep(2)

