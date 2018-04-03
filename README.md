# opc
[alpha] Teenage Engineering Op-1 Companion

![opc-hardware v2](/opc-beta.jpg)


**Hardware Build v2**
- raspberry pi zero w
- 1.3in 128x64 ssh1106, driven by luma.io (Also GPIO buttons)
- pimoro LiPo shim
- 500 mAh Lithium polymer battery (2-3hr)


**Current Features**
- python driven ui on display, list-style menus, button interaction
- ssh106 64x128 menu UI
- Tape backup
- Tape load
- Sample pack load/delete
- Midi forwarding (w/ usb hub)


**Future Features**
- 'scene' load (samples, tape, and presets all at once)
- updates tape
- aiff parser
- count file capacity of op1 sampler/drum
- auto-list directory
- copy to external drive
- google drive backup
- midi chords
- drum sample remove whitespace


**Pre-Release Issues List**
- update tape load ui
- auto-list tapes
- clean up code
- update mounting code (use https://github.com/tacoe/OP1GO/blob/master/op1go.py)

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
            
end
