import pygame
import userFeaturesbasic as ufb
import menusbasic as mb
import scraper as qp
import databaseCommands as db

def scaleimage(image,screen): #default dimensions 1200 by 800
    newimage = pygame.transform.scale(image,(image.get_width()*screen.get_width()/1200,image.get_height()*screen.get_height()/800))
    return newimage

class window:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(title = 'project')
        infoObject = pygame.display.Info() #checks height and width of screen
        self.screen = pygame.display.set_mode((infoObject.current_w/1.2,infoObject.current_h/1.2))
        self.mouse = pygame.mouse.get_pos() #keeping track of mouse
        self.screen.fill((255,255,255)) #fill white
        self.cache = None
        self.width = infoObject.current_w/1.2 #screen size
        self.height = infoObject.current_h/1.2
        self.running = True # for the main loop
        
        self.font = pygame.font.SysFont('timesnewroman', 30)
        
        self.KeyMOUSEdown = False # click detection
        
        self.clock = pygame.time.Clock()
        self.time = 30
        self.menu = mb.optionsMenu(self)
        self.searchbar = ufb.namebox(self.screen)
        self.query = None
        
        self.Research = False


        Add = pygame.image.load("Add.png")
        Add = scaleimage(Add,self.screen)
        
        self.Add = ufb.button(self.screen,Add, (0,0))
        
        self.mainloop()
    def processquery(self): #checks database and websites
        if self.query != None and self.query != '':
            self.results = db.readEntryWithName(self.query)
            for i in range(len(self.results)):
                self.results[i][0] = list(self.results[i][0])
                self.results[i][0].pop(0)
            if self.results != None and self.results != []:
                self.menu.selector.update(self,self.results) #shows related results
            else:
                dataKinput = qp.searchBusiness(self.query)
                self.results = self.results +  dataKinput # search

                for i in dataKinput:
                    db.addEntry(i)


                if self.results != None:
                    self.menu.selector.update(self,self.results)
                
                else: print('no results')


            self.cache = self.query
            self.query = None #clears search bar means this runs once
             
    def kinput(self):
        self.mouse = pygame.mouse.get_pos() #keeping track of mouse
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.KeyMOUSEdown = True
            else:
                self.KeyMOUSEdown = False
                
            if event.type == pygame.QUIT: #when exit pressed close window
                self.running = False
                pygame.display.quit()
        
        if self.searchbar.ison(self.mouse) == True:
            self.query = self.searchbar.takeinput(self.mouse)
            print(self.query)
            self.processquery()
        if self.Add.ison(self.mouse) == True:
            dataKinput = qp.searchBusiness(self.cache)
            self.results = self.results +  dataKinput # search

            for i in dataKinput:
                db.addEntry(i)


            if self.results != None:
                self.menu.selector.update(self,self.results)
            
            
    def action(self): #calls function for the scroller to evaluate stuff
        self.menu.handleinput(self)
    def blip(self): 
        self.menu.blip()
        self.searchbar.blip()
        text = self.font.render('enter correctly spelt name',True,(0,0,0)) #text on top
        self.screen.blit(text,(self.width*3/8,0))
        self.Add.blip()
    
    def mainloop(self):
        while self.running:
            
            self.time = self.clock.get_time() # time since last frame
            self.clock.tick(30) # frame rate cap
            pygame.display.update()
            
            self.kinput()
            self.action()
            self.blip()
hello = window()