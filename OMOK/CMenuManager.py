import pygame
from pygame.locals import *

class CMenu(object):
    def __init__(self, szFontFileName, nFontSize, szText, Pos, OnColor, OffColor, hScreen):
        self.m_hFont = pygame.font.Font(szFontFileName, nFontSize)
        
        self.m_MenuText = szText
        self.m_MenuOn = self.m_hFont.render(szText, True, OnColor)
        self.m_MenuOff = self.m_hFont.render(szText, True, OffColor)
        
        self.m_Pos = Pos
        
        self.m_Width = self.m_MenuOn.get_size()[0]
        self.m_Height = self.m_MenuOn.get_size()[1]
        
        self.m_hScreen = hScreen
        return None
    
    def GetRect(self):
        return (self.m_Pos[0], self.m_Pos[1], self.m_Width, self.m_Height)
    
    def DrawMenu(self, Type):
        if Type:
            self.m_hScreen.blit(self.m_MenuOn, self.m_Pos)
        else:
            self.m_hScreen.blit(self.m_MenuOff, self.m_Pos)
        return None
        
    def InnerCheck(self, CursorPos):
        if (CursorPos[0] > self.m_Pos[0]) and (CursorPos[0] < (self.m_Pos[0]+self.m_Width)) and (CursorPos[1] > self.m_Pos[1]) and (CursorPos[1] < (self.m_Pos[1]+self.m_Height)):
            return True
        return False
    
    def DrawMenuWithPos(self, CursorPos):
        self.DrawMenu(self.InnerCheck(CursorPos))
        return None
    
    def GetMenuText(self):
        return self.m_MenuText

class CMenuManager(object):
    def __init__(self, hScreen):
        self.m_MenuList = []
        self.m_hScreen = hScreen
        return None
    
    def AppendMenu(self, szFontFileName, nFontSize, szText, Pos, OnColor, OffColor):
        self.m_MenuList.append(CMenu(szFontFileName, nFontSize, szText, Pos, OnColor, OffColor, self.m_hScreen))
        return None
    
    def GetActivationMenu(self, CursorPos):
        for i in range(len(self.m_MenuList)):
            if (self.m_MenuList[i].InnerCheck(CursorPos) == True):
                return i
        return -1
    
    def GetMenuState(self, CursorPos):
        MenuState = []
        for Menu in self.m_MenuList:
            MenuState.append(Menu.InnerCheck(CursorPos))
        return MenuState
    
    def CountMenu(self):
        return len(self.m_MenuList)
    
    def DrawMenuList(self, CursorPos):
        for Menu in self.m_MenuList:
            Menu.DrawMenuWithPos(CursorPos)
    
    def GetRect(self, Index):
        return self.m_MenuList[Index].GetRect()
        return None