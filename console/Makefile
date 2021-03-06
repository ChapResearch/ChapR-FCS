#
# This is the target place to deploy the software.  It is assumed
# to be a RPi with login "pi" and password "raspberry".
#
TARGET = 192.168.101.76
MAIN = main.py
HOME = ChapR-FCS/console
TESTDIR = Tests
USER = pi
PASSWORD = raspberry

SCREENS = optionscreen.py startupscreen.py matchsetupscreen.py \
		screen.py numberchangescreen.py \
		bootscreens.py teamassign.py \
		mainscreen.py \
		matchoptionsscreen.py systemoptionsscreen.py \
		systemtests.py robotasignmentscreen.py \
		matchsetup.py startmatch.py \
		bluetoothtests.py \
		runmatchscreen.py About.py 

BLUETOOTH = rn4020.py BLEinterfaceRN4020.py \
		BLEprotocol.py gatt.py \
		BLEinterfaceSimulation.py av1.py \

HARDWARE = hardware.py HDMIdriver.py touchDriver.py

UTILITY = settings.py utils.py globalVariables.py \
	  buttons.py buttontest.py tables.py virtkeyboard.py

OTHER = main.py clock.py HDMIclock.py \
	batteryimage.py statsdisplay.py connectionimage.py \
	Team.py 

DIRS = Media Font Tests
DEPLOYFILES = $(SCREENS) $(BLUETOOTH) $(HARDWARE) $(UTILITY) $(OTHER) $(DIRS)


deploy-all:
	sshpass -p $(PASSWORD) rsync -vr * $(USER)@$(TARGET):$(HOME)

deploy:
#	sshpass -p $(PASSWORD) scp $(DEPLOYFILES) $(USER)@$(TARGET):$(HOME)
	sshpass -p $(PASSWORD) rsync -vr $(DEPLOYFILES) $(USER)@$(TARGET):$(HOME)

deploy-tests:
	cd $(TESTDIR); sshpass -p $(PASSWORD) scp $(DEPLOYTESTFILES) $(USER)@$(TARGET):$(HOME)/$(TESTDIR)

reboot:
	sshpass -p $(PASSWORD) ssh -l $(USER) $(TARGET) sudo reboot

#
# start up the application on the RPi
#
start:	deploy
	sshpass -p $(PASSWORD) ssh -t -l $(USER) $(TARGET) "cd $(HOME); sudo python $(MAIN)"

#
# Tests go here.  Tests are run in order.  Interaction is necessary for all tests.
#
tests:	deploy-tests
	sshpass -p $(PASSWORD) ssh -t -l $(USER) $(TARGET) "cd $(HOME)/$(TESTDIR); sudo python buttonTest.py"

#
# Misc tools
#
#   code-text - generates words to be placed into code - use like:  make word="hello" code-text
#		A good font to use is "slant" but "standard" is good too.
#
code-text:
	figlet -k -f standard $(word) | sed "s/^/# /"
