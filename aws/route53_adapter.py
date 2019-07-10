class Route53Adapter:

    def __init__(self, connection, region):
        self.__connection = connection
        self.__resource = 'route53'
        self.__region = region

    def __get_client_route_53(self):
        return self.__connection.get_client(self.__resource, self.__profile, self.__region)

    def get_zone_id(self, domain):
        return self.__connection.list_hosted_zones_by_name(DNSName=domain)['HostedZones'][0]['Id']
