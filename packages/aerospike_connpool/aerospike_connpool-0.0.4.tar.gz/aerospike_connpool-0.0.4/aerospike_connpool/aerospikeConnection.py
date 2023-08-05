import aerospike 
from aerospike_connpool.aerospikeConnector import AerospikeConnector

class AerospikeConnection():
    connection = None

    def get_connection(self, host, port):
        if not self.connection:
            ac = AerospikeConnector(host, port)
            self.connection = ac.__enter__()
        return self.connection

    def execute_query(self, host, port, namespace, setname, key):
        print ("Inside Aero Connection")
        print ("%s %s %s %s %s" % (host, port, namespace, setname, key))
        #connection = get_connection(host, port)
        try:
            connection = self.get_connection(host, port)
            print ("Query submitting...")
            print (connection)
            (key, metadata, record) = connection.get((namespace,setname,key))
            if metadata is not None:
                print("Record: %s" % (record))
                return str(record)
        except Exception as error:
            return error
