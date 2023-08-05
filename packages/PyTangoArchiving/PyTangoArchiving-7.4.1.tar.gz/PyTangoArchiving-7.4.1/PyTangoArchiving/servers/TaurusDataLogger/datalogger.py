import time
import PyTango
import taurus
import fandango
import traceback

#taurus.core.TaurusEventType.lookup
#Out[10]: {'Change': 0, 'Config': 1, 'Error': 3, 'Periodic': 2}

MAX_SIZE = 1e5
DEFAULT_PERIOD = 3000

class DataLogger(fandango.Object):
    """
    This class is used to subscribe to Tango events and/or Taurus Polling and generate a
    fixed-size log with all events received.
    
    After max_size is reached, no more data will be processed.
    After max_time passed, the logging will stop.
    The bunch_size controls how often data will be exported to file from mem buffer.
    
    """
    
    def __init__(self,model=None,period=0,max_size=MAX_SIZE,max_time=0,bunch_size=1e3,keep_nones=False,trace=False,start=True,filename='',format='table'):
        self.keep_nones = keep_nones
        self.data = []
        self.trace = trace
        self.models = {}
        self._last_type = None
        self._started = False
        self.period = period
        self._periods = {}
        self.max_size = max_size
        self.max_time = max_time
        self.max_bunch = bunch_size
        self.bunches = 0
        self.total = 0
        self.format = format
        self.filename = filename
        if start: self.start()
        self.set_model(model)
        
    def __del__(self):
        if self.models: self.set_model(None)
        
    def state(self):
        return PyTango.DevState.RUNNING if self._started else PyTango.DevState.STANDBY
    
    def start(self):
        self._started = time.time()
        
    def stop(self):
        self._started = 0
        
    def size(self):
        return len(self.data)
        
    def set_model(self,model):
        if model is not None:
            if not fandango.isSequence(model): model = (model,)
            [self.add_model(m,self.period) for m in model]
            #map(self.add_model,((model,self.period))
        elif self.models:
            map(self.remove_model,self.models.keys())
            self.clear()
        
    def add_model(self,model,period=None):
        """
        If period is equal to 0 then polling will be not enabled.
        """
        if model is None: return
        if 1 or self.trace: 
            print 'DataLogger.add_model(%s,%s)'%(model,period)
        model = str(model).lower()
        period = period or self.period or 0
        if model in self.models:
            if period==self.models[model]: 
                return
            else: 
                self.remove_model(model)
        ta = taurus.Attribute(model)
        try:
            ta.addListener(self.event_received)
            if period>0:
                print 'ForcedPolling=%s'%period
                ta.enablePolling(True)
                try:
                    ta.activatePolling(period,force=True)
                except:
                    print 'Forced polling not available!'
                    #ta.activatePolling(period)
        except:
            ta.removeListener(self.event_received)
            print traceback.format_exc()
            return False
        
        self.models[model] = period
        return True
    
    def remove_model(self,model):
        model = str(model).lower()
        if model in self.models:
            taurus.Attribute(model).removeListener(self.event_received)
            self.models.pop(model)
        return
    
    def event_received(self,source,type_,value):
        try:
            now = time.time()
            try: source = source.getNormalName()
            except: source = str(source)
            if not self._started or len(self.data)>=self.max_size: 
                return
            if self.max_time and (self._started+self.max_time)<now: 
                print('%s recorded for %s seconds'%(source,now-self._started))
                self.stop()
                return
            stype = taurus.core.TaurusEventType.reverseLookup[type_]
            if type_ in(0,2): #Change or periodic
                val = value.value
                sval = str(value.value)[:20]+' ...'
            else:
                sval = '\n'.join(l for l in str(value).split('\n') if 'desc =' in l)
                val = sval and sval.replace('\n',';') or None
            t = getattr(value,'time',now)
            if hasattr(t,'tv_sec'): t = fandango.ctime2time(t)
            
            if not self.keep_nones and type_ not in (0,2,self._last_type):
                print('%s, %s at %s: %s' % (source,stype,time.ctime(),sval))
                
            if type_ in (0,2) or self.keep_nones:
                self.data.append((t,str(source).split('?')[0],stype,val))
                if self.trace: print '\t'.join(map(str,self.data[-1]))
                
            if len(self.data) == self.max_bunch: 
                #print('%s data reached max_bunch, %s'%(source,self.max_bunch))
                self.export(append=self.bunches)
                while len(self.data): self.data.pop(0)
                self.bunches+=1
                
            if len(self.data) == self.max_size-1: 
                print('%s data reached max_size, %s'%(source,self.max_size))
                self.stop()
                
            self._last_type = type_
            self.total+=1
        except Exception,e:
            print traceback.format_exc()
            raise e #@todo, @warning, @bug, <- This could crash the taurus polling ?!?!?
            
    def clear(self):
        while len(self.data): self.data.pop(0)
        if self.models: self.set_model(None)
        
    def export(self,model='',filename=None,data=None,clear=False,append=False):
        try:
            import fandango
            t0 = time.time()
            table = self.format=='table'
            models = sorted(m for m in self.models if fandango.matchCl(model,m))
            data = sorted(data or self.data)
            filename = filename or self.filename
            if self.trace or 1: print 'export(%s,%s,table=%s,append=%s,period=%s): [%d]'%(models,filename,table,append,self.period,len(data))
            if not table:
                export = '\r\n'.join((not append and ['Date\tTime\tSource\tType\tValue'] or [])+\
                    ['\t'.join(map(str,(time.ctime(t[0]),t[0],t[1],t[2],t[3]))) for t in data if any(m in t[1] for m in models)])
            else:
                values = dict((a.lower(),[]) for a in models)
                for row in self.data:
                    t,s,ty,v = row[0],row[1].lower(),str(row[2]).lower(),row[3]
                    if 'config' not in ty and s in values:
                        if not values[s] or t!=values[s][-1][0]:
                            values[s].append((t,v))
                        else: values[s][-1] = (t,v)                 
                if self.trace: print ' \n'.join(sorted('%s: %d values'%(a,len(v)) for a,v in values.items()))
                if self.period:
                    Ts = max(v[0][0] for v in values.values() if v),min(v[-1][0] for v in values.values() if v)
                    #for a,v in values.items(): values[a]=[t for t in v if Ts[0]<=t[0]<=Ts[-1]]
                    values = fandango.arrays.correlate_values(values,resolution=self.period*1e-3)
                if self.trace: print ' \n'.join(sorted('%s: %d values'%(a,len(v)) for a,v in values.items()))            
                export = fandango.arrays.values2text(values,order=map(str.lower,models),sep='\t',eof='\r\n',header=not append).replace('None','NaN')
            if filename:
                f = open(filename,'w' if not append else 'a')
                f.write(export+'\r\n')
                f.close()
            else:
                print export
            if clear: self.clear()
            if self.trace or 1: print 'export took %d ms'%(1000*(time.time()-t0))
            return export
        except:
            print 'Export failed!!!: %s'%traceback.format_exc()
        
    
