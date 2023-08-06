def store(eventbus):
    get.cache = eventbus

def get():
    if not get.cache:
        raise Exception("You must call store() before calling get()")
    return get.cache
get.cache = None
