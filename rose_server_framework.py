import httpheaders
import socket
import threading
import time
import asyncio

class HTTP_Server:
    '''
    A basic HTTP Server

    Fairly unremarkable and simply a placeholder for now

    Params:
    host: hostname to be used to access the server
    port: port number to be used
    backlog: backlog for the tcp connection
    '''

    def __init__(self, host: str, port: int, backlog: int):
        self.Host: str = host
        self.Port: int = port
        self.Backlog: int = backlog
        self.Server_Running: bool = False #Used to check if there has been a KeyboardInterrupt
        self.print_lock: threading.Lock = threading.Lock() #Unused threading lock
        self.thread_count_lock: threading.Lock = threading.Lock() #Previously used to cap the number of threads that can be spawned
        self.request_manager_lock: threading.Lock = threading.Lock() #Unused threading lock


    async def ConnectionManagerAsync(self, conn: socket.socket, addr) -> None:
        '''
        This method receives the socket object and the address of the client which it then uses to get the data 
        and pass the HTTP request into the HTTP request manager method with the http_headers seperated
        '''
        loop = asyncio.get_event_loop()
        try:
            data = (await loop.sock_recv(conn, 4096)).decode('utf8', 'ignore')
            http_headers, http_data = data.split('\r\n\r\n')
            await self.HTTPRequestManagerAsync(conn, addr, httpheaders.HTTP_Headers(http_headers), http_data)
        except ValueError:
            sentData = "".encode()
            await loop.sock_sendall(conn, sentData)
            conn.close()
        except Exception as e:
            print(e)
            conn.close()

    async def run_server(self):
        '''
        Main method to run the server. When invoked the TCP socket is created and begins to listen for connections

        There is also an event loop created and the connection manager method is invoked for each connection
        '''
        self.Server_Running = True
        print('Server starting...')
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.Host, self.Port))
        server.listen(self.Backlog)
        server.setblocking(False)
        print('Server listening on '+self.Host+":"+str(self.Port))
        loop = asyncio.get_event_loop()

        try:
            while self.Server_Running:
                sock, addr = await loop.sock_accept(server)
                loop.create_task(self.ConnectionManagerAsync(sock, addr))
        except:
            self.Server_Running = False
    
        print('Server turned off.')

