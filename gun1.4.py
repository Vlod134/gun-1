from random import randrange as rnd, choice
import tkinter as tk
import math
import time

# print (dir(math))

root = tk.Tk()
fr = tk.Frame(root)
root.geometry('800x600')
canv = tk.Canvas(root, bg='white')
canv.pack(fill=tk.BOTH, expand=1)


class ball():
	def __init__(self, x, y):
		""" Конструктор класса ball
		Args:
		x - начальное положение мяча по горизонтали
		y - начальное положение мяча по вертикали
		"""
		self.x = x
		self.y = y
		self.r = 10
		self.vx = 1
		self.vy = 1
		self.color = choice(['blue', 'green', 'yellow', 'brown'])
		self.id = canv.create_oval(
				self.x - self.r,
				self.y - self.r,
				self.x + self.r,
				self.y + self.r,
				fill=self.color, 
		)
		self.live = 30

	def set_coords(self):
		canv.coords(
				self.id,
				self.x - self.r,
				self.y - self.r,
				self.x + self.r,
				self.y + self.r
		)

	def move(self):
		if (self.x+self.vx<800 and self.y-self.vy<550):
			self.vy-=1
		elif (self.x+self.vx>800 or self.x+self.vx<0):
			self.vx=-self.vx
		elif (self.y-self.vy>550):
			self.vy=-int(0.6*self.vy)
			self.vx=int(0.6*self.vx)
		self.x += self.vx
		self.y -= self.vy
		self.set_coords()
		if (self.vx*self.vx+self.vx*self.vx<10):
			self.live -= 1
		if (self.live <0):
			canv.delete(self.id)
			self.x=0
        
        
	def hittest(self, obj):
		"""Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.
		Args:
			obj: Обьект, с которым проверяется столкновение.
		Returns:
			Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
		"""
		if (obj.x-self.x)*(obj.x-self.x)+(obj.y-self.y)*(obj.y-self.y)<(self.r+obj.r)*(self.r+obj.r):
			return True
		else:
			return False


class gun():
	def __init__(self, x, y):
		self.x=x
		self.y=y 
		self.f2_power = 10
		self.f2_on = 0
		self.an = 1
		self.id = canv.create_line(self.x, self.y, self.x+30, self.y-30, width=7) # FIXME: don't know how to set it...

	def fire2_start(self, event):
		self.f2_on = 1

	def fire2_end(self, event):
		"""Выстрел мячом.
		Происходит при отпускании кнопки мыши.
		Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
		"""
		global balls, bullet
		bullet += 1
		new_ball = ball(self.x, self.y)
		new_ball.r += 5
		self.an = math.atan((event.y-new_ball.y) / (event.x-new_ball.x))
		new_ball.vx = self.f2_power * math.cos(self.an)
		new_ball.vy = - self.f2_power * math.sin(self.an)
		balls += [new_ball]
		self.f2_on = 0
		self.f2_power = 10

	def targetting(self, event=0):
		"""Прицеливание. Зависит от положения мыши."""
		if event:
			self.an = math.atan((event.y-self.y) / (event.x-self.x))
		if self.f2_on:
			canv.itemconfig(self.id, fill='orange')
		else:
			canv.itemconfig(self.id, fill='black')
		canv.coords(self.id, self.x, self.y,
					self.x + max(self.f2_power, 20) * math.cos(self.an),
					self.y + max(self.f2_power, 20) * math.sin(self.an)
					)

	def power_up(self):
		if self.f2_on:
			if self.f2_power < 50:
				self.f2_power += 1
			canv.itemconfig(self.id, fill='orange')
		else:
			canv.itemconfig(self.id, fill='black')


