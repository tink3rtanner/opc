from luma.core.interface.serial import spi
from luma.core.render import canvas
from luma.oled.device import sh1106
import time,os,datetime
import RPi.GPIO as GPIO
import shutil as sh
from subprocess import *

def init():

	serial = spi(device=0, port=0)
	device = sh1106(serial,rotate=2)
	
	initgpio()
	keys=dict(right=0,left=0,up=0,down=0,key1=0,key2=0,key3=0) #init keybase
	keys=getKeys(keys)

	return device

def initgpio():

	print "Initializing GPIO"
	#Initialize GPIO
	GPIO.setmode(GPIO.BCM)
	key={}

	#key['key1']=21 #broken on menona
	key['key2']=20
	key['key3']=16

	key['left']=5 
	key['up']=6
	key['press']=13
	key['down']=19
	key['right']=26

	#GPIO.setup(key['key1'], GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(key['key2'], GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(key['key3'], GPIO.IN, pull_up_down=GPIO.PUD_UP)

	GPIO.setup(key['left'], GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(key['up'], GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(key['press'], GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(key['down'], GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(key['right'], GPIO.IN, pull_up_down=GPIO.PUD_UP)

	#GPIO.add_event_detect(key['key1'], GPIO.FALLING)
	GPIO.add_event_detect(key['key2'], GPIO.FALLING,bouncetime=300)
	GPIO.add_event_detect(key['key3'], GPIO.FALLING,bouncetime=300)
	GPIO.add_event_detect(key['left'], GPIO.FALLING,bouncetime=300)
	GPIO.add_event_detect(key['up'], GPIO.FALLING,bouncetime=300)
	GPIO.add_event_detect(key['press'], GPIO.FALLING,bouncetime=300)
	GPIO.add_event_detect(key['down'], GPIO.FALLING,bouncetime=300)
	GPIO.add_event_detect(key['right'], GPIO.FALLING,bouncetime=300)


def getKeys(keys={}):
	#keys={}

	keys['key1']=GPIO.input(5)
	keys['key2']= GPIO.input(20)
	keys['key3']= GPIO.input(16)

	keys['left'] = GPIO.input(5)
	keys['up'] = GPIO.input(6)
	keys['press'] = GPIO.input(13)
	keys['down'] = GPIO.input(19)
	keys['right'] = GPIO.input(26)


	return keys

def wait(keys,waitkey):
	keys=getKeys(keys)
	while keys[waitkey]==1:
		keys=getKeys(keys)
	return

def run_cmd(cmd):
	p = Popen(cmd, shell=True, stdout=PIPE)
	output = p.communicate()[0]
	return output

def copytree(src, dst, symlinks=False, ignore=None):
	ct=0
	print str(len(os.listdir(src))) + " files to move"

	try:
		for item in os.listdir(src):
			s = os.path.join(src, item)
			print "source file: ", s
			
			d = os.path.join(dst, item)
			if os.path.isdir(dst)==0:
				print "destination doesn't exist. creating..."
				os.mkdir(dst)
			if os.path.isdir(s):
				print "recurse!"
				sh.copytree(s, d, symlinks, ignore)
			else:
				sh.copy(s, d)
				ct+=1
				print "file "+str(ct)+" moved"
	except:
		print "must be an error. file full or smt"

def listMenu(device,mlist,alist,mname,draw=0):
	#mlist: menu list
	#alist: action list
	#mname: menu name for action context
	title=mname
	#initial settings
	#keys={}
	key={}
	pos=1
	apos=0

	key['key1']=5 #should be 21, only cuz key1 is broken on menona
	key['key2']=20
	key['key3']=16

	key['left']=5 
	key['up']=6
	key['press']=13
	key['down']=19
	key['right']=26
	#GPIO.add_event_detect(key['down'], GPIO.FALLING,bouncetime=300)


	while True:
		#keys=getKeys(keys)
		dispListMenu(device,title,mlist,alist,pos)

		if GPIO.event_detected(key['down']):
		#if keys["down"]==0:
			#pos=pos+1
			pos=posDown(pos)
			dispListMenu(device,title,mlist,alist,pos)

		elif GPIO.event_detected(key['up']):
			#pos=pos+1
			pos=posUp(pos)
			dispListMenu(device,title,mlist,alist,pos)

		elif GPIO.event_detected(key['key2']):
			dispListMenu(device,title,mlist,alist,pos,apos)
			cont=actionhandler(device,pos,apos,mname)
			apos=1
			if cont==1 : apos=0

			#time.sleep(.3)
			
			#action loop
			done=0
			while done==0:
				
				dispListMenu(device,title,mlist,alist,pos,apos)

				#keys=getKeys(keys)

				if GPIO.event_detected(key['down']):
					#pos=pos+1
					apos=posDown(apos,3)
					dispListMenu(device,title,mlist,alist,pos,apos)

				elif GPIO.event_detected(key['up']):
					#pos=pos+1
					apos=posUp(apos,3)
					dispListMenu(device,title,mlist,alist,pos,apos)

				elif GPIO.event_detected(key['key2']):
					esc=actionhandler(device,pos,apos,mname)
					if esc==1 : return

				elif GPIO.event_detected(key['key1']):
					done=1

					#time.sleep(.2)
			
				time.sleep(.01)

		elif GPIO.event_detected(key['key1']):
			dispListMenu(device,title,mlist,alist,pos)
			#time.sleep(.1)
			return

		time.sleep(.01)

def testMenu(device):
	alist=["go", "[empty]","[empty]"]
	mlist=["test1","test2","test3","test4","test5","test6","test7","asdf","asdfg","more tests"]

	listMenuScroll(device,mlist,alist,"MENU>TEST")


def listMenuScroll(device,mlist,alist,mname,draw=0):
	#mlist: menu list
	#alist: action list
	#mname: menu name for action context
	title=mname

	#key definition MOVE TO GLOBAL
	key={}
	key['key1']=5 #should be 21, only cuz key1 is broken on menona
	key['key2']=20
	key['key3']=16

	key['left']=5 
	key['up']=6
	key['press']=13
	key['down']=19
	key['right']=26

	#initial settings
	keys={}
	pos=1
	apos=0
	vpos=0
	vmax=0

	if len(mlist)>5:
		print "long list"
		
		vmax=len(mlist)-5

	while True:
		
		#vlist=mlist[vpos:vpos+5]		


		dispListMenu(device,title,mlist,alist,pos,0,vpos)
		time.sleep(.3)

		#keys=getKeys(keys)
		if GPIO.event_detected(key['down']):
			#pos=pos+1
			if pos==5 and vpos<vmax:
				vpos+=1
			else:
				pos=posDown(pos)
				if pos==1:vpos=0
			#dispListMenu(device,title,mlist,alist,pos)

		elif GPIO.event_detected(key['up']):
			#pos=pos+1
			if pos==1 and vpos>0:
				vpos-=1
			else:
				pos=posUp(pos,5)
				if pos==5:vpos=vmax
			#dispListMenu(device,title,mlist,alist,pos)

		elif GPIO.event_detected(key['key2']):
			dispListMenu(device,title,mlist,alist,pos,apos,vpos)
			cont=actionhandler(device,pos+vpos,apos,mname)
			apos=1
			if cont==1 : apos=0

			time.sleep(.01)
			
			#action loop
			
			done=0
			while done==0:
				
				dispListMenu(device,title,mlist,alist,pos,apos,vpos)

				#keys=getKeys(keys)

				if GPIO.event_detected(key['down']):
					#pos=pos+1
					apos=posDown(apos,3)
					dispListMenu(device,title,mlist,alist,pos,apos,vpos)

				elif GPIO.event_detected(key['up']):
					#pos=pos+1
					apos=posUp(apos,3)
					dispListMenu(device,title,mlist,alist,pos,apos,vpos)

				elif GPIO.event_detected(key['key2']):
					esc=actionhandler(device,pos+vpos,apos,mname,vpos)
					if esc==1 : return

					#time.sleep(.2)
				elif GPIO.event_detected(key['key1']):
					done=1
			
				time.sleep(.01)

		elif GPIO.event_detected(key['key1']):
			dispListMenu(device,title,mlist,alist,pos)
			time.sleep(.1)
			return

		#time.sleep(.1)

def posUp(pos,lmax=5):
	if pos != 1:
		pos=pos-1
	else:
		pos=lmax
	return pos

def posDown(pos,lmax=5):
	if pos != lmax:
		pos+=1
	else:
		pos=1
	return pos

def dispListMenu(device,title,plist,alist,pos,apos=0,vpos=999):
	
	if vpos!=999:
		mlist=plist[vpos:vpos+5]
	else:
		mlist=plist



	#offsets
	xdist=5 #x offset
	yoffset=4
	
	#menu
	width=100 #width of hilight
	#mlist=["list1", "list2","list3","list4","list5"] #will be parameter
	mlistc=["white"]*len(mlist)
	if pos != 0: #setup cursor
		mlistc[pos-1]="black"

	#action menu
	axdist=64
	#alist=["action1", "action2","action3"]
	alistc=["white"]*len(alist)
	if apos != 0:
		alistc[apos-1]="black"



	with canvas(device) as draw:

		#draw title
		draw.rectangle((0,0,128,12), outline="white", fill="white")
		#draw.rectangle((1,10,126,11), outline="black", fill="black")
		draw.text((2,0),title,"black")

		if os.path.exists("/media/pi/OP1")==1:
			draw.rectangle((116,2,124,10), outline="black", fill="black")
		else:
			draw.rectangle((116,2,124,10), outline="black", fill="white")

		if pos != 0:
			draw.rectangle((xdist, pos*10+yoffset, xdist+width, (pos*10)+10+yoffset), outline="white", fill="white")
		
		for idx,line in enumerate(mlist):
			#print("idx: ",idx,"line: ",line,"fill: ",flist[idx])
			draw.text((xdist,(idx+1)*10+yoffset),line,mlistc[idx])

		if apos != 0:

			draw.rectangle((60,13,128,64), outline="black", fill="black")
			draw.rectangle((60,13,61,48), outline="white", fill="white")

			draw.rectangle((axdist, apos*10+yoffset, axdist+width, (apos*10)+10+yoffset), outline="white", fill="white")
		
			for idx,line in enumerate(alist):
				#print("idx: ",idx,"line: ",line,"fill: ",flist[idx])
				draw.text((axdist,(idx+1)*10+yoffset),line,alistc[idx])

def actionhandler(device,pos,apos,mname,draw=0):
	#returning 1 escapes calling function to return
	if mname=="MAIN":
		if pos==1 and apos==0:
			print 'main: tape menu'
			#MAIN MENU
			tapeMenu(device)
			return(1)
		elif pos==2:
			backupTape(device)

		elif pos==3:
			sampleMenu(device)

		elif pos==4: 
			midiMenu(device)

		elif pos==5 and apos==0:
			testMenu(device)
			#run_cmd("sudo python ui.py -i spi -d sh1106 -r 2 &")


			return(1)
	elif mname=="MAIN>TAPES":
		print "tape actions @POS: ",pos,", apos: ",apos
		if pos==1 and apos==1:
			loadTape(device,"/home/pi/Desktop/tapes/recycling bin v1/tape")
		elif pos==2 and apos==1:
			loadTape(device,"/home/pi/Desktop/tapes/recycling bin v2")
		elif pos==3 and apos==1:
			loadTape(device,"/home/pi/Desktop/op1-tapebackups/primarily pentatonic")
		elif pos==4 and apos==1:
			loadTape(device,"/home/pi/Desktop/op1-tapebackups/2018-02-24")
		elif pos==5 and apos==1:
			loadTape(device,"/home/pi/Desktop/op1-tapebackups/lets start with guitar this time")
		elif pos==6 and apos==1:
			loadTape(device,"/home/pi/Desktop/op1-tapebackups/2018-03-25")

	elif mname=="MAIN>SAMPLES":	
		# 	mlist=["josh", "courtyard","dawless","cmix","more"]
		# 	alist=["load", "unload","[empty]"]

		sampleList=[
		["_josh","/home/pi/Desktop/samplepacks/josh/"],
		["courtyard","/home/pi/Desktop/samplepacks/courtyard/"],
		["dawless","/home/pi/Desktop/samplepacks/dawless/"],
		["C-MIX","/home/pi/Desktop/samplepacks/C-MIX/"],
		["inkd","/home/pi/Desktop/samplepacks/op1_3.2/inkdd/"],
		["Dark Energy","/home/pi/Desktop/samplepacks/op1_3.2/Dark Energy/"],
		["memories","/home/pi/Desktop/samplepacks/CUCKOO OP-1 MEGA PACK/CUCKOO OP-1 MEGA PACK/OP-1 patches/Put in synth/memories/"],
		["opines","/home/pi/Desktop/samplepacks/CUCKOO OP-1 MEGA PACK/CUCKOO OP-1 MEGA PACK/OP-1 patches/Put in synth/opines/"]


		]

		print "sample actions",pos
		if pos==1 or 2 or 3 or 4 or 5 or 6 or 7:
			spath="/home/pi/Desktop/samplepacks/josh/"
			spath=sampleList[pos-1][1]
			if apos==1:
				loadUnloadSample(device,spath,sampleList[pos-1][0],"load")
			elif apos==2:
				loadUnloadSample(device,spath,sampleList[pos-1][0],"delete")
		# elif pos==2:
		# 	spath="/home/pi/Desktop/samplepacks/courtyard/"
		# 	if apos==1:
		# 		loadUnloadSample(device,spath,"courtyard","load")
		# 	elif apos==2:
		# 		loadUnloadSample(device,spath,"courtyard","delete")
		# elif pos==3:
		# 	spath="/home/pi/Desktop/samplepacks/dawless/"
		# 	if apos==1:
		# 		loadUnloadSample(device,spath,"dawless","load")
		# 	elif apos==2:
		# 		loadUnloadSample(device,spath,"dawless","delete")
		# elif pos==4:
		# 	spath="/home/pi/Desktop/samplepacks/C-MIX/"
		# 	if apos==1:
		# 		loadUnloadSample(device,spath,"C-MIX","load")
		# 	elif apos==2:
		# 		loadUnloadSample(device,spath,"C_MIX","delete")

	elif mname=="MAIN>MIDI":
		print "midi actions"
		if pos==1:
			midiSrc="14"
			midiDst="20"
		elif pos==2:
			midiSrc="20"
			midiDst="14"
		elif pos==3:
			midiSrc="20"
			midiDst="24"
		elif pos==4:
			midiSrc="24"
			midiDst="20"


		out=run_cmd('sudo aconnect '+midiSrc+" "+midiDst)
		drawText(device,[out,"done"])
		time.sleep(1)

	elif mname=="MENU>TEST":
		print "test actions"
		#print pos
		#mlist=["test1","test2","test3","test4","test5","test6","test7"]
		#print mlist[pos-1]





	return(0)

def tapeMenu(device):
	mlist=["recycling bin v1", "recycling bin v2","primarily pentatonic","2018-02-24","lets start with guitar this time","spaceman"]
	alist=["load", "[empty]","[empty]"]
	listMenuScroll(device,mlist,alist,"MAIN>TAPES")


def sampleMenu(device):
	mlist=["josh", "courtyard","dawless","cmix","inkd","Dark Energy","memories","opines"]
	alist=["load", "unload","[empty]"]
	listMenuScroll(device,mlist,alist,"MAIN>SAMPLES")	

def drawText(device,textlist):
	with canvas(device) as draw:
		for idx,text in enumerate(textlist):
			#print text, ", ", idx
			draw.text((0,idx*10),text,"white")

def midiMenu(device):
	
	output = run_cmd('sudo aconnect -i -o')
	outlines=output.splitlines()
	drawText(device,outlines)
	wait({},"key2")
	time.sleep(1)


	mlist=["14:20", "20:14","20:24","24:20"]
	alist=["go", "[empty]","[empty]"]
	listMenu(device,mlist,alist,"MAIN>MIDI")


def backupTape(device):
	keys={}
	# with canvas(device) as draw:

	if os.path.exists("/media/pi/OP1")==1:

		# with canvas(device) as draw:
		# 	draw.text((0,0),"op1 connection success","white")
		# 	draw.text((0,10),"backup track?","white")
		# 	draw.text((0,20),"1-back","white")
		# 	draw.text((0,30),"2-yes","white")
		
		# time.sleep(1)
		drawText(device,["op1 connection success","backup tape?","1-back","2-yes"])

			# 			# sh.copy(spath4,dpath)
			# draw.text((0,40),"Track 4 copied","white")


		print "op1 connection success"
		print "Backup Track?"
		print "  1-back"
		print "  2-continue"

		
		#response loop
		while True:
			keys=getKeys(keys)
			if keys['key2']==0:
				print "copying"
				#draw.text((0,10),"copying","white")
				#draw.text((0,20),"Backup tape?","white")
				#Copy Operation
				dpath='/home/pi/Desktop/op1-tapebackups/'+str(datetime.date.today())
				spath1='/media/pi/OP1/tape/track_1.aif'
				spath2='/media/pi/OP1/tape/track_2.aif'
				spath3='/media/pi/OP1/tape/track_3.aif'
				spath4='/media/pi/OP1/tape/track_4.aif'


				if os.path.exists(dpath)==0:
					os.mkdir(dpath)
				
				# if os.path.exists(spath)==1:
				# 	term.println('file exists')
				# 	time.sleep(.5)
				# 	return   					can't check this now. assuming source directory is real
				
				sh.copy(spath1,dpath)
				print 'Track 1 Copied'
				drawText(device,["track 1 copied"])

				sh.copy(spath2,dpath)
				print 'Track 2 Copied'
				drawText(device,["track 1 copied","track 2 copied"])

				sh.copy(spath3,dpath)
				print 'Track 3 Copied'
				drawText(device,["track 1 copied","track 2 copied","track 3 copied"])

				sh.copy(spath4,dpath)
				print 'Track 4 Copied'
				drawText(device,["track 1 copied","track 2 copied","track 3 copied","track 4 copied"])


				time.sleep(.5)
				return

			elif keys['key1']==0:
				return
	else:
		print "no op1 detcted"
		print "Is your device connected and in disk mode?"
		print "  1-Return to Menu"
		with canvas(device) as draw:
			draw.text((0,10),"no op1 found","white")
			draw.text((0,20),"1-return to menu","white")
		#term.println("  2-Menu")

		wait(keys,'key1')
		return

def loadTape(device,source):
	keys={}
	time.sleep(1)

	if os.path.exists("/media/pi/OP1")==1:
		
		print "op1 connection success"
		print "Backup Track?"
		print "  1-Yes"
		print "  2-No"

		drawText(device,["op1 connection success","load tape?","1-back","2-yes"])


		#response loop
		while True:
			keys=getKeys(keys)
			if keys['key2']==0:
				print "copying"


				#Copy Operation
				spath1=source+"/track_1.aif"
				spath2=source+"/track_2.aif"
				spath3=source+"/track_3.aif"
				spath4=source+"/track_4.aif"

				dpath='/media/pi/OP1/tape'

				dpath1='/media/pi/OP1/tape/track_1.aif'
				dpath2='/media/pi/OP1/tape/track_2.aif'
				dpath3='/media/pi/OP1/tape/track_3.aif'
				dpath4='/media/pi/OP1/tape/track_4.aif'

				os.remove(dpath1)
				os.remove(dpath2)
				os.remove(dpath3)
				os.remove(dpath4)

				#if os.path.exists(dpath)==0:
				#	os.mkdir(dpath)
				
				# if os.path.exists(spath)==1:
				# 	term.println('file exists')
				# 	time.sleep(.5)
				# 	return   					can't check this now. assuming source directory is real
				
				sh.copy(spath1,dpath)
				print 'Track 1 Copied'
				drawText(device,["track 1 copied"])

				sh.copy(spath2,dpath)
				print 'Track 2 Copied'
				drawText(device,["track 1 copied","track 2 copied"])

				sh.copy(spath3,dpath)
				print 'Track 3 Copied'
				drawText(device,["track 1 copied","track 2 copied","track 3 copied"])

				sh.copy(spath4,dpath)
				print 'Track 4 Copied'
				drawText(device,["track 1 copied","track 2 copied","track 3 copied","track 4 copied"])





				time.sleep(.5)
				return

			elif keys['key1']==0:
				return
	else:
		print "no op1 detcted"
		print "Is your device connected and in disk mode?"
		print "  1-Return to Menu"

		drawText(device,["no op1 found","1-return to menu"])
		#term.println("  2-Menu")

		wait(keys,'key1')
		return

def loadUnloadSample(device,spath,name,op):
	keys={}
	time.sleep(1)

	#op: "load"-load to op1	"del"-delete from op1

	# term.clear()
	# term.println("Load/Unload?")
	# term.println("  1-load")
	# term.println("  2-unload")
	# term.println("  3-back")
	# drawText([])
	if os.path.exists("/media/pi/OP1")==1:
		
		print "op1 connection success"


		drawText(device,["op1 connection success","you sure?","1-back","2-yes"])


		while True:
			keys=getKeys()
			if keys['key2']==0:
				print "copying"

				dpath="/media/pi/OP1/synth/_" + str(name) + "/"

				print spath,">",dpath
						
				if op=="load":
					print "copying"
					copytree(spath,dpath)
					return
					
				elif op=="delete":
					#sampleLoadMenu(term,keys)
					sh.rmtree(dpath)
					print name+' pack deleted'
					return


			elif keys['key1']==0:
				return
	else:
		print "no op1 detcted"
		print "Is your device connected and in disk mode?"
		print "  1-Return to Menu"

		drawText(device,["no op1 found","1-return to menu"])
		#term.println("  2-Menu")

		wait(keys,'key1')


def main():
	device=init()

	#MAIN MENU
	mlist=["load tape", "backup tape","sample packs","midi","listMenuScroll"]
	alist=["action1", "action2","action3"]
	listMenu(device,mlist,alist,"MAIN")



main()
