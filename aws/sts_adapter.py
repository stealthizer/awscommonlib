class StsAdapter:

    def __init__(self, connection, region):
        self.__connection = connection
        self.__resource = 'sts'
        self.__region = region

    def __get_connection_sts(self):
        return self.__connection.get_client(self.__resource, self.__profile, self.__region)

    def get_account_id(self):
        return self.__connection.get_caller_identity()['Account']
