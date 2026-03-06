import time
from update import update_all
from Configuration import _DEFAULT_CONFIGURATION

def cycle_with_interval():
    config = _DEFAULT_CONFIGURATION
    while True:
        while not update_all():
            pass
        time.sleep(config.interval)

if __name__ == "__main__":
    cycle_with_interval()