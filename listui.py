from luma.core.interface.serial import spi
from luma.core.render import canvas
from luma.oled.device import sh1106
import time,os,datetime
import RPi.GPIO as GPIO
import shutil as sh
import usb.core
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

VENDOR = 0x2367
PRODUCT = 0x0002
MOUNT_DIR = "/media/op1"
USBID_OP1 = "*Teenage_OP-1*"

op1path=MOUNT_DIR
homedir="/home/pi/opc"


#LIST OF SAMPLE PACKS AND PATHS
sampleListSynth=[
		["_josh","/home/pi/opc/samplepacks/_josh/"],
		["courtyard","/home/pi/opc/samplepacks/courtyard/"],
		["dawless","/home/pi/opc/samplepacks/dawless/"],
		["C-MIX","/home/pi/opc/samplepacks/C-MIX/"],
		["inkd","/home/pi/opc/samplepacks/op1_3.2/inkdd/"],
		["Dark Energy","/home/pi/opc/samplepacks/op1_3.2/Dark Energy/"],
		["memories","/home/pi/opc/samplepacks/CUCKOO OP-1 MEGA PACK/CUCKOO OP-1 MEGA PACK/OP-1 patches/Put in synth/memories/"],
		["opines","/home/pi/opc/samplepacks/CUCKOO OP-1 MEGA PACK/CUCKOO OP-1 MEGA PACK/OP-1 patches/Put in synth/opines/"],
		["vanilla sun","/home/pi/opc/samplepacks/vanilla sun/"],
		["mellotron","/home/pi/opc/samplepacks/mellotronAifs/"],
		["hs dsynth","/home/pi/opc/samplepacks/hs dsynth vol1/"],
		["cassette","/home/pi/opc/samplepacks/cassette/"],
		["SammyJams","/home/pi/opc/samplepacks/SammyJams Patches"]



		]

sampleListSynth=[["test","test"]]
sampleListDrum=[["test","test"]]

#List of tapes and paths
tapeList=[
		["recycling bin v1","/home/pi/Desktop/tapes/recycling bin v1/tape"],
		["recycling bin v2","/home/pi/Desktop/tapes/recycling bin v2"],
		["fun with sequencers","/home/pi/Desktop/op1-tapebackups/fun with sequencers"],
		["lofi family","/home/pi/Desktop/op1-tapebackups/lofi family"],
		["primarily pentatonic","/home/pi/Desktop/op1-tapebackups/primarily pentatonic"],
		["2018-02-24","/home/pi/Desktop/op1-tapebackups/2018-02-24"],
		["lets start with guitar","/home/pi/Desktop/op1-tapebackups/lets start with guitar this time"],
		["spaceman","/home/pi/Desktop/op1-tapebackups/2018-03-25"],
		["slow & somber","/home/pi/Desktop/op1-tapebackups/slow & somber"],
		["cool solo","/home/pi/Desktop/op1-tapebackups/cool solo"],
		["technical advantage","/home/pi/Desktop/op1-tapebackups/technical advantage"],
		["heartbeat slide","/home/pi/Desktop/op1-tapebackups/heartbeat slide"]

		]
#print tapeList
keys={}

tapeList=[["test","test"]]

# INITIALIZATION

def init():

	serial = spi(device=0, port=0)
	device = sh1106(serial,rotate=2)
	drawText(device,['Initializing GPIO'])
	initgpio()
	drawText(device,['Initializing GPIO',"Scanning Tapes"])
	scanTapes(device)
	drawText(device,['Initializing GPIO',"Scanning Tapes","Scanning Samples"])
	scanSamples("dummy")
	drawText(device,['Initializing GPIO',"Scanning Tapes","Scanning Samples","done."])

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


# SYSTEM UTILITIES

def run_cmd(cmd):
	p = Popen(cmd, shell=True, stdout=PIPE)
	output = p.communicate()[0]
	return output

def is_connected():
  return usb.core.find(idVendor=VENDOR, idProduct=PRODUCT) is not None

def getmountpath():
  o = os.popen('readlink -f /dev/disk/by-id/' + USBID_OP1).read()
  if USBID_OP1 in o:
    raise RuntimeError("Error getting OP-1 mount path: {}".format(o))
  else:
    return o.rstrip()

def mountdevice(source, target, fs, options=''):
  ret = os.system('mount {} {}'.format(source, target))
  if ret not in (0, 8192):
    raise RuntimeError("Error mounting {} on {}: {}".format(source, target, ret))

