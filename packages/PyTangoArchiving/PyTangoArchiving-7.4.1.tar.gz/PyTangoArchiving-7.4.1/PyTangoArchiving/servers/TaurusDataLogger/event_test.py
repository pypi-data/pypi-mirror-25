


import taurus,time,logging

target = 'test/test/test/Time'

class Hi():
    def __init__(self,logger):
        for k in 'debug info warning error'.split():
            setattr(self,k,getattr(logger,k,None))
        logger.setLogLevel(logging.DEBUG)
        self.count=1
        
    def event_received(self,source,type_,value):
        stype = taurus.core.TaurusEventType.reverseLookup.get(type_,'Unknown')
        if type_ in (0,2):
           self.info('%s at %s: %s(%s)' % (source,value.time,stype,value.value))
           if 'UNKNOWN' in str(value.value):
              status = taurus.Attribute(str(source).replace('state','status')).read().value
              print(status)
              ls = [a for a in status.split('\n') if a.startswith('sr') and 'UNKNOWN' in a]
              self.info('\n'.join(ls))
              for l in ls:
                 try: 
                     val = taurus.Attribute(l.split(':')[0]+'/status').read().value
                     val = dict(zip(val))
                     self.info(val)
                 except:pass
        else:
           self.info('%s, %s at %s:\n %s' % (source,stype,time.ctime(),value))
        self.count+=1
        if not self.count%5: 
            source.VayaPorDios
            #raise Exception('VayaPorDios!')
           
           
ta = taurus.Attribute(target)
h = Hi(ta)
ta.addListener(h.event_received)
print 'Waiting for events ...'
import threading
while True: 
    threading.Event().wait(5.)