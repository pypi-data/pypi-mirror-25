# Internal CAN database.

class Database(object):
    """Internal CAN database file.

    """

    def __init__(self,
                 messages,
                 nodes,
                 buses,
                 attributes,
                 default_attrs,
                 version):
        self.messages = messages
        self.nodes = nodes
        self.buses = buses
        self.attributes = attributes
        self.default_attrs = default_attrs
        self.version = version
