from src.utilities.Logger import Level, Logger


class IPAddr:
    """
    An IP address.
    """
    def __init__(self, addr = None):
        self.text = addr
        self.bytes = bytes(int(part, 10) for part in addr.split("."))
        if len(self.bytes) > 4:
            Logger.instance.log(Level.ERROR, f"IP addr {self.text} is longer than four bytes.")


    def __str__(self):
        return self.text

    def __eq__(self, other):
        if isinstance(other, IPAddr):
            return self.bytes == other.bytes
        return False