def unmountdevice(target):
  ret = os.system('umount {}'.format(target))
  if ret != 0:
    raise RuntimeError("Error unmounting {}: {}".format(target, ret))

def forcedir(path):
  if not os.path.isdir(path):
    os.makedirs(path)

# UI UTILITES

def wait(keys,waitkey):

	done=0
	while done==0:
		if GPIO.event_detected(key[waitkey]):
			done=1
		time.sleep(.01)
	return

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
			if apos==1:
				sampleMenuSynth(device)
			if apos==2:
				sampleMenuDrum(device)

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

	elif mname=="MAIN>SYNTH SAMPLES":	
		
		#if pos==1 or 2 or 3 or 4 or 5 or 6 or 7: 
		#assuming pos is valid bc was built from sampleList
		spath=sampleListSynth[pos-1][1]
		dpath=op1path+"/synth/_" + str(sampleListSynth[pos-1][0]) + "/"
		if apos==1:
			loadUnloadSample(device,spath,dpath,sampleListSynth[pos-1][0],"load")
		elif apos==2:
			loadUnloadSample(device,spath,dpath,sampleListSynth[pos-1][0],"delete")

	elif mname=="MAIN>DRUM SAMPLES":	
		
		#if pos==1 or 2 or 3 or 4 or 5 or 6 or 7: 
		#assuming pos is valid bc was built from sampleList
		spath=sampleListDrum[pos-1][1]
		dpath=op1path+"/drum/_" + str(sampleListDrum[pos-1][0]) + "/"
		if apos==1:
			loadUnloadSample(device,spath,dpath,sampleListDrum[pos-1][0],"load")
		elif apos==2:
			loadUnloadSample(device,spath,dpath,sampleListDrum[pos-1][0],"delete")

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

		elif pos==4:
			print 'loading firmware'
			loadFirmware(device)


	return(0)


# DISPLAY UTILITIES

def listMenuScroll(device,mlist,alist,mname,draw=0,actions=False,exit=True):
	#mlist: menu list
	#alist: action list
	#mname: menu name for action context
	title=mname
	print mlist

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

		if is_connected()==1:
			draw.rectangle((116,2,124,10), outline="black", fill="black")
		else:
			draw.rectangle((116,2,124,10), outline="black", fill="white")

		# if GPIO.event_detected(lowBat):
		# 	draw.rectangle((96,3,108,9), outline="black", fill="black")
		# else:
		# 	draw.rectangle((96,3,108,9), outline="black", fill="white")




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

def drawText(device,textlist):
	with canvas(device) as draw:
		for idx,text in enumerate(textlist):
			#print text, ", ", idx
			draw.text((0,idx*10),text,"white")



# MENUS

def sampleMenuSynth(device):
	#mlist=["josh", "courtyard","dawless","cmix","inkd","Dark Energy","memories","opines"]
	mlist=[]
	for item in sampleListSynth: #build menu list from sampleList global
		print item
		mlist.append(item[0])

	alist=["load", "unload","[empty]"]
	listMenuScroll(device,mlist,alist,"MAIN>SYNTH SAMPLES",None,True)

def sampleMenuDrum(device):
	#mlist=["josh", "courtyard","dawless","cmix","inkd","Dark Energy","memories","opines"]
	mlist=[]
	for item in sampleListDrum: #build menu list from sampleList global
		print item
		mlist.append(item[0])

	alist=["load", "unload","[empty]"]
	listMenuScroll(device,mlist,alist,"MAIN>DRUM SAMPLES",None,True)	

def tapeMenu(device):
	#print "building menu list"
	mlist=[]
	for item in tapeList: #build menu list from tapeList global
		mlist.append(item[0])
	#mlist=["recycling bin v1", "recycling bin v2","primarily pentatonic","2018-02-24","lets start with guitar this time","spaceman"]
	
	alist=["load", "[empty]","[empty]"]
	listMenuScroll(device,mlist,alist,"MAIN>TAPES",None,True)

	if ['test', 'test'] in tapeList: 
		tapeList.remove(['test','test'])

def midiMenu(device):
	
	output = run_cmd('sudo aconnect -i -o')
	outlines=output.splitlines()
	drawText(device,outlines)
	wait({},"key2")
	time.sleep(1)


	mlist=["14:20", "20:14","20:24","24:20"]
	alist=["go", "[empty]","[empty]"]
	listMenuScroll(device,mlist,alist,"MAIN>MIDI")

