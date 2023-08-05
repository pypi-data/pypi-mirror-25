import aerospike

class AerospikeConnector(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.dbconn = None
    
    # creats new connection
    def create_connection(self):
        print ("Initializing DB connection...")
        config = {'hosts': [(self.host, int(self.port))]}
        print (self.host)
        print (int(self.port))
        print ("Config: %s"% str(config))
        client = aerospike.client(config).connect()
        print ("Done. Initializing DB connection.")
        return client

    # For explicitly opening database connection
    def __enter__(self):
        self.dbconn = self.create_connection()
        return self.dbconn
    
    def __exit__(self):
        self.dbconn.close()
