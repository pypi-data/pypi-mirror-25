from queue import Queue, Empty
from time import time
from aerospike_connpool.aerospikeConnection import AerospikeConnection

class ClientUnavailableError(Exception):
    pass

class AerospikeConnectionWrapper(object):
    def __init__(self, creds_val):
        ac = AerospikeConnection()
        self.conn = ac.get_connection(str(creds_val['host']), int(creds_val['port']))
        self.use_count = 0
        self.use_time = 0
        self.last_use_time = 0

    def start_using(self):
        self.last_use_time = time()

    def stop_using(self):
        self.use_time += time() - self.last_use_time
        self.use_count += 1

class Pool(object):
    def __init__(self, connargs, initial=4, max_clients=10):
        self._q = Queue()
        self._l = []
        self._connargs = connargs
        self._cur_clients = 0
        self._max_clients = max_clients

        for x in range(initial):
            self._q.put(self._make_client())
            self._cur_clients += 1

    def _make_client(self):
        ret = AerospikeConnectionWrapper(self._connargs)
        self._l.append(ret)
        return ret

    def get_client(self, initial_timeout=0.05, next_timeout=200):
        try:
            cb = self._q.get(True, initial_timeout)
            cb.start_using()
            return cb
        except Empty:
            try:
                if self._cur_clients == self._max_clients:
                    raise ClientUnavailableError("Too many clients in use")
                    cb = self._make_client()
                    self._cur_clients += 1
                    cb.start_using()
                    return cb
            except ClientUnavailableError as ex:
                try:
                    return self._q.get(True, next_timeout)
                except Empty:
                    raise ex

    def release_client(self, cb):
        cb.stop_using()
        self._q.put(cb, True)

def main():
    pool = Pool("mmm", 5, 15)

    for c in pool._l:
        print ("Have client %s" % (str(c.conn)))
        print ("Time In Use: {0}, use count: {1}".format(c.use_time, c.use_count))

#if __name__ == "__main__":
#    main()

