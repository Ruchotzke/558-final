
class RouteTable:

    tables = []
    """
    A set of all tables in the simulation.
    """

    """
    A simple route table implementation
    """
    def __init__(self):
        self.table = {}
        RouteTable.tables.append(self)

    def __del__(self):
        RouteTable.tables.remove(self)

class ArpTable:
    """
    A simple ARP table implementation
    """