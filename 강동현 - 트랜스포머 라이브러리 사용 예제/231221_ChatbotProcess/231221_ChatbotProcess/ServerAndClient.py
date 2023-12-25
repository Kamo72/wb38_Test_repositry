# -*- coding: cp949 -*-
import socket
import threading

class Server ():
    # callback => (Socket s, string str) => {}
    def __init__(self, ip, port, callback) :
        # ���� ����
        self.host = ip
        self.port = port
        # ���� ����
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #Ŭ���̾�Ʈ �����
        self.readThreads = []
        self.clients = []
        self.callback = callback
        
    def Deploy(self) :
        # �ּҿ� ��Ʈ�� ���Ͽ� ���ε�
        self.server_socket.bind((self.host, self.port))

        # ���� ���
        self.server_socket.listen()

        print(f"������ {self.host}:{self.port}���� ��� ���Դϴ�.")
        
        self.acceptThread = threading.Thread(target = self.AcceptThread)
        self.acceptThread.start()
        
    def Send(self, msg) :
        self.clients[0].send((msg + "\n").encode('utf-8'))
    
    def AcceptThread(self) :
        
        print("���� - AcceptThread ����")
        while True :
            # Ŭ���̾�Ʈ ���� ����

            print("���� - ���� �����...")
            client_socket, client_address = self.server_socket.accept()
            print(f"{client_address}�� ����Ǿ����ϴ�.")
            
            self.clients.append(client_socket)
            
            thread = threading.Thread(target = self.ReadThread, args=[client_socket])
            self.readThreads.append(thread)
            thread.start()

    def ReadThread(self, client_socket) :
        while True :
            # Ŭ���̾�Ʈ�κ��� ������ �ޱ�
            data = client_socket.recv(1024).decode('utf-8')
            #print(f"������ ������ ������: {data}")
            spDatas = data.split('\n')
            for spData in spDatas :
                self.callback(client_socket, spData)
            
    def __del__ (self) :
        # ���� ����
        self.client_socket.close()
        self.server_socket.close()


class Client ():
    # callback => (string str) => {}
    def __init__(self, ip, port, callback) :
        # ���� ����
        self.host = ip
        self.port = port
        # ���� ����
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #���� �����
        self.callback = callback
        
    def Connect(self) :
        # ������ ����
        self.client_socket.connect((self.host, self.port))
        print(f"������ ����Ǿ����ϴ�.")

        self.readThread = threading.Thread(target = self.ReadThread)
        self.readThread.start()
        
    def Send(self, msg) :
        self.client_socket.send((msg + "\n").encode('utf-8'))
    
    def ReadThread(self) :
        while True :
            # Ŭ���̾�Ʈ�κ��� ������ �ޱ�
            data = self.client_socket.recv(1024).decode('utf-8')
            # print(f"Ŭ���̾�Ʈ�� ������ ������: {data}")
            spDatas = data.split('\n')
            for spData in spDatas :
                self.callback(spData)
            
    def __del__ (self) :
        # ���� ����
        self.client_socket.close()


