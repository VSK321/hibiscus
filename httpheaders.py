
class HTTP_Headers:

    def __init__(self, headers):
        headers = headers.split('\r\n')
        self.HTTP_Type = headers[0].split(" ")[0]
        self.Url = headers[0].split(" ")[1]
        self.HTTP_Level = headers[0].split(" ")[2]
        self.Headers = {}
        for header in headers[1:]:
            self.Headers[header.split(': ')[0]] = header.split(': ')[1:]

def HTTP_Headers_Constructor(headers):
    actualHeader = ""
    for val in headers:
        actualHeader = actualHeader + val + ': ' + headers[val] + '\r\n'
    actualHeader = actualHeader + '\r\n'
    return actualHeader

def HTTP_Headers_Uvicorn_Constructor(headers) -> list[tuple[str, str]]:
    setOfHeaders: list[tuple[str, str]] = []
    for val in headers:
        setOfHeaders.append([val.encode(), headers[val].encode()])
    return setOfHeaders