def sysMenu(device):
	alist=["go", "[empty]","[empty]"]
	mlist=["wireless","reboot","nest test","load firmware","rename op1","test6","test7","asdf","asdfg","more tests"]

	listMenuScroll(device,mlist,alist,"MAIN>SYS")

def nestMenu(device):
	alist=["[empty]", "[empty]","[empty]"]
	mlist=["nest test!","test5d","test6","test7","asdf","asdfg","more tests"]

	listMenuScroll(device,mlist,alist,"MAIN>SYS>NEST")



# FILE OPERATIONS

def backupTape(device):

	if os.path.exists(op1path)==1:

		# with canvas(device) as draw:
		# 	draw.text((0,0),"op1 connection success","white")
		# 	draw.text((0,10),"backup track?","white")
		# 	draw.text((0,20),"1-back","white")
		# 	draw.text((0,30),"2-yes","white")
		
		# time.sleep(1)
		drawText(device,["op1 connection success","backup tape?"," -yup"," -back"])

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

	if os.path.exists(op1path)==1:
		
		print "op1 connection success"
		print "Backup Track?"
		print "  1-Yes"
		print "  2-No"

		drawText(device,["op1 connection success","load tape?"," - back","2-yes"])


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

def loadUnloadSample(device,spath,dpath,name,op):
	keys={}
	time.sleep(1)

	#op: "load"-load to op1	"del"-delete from op1

	# term.clear()
	# term.println("Load/Unload?")
	# term.println("  1-load")
	# term.println("  2-unload")
	# term.println("  3-back")
	# drawText([])
	if is_connected():
		forcedir(MOUNT_DIR)
		mountpath = getmountpath()
		print(" > OP-1 device path: %s" % mountpath)
		mountdevice(mountpath, MOUNT_DIR, 'ext4', 'rw')
		print(" > Device mounted at %s" % MOUNT_DIR)

	if os.path.exists(op1path)==1:
		
		print "op1 connection success"


		drawText(device,["op1 connection success","you sure?","1-back","2-yes"])


		while True:
			if GPIO.event_detected(key['key2']):
				print "copying"

				

				
				print spath,">",dpath
						
				if op=="load":
					print "copying"
					copytree(spath,dpath)
					print(" > Unmounting OP-1")
					unmountdevice(MOUNT_DIR)
					print(" > Done.")
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

def loadFirmware(device):
	if os.path.exists("/media/pi/OP-1")==1:
		drawText(device,["op1 connection success","load firmware?"," -yup"," -back"])
		while True:
			if GPIO.event_detected(key['key2']):
				print "copying firmware"
				drawText(device,["copying firmware..."])
				spath="/home/pi/Desktop/misc/op1_225.op1"
				dpath="/media/pi/OP-1/"
				sh.copy(spath,dpath)
				return


			elif GPIO.event_detected(key['key1']):
				return


	else:
		drawText(device,["op1 not detected","","returning to menu..."])
		time.sleep(1)
		return

def scanTapes(device):
	#directory="/home/pi/Desktop/op1-tapebackups/"
	directory=homedir+"/op1-tapebackups/"

	print
	print "updating tape index"
	
	#tapelist=[
	# 	["recycling bin v1","/home/pi/Desktop/tapes/recycling bin v1/tape"],
	# 	["recycling bin v2","/home/pi/Desktop/tapes/recycling bin v2"]
	# 	]

	for filename in os.listdir(directory):
		#print filename
		fullPath = directory + filename
		tapeList.append([filename,fullPath])
	    #if filename.endswith(".atm") or filename.endswith(".py"): 

	print 
	print "[TAPES]"
	print tapeList

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

