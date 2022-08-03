import base64
import hashlib

def WebSocketDataEncoder(data, fin, opcode):
    payloadLength = len(data)
    #data = data.encode()
    sentData = (((2**7)*fin) + opcode).to_bytes(1, byteorder="big")
    if payloadLength <= 125:
        sentData = sentData + chr(payloadLength).encode()
    elif payloadLength <= 65536 and payloadLength > 125:
        #fill 16 bits
        sentData = sentData + chr(126).encode() + (payloadLength).to_bytes(2, byteorder="big")
    elif payloadLength > 65536:
        #fill 64 bits
        sentData = sentData + chr(127).encode() + (payloadLength).to_bytes(16, byteorder="big")
    sentData = sentData + data
    #print(sentData)
    return sentData

def WebSocketPayloadMask(data, pointer):
    mask = data[pointer: pointer+4]
    #print(mask)
    pointer = pointer + 4
    return mask, pointer

def WebSocketPayloadLength(data):
    pointer = 1
    payload_Length = data[1] - 128
    if payload_Length <= 125:
        pointer = 2
    elif payload_Length == 126:
        payload_Length = data[2:4]
        new = ""
        for x in payload_Length:
            new = new + str(x)
        payload_Length = int(new)
        pointer = 4
    elif payload_Length == 127:
        payload_Length = data[2:10]
        new = ""
        for x in payload_Length:
            new = new + str(x)
        payload_Length = int(new)
        pointer = 10
    else:
        payload_Length = None
    return payload_Length, pointer

def XORCipher(data, pointer, mask, payload_Length):
    decoded = ""
    data = data[pointer:(pointer+payload_Length)]
    for currentByte in range(len(data)):
        #print(currentByte)
        decoded = decoded + chr(data[currentByte] ^ mask[currentByte%4])
    return decoded

def WebSocketDataDecoder(data):
    #data = data.encode()
    temp = str(bin(data[0]))[2:]
    opcode = temp[4:]
    fin = temp[0]
    payload_Length, pointer = WebSocketPayloadLength(data)
    mask, pointer = WebSocketPayloadMask(data, pointer)
    decoded = XORCipher(data, pointer, mask, payload_Length)
    return decoded, fin, opcode

def VerifyWebSocketRequest(http_headers):
    #print(http_headers.Headers)
    try:
        sec_WebSocket_Key = http_headers.Headers['Sec-WebSocket-Key']
    except:
        sec_WebSocket_Key = None
    try:
        upgrade = http_headers.Headers['Upgrade']
    except:
        upgrade = None
    try:
        connection = http_headers.Headers['Connection']
    except:
        connection = None
    if sec_WebSocket_Key != None and upgrade != None and connection != None:
        webSocketRequest = True
    else:
        webSocketRequest = False

    #print(sec_WebSocket_Key, upgrade, connection)

    return webSocketRequest, sec_WebSocket_Key

def AcceptWebSocketRequest(conn, sec_WebSocket_Key, http_headers):
    softpath = http_headers.Url
    #keys = self.Module_Discovery.keys()
    #Check if softpath is "/" or in keys for controllers
    return_Key = base64.b64encode((hashlib.sha1((sec_WebSocket_Key[0] + "258EAFA5-E914-47DA-95CA-C5AB0DC85B11").encode()).digest())).decode()
    sentData = "HTTP/1.1 101 Switching Protocols\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Accept: "+return_Key+"\r\n\r\n"
    conn.send(sentData.encode())
