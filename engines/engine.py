from engines import dataCollectionEngine, actionEngine


def mainEngine():
    """
    This function is our entire agent flow, it collects data and performs action
    """
    dataCollectionEngine()
    actionEngine()
    return "Successfull Task Completion"
    