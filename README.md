# opc
[beta] Teenage Engineering Op-1 Companion

![opc-hardware v2](/opc-beta.jpg)


**Hardware Build v2**
- raspberry pi zero w
- 1.3in 128x64 ssh1106, driven by luma.io (Also GPIO buttons)
- pimoro LiPo shim
- 500 mAh Lithium polymer battery (2-3hr runtime)


**Current Features**
- python driven ui on display, list-style menus, button interaction
- ssh106 64x128 menu UI
- Tape backup
- Tape load (from directory listing)
- Sample packs load/delete (from defined list)
- Samba file server accessable via pc or android
- Midi forwarding (w/ usb hub model[mendota])
- firmware load (got a case of the slanty stripes? reformat on the road when messy tapes corrupt your filesystem now!)


**Future Features**
- 'scene' load (samples, tape, and presets all at once)
- update tapes (text input is going to be ugh.)
- aiff parser (theres some cool goodies in .aiff metadata)
- count file capacity of op1 sampler/drum (how close are you to the magic 42?)
- copy to external drive
- google drive backup
- drum sample remove whitespace


**Pre-Release Issues List**
- *sample load synth/drum split*
- forces op-1 to defrag... like a lot
- update mounting code (ref https://github.com/tacoe/OP1GO/blob/master/op1go.py)
  - find op1 mount directory
- low battery indicator
- loading bar

**Changelog**

3/18/2018:
- Uploaded alpha to github

3/25/2018:
- Updated GPIO from polling to event detection
- Moved sampleList and tapeList to globals to make extensible

4/2/2018:
- added boot logo ;)
- added system menu w/ wlan,reboot,test
- updated wait to event detection
- added exit & action parameters to listmenu scroll, fixed return bug
- depricated listMenu
- attempt at low battery status bar (doesnt work)
- general cleanup

5/7/2018:
- firmware upload (op1-225.op1) (reformat on the road when messy tapes corrupt your filesystem)
- tapeMenu now autobuilds from a directory (no input checking, be careful!)

5/14/2018:
- organized functions
- readAif metadata scanner (get's cool aiff metadata. will use to discriminate synth&drum for sampleload. got the idea from [here](https://www.operator-1.com/index.php?p=/discussion/comment/8080/))
- pulled out op1 mount path. want to make this extensible but it's one arg for now, tied to my device id.

5/15/2018:
- worked on scanSample.py, which recuses over nested directories and wrangles up sample packs. uses readAif to get sample metadata to sort into synth/drum.

5/28/2018:
- added sample scanning. loops through sample directory and lists sample packs, categorizing them by synth, drum, or mixed
- updated mount code to use pyusb (thanks https://github.com/tacoe/OP1GO/blob/master/op1go.py)

6/10/2018:
- fixed system wlan0 sometimes chopping off ip characters
- updated tapeload and backuptape to have a nifty progress bar
- updated tapeload and backuptape to new mounting code
- added new system menu option to delete all synth folder
