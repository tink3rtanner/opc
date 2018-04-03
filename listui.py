from luma.core.interface.serial import spi
from luma.core.render import canvas
from luma.oled.device import sh1106
import time,os,datetime
import RPi.GPIO as GPIO
import shutil as sh
from subprocess import *

#GLOBALS

#KEYS
key={}
key['key1']=5 #broken on menona
key['key2']=20
key['key3']=16

key['left']=5 
key['up']=6
key['press']=13
key['down']=19
key['right']=26


lowBat=4


#LIST OF SAMPLE PACKS AND PATHS
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
#List of tapes an paths
tapeList=[
		["recycling bin v1","/home/pi/Desktop/tapes/recycling bin v1/tape"],
		["recycling bin v2","/home/pi/Desktop/tapes/recycling bin v2"],
		["fun with sequencers","/home/pi/Desktop/op1-tapebackups/fun with sequencers"],
		["lofi family","/home/pi/Desktop/op1-tapebackups/lofi family"],
		["primarily pentatonic","/home/pi/Desktop/op1-tapebackups/primarily pentatonic"],
		["2018-02-24","/home/pi/Desktop/op1-tapebackups/2018-02-24"],
		["lets start with guitar","/home/pi/Desktop/op1-tapebackups/lets start with guitar this time"],
		["spaceman","/home/pi/Desktop/op1-tapebackups/2018-03-25"],

		]


def init():

	serial = spi(device=0, port=0)
	device = sh1106(serial,rotate=2)
	
	initgpio()

	#boot logo!
	drawText(device,['','         OPC         ','','     tink3rtanker    '])
	time.sleep(2)


	return device

