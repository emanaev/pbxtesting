from monitor import Monitor
import unittest
import re
import codecs


class TestStringMethods(unittest.TestCase):
      
  def setUp(self):
    self.mon = Monitor()
    self.mon.startcmd('YATE', ['yate','-v'])
    for event in self.mon.capture():
      if event.text=='Initialization complete':
        print("[YATE] === Yate started")
        self.mon.stopCapture()

  def test_call(self):
    self.mon.startcmd('INT1', ['sip-audio-session', '-S', '-b', '-a', '112@pbx.test','--auto-answer'])
    self.mon.startcmd('EXT1', ['sip-audio-session', '-S', '-b', '-a', '9164440001@pbx.test','--auto-hangup', '1', '112@pbx.test'])
    self.mon.startcmd('TIME', ['bash', '-c', 'sleep 3; echo "ERROR"'])
    state = {'INT1': 0, 'EXT1': 0}
    for event in self.mon.capture():
      if event.proc in ('INT1', 'EXT1') and re.match(r'Session started', event.text):
        print("[%s] === Call started" % event.proc)
      elif event.proc=='INT1' and event.text=='Session   ended by remote party':
        print("[INT1] === Remote hanged up")
        self.mon.stopCapture()
      elif event.proc=='TIME' and event.text=='ERROR':
        self.mon.stopCapture()
        self.fail("Timeout")

      #if event.proc!='YATE':
      #  print('['+event.proc+']', '"'+event.text+'"') 

  def tearDown(self):
    self.mon.shutdownall()

if __name__ == '__main__':
  unittest.main()