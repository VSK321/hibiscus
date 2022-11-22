import httpheaders
import socket
import threading
import time
import asyncio

class HTTP_Server:

    def __init__(self, host: str, port: int, backlog: int):
        self.Host: str = host
        self.Port: int = port
        self.Backlog: int = backlog
        self.Server_Running: bool = False
        self.print_lock: threading.Lock = threading.Lock()
        self.thread_count_lock: threading.Lock = threading.Lock()
        self.request_manager_lock: threading.Lock = threading.Lock()


    async def ConnectionManagerAsync(self, conn: socket.socket, addr) -> None:
        loop = asyncio.get_event_loop()
        data = (await loop.sock_recv(conn, 4096)).decode('utf8', 'ignore')
        try:
            http_headers, http_data = data.split('\r\n\r\n')
            await self.HTTPRequestManagerAsync(conn, addr, httpheaders.HTTP_Headers(http_headers), http_data)
        except ValueError:
            sentData = "".encode()
            await loop.sock_sendall(conn, sentData.encode('utf8'))
            conn.close()

    def AcceptLockThread(self) -> None:
        while self.Server_Running:
            time.sleep(5)
            if self.Server_Running:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP) as s:
                    s.connect((self.Host, self.Port))
            

    async def run_server(self):
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

