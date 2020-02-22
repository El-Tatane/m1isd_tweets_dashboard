import threading
import random
import time
JOB_RESULTS = {}


def worker(function, id_job, args):
    """thread worker function"""
    time.sleep(1)
    global JOB_RESULTS
    print("debut worker %s" % id_job)
    verrou = threading.Lock()

    result = function(**args)
    print("execution %s %s" % (id_job, result))

    verrou.acquire()
    JOB_RESULTS[id_job] = result
    verrou.release()
    return


def set_orchestrator():
    def wrapper_set_orchestrator(function):
        def create_job(**args):
            id_job = None
            while id_job is None or id_job in JOB_RESULTS.keys():
                id_job = random.randrange(0, 999999)
            JOB_RESULTS[id_job] = "Started"
            threading.Thread(target=worker, args=(function, id_job, args)).start()
            return id_job
        return create_job
    return wrapper_set_orchestrator
