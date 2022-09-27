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
import json


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
        elif('/give' in self.requestline):
            print(self.requestline)
            file = open("file1.json", "r+", encoding="utf-8")
            JSONcontent = file.read()
            print(JSONcontent)
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            if('eN' in self.requestline):
                number = self.requestline[self.requestline.find('N') + 1:self.requestline.find(' HTTP')]
                print('number: {}'.format(number))
                toFind = '"Номер": {}'.format(number)
                print(toFind)
                place = JSONcontent.find(toFind)
                print(place)
                if(place != -1):
                    place1 = JSONcontent.find('"Данные":', place) + 9
                    place2 = JSONcontent.find('}]}', place1) + 3
                    neededSet = JSONcontent[place1:place2]
                    self.send_header("Content-Length", str(len(neededSet)))
                    self.end_headers()
                    self.wfile.write(neededSet.encode('cp1251'))
                else:
                    http.server.SimpleHTTPRequestHandler.send_error(self, code, message)
            else:
                self.send_header("Content-Length", str(len(JSONcontent)))
                self.end_headers()
                self.wfile.write(JSONcontent.encode('cp1251'))
            file.close()
        elif('/deleteset' in self.requestline):
            file = open("file1.json", "r+", encoding="utf-8")
            JSONcontent = file.read()
            file.close()
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            number = self.requestline[self.requestline.find('N') + 1:self.requestline.find(' HTTP')]
            toFind = '"Номер": {}'.format(number)
            print(toFind)
            place = JSONcontent.find(toFind)
            print(place)
            if(place != -1):
                file = open("file1.json", "w+", encoding="utf-8")
                place1 = place - 22
                print(place1)
                place2 = JSONcontent.find('}]}', place1) + 5
                print(place2)
                if(place2 < len(JSONcontent)):
                    neededSet = JSONcontent[place1:place2]
                    print(neededSet)
                    self.send_header("Content-Length", str(len(neededSet)))
                    self.end_headers()
                    JSONcontent = JSONcontent.replace(neededSet, '')
                elif(place1 != 1):
                    place2 -= 2
                    place1 -= 2
                    neededSet = JSONcontent[place1:place2]
                    self.send_header("Content-Length", str(len(neededSet)))
                    self.end_headers()
                    JSONcontent = JSONcontent.replace(neededSet, '')
                else:
                    JSONcontent = '['
                if(JSONcontent == '['):
                    file.write('')
                else:
                    file.write(JSONcontent)
                file.close()
        elif(code == 404):
            http.server.SimpleHTTPRequestHandler.send_error(self, code, message)
    def do_POST(self):
        if('/newset' in self.requestline):
            i = 1
            newFile = open("file{}.json".format(i), "r+", encoding="utf-8")
            JSfileCont = json.loads(newFile.read())
            newFile.close()
            newFile = open("file{}.json".format(i), "w+", encoding="utf-8")
            content_length = int(self.headers.get("Content-Length"))
            # read that many bytes from the body of the request
            body = self.rfile.read(content_length)
            bodyJS = body.decode("utf-8")
            JSON = json.loads(bodyJS)
            numberFile = open('number.txt', 'r+', encoding="utf-8")
            number = int(numberFile.read())+1
            numberFile.close()
            numberFile = open('number.txt', 'w+', encoding="utf-8")
            numberFile.write(str(number))
            numberFile.close()
            JSON['Номер'] = number
            JSfileCont.append(JSON)
            print(JSfileCont)
            strJSON = json.dumps(JSfileCont, ensure_ascii=False)
            self.send_response(200)
            self.end_headers()
            newFile.write(strJSON)
            newFile.close()
            return
        elif('/changeset' in self.requestline):
            i = 1
            print(self.requestline)
            newFile = open("file{}.json".format(i), "r+", encoding="utf-8")
            JSfileCont = json.loads(newFile.read()) #объект json файла
            newFile.close()
            newFile = open("file{}.json".format(i), "w+", encoding="utf-8")
            content_length = int(self.headers.get("Content-Length"))
            # read that many bytes from the body of the request
            body = self.rfile.read(content_length)
            bodyJS = body.decode("utf-8") #объект который надо поменять
            JSON = json.loads(bodyJS) #он же в json
            number = int(self.requestline[self.requestline.find('N') + 1:self.requestline.find(' HTTP')])
            for j in range(len(JSfileCont)):
                if(JSfileCont[j]['Номер'] == number):
                    JSfileCont[j]['Данные'] == JSON['Данные']
                    strJSON = json.dumps(JSfileCont, ensure_ascii=False)
                    self.send_response(200)
                    self.end_headers()
                    newFile.write(strJSON)
                    newFile.close()
                    return
            
        # echo the body in the response
        # bodyJSON1 = json.loads(bodyJS)
        # bodyJSON2 = json.loads(self.newFile.read())
        # temp = []
        # for i in range(len(bodyJSON2)):
        #     temp.append((bodyJSON2[i]))
        # temp.append(bodyJSON1)
        # print(bodyJS)
        # self.newFile.close()
        # i = 1
        # flag = 0
        # while(flag == 0):
        #     try:
        #         self.newFile = open("file{}.json".format(i), "w+", encoding="utf-8")
        #         flag = 1
        #     except FileExistsError:
        #         i += 1
        # json_string = json.dumps(temp)
        
        
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
    print("[+] Starting server...")
    start_https_server(listening_port)
    
    
    
    
    
    
    
