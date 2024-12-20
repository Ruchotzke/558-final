from src.utilities.Logger import Logger, Level


class EthernetAddr:
    """
    An Ethernet address.
    """
    def __init__(self, addr = None):
        if addr is None:
            self.text = "FF:FF:FF:FF:FF:FF"
            self.bytes = bytes(int(part, 16) for part in self.text.split(":"))
        else:
            self.text = addr
            self.bytes = bytes(int(part, 16) for part in addr.split(":"))
            if len(self.bytes) > 6:
                Logger.instance.log(Level.ERROR, f"Ethernet addr {self.text} is longer than six bytes.")


    def __str__(self):
        return self.text

    def is_broadcast(self):
        return self.bytes == b'\xff\xff\xff\xff\xff\xff'

    def filter(self, addr):
        return addr.is_broadcast() or addr.bytes == self.bytes