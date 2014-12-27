#! /usr/bin/python
import subprocess
import shlex
import string,cgi,time
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from merge import merger
from ximu import xgraph
from graph import graph
import sys
import socket
from appconf import ximu_host

from appconf import app_path, os_div, data_path, ss_path, ws_html_file

class MyHandler(BaseHTTPRequestHandler):
        
    def do_GET(self):
        try:
            if self.path.endswith(".css"):
                file_prefix = self.path[1:-4]
                print(file_prefix)
                gr = graph(data_path, ss_path, file_prefix)
                gr.saveAllData()
                xgr = xgraph(data_path, ss_path, file_prefix)
                xgr.saveAll()
                f = open(ws_html_file)
                self.wfile.write(f.read())
                f.close()
                return

            if self.path.endswith(".xml"):
                file_prefix = self.path[1:-4]
                print(file_prefix)
                m = merger(data_path, ss_path, file_prefix)
                m.merge()
                f = open(ws_html_file)
                self.wfile.write(f.read())
                f.close()
                return
                
            if self.path.endswith(".html"):
                self.send_response(200)
                self.send_header('Content-type',	'text/html')
                self.end_headers()
                cmd = self.path[1:-5]
                
                sc = TensorSocket()
                sc.socket_send(cmd)
                
                es = EncoderSocket()
                es.socket_send(cmd)
                
                ximu = XimuSocket()
                ximu.socket_send(cmd)

                f = open(ws_html_file)
                self.wfile.write(f.read())
                f.close()
                return
               
            return
                
        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)
     
class XimuSocket():
    def socket_send(self, msg):
	HOST, PORT = ximu_host, 8001
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((HOST,PORT))
	sock.send(msg)
	sock.close()

class TensorSocket():
    def socket_send(self, msg):
        cmd = 'python test_client.py %s'%msg
        args = shlex.split(cmd)
        p=subprocess.Popen(args,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        result = p.communicate()[0]
        print result  

class EncoderSocket():
    def socket_send(self, msg):
        cmd = 'python encoder_client.py %s'%msg
        args = shlex.split(cmd)
        p=subprocess.Popen(args,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        result = p.communicate()[0]
        print result  


def main():
    try:
        server = HTTPServer(('', 9001), MyHandler)
        print 'started httpserver...'
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()

if __name__ == '__main__':
    main()

