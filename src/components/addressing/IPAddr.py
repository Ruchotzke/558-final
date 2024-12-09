from src.utilities.Logger import Level, Logger


class IPAddr:
    """
    An IP address.
    """
    def __init__(self, addr = None):
        self.text = addr
        self.bytes = bytes(int(part, 10) for part in addr.split("."))
        if len(self.bytes) != 4:
            Logger.instance.log(Level.ERROR, f"IP addr {self.text} is not four bytes.")

    @staticmethod
    def from_bytes(b: bytes):
        if len(b) != 4:
            Logger.instance.log(Level.ERROR, f"IP addr {b} is not four bytes.")
            return None

        text = ".".join(str(byte) for byte in b)
        return IPAddr(text)

    def __str__(self):
        return self.text

    def __eq__(self, other):
        if isinstance(other, IPAddr):
            return self.bytes == other.bytes
        return False

    def apply_netmask(self, netmask: "IPAddr"):
        # AND the netmask and ip bytes
        network = bytes([a & b for a, b in zip(self.bytes, netmask.bytes)])
        return IPAddr.from_bytes(network)