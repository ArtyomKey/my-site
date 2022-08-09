# -*- coding: utf-8 -*-
"""
Created on Sun Jul 24 18:38:07 2022

@author: 4rKu5P3rs0N
"""
import time
import sys
import http.server
import socketserver
import threading

PORT = 2526
Server = http.server.SimpleHTTPRequestHandler

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def send_error(self, code, message=None):
        if('/kill' in self.requestline):
            global https_server
            print('Программа завершена')
            
            assassin = threading.Thread(target=https_server.shutdown)
            assassin.daemon = True
            assassin.start()
            https_server.server_close()
            print(time.asctime(), 'Server DOWN')
            sys.exit(0)
        if code == 404:
            http.server.SimpleHTTPRequestHandler.send_error(self, code, message)
    def do_POST(self):
        # read the content-length header
        flag = 0
        i = 1
        while(flag == 0):
            try:
                self.newFile = open("file{}.json".format(i), "w+", encoding="utf-8")
                flag = 1
            except FileExistsError:
                i += 1
        content_length = int(self.headers.get("Content-Length"))
        # read that many bytes from the body of the request
        body = self.rfile.read(content_length)
        bodyJS = body.decode("utf-8")
        self.send_response(200)
        self.end_headers()
        # echo the body in the response
        self.newFile.write(bodyJS)
        self.newFile.close()
        return
def start_https_server(listening_port):
    global https_server 
    https_server = http.server.HTTPServer(("", listening_port), MyHandler)
    try:
        https_server.serve_forever()
    except KeyboardInterrupt:
        print("\n[!] Keyboard interrupt received, exiting...")
        https_server.server_close()
        sys.exit(0)
if __name__ == '__main__':
    listening_port = PORT
    print("[+] Staring server...")
    start_https_server(listening_port)
    
    
    
    
    
    
    
