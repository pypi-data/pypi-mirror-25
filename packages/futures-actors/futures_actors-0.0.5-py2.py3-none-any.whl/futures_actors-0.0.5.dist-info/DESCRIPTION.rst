Allows a class to be created in a separate thread/process. Unlike the simple functions that can be run using the builtin concurrent.futures module, the class instance can   maintain its own private state. Messages (in the form of arbitrary pickleable objects) can be send to this process allowing communication. The actor responds in the form of a Future object.


