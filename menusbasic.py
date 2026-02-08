import pygame
import math
import userFeaturesbasic as uf

class menu:
    def __init__(self,screen,coords,width,height,color,bordersize,text,textcoords,textsize,textcolor,buttons,sliders,inputboxes): #pass in lists of everything from text onwards. will not be directly initalised.
        self.visible = True
        self.screen = screen
        
        self.coords = coords #where the menu is
        self.width = width
        self.height = height
        
        self.color = color
        self.bordersize = bordersize
        
        #length of lists should be same length
        self.text = text  #str
        self.textcoords = textcoords #int
        self.textsize = textsize #int
        self.textcolor = textcolor
        
        
        self.buttons = buttons
        self.sliders = sliders
        self.inputboxes = inputboxes
        
        self.input = None #what has been pressed so that the subclasses can handle it individually
    def simpleblip(self): #so that i can reference even with polymorphism
        pygame.draw.rect(self.screen,(0,0,0),(self.coords[0] -3,self.coords[1] -3,self.width + 6,self.height + 6))
        pygame.draw.rect(self.screen,self.color,(self.coords[0],self.coords[1],self.width,self.height))
        font = []
        for i in range(len(self.text)):
            font.append(pygame.font.SysFont('timesnewroman', self.textsize[i]))
            text = font[i].render(self.text[i],True,self.textcolor[i])
            self.screen.blit(text,self.textcoords[i])
        for i in self.buttons: #interactive elements in front of static elements
            i.blip()
        for i in self.sliders:
            i.blip()
        for i in self.inputboxes:
            i.blip()
    def blip(self):
        if self.visible == True:
            self.simpleblip()
    def simplecheckinput(self,mousepos,mousedown):
        changed = False #check if an input has actually happened
        if self.visible == True:
            for i in range(len(self.buttons)):
                if self.buttons[i].ison(mousepos) == True and  mousedown == True:
                    self.input = [1,i] #[type,index]
                    changed = True
            for i in range(len(self.sliders)):
                if self.sliders[i].ison(mousepos) == True and  mousedown == True:
                    self.input = [2,i]
                    changed = True
            for i in range(len(self.inputboxes)):
                if self.inputboxes[i].ison(mousepos) == True and  mousedown == True:
                    self.input = [3,i]
                    changed = True
        else:
             pass
            
            
            
            
        if changed == False:
             self.input = None
    def checkinput(self,mousepos,mousedown):
        self.simplecheckinput(mousepos,mousedown)
           
    def setvisible(self,new):
        self.visible = new
                     
class optionsMenu(menu): 
    def __init__(self,window):
        color = (255,255,255) #height can be used interchangabky with screen height since they are the same for this menu
        height = (2/3)*window.screen.get_height() #fraction of the screen the menu takes up is in the brackets
        width = (3/4)*window.screen.get_width()
        coords = (window.screen.get_width()/2- width/2,window.screen.get_height()/3)
        
        bordersize = round(3*window.screen.get_width()*height/(1200*800)) #with respect to the area of the menu instead of just any length
        self.selector = uf.verticescroller(window,coords,width,height)
        
        
        text = []
        textcoords = []
        textsize = []
        textcolor = []
        
        buttons = []
        
        sliders = []
        inputboxes = []
        
        super().__init__(window.screen,coords,width,height,color,bordersize,text,textcoords,textsize,textcolor,buttons,sliders,inputboxes) 
            
            

        
    def blip(self):
        super().blip()
        if self.visible == True:
            self.selector.blip()

    def handleinput(self,window):
        if self.visible == True:
            self.selector.takeinput(window)
        if self.input == None:
            pass
        else: #no need to check type of object pressed as only objects are
            if self.input[0] == 0: #left and right arrows
                self.visible = True
            elif self.input[1] == 2: #no need to check object type as only buttons  in this menu
                self.visible = False