def scanSamples(directory):
	#scans sample packs in a path and updates sample lists
	print
	print "Scanning for samplepacks"

	directory="/home/pi/opc/samplepacks/"
	for file in os.listdir(directory):
		fullPath = directory + file
		if os.path.isdir(fullPath):
			#print
			#print "directory: ",file
			#print fullPath

			containsAif=0
			#each folder in parent directory
			for subfile in os.listdir(fullPath):
				subfullPath=fullPath+"/"+subfile
				#a path within a path
				#print "SUBFILE: ",subfile
				if os.path.isdir(subfullPath):

					if subfile=="synth" or "drum":
						#print "nested directories, but it's okay cuz you named them"
						pack=readAifDir(subfile,subfullPath)
						pack[2]["_types"]=subfile #if in synth or drum folder, override type
						pack[0]=file
						#pack[1]=fullPath

						if pack[2]["_types"]=='synth':
							sampleListSynth.append(pack)
						elif pack[2]["_types"]=='drum':
							sampleListDrum.append(pack)

				elif subfile.endswith(".aif") or subfile.endswith(".aiff"):
					containsAif=1
				elif subfile.endswith(".DS_Store"):
					continue
				else:
					print "what's going on here. name your folders or hold it with the nesting"
					print "SUBFILE: ",subfile
			if containsAif==1:
				pack=readAifDir(file,fullPath)
				if pack[2]["_types"]=='synth':
					sampleListSynth.append(pack)
				elif pack[2]["_types"]=='drum':
					sampleListDrum.append(pack)

		# else:
		# 	sampleList.append([file,fullPath]) #adds file andfullpath to samplelist
	 #    #if file.endswith(".atm") or file.endswith(".py"): 

	if ['test', 'test'] in sampleListSynth: 
		sampleListSynth.remove(['test','test'])
	if ['test', 'test'] in sampleListDrum: 
		sampleListDrum.remove(['test','test'])

	print
	print "[SYNTH PACKS]"
	print sampleListSynth
	print
	print "[DRUM PACKS]"
	print sampleListDrum


	# for sample in sampleList:
	# 	print
	# 	print sample[1] #fullpath
	# 	atts=readAif(sample[1]) #reads aiff and gets attributes!
	# 	print atts['type']
	# 	#print atts

def readAifDir(name,path):
	#should return amount of .aif's found in dir
	aifsampleList=[["a","a"]]
	#print
	#print "readAif directory: ",name
	#print "path: ", path
	pack=[name,path+"/",dict([('_types','mixed')])]

	for file in os.listdir(path):
		fullPath=path+"/"+file
		if file.endswith('.aif')or file.endswith(".aiff"):
			#print "aif found at file: ",fullPath
			atts=readAif(fullPath)
			aifsampleList.append([file,fullPath,atts['type']])
			#print atts['type']

		elif file.endswith(".DS_Store"):
			#ignore .DS_Store mac files
			continue
		else:
			print fullPath, " is not a aif. what gives?"
	if ["a","a"] in aifsampleList:
			aifsampleList.remove(["a","a"])


	for sample in aifsampleList:
	 	#print sample[1] #fullpath
	 	#print sample[2]
	 	sampleType=sample[2]
	 	if sampleType in pack[2]:
	 		pack[2][sampleType]=pack[2][sampleType]+1
	 	else:
	 		pack[2][sampleType]=1
	 	
	 	#print att
	if ('cluster' in pack[2]) or ('sampler' in pack[2]) or ('drwave' in pack[2]) or ('string' in pack[2]) or ('pulse' in pack[2]) or ('phase' in pack[2]) or ('voltage' in pack[2]) or ('digital' in pack[2]) or ('dsynth' in pack[2]) or ('fm' in pack[2]):
		#print "pack has synths", pack[2]
		pack[2]['_types']='synth'

	if 'drum' in pack[2]:
		#print "pack has drums"
		#print pack[2]['_types']
		if pack[2]['_types']=='synth':
			#print "but synths too"
			pack[2]['_types']='mixed'
		else:
			pack[2]['_types']='drum'


	return pack

