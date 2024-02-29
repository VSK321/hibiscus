import httpheaders
import socket
import threading
import time
import asyncio
from queue import Queue
import queue
import sys

class HTTP_Server:
    '''
    A basic HTTP Server

    Fairly unremarkable and simply a placeholder for now

    Params:
    host: hostname to be used to access the server
    port: port number to be used
    backlog: backlog for the tcp connection
    threads: number of concurrent threads to run
    '''

    def __init__(self, host, port, backlog, threads):
        self.Host = host
        self.Port = port
        self.Backlog = backlog
        self.Create_Threads = threads
        self.q = Queue()
        self.Server_Running = False
        self.print_lock = threading.Lock()
        self.thread_count_lock = threading.Lock()
        self.thread_count = 0


    def Connection_Manager(self, conn, addr):
        data = conn.recv(4096).decode('utf-8', 'ignore')
        try:
            http_headers, http_data = data.split('\r\n\r\n')
            asyncio.run(self.HTTPRequestManagerAsync(conn, addr, httpheaders.HTTP_Headers(http_headers), http_data))
        except ValueError:
            sentData = "".encode()
            conn.send(sentData)
            conn.close()

    def AcceptLockThread(self):
        '''
        Windows requires this to run in the background to ensure that KeyboardInterrupts are caught within 5 seconds
        '''
        while self.Server_Running:
            time.sleep(5)
            if self.Server_Running:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP) as s:
                    s.connect((self.Host, self.Port))

    def Thread_Manager(self):
        while self.q.empty() != True:
            try:
                conn, addr = self.q.get(block=False)
                self.Connection_Manager(conn, addr)
                self.q.task_done()
            except queue.Empty:
                pass
            #except Exception as e:
            #    with self.print_lock:
            #        print(e)
        with self.thread_count_lock:
            #print(self.thread_count)
            self.thread_count = self.thread_count - 1

    def Start_Server(self):
        self.Server_Running = True
        if sys.platform == "win32":
            threading.Thread(target = self.AcceptLockThread, daemon = True).start()
        print('Server starting...')
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP) as sock:
            sock.bind((self.Host, self.Port))
            sock.listen(self.Backlog)
            print('Server listening on '+self.Host+":"+str(self.Port))
            try:
                while self.Server_Running:
                    conn, addr = sock.accept()
                    self.q.put((conn, addr))
                    if self.thread_count < self.Create_Threads and self.q.empty() == False:
                        threading.Thread(target = self.Thread_Manager, daemon = True).start()
                        with self.thread_count_lock:
                            self.thread_count = self.thread_count + 1
                    else:
                        pass
            except KeyboardInterrupt:
                self.Server_Running = False
        print('Server turned off.')