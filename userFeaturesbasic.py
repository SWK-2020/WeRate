import pygame

class button:
    def __init__(self,screen,image,coord): #coord is the top left point (2D)
        self.screen = screen
        self.imageD = image #this is a image
        self.width = image.get_width()
        self.height = image.get_height()
        
        self.coord = coord
    def ison(self,camera):
        if camera[0] > self.coord[0] and camera[0] <self.coord[0] + self.width and camera[1] > self.coord[1] and camera[1] <self.coord[1] + self.height:
            return True
        else:
            return False
    def blip(self):
        self.screen.blit(self.imageD,self.coord)
        
class inputbox:
    def __init__(self,screen,coords,height): #min height is 6
        self.screen = screen
        self.coords = coords
        self.dwidth = height*25 #default width
        self.pwidth = 0 #length of text
        self.height = height
        
        
        self.text = ''
        self.fontsize = int(height - 6)
        if height < 6:
            raise Exception('screen too small')
    def clear(self):
        self.text = ''
    def checknum(self):
        try:
            float(self.text)
        except:
            return False
        else:
            return True
    def CLEARtext(self):
        self.text = ''
    def GETtext(self):
        return self.text
    def blip(self):
        font = pygame.font.SysFont('timesnewroman', self.fontsize)
        text = font.render(self.text,True,(0,0,0))
        self.pwidth = text.get_width()
        if self.pwidth >self.dwidth: #so text fits in box
            pygame.draw.rect(self.screen,(255,255,255),(self.coords[0],self.coords[1],self.pwidth+6,self.height+6)) #+6 to take in account border
            pygame.draw.rect(self.screen,(0,0,0),(self.coords[0],self.coords[1],self.pwidth+6,self.height+6),3)
        else:
            pygame.draw.rect(self.screen,(255,255,255),(self.coords[0],self.coords[1],self.dwidth+6,self.height+6))
            pygame.draw.rect(self.screen,(0,0,0),(self.coords[0],self.coords[1],self.dwidth+6,self.height+6),3)
        self.screen.blit(text,(self.coords[0]+3,self.coords[1]+ 3))
    def ison(self,mousecoord):
        if self.pwidth >self.dwidth: #check which width to use
            width = self.pwidth
        else:
            width = self.dwidth 
        if mousecoord[0] > self.coords[0] and mousecoord[0] <self.coords[0] + width and mousecoord[1] > self.coords[1] and mousecoord[1] <self.coords[1] + self.height:
            return True
        else:
            return False
    def takeinput(self,window):
        Running = True
        while Running == True:
            pygame.display.update()
            self.blip()
            mouse = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT: #when exit pressed close window
                    Running = False
                    pygame.display.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN: #press off
                    if self.ison(mouse) == False:
                        Running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1]
                    elif event.key == pygame.K_RETURN: #return key
                        Running = False
                    else:
                        self.text += event.unicode
        output = self.text
        self.text = ''
        return output
        
class namebox(inputbox):
    def __init__(self,screen):
        super().__init__(screen,(screen.get_width()/8,screen.get_height()/6),35)
        
class Vslider: #very similar code to horizontal slider
    def __init__(self,screen,coords,width,height,Lowest,Highest,initial): #main difference is no writing
        self.screen = screen
        self.coords = coords
        
        self.width = width
        self.height = height
        
        
        self.lowest = Lowest #range of the slider
        self.highest = Highest
        
        self.pos = coords[1]+(initial-Lowest)*width/Highest
        
        self.Running = False
    def reset(self):
        self.pos = self.coords[1]
    def blip(self):
        pygame.draw.rect(self.screen,(150,150,150),(self.coords[0],self.coords[1]-self.height/(2*(self.height + self.width)),self.width,self.height+self.height/(self.height + self.width)))
        pygame.draw.line(self.screen,(0,0,0),[self.coords[0] + self.width/2,self.coords[1]],(self.coords[0]+self.width/2,self.coords[1]+self.height),4)
        pygame.draw.circle(self.screen,(0,0,0),(self.coords[0] + self.width/2,self.pos),self.width/2)# 2 is to centre the cirlce
    def ison(self,coord):
        if coord[0] < self.coords[0] + self.width and coord[0] > self.coords[0] and coord[1] > self.coords[1] and coord[1] < self.coords[1] + self.height:
            return True
        else:
            return False
        
    def getvalue(self):
        difference = self.pos - self.coords[1]
        ratio = difference/self.height
        actualdif = self.highest - self.lowest
        moremin = ratio*actualdif
        return round(self.lowest + moremin)
    def takeinput(self,window):
        self.Running = True
        while self.Running == True:
            self.inputslice(window)
    def inputslice(self,window):
        pygame.display.update()
        window.blip()
        self.blip()
        mouse = pygame.mouse.get_pos()
        if mouse[1] < self.coords[1]:
            self.pos = self.coords[1]
        elif mouse[1] > self.coords[1] + self.height:
            self.pos = self.coords[1] + self.height
        else:
            self.pos = mouse[1]
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.Running = False
        
class widgetslider(Vslider):
    def __init__(self,screen,coord,width,height):
        super().__init__(screen,[coord[0],coord[1] + width/20] ,width/10,height-width/10,0,1,0)
    def getvalue(self): #same function but returns unrounded number
        difference = self.pos - self.coords[1]
        ratio = difference/self.height
        actualdif = self.highest - self.lowest
        moremin = ratio*actualdif
        return self.lowest + moremin
    def takeinput(self,window,widget): #updates attribute as the user scrolls
        self.Running = True
        while self.Running == True:
            self.inputslice(window)
            widget.blipupdate()
            widget.scroll = self.getvalue()

    