def readAif(path):

	#print "//READAIFF from file ", path
	#print

	# SAMPLE DRUM AIFF METADATA
	# /home/pi/Desktop/samplepacks/kits1/rz1.aif
	# drum_version : 1
	# type : drum
	# name : user
	# octave : 0
	# pitch : ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
	# start : ['0', '24035422', '48070845', '86012969', '123955093', '144951088', '175722759', '206494430', '248851638', '268402991', '312444261', '428603973', '474613364', '601936581', '729259799', '860697810', '992135821', '1018188060', '1044240299', '1759004990', '1783040413', '1820982537', '1845017959', '1882960084']
	# end : ['24031364', '48066787', '86008911', '123951035', '144947030', '175718701', '206490372', '248847580', '268398933', '312440203', '428599915', '474609306', '601932523', '729255741', '860693752', '992131763', '1018184002', '1044236241', '1759000932', '1783036355', '1820978479', '1845013902', '1882956026', '1906991448']
	# playmode : ['8192', '8192', '8192', '8192', '8192', '8192', '8192', '8192', '8192', '8192', '8192', '8192', '8192', '8192', '8192', '8192', '8192', '8192', '8192', '8192', '8192', '8192', '8192', '8192']
	# reverse : ['8192', '8192', '8192', '8192', '8192', '8192', '8192', '8192', '8192', '8192', '8192', '8192', '8192', '8192', '8192', '8192', '8192', '8192', '8192', '8192', '8192', '8192', '8192', '8192']
	# volume : ['8192', '8192', '8192', '8192', '8192', '8192', '8192', '8192', '8192', '8192', '8192', '8192', '8192', '8192', '8192', '8192', '8192', '8192', '8192', '8192', '8192', '8192', '8192', '8192']
	# dyna_env : ['0', '8192', '0', '8192', '0', '0', '0', '0']
	# fx_active : false
	# fx_type : delay
	# fx_params : ['8000', '8000', '8000', '8000', '8000', '8000', '8000', '8000']
	# lfo_active : false
	# lfo_type : tremolo
	# lfo_params : ['16000', '16000', '16000', '16000', '0', '0', '0', '0']

	# SAMPLE SYNTH METADATA
	# /home/pi/Desktop/samplepacks/C-MIX/mtrap.aif
	# adsr : ['64', '10746', '32767', '14096', '4000', '64', '4000', '4000']
	# base_freq : 440.0
	# fx_active : true
	# fx_params : ['64', '0', '18063', '16000', '0', '0', '0', '0']
	# fx_type : nitro
	# knobs : ['0', '2193', '2540', '4311', '12000', '12288', '28672', '8192']
	# lfo_active : false
	# lfo_params : ['16000', '0', '0', '16000', '0', '0', '0', '0']
	# lfo_type : tremolo
	# name : mtrap
	# octave : 0
	# synth_version : 2
	# type : sampler



	attdata={}

	with open(path,'rb') as fp:
		line=fp.readline()
		#print line
		if 'op-1' in line:
			#print
			#print 'op-1 appl chunk found!'


			#print subline=line.split("op-1")
			
			# subline=line.split("op-1")[0]
			# print subline[1]

			data=line.split('{', 1)[1].split('}')[0] #data is everything in brackets
			
			#print 
			#print "data!"
			#print data

			data=switchBrack(data,",","|")

			attlist=data.split(",")

			#print
			#print "attlist"
			#print attlist

			

			#print
			#print "attname: attvalue"

			for i,line in enumerate(attlist):
				#print line
				linesplit=line.split(":")
				attname=linesplit[0]
				attname=attname[1:-1]
				attvalue=linesplit[1]

				valtype=""

				#print attvalue
				if isInt(attvalue):
					valtype='int'

				if isfloat(attvalue):
					valtype='float'

				if attvalue=="false" or attvalue=="true":
					valtype='bool'

				for j,char in enumerate(list(attvalue)):
					#print "j,char"
					#print j, char
					if valtype=="":
						if char=='"':
							#print "string: ",char
							valtype="string"
						elif char=="[":
							valtype="list"


				if valtype=="":
					valtype="no type detected"
				elif valtype=="string":
					attvalue=attvalue[1:-1]
				elif valtype=="list":
					attvalue=attvalue[1:-1]
					attvalue=attvalue.split("|")
					#print "list found"
					# for k,item in enumerate(attvalue):
					# 	print k,item
						#attvalue[k]=
					#print attvalue[1]
				

				
				#print attname,":",attvalue
				#print valtype
				#print

				attdata.update({attname:attvalue})
				
		#print attdata['type']
		if 'type' in attdata:
			#print "type exists"
			True
		else:
			#print "type doesn't exist"
			attdata.update({'type':'not specified'})
		#except:
		#	attdata.update({'type':'not specified'})

			

		return attdata

			# attdata[attname]=value
			
			#print attdata

def isInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def isfloat(s):
    try: 
        float(s)
        return True
    except ValueError:
        return False
					
def switchBrack(data,fromdelim,todelim):

			datalist=list(data)

			inbrack=0

			for i,char in enumerate(datalist):
				#print i, " ",char
				if char=="[":
					inbrack=1
					#print "in brackets"

				if char=="]":
					inbrack=0
					#print "out of brackets"

				if inbrack ==1:

					if char==fromdelim:
						#print "comma found!"
						if data[i-1].isdigit():
							#print "num preceding comma found"
							datalist[i]=todelim
			
			newdata="".join(datalist)
			#print newdata
			return newdata




# MAIN

def main():
	device=init()

	#MAIN MENU
	mlist=["tape deck", "backup tape","sample packs","midi","system"]
	alist=["synth", "drum"," "]
	listMenuScroll(device,mlist,alist,"MAIN",None,True,False) #no exit


main()