class target():
	def __init__(self): 
		self.points = 0
		self.live = 1
		self.vx=rnd(-10, 10)
		self.vy=rnd(-10, 10)
		if self.vx==0:
			self.vx=1
		if self.vy==0:
			self.vy=1
		self.id = canv.create_oval(0,0,0,0)
		self.id_points = canv.create_text(30,30,text = self.points,font = '28')

	def new_target(self):
		""" Инициализация новой цели. """
		x = self.x = rnd(600, 740)
		y = self.y = rnd(60, 490)
		r = self.r = rnd(20, 50)
		self.Life=1
		color = self.color = 'red'
		canv.coords(self.id, x-r, y-r, x+r, y+r)
		canv.itemconfig(self.id, fill=color, outline=color)
		self.vx=rnd(-10, 10)
		self.vy=rnd(-10, 10)
	
	def move(self):
		if self.Life==1:
			global balls
			dist=0
			dopvx=0
			dopvy=0
			force=0
			for b in balls:
				dist=math.sqrt((b.x-self.x)*(b.x-self.x)+(b.y-self.y)*(b.y-self.y))
				force+=int(10000000/(dist*dist*dist))
				dopvx+=force*(self.x-b.x)/dist
				dopvy+=force*(self.y-b.y)/dist
			self.x=self.x+self.vx+dopvx
			self.y=self.y+self.vy+dopvy
			
			ogr=100
			if (dopvx>ogr):
				dopvx=ogr
			elif (dopvx<-ogr):
				dopvx=-ogr
			if (dopvy>ogr):
				dopvy=ogr
			elif (dopvy<-ogr):
				dopvy=-ogr
				
			if (self.x+self.vx+dopvx>800):
				self.x=800-(self.vx+dopvx-(800-self.x))
				self.vx=-self.vx
				dopvx=-dopvx
			if (self.x+self.vx+dopvx<500):
				self.x=500-(self.vx+dopvx+(self.x-500))
				self.vx=-self.vx
				dopvx=-dopvx
			if (self.y+self.vy+dopvy>550):
				self.y=550-(self.vy+dopvy-(550-self.y))
				self.vy=-self.vy
				dopvy=-dopvy
			if (self.y+self.vy+dopvy<0):
				self.y=-self.vy-dopvy-self.y
				self.vy=-self.vy
				dopvy=-dopvy
				
			canv.coords(
					self.id,
					self.x - self.r,
					self.y - self.r,
					self.x + self.r,
					self.y + self.r)

	def hit(self, points=1):
		"""Попадание шарика в цель."""
		if self.Life==1:
			self.points += points

		self.Life=0
		death_animation(self,1)()
		canv.itemconfig(self.id_points, text=self.points)
def death_animation(self, r):
	def temp():	
		canv.coords(self.id, self.x-r, self.y-r, self.x+r, self.y+r)
		if (r<35):
			canv.itemconfig(self.id, fill='black')
			root.after(100, death_animation(self,r+10))
		elif (r<500):
			canv.itemconfig(self.id, fill=choice(['blue', 'green', 'red', 'brown']))
			root.after(100, death_animation(self,r+20+r/1))
		else:
			canv.coords(self.id,0,0,0,0)
			
	return temp

def target_all_live():
	global targets
	u=0
	for t in targets:
		if t.live==1:
			u=1
	return u

def fire_start(event):
	global guns
	for g in guns:
		g.fire2_start(event)
		
def fire_end(event):
	global guns
	for g in guns:
		g.fire2_end(event)

def targettingg(event):
	global guns
	for g in guns:
		g.targetting(event)

def new_game(event=''):
	global gun, screen1, balls, bullet, targets, guns
	bullet = 0
	balls = []
	guns=[]
	for g in range(1):
		new_g=gun(20, g*40+50)
		guns.append(new_g)
	targets=[]
	for t in range(10):
		new_t=target()
		targets.append(new_t)
	
	for t in targets:
		t.new_target()
	canv.bind('<Button-1>', fire_start)
	canv.bind('<ButtonRelease-1>', fire_end)
	canv.bind('<Motion>', targettingg)

	for t in targets:
		t.live = 1
	while target_all_live() or balls:
		for t in targets:
			t.move()
		for b in balls:
			b.move()
			for t in targets:
				if b.hittest(t) and t.live:
					t.live = 0
					t.hit()
			if target_all_live()==0:	
				canv.bind('<Button-1>', '')
				canv.bind('<ButtonRelease-1>', '')
				canv.itemconfig(screen1, text='Вы уничтожили цели за ' + str(bullet) + ' выстрелов')
		canv.update()
		time.sleep(0.03)
		for g in guns:
			g.targetting()
			g.power_up()
	canv.itemconfig(screen1, text='')
	canv.delete(gun)
	root.after(750, new_game)


screen1 = canv.create_text(400, 300, text='', font='28')
bullet = 0
balls = []


new_game()

mainloop()


