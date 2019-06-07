import pygame
from pygame.locals import *
import os
import random

class CSound(object):
    def __init__(self, szFileName):
        self.m_Sound = pygame.mixer.Sound(szFileName)
    
    def Play(self):
        self.m_Sound.play()
    
    def Stop(self):
        self.m_Sound.stop()

class CBgmManager(object):
    def __init__(self):
        self.m_PlayIndex = 0
        self.m_BgmList = []
    
    def AppendBgm(self, szFileName):
        self.m_BgmList.append(CSound(szFileName))
    
    def PlayRandomBgm(self):
        if (len(self.m_BgmList) == 0):
            return None
        elif (len(self.m_BgmList) == 1):
            self.m_BgmList[0].Play()
        else:
            index = random.randint(0, len(self.m_BgmList)-1)
            self.m_BgmList[index].Play()
            
    def PlayNextBgm(self):
        if (len(self.m_BgmList) == 0):
            return None
        
        self.m_BgmList[self.m_PlayIndex].Stop()
        self.m_PlayIndex+=1
        if ( self.m_PlayIndex < len(self.m_BgmList) ):
            self.m_BgmList[self.m_PlayIndex].Play()
        else:
            self.m_PlayIndex = 0
            self.m_BgmList[self.m_PlayIndex].Play()
    
    def AppendBgmFromDir(self, szDirName="."):
        flist = os.listdir(szDirName)
        for f in flist:
            next = os.path.join(szDirName, f)
            if (os.path.isdir(next)):
                self.LoadBgmList(next)
                break
            else:
                ext = os.path.splitext(next)[-1]
                if (ext == '.ogg') or (ext == '.wav'):
                    self.m_BgmList.append(CSound(next))
                    print ("Load Bgm -", next)
        
