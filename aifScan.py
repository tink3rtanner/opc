import os

directory="/home/pi/Desktop/samplepacks/"


sampleList=[["test","test"]]


def main():

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
						readAifDir(subfile,subfullPath)


				elif subfile.endswith(".aif") or subfile.endswith(".aiff"):
					containsAif=1
				elif subfile.endswith(".DS_Store"):
					continue
				else:
					print "what's going on here. name your folders or hold it with the nesting"
					print "SUBFILE: ",subfile
			if containsAif==1:
				readAifDir(file,fullPath)

		# else:
		# 	sampleList.append([file,fullPath]) #adds file andfullpath to samplelist
	 #    #if file.endswith(".atm") or file.endswith(".py"): 

	if ['test', 'test'] in sampleList: 
		sampleList.remove(['test','test'])

	#print sampleList


	# for sample in sampleList:
	# 	print
	# 	print sample[1] #fullpath
	# 	atts=readAif(sample[1]) #reads aiff and gets attributes!
	# 	print atts['type']
	# 	#print atts


def readAifDir(name,path):
	#should return amount of .aif's found in dir
	aifsampleList=[["a","a"]]
	print
	print "readAif directory: ",name
	print path
	for file in os.listdir(path):
		fullPath=path+"/"+file
		if file.endswith('.aif')or file.endswith(".aiff"):
			#print "aif found at file: ",fullPath
			atts=readAif(fullPath)
			aifsampleList.append([file,fullPath])
			#print atts['type']

		elif file.endswith(".DS_Store"):
			#ignore .DS_Store mac files
			continue
		else:
			print fullPath, " is not a aif. what gives?"
	if ["a","a"] in aifsampleList:
			aifsampleList.remove(["a","a"])

	for sample in aifsampleList:
	 	print sample[1] #fullpath
	 	atts=readAif(sample[1]) #reads aiff and gets attributes!
	 	print atts['type']
	 	#print atts
	


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




main()