def initgpio():

	print "Initializing GPIO"
	#Initialize GPIO
	GPIO.setmode(GPIO.BCM)
	

	#GPIO.setup(key['key1'], GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(key['key2'], GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(key['key3'], GPIO.IN, pull_up_down=GPIO.PUD_UP)

	GPIO.setup(key['left'], GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(key['up'], GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(key['press'], GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(key['down'], GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(key['right'], GPIO.IN, pull_up_down=GPIO.PUD_UP)
	
	#LIPO LOW BATTERY
	GPIO.setup(lowBat, GPIO.IN,pull_up_down=GPIO.PUD_UP)

	#GPIO.add_event_detect(key['key1'], GPIO.FALLING)
	GPIO.add_event_detect(key['key2'], GPIO.FALLING,bouncetime=300)
	GPIO.add_event_detect(key['key3'], GPIO.FALLING,bouncetime=300)
	GPIO.add_event_detect(key['left'], GPIO.FALLING,bouncetime=300)
	GPIO.add_event_detect(key['up'], GPIO.FALLING,bouncetime=300)
	GPIO.add_event_detect(key['press'], GPIO.FALLING,bouncetime=300)
	GPIO.add_event_detect(key['down'], GPIO.FALLING,bouncetime=300)
	GPIO.add_event_detect(key['right'], GPIO.FALLING,bouncetime=300)

def wait(keys,waitkey):

	done=0
	while done==0:
		if GPIO.event_detected(key[waitkey]):
			done=1
		time.sleep(.01)
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

def sysMenu(device):
	alist=["go", "[empty]","[empty]"]
	mlist=["wireless","reboot","nest test","test4","test5","test6","test7","asdf","asdfg","more tests"]

	listMenuScroll(device,mlist,alist,"MAIN>SYS")

def nestMenu(device):
	alist=["[empty]", "[empty]","[empty]"]
	mlist=["nest test!","test5d","test6","test7","asdf","asdfg","more tests"]

	listMenuScroll(device,mlist,alist,"MAIN>SYS>NEST")

def listMenuScroll(device,mlist,alist,mname,draw=0,actions=False,exit=True):
	#mlist: menu list
	#alist: action list
	#mname: menu name for action context
	title=mname

	#key definition MOVE TO GLOBAL

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
			#dispListMenu(device,title,mlist,alist,pos,apos,vpos)
			actionhandler(device,pos+vpos,apos,mname)
			
			
			if actions==True:
				done=0
				apos=1
			else:
				done=1
				apos=0


			#action loop
			
			#done=0
			while done==0:
				
				dispListMenu(device,title,mlist,alist,pos,apos,vpos)

				if GPIO.event_detected(key['down']):
					#pos=pos+1
					apos=posDown(apos,3)
					dispListMenu(device,title,mlist,alist,pos,apos,vpos)

				elif GPIO.event_detected(key['up']):
					#pos=pos+1
					apos=posUp(apos,3)
					dispListMenu(device,title,mlist,alist,pos,apos,vpos)

				elif GPIO.event_detected(key['key2']):
					actionhandler(device,pos+vpos,apos,mname,vpos)
					apos=0
					done=1

					#time.sleep(.2)
				# back exit
				elif GPIO.event_detected(key['key1']):
					done=1
					apos=0
			
				time.sleep(.01)


		#// EXIT STRATEGY
		


		elif GPIO.event_detected(key['key1']):
			if exit==True:

				return

		time.sleep(.01)

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

		# // STATUS BAR //

		if os.path.exists("/media/pi/OP1")==1:
			draw.rectangle((116,2,124,10), outline="black", fill="black")
		else:
			draw.rectangle((116,2,124,10), outline="black", fill="white")

		if GPIO.event_detected(lowBat):
			draw.rectangle((96,3,108,9), outline="black", fill="black")
		else:
			draw.rectangle((96,3,108,9), outline="black", fill="white")




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
	print 'action handler @',mname
	print "pos: ",pos,"apos" ,apos


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
			sysMenu(device)
			#run_cmd("sudo python ui.py -i spi -d sh1106 -r 2 &")


			return(1)
	elif mname=="MAIN>TAPES":
		print "tape actions @POS: ",pos,", apos: ",apos	

		if apos==1: #assuming pos is valid becasue menuList was built from tapeList
			loadTape(device,tapeList[pos-1][1])

	elif mname=="MAIN>SAMPLES":	

		

		#if pos==1 or 2 or 3 or 4 or 5 or 6 or 7: 
		#assuming pos is valid bc was built from sampleList
		spath=sampleList[pos-1][1]
		if apos==1:
			loadUnloadSample(device,spath,sampleList[pos-1][0],"load")
		elif apos==2:
			loadUnloadSample(device,spath,sampleList[pos-1][0],"delete")

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

	elif mname=="MAIN>SYS":

		if pos==1:
			
			getip="ip addr show wlan0 | grep inet | awk '{print $2}' | cut -d/ -f1"
			netstat=run_cmd(getip)
			ip=netstat[:-27]

			print("wlan0 status")
			print ip

			drawText(device,["wlan0 status",ip])
			wait({},"key3")
		# 	term.println(ip)
		elif pos==2: #reboot
			drawText(device,['rebooting...'])
			run_cmd("sudo reboot")
			return

		elif pos==3:
			print 'nestTest'
			nestMenu(device)


	return(0)

def tapeMenu(device):
	mlist=[]
	for item in tapeList: #build menu list from tapeList global
		mlist.append(item[0])
	#mlist=["recycling bin v1", "recycling bin v2","primarily pentatonic","2018-02-24","lets start with guitar this time","spaceman"]
	alist=["load", "[empty]","[empty]"]
	listMenuScroll(device,mlist,alist,"MAIN>TAPES",None,True)

def sampleMenu(device):
	#mlist=["josh", "courtyard","dawless","cmix","inkd","Dark Energy","memories","opines"]
	mlist=[]
	for item in sampleList: #build menu list from sampleList global
		mlist.append(item[0])

	alist=["load", "unload","[empty]"]
	listMenuScroll(device,mlist,alist,"MAIN>SAMPLES",None,True)	

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
	listMenuScroll(device,mlist,alist,"MAIN>MIDI")

def backupTape(device):

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
			if GPIO.event_detected(key['key2']):
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
				drawText(device,["copying..."])

				sh.copy(spath1,dpath)
				print 'Track 1 Copied'
				drawText(device,["copying...","track 1 copied"])

				sh.copy(spath2,dpath)
				print 'Track 2 Copied'
				drawText(device,["copying...","track 1 copied","track 2 copied"])

				sh.copy(spath3,dpath)
				print 'Track 3 Copied'
				drawText(device,["copying...","track 1 copied","track 2 copied","track 3 copied"])

				sh.copy(spath4,dpath)
				print 'Track 4 Copied'
				drawText(device,["copying...","track 1 copied","track 2 copied","track 3 copied","track 4 copied"])


				time.sleep(.5)
				return

			elif GPIO.event_detected(key['key1']):
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
			if GPIO.event_detected(key['key2']):
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
				# 	return   					
				# can't check this now. assuming source directory is real

				
				drawText(device,["copying..."])

				sh.copy(spath1,dpath)
				print 'Track 1 Copied'
				drawText(device,["copying...","track 1 copied"])

				sh.copy(spath2,dpath)
				print 'Track 2 Copied'
				drawText(device,["copying...","track 1 copied","track 2 copied"])

				sh.copy(spath3,dpath)
				print 'Track 3 Copied'
				drawText(device,["copying...","track 1 copied","track 2 copied","track 3 copied"])

				sh.copy(spath4,dpath)
				print 'Track 4 Copied'
				drawText(device,["copying...","track 1 copied","track 2 copied","track 3 copied","track 4 copied"])





				time.sleep(.5)
				return

			elif GPIO.event_detected(key['key1']):
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
			if GPIO.event_detected(key['key2']):
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


			elif GPIO.event_detected(key['key1']):
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
	mlist=["tape deck", "backup tape","sample packs","midi","system"]
	alist=["action1", "action2","action3"]
	listMenuScroll(device,mlist,alist,"MAIN",None,None,False) #no exit


main()
