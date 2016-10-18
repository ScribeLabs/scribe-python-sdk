# Abstracted interface to fork python process and communicate between parent and child
# This whole thing is a mess but using this module makes it less of a mess
# Useful when two different functions need to run in the main thread at the same time

import os
import fcntl
import cPickle as pickle

# Functions to encode and decode variable length integers to send message lengths over kernel pipes
def varint_enc(num):
    assert num >= 0
    if num == 0: return "\x00"
    result = ""
    while num != 0:
        lower_7 = num & 127
        num >>= 7
        if num != 0:
            result += chr(128 + lower_7)
        else:
            result += chr(lower_7)
    return result

def varint_dec_stream(stream, *args, **kwargs):
    result = 0
    num = ord(stream.read(1, *args, **kwargs))
    result += num & 127
    pow = 1
    while num & 128 != 0:
        num = ord(stream.read(1, *args, **kwargs))
        result += (num & 127) << (7 * pow)
        pow += 1
    return result

# Represents another process running at the same time
# The writeobj and readobj functions serialize python objects and send them over pipes
class Process:
    def __init__(self, rfd, wfd):
        self.rfd = rfd
        self.wfd = wfd
        self.flag = fcntl.fcntl(self.rfd, fcntl.F_GETFL)
        self.blocking = True

    def write(self, value):
        os.write(self.wfd, value)

    def close(self):
        os.close(self.rfd)
        os.close(self.wfd)

    def read(self, n, block=True):
        if self.blocking != block:
            if block:
                fcntl.fcntl(self.rfd, fcntl.F_SETFL, self.flag)
            else:
                fcntl.fcntl(self.rfd, fcntl.F_SETFL, self.flag | os.O_NONBLOCK)
            self.blocking = block
        return os.read(self.rfd, n)

    def writeobj(self, obj):
        pickled = pickle.dumps(obj, pickle.HIGHEST_PROTOCOL)
        length = varint_enc(len(pickled))
        self.write(length + pickled)

    def readobj(self, block=True):
        length = varint_dec_stream(self, block=block)
        pickled = self.read(length)
        return pickle.loads(pickled)

# For the child process, this will return an object representing the parent process
# For the parent process, this will return an object representing the child process
def fork():
    "fork() -> child, parent"
    rfd_p, wfd_c = os.pipe()
    rfd_c, wfd_p = os.pipe()

    child = Process(rfd_c, wfd_c)
    parent = Process(rfd_p, wfd_p)
    pid = os.fork()
    if pid == 0:
        return child, None
    return None, parent