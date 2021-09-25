from monitor import Monitor

monitor = Monitor()
monitor.start('YATE', ['yate','-v'])
monitor.start('INT1', ['sip-audio-session', '-S', '-b', '-a', '112@pbx.test','--auto-answer'])
monitor.start('EXT1', ['sip-audio-session', '-S', '-b', '-a', '9164440001@pbx.test','--auto-hangup', '5', '112@pbx.test'])
for event in monitor.process():
  line = event[0]
  name = '['+event[1]+']'
  print(name, line)
