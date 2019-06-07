from socket import *
import _thread
import select

lock = _thread.allocate_lock()

class CServerManager(object):
    def __init__(self):
        self.m_ServSock = None
        self.m_ClientList = []
        self.m_ServFlag = False
        return None
    
    def InitServer(self, nPort):
        try:
            self.m_ServSock = socket(AF_INET, SOCK_STREAM)
            self.m_ServSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            self.m_ServSock.bind(('', nPort))
            
            self.m_ServSock.listen(5)
            #self.m_ServSock.setblocking(0)
            self.m_ServFlag = True
            
            print ("InitServer() - Success...")
        except:
            print ("InitServer() - Failed...")
            return False
        return True
    
    def SelectLoop(self):
        readset = [self.m_ServSock]
        writeset = []
        errorset = []
        while (self.m_ServFlag):
            rset, wset, eset = select.select(readset, writeset, errorset, 0)
            for sock in rset:
                if(sock == self.m_ServSock):
                    clntSock, clntaddr = self.m_ServSock.accept()
                    print ("Connected by", clntaddr)
                    self.m_ClientList.append(clntSock)
                    readset.append(clntSock)
                else:
                    try:
                        pData = sock.recv(32)
                    except:
                        readset.remove(sock)
                        self.m_ClientList.remove(sock)
                        print ("Disconnected by", sock.getpeername())
                        sock.close()
                        for clnt in self.m_ClientList:
                            clnt.send("2")
                    if (len(pData) == 0):
                        readset.remove(sock)
                        self.m_ClientList.remove(sock)
                        print ("Disconnected by", sock.getpeername())
                        sock.close()
                        break
                    for clnt in self.m_ClientList:
                        try:
                            clnt.send(pData)
                        except:
                            print ("Send Failed...")
        self.m_ServSock.close()
        print ("Close Select Loop...")
        return None
    
    def StartSelectLoop(self):
        thread.start_new_thread(self.SelectLoop, ())
        return None
    
    def StopServer(self):
        self.m_ServFlag = False
        return None
    
    def GetClientCount(self):
        return len(self.m_ClientList)

class CClientManager(object):
    def __init__(self):
        self.m_Sock = None
        return None
    
    def ConnectToServer(self, szHost, nPort):
        self.m_Sock = socket(AF_INET, SOCK_STREAM)
        
        try:
            self.m_Sock.connect((szHost, nPort))
        except:
            print ("Connect Refused...")
            return False
        print ("Connect Success...")
        return True
    
    def Receive(self, nSize):
        try:
            pData = self.m_Sock.recv(nSize)
            return pData
        except:
            print ("Receive Failed...")
            return False
    
    def Send(self, pData):
        try:
            self.m_Sock.send(pData)
        except:
            print ("Send Failed...")
            return False
        return True
    
    def Close(self):
        self.m_Sock.close()
        return None
    
class CMultiPlayManager(CServerManager, CClientManager):
    def __init__(self):
        CServerManager.__init__(self)
        CClientManager.__init__(self)
        return None
    
    def SendStonPos(self, CursorX, CursorY, Type):
        pData = "1," + str(CursorX) + "," + str(CursorY) + "," + str(Type)
        self.Send(pData)
        return None
    
