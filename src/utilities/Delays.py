import random


"""
NETWORK STACK
"""



def HW_QUEUE_DELAY():
    """
    The delay the HW queues experience (processing time)
    :return:
    """
    return random.normalvariate(0.03, 0.01)

def IP_QUEUE_DELAY():
    """
    The delay the IP queues experience (processing time)
    :return:
    """
    return random.normalvariate(0.05, 0.02)

def APP_QUEUE_DELAY():
    """
    The delay a packet experiences between an app and IP layer.
    :return:
    """
    return random.normalvariate(0.07, 0.05)

