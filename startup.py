from rose_mvc_framework import *
import socket

instance = MVC(socket.gethostbyname(socket.gethostname()), 80, 50)
#instance = MVC("127.0.0.1", 80, 50)
instance.Build()
#instance.Start_Server()
try:
    asyncio.run(instance.run_server())
except:
    file = open("./models/EMCPG.txt", 'wb')
    file.write(pickle.dumps(AppLoc.EMCPG))
    file.close()
