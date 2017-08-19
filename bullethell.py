mainMenu = True
import sys, pygame, random, time, os, ctypes, copy, math, os, string
from pygame.locals import *
os.environ['SDL_VIDEO_WINDOW_POS'] = '%d,%d'%(3,25)
user32 = ctypes.windll.user32
width,height = user32.GetSystemMetrics(0) - 6,user32.GetSystemMetrics(1) - 70
freeplay,missions = True, False
while True:
	import time
	starttime = time.time()
	if mainMenu:
		diff = 0
	timeoflastspacebar = 0
	class Player(pygame.sprite.Sprite):
		def __init__(self):
			super(Player,self).__init__()
			self.surf = pygame.image.load('spaceship.png').convert_alpha()
			self.rect = self.surf.get_rect()
			self.hp = 100
			self.rect.centerx = width / 2
			self.rect.centery = height / 2
			self.speedtime = 0
			self.spacebar = None
	class Enemy(pygame.sprite.Sprite):
		def __init__(self):
			super(Enemy,self).__init__()
			enemytype = str(random.randint(1,1))
			self.surf = pygame.image.load('enemy' + enemytype +'.png')
			self.rect = self.surf.get_rect()
			self.hp = 100
	class Laser(pygame.sprite.Sprite):
		def __init__(self,facing,parent): #facing is left/right/up/down, parent is the enemy that shot the laser
			super(Laser,self).__init__()
			parentsize = parent.get_size()
			if facing == 'left':
				self.surf = pygame.Surface((1,2))
				self.x = parent.x - 2
				self.y = parent.centery
			elif facing == 'right':
				self.surf = pygame.Surface((1,2))
				self.x = parent.x + parentsize[0] + 1
				self.y = parent.centery
			elif facing == 'up':
				self.surf = pygame.Surface((2,1))
				self.x = parent.centerx
				self.y = parent.y - 2
			else:
				self.surf = pygame.Surface((2,1))
				self.x = parent.centerx
				self.y = parent.y + parentsize[1] + 1
			self.surf.fill(255,70,70)
			self.rect = self.surf.get_rect()

	class SpacebarSprite(pygame.sprite.Sprite):
		def __init__(self):
			super(SpacebarSprite,self).__init__()
			self.type = random.choice(spacebartypes)
			self.surf = pygame.image.load(self.type).convert_alpha()
			self.rect = self.surf.get_rect()
			self.rect.centerx = random.randint(36,width - 36)
			self.rect.centery = random.randint(36,height - 36)
			self.time = 0
	class Bullet(pygame.sprite.Sprite):
		def __init__(self):
			super(Bullet,self).__init__()
			self.bulletsize = random.choice([8,12,16,20])
			if self.bulletsize == 8:
				self.surf = pygame.image.load('rock8.png').convert()
			elif self.bulletsize == 12:
				self.surf = pygame.image.load('rock12.png').convert()
			elif self.bulletsize == 16:
				self.surf = pygame.image.load('rock16.png').convert()
			else:
				self.surf = pygame.image.load('rock20.png').convert()
			self.surf.set_colorkey((255,255,255))
			self.rect = self.surf.get_rect()
			self.spawnside = random.choice(['top','left','right', 'bottom'])
			if self.spawnside == 'top':
				self.speed = [random.randint(1,6),random.randint(1,6)]
				self.speed[0] = random.choice([-1,1]) * self.speed[0]
				self.rect.centerx = random.randint(0,width)
				self.rect.y = 0
			elif self.spawnside == 'left':
				self.speed = [random.randint(1,6),random.randint(1,6)]
				self.speed[1] = random.choice([-1,1]) * self.speed[1]
				self.rect.x = 0
				self.rect.centery = random.randint(0,height) 
			elif self.spawnside == 'right':
				self.speed = [-random.randint(1,6),random.randint(1,6)]
				self.speed[1] = random.choice([-1,1]) * self.speed[1]
				self.rect.x = width
				self.rect.centery = random.randint(0,height) 
			else:
				self.speed = [random.randint(1,6),-random.randint(1,6)]
				self.speed[0] = random.choice([-1,1]) * self.speed[0]
				self.rect.centerx = random.randint(0,width)
				self.rect.y = height
			self.time = 0
			
	class Medpack(pygame.sprite.Sprite):
		def __init__(self):
			super(Medpack,self).__init__()
			self.surf = pygame.image.load('medpack.png')
			self.rect = self.surf.get_rect()
			self.time = 0
			self.healing = random.randint(1,40//diff)
			self.rect.centerx = random.randint(18,width - 18)
			self.rect.centery = random.randint(18,height - 18)
	class ShieldPowerUp(pygame.sprite.Sprite):
		def __init__(self):
			super(ShieldPowerUp,self).__init__()
			self.surf = pygame.image.load('shieldpowerup.png')
			self.rect = self.surf.get_rect()
			self.time = 0
			self.rect.centerx = random.randint(18,width - 18)
			self.rect.centery = random.randint(18,height - 18)
	class SpeedPowerUp(pygame.sprite.Sprite):
		def __init__(self):
			super(SpeedPowerUp,self).__init__()
			self.surf = pygame.image.load('speedpowerup.png')
			self.rect = self.surf.get_rect()
			self.time = 0
			self.rect.centerx = random.randint(18,width - 18)
			self.rect.centery = random.randint(18,height - 18)

	clock = pygame.time.Clock()
	pygame.init()
	size = width, height
	screen = pygame.display.set_mode(size)
	screen = pygame.display.set_mode(size)
	clock = pygame.time.Clock()
	if mainMenu:
		start = False
	else:
		start = True
	rotator = 0
	spawningpaused = [False,None]
	playerspeed = [6,6]
	heat = 0
	bulletgroup = pygame.sprite.Group()
	medpackgroup = pygame.sprite.Group()
	shieldpowerupgroup = pygame.sprite.Group()
	speedpowerupgroup = pygame.sprite.Group()
	spacebarspritegroup = pygame.sprite.Group()
	dead = False
	highscores = False
	player = Player()
	bulletticks = 0
	pygame.mixer.music.load('Sounds\Ballista.wav')
	powerupticks = 0
	shieldactive = False
	speedactive = [False,[10,10]]
	inf = 0
	level = 0
	flashing = [False, 0] #if player is flashing/immune, this number // 12 %2 determines if the player is showing or not (by truthiness) and determines how long its been flashing (at 60 it stops)
	spacebartypes = ['clear.png','pause.png']
	submitname = False
	def text_objects(text, font, color):
		textSurface = font.render(text, True, color)
		return textSurface, textSurface.get_rect()
	def message_display(text,fontsize,xc,yc,color = (255,255,255),font = 'consolas'):
		largeText = pygame.font.SysFont(font,fontsize)
		TextSurf, TextRect = text_objects(text, largeText, color)
		TextRect.center = ((xc),(yc))
		screen.blit(TextSurf, TextRect)
	def make_button(xc,yc,length,how_tall,text,fontsize,var,color = (0,0,0),border = (0,0,0),events = pygame.event.get(),font = None):
		pygame.draw.rect(screen,(211,211,211),(xc,yc,length,how_tall),0)
		buttonrect = Rect((xc, yc), (length, how_tall))
		for event in events:
			mousepos = pygame.mouse.get_pos()
			if buttonrect.collidepoint(mousepos):
				if event.type == pygame.MOUSEBUTTONDOWN:
					return 'pressed'
				return 'hover'
		pygame.draw.rect(screen,border,(xc,yc,length,how_tall),2)
		if font != None:
			message_display(text,fontsize,xc + length / 2, yc + how_tall / 2, color,font = font)
		else:
			message_display(text,fontsize,xc + length / 2, yc + how_tall / 2, color)
		if len(events) > 0:
			return None
		else:
			return var
	def make_button_hover(xc,yc,length,how_tall,text,fontsize,color = (0,0,0),border = (0,0,0),font = None):
		pygame.draw.rect(screen,(169,169,169),(xc,yc,length,how_tall),0)
		pygame.draw.rect(screen,border,(xc,yc,length,how_tall),2)
		if font != None:
			message_display(text,fontsize,xc + length / 2, yc + how_tall / 2, color,font = font)
		else:
			message_display(text,fontsize,xc + length / 2, yc + how_tall / 2, color)
	pygame.mixer.music.play(-1,0.)
	title = True
	info = False
	freeplayButton,missionsButton,instructionsButton,backButton = None,None,None,None
	while (not start) and mainMenu:
		screen.fill((30,50,50))
		mousepos = pygame.mouse.get_pos()
		events = pygame.event.get()
		buttonhover = None
		if title:
			titlesurf = pygame.transform.scale2x(pygame.image.load('Title.png').convert_alpha())
			screen.blit(titlesurf,(width / 2 - 400, 40))
			instructionsButton = make_button(width / 2 - 125,height / 2 - 85,250,50,'Instructions',30,instructionsButton,events = events)
			if instructionsButton == 'hover':
				make_button_hover(width / 2 - 125,height / 2 - 85,250,50,'Instructions',30)
			elif instructionsButton == 'pressed':
				title = False
				info = True
			missionsButton = make_button(width / 2 - 125,height / 2 - 25,250,50,'Missions',30,missionsButton,events = events)
			if missionsButton == 'hover':
				make_button_hover(width / 2 - 125,height / 2 - 25,250,50,'Missions',30)
			elif missionsButton == 'pressed':
				start = True
				missions = True
			freeplayButton = make_button(width / 2 - 125,height / 2 + 35,250,50,'Freeplay',30,freeplayButton,events = events)
			if freeplayButton == 'hover':
				make_button_hover(width / 2 - 125,height / 2 + 35,250,50,'Freeplay',30)
			elif freeplayButton == 'pressed':
				start = True
				freeplayButton = True
			shipimagesurface = pygame.transform.rotate(pygame.transform.scale(pygame.image.load('spaceship.png').convert_alpha(),(200,200)),315)
			screen.blit(shipimagesurface,(100,300))
			enemyimagesurface = pygame.transform.rotate(pygame.transform.scale(pygame.image.load('enemy1.png').convert_alpha(),(200,200)),45)
			screen.blit(enemyimagesurface,(width - 400,300))
		for event in events:
			if event.type == pygame.KEYDOWN:
				if event.key == K_1:
					start = 1
				if event.key == K_ESCAPE:
					os._exit(0)
			if event.type == pygame.QUIT:
				os._exit(0)
		if info:
			backButton = make_button(width/2 - 75,height - 150,150,75,'Back',30,backButton,events = events)
			if backButton == 'hover':
				make_button_hover(width/2 - 75,height - 150,150,75,'Back',30)
			if backButton == 'pressed':
				title = True
				info = False
			message_display('Controls:',30,width/2,100)
			message_display('Arrow keys to move',30,width/2,130)
			message_display('Shift to slow down',30,width/2,160)
			message_display('Spacebar to activate item',30,width/2,190)
			message_display('Speed power-ups give your ship a temporary speed boost',30,width/2,280)
			spusurf = pygame.image.load('speedpowerup.png')
			screen.blit(spusurf,(200,272))
			message_display('Shield power-ups give your ship a shield',30,width/2,310)
			shpusurf = pygame.image.load('shieldpowerup.png')
			screen.blit(shpusurf,(320,302))
			message_display("Health power-ups allow you to recover HP if you've lost any",30,width/2,340)
			hpusurf = pygame.image.load('medpack.png')
			screen.blit(hpusurf,(160,332))
			message_display("If your ship hits an asteroid, you lose 10 HP or your shield if you have one",30,width/2,370)
			message_display("If your ship reaches 0 HP, you lose",30,width/2,400)
			message_display('Your goal in freeplay mode is to survive as long as possible',30,width/2,430)
			message_display("Your goal in missions mode is to complete the objective",30,width/2,460)
		pygame.display.update()
		clock.tick(60)
		## TODO 1:ALL THE BUTTONS
		easyButton,normalButton,hardButton,insaneButton,infernalButton = None,None,None,None,None
	while mainMenu: 
		screen.fill((100,100,255))
		mousepos = pygame.mouse.get_pos()
		message_display('Choose your difficulty:',50,width/2,height/2 - 200)
		events = pygame.event.get()
		easyButton = make_button(width/2 - 125,height/2 - 125,250,50,'Easy',30,easyButton,events = events,color = (255,255,255))
		if easyButton == 'hover':
			make_button_hover(width/2 - 125,height/2 - 125,250,50,'Easy',30,color = (255,255,255))
		elif easyButton == 'pressed':
			diff = 2
			mainMenu = False
		normalButton = make_button(width/2 - 125,height/2 - 50,250,50,'Normal',30,normalButton,events = events,color = (255,255,255))
		if normalButton == 'hover':
			make_button_hover(width/2 - 125,height/2 - 50,250,50,'Normal',30,color = (255,255,255))
		elif normalButton == 'pressed':
			diff = 3
			mainMenu = False
		hardButton = make_button(width/2 - 125,height/2 + 25,250,50,'Hard',30,hardButton,events = events,color = (255,255,255))
		if hardButton == 'hover':
			make_button_hover(width/2 - 125,height/2 + 25,250,50,'Hard',30,color = (255,255,255))
		elif hardButton == 'pressed':
			diff = 5
			mainMenu = False
		insaneButton = make_button(width/2 - 125,height/2 + 100,250,50,'Insane',30,insaneButton,events = events,color = (255,255,255))
		if insaneButton == 'hover':
			make_button_hover(width/2 - 125,height/2 + 100,250,50,'Insane',30,color = (255,255,255))
		elif insaneButton == 'pressed':
			diff = 8
			mainMenu = False
		if inf == 3:
			infernalButton = make_button(width/2 - 125,height/2 + 175,250,50,'INFERNAL',40,infernalButton,events = events,color = (255,0,0),font = 'vinerhanditc',border = (255,100,100))
			if infernalButton == 'hover':
				make_button_hover(width/2 - 125,height/2 + 175,250,50,'INFERNAL',40,color = (255,0,0),font = 'vinerhanditc',border= (255,100,100))
			elif infernalButton == 'pressed':
				diff = 12
				mainMenu = False
		for event in events:
			if event.type == pygame.KEYDOWN:
				if event.key == K_ESCAPE:
					os._exit(0)
				if event.key == K_6:
					inf += 1
			if event.type == pygame.QUIT:
				os._exit(0)
		pygame.display.update()
		clock.tick(60)
		stabilizer = 0 
	print diff
	pygame.mixer.music.load('Sounds\Infernal Showdown.wav')
	pygame.mixer.music.play(-1,0.)
	playershowing = True
	while start:
		timenow = time.time()-starttime
		if speedactive[0]:
			localspeed = copy.deepcopy(speedactive[1])
			player.speedtime += 1
		else:
			localspeed = copy.deepcopy(playerspeed)
		if player.speedtime >= 180:
			speedactive[0] = False
			player.speedtime = 0
		if flashing[0]:
			if flashing[1]> 60:
				flashing[0] = False
				flashing[1] = 0
				playershowing = True
			#if player has been flashing for one second, they stop flashing
			else:
				flashing[1] += 1
				playershowing = bool((flashing[1] // 12) % 2)
			#the flashing is incremented, and whether the player is showing is calculated
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				print 'You quit. You survived for {} seconds. Better luck next time.'.format(str(time.time()-starttime))
				os._exit(0)
			if event.type == pygame.KEYDOWN:
				if event.key == K_ESCAPE:
					print 'You quit. You survived for {} seconds. Better luck next time.'.format(str(time.time()-starttime))
					os._exit(0)
		level = int((15 + timenow) //15)
		moveup = 0
		moveright = 0

		keysdict = pygame.key.get_pressed()
		if keysdict[K_UP] and not(player.rect.y <= 0): moveup -= 1
		if keysdict[K_DOWN] and not(player.rect.y + 33 >= height): moveup += 1
		if keysdict[K_RIGHT] and not(player.rect.x + 25 >= width): moveright += 1
		if keysdict[K_LEFT] and not(player.rect.x <= 0 ): moveright -= 1
		if keysdict[K_RSHIFT] or keysdict[K_LSHIFT]: localspeed = map(lambda n: n / 2,localspeed)
		player.rect = player.rect.move([localspeed[0]*moveright,localspeed[1]*moveup])
		if diff == 12: heat = 255
		screen.fill((heat,0,0))
		if moveup == -1:
			if moveright == 1:
				rotator = 315
			elif moveright == 0:
				rotator = 0
			else:
				rotator = 45
		elif moveup == 0:
			if moveright == 1:
				rotator = 270
			elif moveright == -1:
				rotator = 90
		else:
			if moveright == 1:
				rotator = 225
			elif moveright == 0:
				rotator = 180
			else:
				rotator = 135
		if playershowing: screen.blit(pygame.transform.rotate(player.surf,rotator),player.rect)

		if bulletticks != 0 and bulletticks % (60 // level) == 0 and (not spawningpaused[0]):
			bulletticks = 0
			for n in range(diff):
				bulletgroup.add(Bullet())
			powerupticks += 1
		if powerupticks == (2 * diff * level) // 2:
			if random.randint(1,3) == 1:
				medpackgroup.add(Medpack())
			elif random.randint(1,2) == 1:
				shieldpowerupgroup.add(ShieldPowerUp())
			else:
				speedpowerupgroup.add(SpeedPowerUp())
			powerupticks = 0
		if random.choice(range(int((diff * 4000) / (1 + int(timenow) - timeoflastspacebar)))) == 1:
			timeoflastspacebar = int(timenow)
			spacebarspritegroup.add(SpacebarSprite())
		if level < 10:
			message_display('Level {}'.format(str(level)),40,width - 80,24)
		else:
			message_display('Level {}'.format(str(level)),40,width - 100,24)
		message_display('HP: {}'.format(str(player.hp)),40,80,height - 24)

		deadbullets = pygame.sprite.spritecollide(player,bulletgroup,False)
		deadmedpacks = pygame.sprite.spritecollide(player,medpackgroup,False)
		deadshieldpowerups = pygame.sprite.spritecollide(player,shieldpowerupgroup,False)
		deadspeedpowerups = pygame.sprite.spritecollide(player,speedpowerupgroup,False)
		deadspacebaritems = pygame.sprite.spritecollide(player,spacebarspritegroup,False)
		if keysdict[K_SPACE] and player.spacebar != None:
			if player.spacebar == 'clear.png':
				player.spacebar = None
				for bullet in bulletgroup:
					bullet.kill()
				clearsound = pygame.mixer.Sound('Sounds\clearsound.wav')
				pygame.mixer.Sound.play(clearsound)
			elif player.spacebar == 'pause.png':
				player.spacebar = None
				#sound effect
				spawningpaused = [True, 0]
		if keysdict[K_TAB]:
			player.hp = 0
		if len(bulletgroup) != 0:
			for bullet in bulletgroup:
				bullet.rect = bullet.rect.move(bullet.speed)
				bullet.time += 1
				screen.blit(bullet.surf,bullet.rect)
				if bullet.rect.centerx > width or bullet.rect.centery > height or bullet.rect.centery < 0:
					bullet.kill()
			for bullet in deadbullets:
				bullet.kill()
				if shieldactive:
					shieldactive = False
					shieldsdownsound = pygame.mixer.Sound('Sounds\shieldsdown.wav')
					pygame.mixer.Sound.play(shieldsdownsound)
				else:
					if not flashing[0]: 
						player.hp -= 10 #player is immune when flashing, otherwise they take 10 points of damage
						flashing = [True,0]
						damagesound = pygame.mixer.Sound('Sounds\damagesound.wav')
						if player.hp != 0:
							pygame.mixer.Sound.play(damagesound)
		if len(medpackgroup) != 0:
			for medpack in medpackgroup:
				medpack.time += 1
				screen.blit(medpack.surf,medpack.rect)
				if medpack.time > 300:
					medpack.kill()
			for medpack in deadmedpacks:
				player.hp += medpack.healing
				if player.hp > 100:
					player.hp = 100
				medpack.kill()
				powerupsound = pygame.mixer.Sound('Sounds\powerupget.wav')
				pygame.mixer.Sound.play(powerupsound)
		if len(shieldpowerupgroup) != 0:
			for shieldpowerup in shieldpowerupgroup:
				shieldpowerup.time += 1
				screen.blit(shieldpowerup.surf,shieldpowerup.rect)
				if shieldpowerup.time > 300:
					shieldpowerup.kill()
			for shieldpowerup in deadshieldpowerups:
				shieldactive = True
				shieldpowerup.kill()
				powerupsound = pygame.mixer.Sound('Sounds\powerupget.wav')
				pygame.mixer.Sound.play(powerupsound)
		if len(speedpowerupgroup) != 0:
			for speedpowerup in speedpowerupgroup:
				speedpowerup.time += 1
				screen.blit(speedpowerup.surf,speedpowerup.rect)
				if speedpowerup.time > 300:
					speedpowerup.kill()
			for speedpowerup in deadspeedpowerups:
				speedactive[0] = True
				player.speedtime = 0
				speedpowerup.kill()
				powerupsound = pygame.mixer.Sound('Sounds\powerupget.wav')
				pygame.mixer.Sound.play(powerupsound)
		if len(spacebarspritegroup) != 0:
			for spacebaritem in spacebarspritegroup:
				spacebaritem.time += 1
				screen.blit(spacebaritem.surf,spacebaritem.rect)
				if spacebaritem.time >= 300:
					spacebaritem.kill()
			for spacebaritem in deadspacebaritems:
				player.spacebar = spacebaritem.type
				spacebaritem.kill()
				powerupsound = pygame.mixer.Sound('Sounds\powerupget.wav')
				pygame.mixer.Sound.play(powerupsound)
		if player.hp <= 0:
			start = False
			dead = True
			finaltime = time.time()
		if shieldactive:
			shieldsurf = pygame.image.load('shield.png').convert()
			shieldsurf.set_colorkey((255,255,255))
			if rotator % 180 == 0:
				screen.blit(pygame.transform.rotate(shieldsurf,rotator),(player.rect.x - 2,player.rect.y - 6))
			elif rotator % 90 == 0:
				screen.blit(pygame.transform.rotate(shieldsurf,rotator),(player.rect.x - 6,player.rect.y - 2))
			elif rotator == 135 or rotator == 315:
				screen.blit(pygame.transform.rotate(shieldsurf,rotator),(player.rect.x - 4,player.rect.y - 6))
			else:
				screen.blit(pygame.transform.rotate(shieldsurf,rotator),(player.rect.x - 6,player.rect.y - 4))
		pygame.draw.rect(screen,(211,211,211),(0,0,116,116),0)
		pygame.draw.rect(screen,(47,79,79),(0,0,116,116),2)
		pygame.draw.rect(screen,(0,0,0),(114,116,3,1),0)
		pygame.draw.rect(screen,(0,0,0),(116,114,1,3),0)
		pygame.draw.rect(screen,(0,0,0),(0,0,3,1),0)
		pygame.draw.rect(screen,(0,0,0),(0,0,1,3),0)
		pygame.draw.rect(screen,(0,0,0),(114,0,3,1),0)
		pygame.draw.rect(screen,(0,0,0),(116,0,1,3),0)
		pygame.draw.rect(screen,(0,0,0),(0,116,3,1),0)
		pygame.draw.rect(screen,(0,0,0),(0,114,1,3),0)
		if player.spacebar != None: 
			spacesurf = pygame.image.load(player.spacebar).convert()
			spacesurf.set_colorkey((255,255,255))
			screen.blit(pygame.transform.scale2x(spacesurf),(8,8))
		pygame.display.update()
		pygame.display.flip()
		bulletticks += 1
		if spawningpaused[0]:
			spawningpaused[1] += 1
			if spawningpaused[1] >= 240:
				spawningpaused = [False,None]
		if heat < 255: heat += .001 * diff
		clock.tick(60)
	pygame.mixer.music.load('Sounds\Deathsound.midi')
	pygame.mixer.music.play(0,0.)
	pygame.mixer.music.set_endevent(pygame.USEREVENT)
	while dead:
		if diff == 2:
			difficulty = 'easy'
		elif diff == 3:
			difficulty = 'normal'
		elif diff == 5:
			difficulty = 'hard'
		elif diff == 8:
			difficulty = 'insane'
		else:
			difficulty = 'INFERNAL'
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				dead = False
				os._exit(0)
			if event.type == pygame.KEYDOWN:
				if event.key == K_ESCAPE:
					dead = False
					os._exit(0)
			if event.type == pygame.USEREVENT:
				pygame.mixer.music.load('Sounds\\ballista.wav')
				pygame.mixer.music.play(0,-1)
			screen.fill((255,50,50))
			message_display('You died. You survived for {} seconds on {} difficulty. Better luck next time.'.format(str("{0:.2f}".format(finaltime - starttime)), difficulty),width / 50,width/2,height/2)
			pygame.draw.rect(screen,(211,211,211),(20,height - 70,200,50),0)
			pygame.draw.rect(screen,(211,211,211),(width // 2 - 100,height - 70,200,50),0)
			pygame.draw.rect(screen,(211,211,211),(width - 220,height - 70,200,50),0)
			mousepos = pygame.mouse.get_pos()
			if (height - 70 < mousepos[1] < height - 20):
				if (20 < mousepos[0] < 220):
					pygame.draw.rect(screen,(169,169,169),(20,height - 70,200,50),0)
					if event.type == MOUSEBUTTONDOWN:
						dead = False
						mainMenu = True
				if (width - 220 < mousepos[0] < width -20):
					pygame.draw.rect(screen,(169,169,169),(width - 220,height - 70,200,50),0)
					if event.type == MOUSEBUTTONDOWN:
						dead = False
						mainMenu = False
				if (width // 2 - 100 < mousepos[0] < width // 2 + 100):
					pygame.draw.rect(screen,(169,169,169),(width // 2 - 100,height - 70,200,50),0)
					if event.type == MOUSEBUTTONDOWN:
						highscores = True
						submitname = True
						dead = False
			pygame.draw.rect(screen,(0,0,0),(20,height - 70,200,50),2)
			pygame.draw.rect(screen,(0,0,0),(width - 220,height - 70,200,50),2)
			pygame.draw.rect(screen,(0,0,0),(width // 2 - 100,height - 70,200,50),2)
			message_display('Main Menu',30,120,height - 45,(0,0,0))
			message_display('Retry',30,width - 120,height - 45,(0,0,0))
			message_display('Submit Score',26,width // 2, height - 45,(0,0,0))
		pygame.display.update()
		clock.tick(60)
	screentext = ''
	madeerrorininputl = False
	madeerrorininputs = False
	while highscores and submitname:
		mousepos = pygame.mouse.get_pos()
		for event in pygame.event.get():
			screen.fill((50,255,50))
			if event.type == pygame.QUIT:
				dead = False
				os._exit(0)
			if event.type == pygame.KEYDOWN:
				if event.key == K_ESCAPE:
					dead = False
					os._exit(0)
				if event.key == K_RETURN:
					if len(screentext) > 2:
						submitname = False
						name = screentext
					else:
						madeerrorininputs = True
				if event.key == K_BACKSPACE and len(screentext) > 0:
					screentext = screentext [:-1]
				if str(event.unicode) in string.ascii_lowercase + ' ':
					if len(screentext) < 10:
						screentext += str(event.unicode).upper()
					else:
						madeerrorininputl = True
			if event.type == pygame.USEREVENT:
				pygame.mixer.music.load('Sounds\\ballista.wav')
				pygame.mixer.music.play(0,-1)
			message_display('Enter Your Name',30,width // 2 -100,height //2 - 100,(0,0,0))
			pygame.draw.rect(screen,(255,255,255),(width // 2  - 400,height //2 - 25,600,50),0)
			pygame.draw.rect(screen,(169,169,169),(width // 2  - 400,height //2 - 25,600,50),2)
			message_display(screentext,30,width // 2 -100,height //2,(0,0,0))
			pygame.draw.rect(screen,(211,211,211),(width // 2 + 250,height //2 - 25,150,50),0)
			pygame.draw.rect(screen,(169,169,169),(width // 2 + 250,height //2 - 25,150,50),2)
			if (width // 2 + 250 < mousepos[0] < width + 400) and (height // 2 - 25 < mousepos[1] < height // 2 + 25):
				pygame.draw.rect(screen,(169,169,169),(width // 2 + 250,height //2 - 25,150,50),0)
				if event.type == MOUSEBUTTONDOWN:
					if len(screentext) > 2:
						submitname = False
						name = screentext
					else:
						madeerrorininputs = True
			message_display('->',30,width // 2 + 325,height // 2,(0,0,0))
			if madeerrorininputs:
				message_display('Your name must be at least 3 characters long',30,width // 2,60,(255,255,255))
			if madeerrorininputl:
				message_display('Your name must be less than 10 characters long',30,width // 2,120,(255,255,255))
		pygame.display.update()
		clock.tick(60)
	if highscores:
		scorelista = open('highscores_{}.txt'.format(difficulty), 'a')
		scorelista.write(name + ' ' + "{0:.2f}".format(finaltime - starttime) + '\n')
		scorelista.close()
		scorelistr = open('highscores_{}.txt'.format(difficulty),'r')
		scores = scorelistr.read()[:-1]
		scores = scores.split('\n')
		scores.sort(reverse = True, key = lambda g: float(g.split(' ')[-1]))
		playerscore = scores.index(name + ' ' + "{0:.2f}".format(finaltime - starttime))
	while highscores:
		mousepos = pygame.mouse.get_pos()
		numscores = height // 50 - 7
		if numscores < 5: numscores = 5
		for scoreindex in range(numscores - numscores % 5):
			if scoreindex == playerscore:
				clr = (0,255,0)
			else:
				clr = (255,255,255)
			message_display(str(scoreindex + 1) + '. ' + scores[scoreindex],30,width // 2,50 + 50 * scoreindex,clr)
		if playerscore > 3:
			for scoreindex in range(playerscore - 2, playerscore + 3):
				if scoreindex == playerscore:
					message_display(str(scoreindex + 1) + '. ' + scores[scoreindex],30,width // 2,50 * numscores + 250,(0,255,0))
				else:
					message_display(str(scoreindex + 1) + '. ' + scores[scoreindex],30,width // 2,50 * numscores + 50 * (scoreindex - playerscore + 5),(255,255,255))
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				dead = False
				os._exit(0)
			if event.type == pygame.KEYDOWN:
				if event.key == K_ESCAPE:
					dead = False
					os._exit(0)
			if event.type == pygame.USEREVENT:
				pygame.mixer.music.load('Sounds\\ballista.wav')
				pygame.mixer.music.play(0,-1)
			screen.fill((50,50,255))
			pygame.draw.rect(screen,(211,211,211),(20,height - 70,200,50),0)
			pygame.draw.rect(screen,(211,211,211),(width - 220,height - 70,200,50),0)
			if (height - 70 < mousepos[1] < height - 20):
				if (20 < mousepos[0] < 220):
					pygame.draw.rect(screen,(169,169,169),(20,height - 70,200,50),0)
					if event.type == MOUSEBUTTONDOWN:
						highscores = False
						mainMenu = True
				if (width - 220 < mousepos[0] < width -20):
					pygame.draw.rect(screen,(169,169,169),(width - 220,height - 70,200,50),0)
					if event.type == MOUSEBUTTONDOWN:
						highscores = False
						mainMenu = False
			pygame.draw.rect(screen,(0,0,0),(20,height - 70,200,50),2)
			pygame.draw.rect(screen,(0,0,0),(width - 220,height - 70,200,50),2)
			message_display('Main Menu',30,120,height - 45,(0,0,0))
			message_display('Retry',30,width - 120,height - 45,(0,0,0))
		pygame.display.update()
		clock.tick(60)
	
	#levels
	#enemies w/ ai (HARD)
	#bouncy enemy
	#level screen with buttons
	#more items
	#gun of some sort (mouse? twin stick?)
	#upgrades
	#idea: turret on something (class w/ spawn location param) that reflects asteroids and shoots at you (With shooting/ aiming AI)