if __name__ == '__main__':
    import sys,threading
    models = [a for a in sys.argv[1:] if not a.startswith('--')] or ''
    args = dict((k.strip('--'),v) for k,v in ((a.split('=') if '=' in a else (a,True)) for a in sys.argv[1:] if a.startswith('--')))
    filename = args.get('filename')
    if filename:
        filename = '.'.join((filename.rsplit('.',1)[0],fandango.replaceCl('[^0-9]','',fandango.time2str()),filename.rsplit('.',1)[1]))
    if not models:
        print 'Usage: datalogger.py XXXXX(s) model1 model2 model3 model4 [--polling=XXXXX(s)] [--format=list/table] --bunches=XXX'
    else:
        print time.ctime()
        max_time,models = models[0],models[1:]
        now = time.time()
        time.sleep(.25)
        trace = '--trace' in sys.argv
        dl = DataLogger(keep_nones=True,trace=trace,start=True,max_time=float(max_time),
                        filename=filename,
                        period=float(args.get('polling',0))*1e3,
                        bunch_size=int(args.get('bunches',1e3)),
                        format=args.get('format','table'))
        dl.set_model(models)
        event = threading.Event()
        while dl._started: event.wait(5.)
        print '-'*40+' saving %d values to %s '%(dl.total,filename) + '-'*40
        dl.export(append=dl.bunches)
    
    
