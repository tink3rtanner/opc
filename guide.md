Hardware

Overview

The opc has 3 main
subcomponents:

1. Raspberry Pi Zero W, the
     brains of the operation 
    1. I usually get [this kit](https://smile.amazon.com/CanaKit-Raspberry-Wireless-Official-Supply/dp/B071L2ZQZX/ref=sr_1_4?ie=UTF8&qid=1528171057&sr=8-4&keywords=CanaKit+Raspberry+Pi+Zero+W)…$22.99
    2. microSD card
        1. Grab [this 32GB](https://smile.amazon.com/SanDisk-microSDHC-Standard-Packaging-SDSQUNC-032G-GN6MA/dp/B010Q57T02/ref=sr_1_6?s=electronics&ie=UTF8&qid=1528173776&sr=1-6&keywords=micro+sd+card) card for a good value … $13.33
        2. Or you can ball out and get
       [64GB](https://smile.amazon.com/Sandisk-Ultra-Micro-UHS-I-Adapter/dp/B073JYVKNX/ref=pd_sbs_147_3?_encoding=UTF8&pd_rd_i=B073JYVKNX&pd_rd_r=VDFAVDHAKKDWWR92TQJK&pd_rd_w=xSKQ8&pd_rd_wg=Q46i5&psc=1&refRID=VDFAVDHAKKDWWR92TQJK) … $19.99
        3. Theoretically, can be up to
       256GB or more , but those sd cards get pricey

 

1. Display/Button Hat &
     Power Assembly
    1. [WaveShare sh1106 128x64 OLED](https://smile.amazon.com/dp/B078D6NXFM/ref=twister_B077Z9Q39G?_encoding=UTF8&psc=1) w/ Buttons (opc
      doesn’t support the 128x128…yet)…$16.99
        1. A display board
       built for the Pi (you can make a tiny gameboy), with some nifty buttons
       that'll take care of navigating the opc's menus.
        2. All the wiring is done
       here, so you won't have to solder directly onto the Pi (besides the
       header pins). Also adds the benefits of making it easy to switch out the
       components.

    2. [Adafruit Powerboost 1000c](https://smile.amazon.com/gp/product/B01BMRBTH2) …$19.39
        1. This boosts the
       output of the 3.7v lipo to the 5v ~1a that the Pi needs(sometimes,
       mostly draws ~100mA), and also takes care of charging the battery

    3. On/off Switch (Any switch
      will do, but I used one from this [pack](https://smile.amazon.com/gp/product/B01NBVGPH5/ref=oh_aui_search_detailpage?ie=UTF8&psc=1))…$7.29
        1. Every good
       gadget needs an on/off switch!

    4. [mUsb breakout](https://smile.amazon.com/Adafruit-USB-Micro-B-Breakout-Board/dp/B00KLDPZVU/ref=sr_1_2?ie=UTF8&qid=1528171545&sr=8-2&keywords=microusb+breakout)…$5.29
        1. I could have
       used the musb on the 1000c, but it couldn't quite line up for any of the
       layouts I tried

2. A battery to power it all (I
     use [this 2000mAh lipo](https://smile.amazon.com/gp/product/B0798H3762/ref=oh_aui_detailpage_o00_s00?ie=UTF8&psc=1))…$10.99
    1. You can use any
      lipo battery(make sure the pins are right before you plug it in!), I use
      this one because it's 2000mAh & it perfectly fits the footprint of
      the pi. With this battery I'm getting 5+[confirm] hours of
      runtime.

 

Components List

 

Raspberry
  Pi Zero W (includes power supply)

 

$22.99 

 

SanDisk
  32GB microSD card

 

$13.33 

 

Waveshare
  128x64 OLED w/ Buttons

 

$16.99 

 

Adafruit
  Powerboost 1000c

 

$19.39 

 

On/Off
  Switch

 

$7.29 

 

mUsb
  Breakout

 

$5.29 

 

Uxcell
  2000mAh lipo

 

$10.99 

 

Total   

 

$96.27 

 

Assembly

 

Start with soldering
the header pins onto the raspberry pi. This should be old hat for you if you've
ever done a Pi zero project before. Make sure to solder the short end of the
header pins to the pi so that the long ends are sticking up. 

[pic of the
described]

 

Software

 

Bake sd card with
raspbianlite

Get
connected! WiFi

Samba

Opc
(clone from git here0)

 

 

 

Display/Power Assembly

 

Start with gluing
the mUsb breakout to the top of the board (number)

 

Next cut your wires
to length and start with the 2 soldered directly onto the display (5V &
GND)

 

After that, glue
down the powerboost board. I'd recommend laying down a piece of electrical tape
between the two boards to make sure you're not getting any unintended
connections. I like to use a few globs of sticky tack to hold the components in
place and then push the hat and the pi together to make sure everything lines
up before gluing

 

Then, solder the
powerboost pins to the mUsb breakout and to the wires you earlier soldering. I
recommend intermittent testing between each connection, using a multimeter or
just connecting things and seeing if they light up (should be blue when powered
by the mUsb, and your pi should turn on if you've soldered everything
correctly)

 

Lastly, glue down
the switch.  Everything will work without
the switch, it's just a little nicer on everybody if you don't have to pull out
the battery terminal all the time. Once again, the sticky thing is super helpful
here. You'll have to remove a ribbon connector from the Pi for the switch to
fit snugly [detail].

 

At this point you
should be able to sandwich the two components together and get to business.
Test your wiring by plugging a hot mUsb cable into the breakout board and
seeing if your Pi blinks green. We haven't loaded an OS yet, but you'll be able
to test if you've soldered correctly. Once we set up the software & GUI,
you'll be able to see the display come alive.

 

 

 

Using

Tape
list

Sample
list

Transferring,
renaming files

 

Bonus

Contributing

Needs/down
the pipe

Case
design (s/o)

Easy
dist

Midi
stuff

Audio
processing

Forum
link