class scrollerbox:
    def __init__(self,screen,cliprect,width,height,pixelsfromtop,strings): #dimensions of the actual box, followed by how far down the screen the box can actually be.
        self.coords = (cliprect[0],cliprect[1] +pixelsfromtop)
        self.default = self.coords
        self.screen = screen
        
        self.width = width
        self.height = height
        self.cliprect = cliprect
        self.pixelsfromtop = pixelsfromtop
        
        self.string = strings
        
        self.topcoord = cliprect[1] # default setting is to assume that the program is scrolled to the very top
        self.Vpos = 0 #how far scrolled down the user is
        self.hover = False
        self.selected = False
        self.fontsize = 12
        
    def SETselected(self,boolean):
        self.selected = boolean
    def SETpos(self,num):
        self.Vpos = num
    def blip(self):
        if (self.coords[1] + self.Vpos >self.cliprect[1] and self.coords[1] + self.Vpos < self.cliprect[1] + self.cliprect[3]) or (self.coords[1] + self.Vpos + self.height >self.cliprect[1] and self.coords[1] + self.Vpos + self.height < self.cliprect[1] + self.cliprect[3]):
            self.screen.set_clip(self.cliprect)
            if self.hover == False and self.selected == False:
                pygame.draw.rect(self.screen,(255,255,255),(self.coords[0],self.coords[1] + self.Vpos,self.width,self.height))
            else:
                pygame.draw.rect(self.screen,(200,200,200),(self.coords[0],self.coords[1] + self.Vpos,self.width,self.height))
            pygame.draw.rect(self.screen,(0,0,0),(self.coords[0],self.coords[1] +self.Vpos,self.width,self.height),3)
            
            font = pygame.font.SysFont('timesnewroman', self.fontsize)
            countery = -1
            extracounter = 0
            for i in range (len(self.string)):
                if i != 0:
                    countery +=1 
                    text = font.render(str(self.string[i]),True,(0,0,0))
                    self.screen.blit(text,(self.coords[0]+3,self.coords[1] + self.height/16 + self.Vpos +countery*self.fontsize)) #fix when data comes
                else:
                    countery += 1
                    text = font.render(str(self.string[0][0]) + ' ' + str(self.string[0][1]) + ' ' + str(self.string[0][2]) + ' ' + str(self.string[0][3]) + ' ' + str(self.string[0][4]),True,(0,0,0))
                    self.screen.blit(text,(self.coords[0]+3,self.coords[1] + self.height/16 + self.Vpos +countery*self.fontsize)) #fix when data comes
                    countery += 1
                    text = font.render(str(self.string[0][5]) + ' ' + str(self.string[0][6]) + ' ' +  str(self.string[0][7]) + ' ' + str(self.string[0][8]) + ' ' + str(self.string[0][9]), True, (0,0,0))
                    self.screen.blit(text,(self.coords[0]+3,self.coords[1] + self.height/16 + self.Vpos +countery*self.fontsize)) #fix when data comes

            self.screen.set_clip(None) # so that blipping is nolonger restrained.
    def ison(self,mousecoord):
        if mousecoord[0] > self.coords[0] and mousecoord[1] > self.coords[1] + self.Vpos and mousecoord[0] < self.coords[0] + self.width and mousecoord[1] < self.coords[1] + self.height +self.Vpos and mousecoord[1] > self.cliprect[1] and mousecoord[1] < self.cliprect[1] + self.cliprect[3]:
            self.hover = True
            return True #also checks if the mouse is in the clipping region
        else:
            self.hover = False
            return False
        
class verticescroller:
    def __init__(self,window,coords,width,height):
        self.screen = window.screen
        self.coords = coords
        self.width = width
        self.height = height
        self.slider = widgetslider(window.screen,coords,width,height) #for the user to scroll
        
        self.scroll = 0 #value from 0 to 1 will represent how far down the 'page' the user is looking
        
        self.update(window,[])
            
    def update(self,window,results): #updates the boxes if the user has added or removed vertices
        self.slider.reset()
        self.coordboxes = []
        self.keys = []
        counter = 0
        for i in results:
            self.coordboxes.append(scrollerbox(self.screen,(self.coords[0] + self.width/10,self.coords[1],self.width*9/10,self.height),self.width*9/10,100,100*counter,i))
            counter += 1
        self.totalheight = counter*100
        self.verticalmovement = self.totalheight -self.height
        self.selected = None
    def getselected(self):
        if self.selected == None:
            return None
        else:
            return self.keys[self.selected]
    def blipupdate(self):
        if self.verticalmovement > 0: #no need to scroll if coords fit on screen
            for i in self.coordboxes:
                i.SETpos(-self.verticalmovement*self.scroll)
        
    def blip(self):
        pygame.draw.rect(self.screen,(100,100,100),(self.coords[0],self.coords[1],self.width,self.height))
        self.slider.blip()
        for i in self.coordboxes:
            i.blip()
    def takeinput(self,window):
        for i in range(len(self.coordboxes)):
            self.coordboxes[i].ison(window.mouse)
        if window.KeyMOUSEdown == True and window.mouse[0] > self.coords[0] and window.mouse[1] > self.coords[1] and window.mouse[0] < self.coords[0] + self.width and window.mouse[1] < self.coords[1] + self.height:
            selected = False
            for i in range(len(self.coordboxes)):
                self.coordboxes[i].SETselected(False)
                if self.coordboxes[i].hover == True:
                    self.selected = i
                    selected = True
                    self.coordboxes[i].SETselected(True)
                
            if self.slider.ison(window.mouse) == True:
                self.slider.takeinput(window,self)
                selected = True
            if selected == False:
                self.selected = None
