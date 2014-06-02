#
# StSimpleApi.py
#
# functions to enable simple value fetching from the sensortag
# 

# import stuff
import os, sys, pexpect
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir) 
import sensortag
from sensor_calcs import *

# SensorTag class
# from 
#    https://github.com/msaunby/ble-sensor-pi/blob/master/sensortag/sensortag.py
class SensorTag:

	def __init__( self, bluetooth_adr ):
		self.con = pexpect.spawn('gatttool -b ' + bluetooth_adr + ' --interactive')
		self.con.expect('\[LE\]>', timeout=600)
		print >> sys.stderr, "Preparing to connect. You might need to press the side button..."
		self.con.sendline('connect')
		# test for success of connect
		self.con.expect('Connection successful.*\[LE\]>')
		# Earlier versions of gatttool returned a different message.  Use this pattern -
		#self.con.expect('\[CON\].*>')
		self.cb = {}
		return

        # legacy stuff
		#self.con.expect('\[CON\].*>')
		#self.cb = {}
		#return

	def char_write_cmd( self, handle, value ):
		# The 0%x for value is VERY naughty!  Fix this!
		cmd = 'char-write-cmd 0x%02x 0%x' % (handle, value)
		print >> sys.stderr, "Sending %s"%cmd
		self.con.sendline( cmd )
		return

	def char_read_hnd( self, handle ):
		self.con.sendline('char-read-hnd 0x%02x' % handle)
		self.con.expect('descriptor: .*? \r')
		after = self.con.after
		rval = after.split()[1:]
		print >> sys.stderr, "Received %s"%rval
		return [long(float.fromhex(n)) for n in rval]
        
    # deletes stuff related to notification

def getHum( ST ):
    ''' uses the Sensortag object to read, process and return the humidity
    '''
    # enable humidity
    ST.char_write_cmd(0x3c,0x01)
    
    # read the value
    v = ST.char_read_hnd( 0x38 )

    # copied from
    #    https://github.com/msaunby/ble-sensor-pi/blob/master/sensortag/sensortag.py
    # line 118
    rawT = (v[1]<<8)+v[0]
    rawH = (v[3]<<8)+v[2]
    (t, rh) = calcHum(rawT, rawH)
    print >> sys.stderr, "HUMD %.1f TEMP %.1f" % (rh, t)
    
    return (t, rh)
    
# and a test run main
if __name__ == "__main__":
    if len( sys.argv ) < 2:
        print "usage: %s <Sensortag MAC>"%sys.argv[0]
        exit(1)
    else:
        StMac = sys.argv[1]
        
    print "Reading data from sensortag with MAC: %s"%StMac

    ST = SensorTag( StMac )
    print getHum( ST )