"""
taurustrend -a lab/vc/mks-lab-1/P2 lab/vc/mks-lab-1/P1 lab/vc/spbx-1049/P1 lab/vc/spbx-1049/P2 lab/vc/spbx-1049/P3 lab/vc/dual-01/P2 &
attrs = fandango.get_matching_attributes('lab/vc/(dual-01|spbx-1049|mks-lab-1)/((p|i)[0-9]|hv[12]code|state)')
attrs.append('lab/vc/spbx-1049/status')

 tdb.start_archiving(attrs,{'MODE_P' :[1000]})

FAAAAAAAAAAAILEEEEED!!!! , everything archived at 60 seconds!


PROBLEMS>
Unable to write ilock value in DUAL:
In [47]: dp = PyTango.DeviceProxy('lab/vc/dual-01')

In [48]: dp.read_attribute('pressuresetpoints')
Out[48]: DeviceAttribute(data_format = PyTango._PyTango.AttrDataFormat.SPECTRUM, dim_x = 2, dim_y = 0, has_failed = False, is_empty = False, name = 'PressureSetPoints', nb_read = 2, nb_written = 2, quality = PyTango._PyTango.AttrQuality.ATTR_VALID, r_dimension = AttributeDimension(dim_x = 2, dim_y = 0), time = TimeVal(tv_nsec = 0, tv_sec = 1362744946, tv_usec = 200627), type = PyTango._PyTango.CmdArgType.DevString, value = ('1.0e-05', '1.5e-05'), w_dim_x = 2, w_dim_y = 0, w_dimension = AttributeDimension(dim_x = 2, dim_y = 0), w_value = ('1.0e-05', '1.5e-05'))

In [49]: dp.read_attribute('pressuresetpoints').value
Out[49]: ('1.0e-05', '1.5e-05')

In [50]: val = dp.read_attribute('pressuresetpoints').value

In [51]: dp.write_attribute('pressuresetpoints',val)
---------------------------------------------------------------------------
DevFailed                                 Traceback (most recent call last)

/homenfs/srubio/PROJECTS/Utils/TaurusDataLogger/<ipython console> in <module>()

DevFailed: DevFailed[
DevError[
    desc = Write not allowed to channel ON
  origin = SendCommand
  reason = ProtocolError
severity = ERR]

DevError[
    desc = Failed to write_attribute on device lab/vc/dual-01, attribute PressureSetPoints
  origin = DeviceProxy::write_attribute()
  reason = API_AttributeFailed
severity = ERR]
]

In [52]: dp.HV2Off()
---------------------------------------------------------------------------
AttributeError                            Traceback (most recent call last)

/homenfs/srubio/PROJECTS/Utils/TaurusDataLogger/<ipython console> in <module>()

/homelocal/sicilia/lib/python/site-packages/PyTango/device_proxy.pyc in __DeviceProxy__getattr(self, name)
    108
    109     if not find_attr or name_l not in self.__attr_cache:
--> 110         raise AttributeError, name
    111
    112     return self.read_attribute(name).value

AttributeError: HV2Off

In [53]: dp.HV
dp.HV1Code    dp.HV1Status  dp.HV2Code    dp.HV2Status

In [53]: dp.
Display all 218 possibilities? (y or n)

In [53]: dp.H
dp.HV1Code    dp.HV1Status  dp.HV2Code    dp.HV2Status

In [53]: dp.Of
dp.Off     dp.OffHV1  dp.OffHV2

In [53]: dp.OffHV2()
Out[53]: 'DONE'

In [54]: dp.write_attribute('pressuresetpoints',val)
---------------------------------------------------------------------------
DevFailed                                 Traceback (most recent call last)

/homenfs/srubio/PROJECTS/Utils/TaurusDataLogger/<ipython console> in <module>()

DevFailed: DevFailed[
DevError[
    desc = Write value exceeding the allowed limits or step not allowed
  origin = SendCommand
  reason = ProtocolError
severity = ERR]

DevError[


Able to write ilock value in SPBX
In [19]: spbx.read_attribute('interlockthresholds').value
Out[19]: ('5e-06', '5e-06', '5e-06', '5e-06', '5e-06')
In [22]: val = ('1e-07', '1e-07', '1e-07', '1e-07', '1e-07')
In [23]: spbx.write_attribute('interlockthresholds',val)

    
How to record relay status of MKS!?

[0]  Fri Mar  8 12:46:20 2013,1362743180.8,<EPS:Conf/0:0:0:0:0>
[1]  Fri Mar  8 12:46:21 2013,1362743181.06,<INTERLOCK:CH/0>
[2]  Fri Mar  8 13:04:02 2013,1362744242.7,<WARNING:CH/1:0:0:0:0>
[3]  Fri Mar  8 13:04:07 2013,1362744247.72,<WARNING:CH/1:1:0:0:0>
[4]  Fri Mar  8 13:04:12 2013,1362744252.72,<WARNING:CH/1:1:1:0:0>
[5]  Fri Mar  8 13:04:29 2013,1362744269.22,<WARNING:OFF>

[0]  Fri Mar  8 13:10:11 2013,1362744611.25,<EPS:Conf/0:0:0:0:0>
[1]  Fri Mar  8 13:10:11 2013,1362744611.49,<INTERLOCK:CH/0>

DUAL switched off at [datetime.datetime(2013, 3, 8, 13, 15, 55), 2e-08],



Warning thresholds set to 5e-9 at 
'Fri Mar  8 13:30:00 2013'
[0]  Fri Mar  8 13:24:36 2013,1362745476.54,<EPS:Conf/0:0:0:0:0>
[1]  Fri Mar  8 13:24:36 2013,1362745476.78,<INTERLOCK:CH/0>
[2]  Fri Mar  8 13:29:50 2013,1362745790.76,<WARNING:CH/1:0:0:0:0>
[3]  Fri Mar  8 13:29:55 2013,1362745795.82,<WARNING:CH/1:1:1:0:0>
[4]  Fri Mar  8 13:30:03 2013,1362745803.64,<WARNING:OFF> !_!_!_!_!_! ??????

In [72]: 

val = ('1e-09', '1e-09', '1e-09', '1e-09', '1e-09')

In [73]: time.ctime(),spbx.write_attribute('warningthresholds',val)
Out[73]: ('Fri Mar  8 13:33:02 2013', None)


array length: 4
[0]  Fri Mar  8 13:32:56 2013,1362745976.51,<EPS:Conf/0:0:0:0:0>
[1]  Fri Mar  8 13:32:56 2013,1362745976.77,<INTERLOCK:CH/0>
[2]  Fri Mar  8 13:33:02 2013,1362745982.66,<WARNING:CH/1:0:0:0:0>
[3]  Fri Mar  8 13:33:07 2013,1362745987.71,<WARNING:CH/1:1:1:0:0>
In [74]: val = ('1.1e-09', '1.1e-09', '1.1e-09', '1.1e-09', '1.1e-09')

In [75]: time.ctime(),spbx.write_attribute('interlockthresholds',val)
Out[75]: ('Fri Mar  8 13:33:53 2013', None)


array length: 7
[0]  Fri Mar  8 13:32:56 2013,1362745976.51,<EPS:Conf/0:0:0:0:0>
[1]  Fri Mar  8 13:32:56 2013,1362745976.77,<INTERLOCK:CH/0>
[2]  Fri Mar  8 13:33:02 2013,1362745982.66,<WARNING:CH/1:0:0:0:0>
[3]  Fri Mar  8 13:33:07 2013,1362745987.71,<WARNING:CH/1:1:1:0:0>
[4]  Fri Mar  8 13:33:53 2013,1362746033.68,<EPS:Conf/1:0:0:0:0>
[5]  Fri Mar  8 13:33:56 2013,1362746036.39,<EPS:Conf/1:1:1:0:0>
[6]  Fri Mar  8 13:33:58 2013,1362746038.28,<!EPS_EXECUTED!>

val = ('1e-09', '1e-09', '1e-09', '1e-09', '1e-09')

Command: lab/vc/spbx-1049/ResetAlarms
Duration: 14 msec
Command OK
----------------------------------------------------
Command: lab/vc/spbx-1049/GetAlarms
Duration: 3 msec
Output argument(s) :
array length: 3
[0]  Fri Mar  8 13:38:48 2013,1362746328.56,<EPS:Conf/1:1:1:0:0>
[1]  Fri Mar  8 13:38:48 2013,1362746328.81,<WARNING:CH/1:1:1:0:0>
[2]  Fri Mar  8 13:38:48 2013,1362746328.81,<INTERLOCK:CH/0>
----------------------------------------------------
Command: lab/vc/spbx-1049/GetAlarms
Duration: 3 msec
Output argument(s) :
array length: 4
[0]  Fri Mar  8 13:38:48 2013,1362746328.56,<EPS:Conf/1:1:1:0:0>
[1]  Fri Mar  8 13:38:48 2013,1362746328.81,<WARNING:CH/1:1:1:0:0>
[2]  Fri Mar  8 13:38:48 2013,1362746328.81,<INTERLOCK:CH/0>
[3]  Fri Mar  8 13:38:58 2013,1362746338.25,<!EPS_EXECUTED!>


In [79]: val = ('1.1e-08', '1.1e-08', '1.1e-08', '1.1e-08', '1.1e-08')

In [80]: spbx.write_attribute('interlockthresholds',val)

In [81]: spbx.GetAlarms()
Out[81]:
['Fri Mar  8 13:38:48 2013,1362746328.56,<EPS:Conf/1:1:1:0:0>',
 'Fri Mar  8 13:38:48 2013,1362746328.81,<WARNING:CH/1:1:1:0:0>',
 'Fri Mar  8 13:38:48 2013,1362746328.81,<INTERLOCK:CH/0>',
 'Fri Mar  8 13:38:58 2013,1362746338.25,<!EPS_EXECUTED!>',
 'Fri Mar  8 13:41:23 2013,1362746483.83,<EPS:OFF>',
 'Fri Mar  8 13:41:24 2013,1362746484.94,<EPS:Conf/0:0:0:0:0>']

In [82]: spbx.ResetAlarms()

In [83]: val = ('1.1e-09', '1.1e-08', '1.1e-08', '1.1e-08', '1.1e-08')

In [84]: spbx.P1
Out[84]: 1.63e-09

In [85]: time.ctime(),spbx.write_attribute('interlockthresholds',val)
Out[85]: ('Fri Mar  8 13:42:04 2013', None)

In [86]: spbx.GetAlarms()
Out[86]:
['Fri Mar  8 13:41:44 2013,1362746504.51,<WARNING:CH/1:1:1:0:0>',
 'Fri Mar  8 13:42:03 2013,1362746523.58,<EPS:Conf/0:0:0:0:0>',
 'Fri Mar  8 13:42:03 2013,1362746523.84,<INTERLOCK:CH/0>',
 'Fri Mar  8 13:42:04 2013,1362746524.46,<WARNING:CH/',
 'Fri Mar  8 13:42:04 2013,1362746524.84,<EPS:Conf/1:0:0:0:0>',
 'Fri Mar  8 13:42:09 2013,1362746529.32,<!EPS_EXECUTED!>']

In [87]:


HIPOTHESIS> Splitter warnings were late because of lower splitter readings and higher splitter interlock thresholds (5e-6 for eps, how much for warning?)!! Note: delay in splitter is sometimes 5 or sometimes 10, why?
"""