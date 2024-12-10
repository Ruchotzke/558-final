import random


"""
NETWORK STACK
"""



def HW_QUEUE_DELAY():
    """
    The delay the HW queues experience (processing time)
    :return:
    """
    # val = random.normalvariate(0.1, 0.01)
    val = 0
    return val if val >= 0 else 0

def IP_QUEUE_DELAY():
    """
    The delay the IP queues experience (processing time)
    :return:
    """
    # val = random.normalvariate(0.05, 0.01)
    val = 0
    return val if val >= 0 else 0

def APP_QUEUE_DELAY():
    """
    The delay a packet experiences between an app and IP layer.
    :return:
    """
    # val = random.normalvariate(0.07, 0.01)
    val = 0
    return val if val >= 0 else 0

def ROUND_ROBIN_DELAY():
    """
    The delay between round robin steps.
    :return:
    """
    return 0.01
