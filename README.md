# in-memory-elf

Execute ELF binary filelessly

- Create anonymous fd
- Open socket
- Read ELF binary from socket and write into fd
- execve fd
