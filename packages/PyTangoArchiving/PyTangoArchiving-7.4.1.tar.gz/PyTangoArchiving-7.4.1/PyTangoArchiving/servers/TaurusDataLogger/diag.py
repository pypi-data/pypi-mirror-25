#!/usr/bin/env python

import PyTango
import time

ior_pm_tm = 'ioregister/diag1_ior_ctrl/1'
ior_pm_tm_attr = 'value'

pm_tm = 'BL29/CT/EPS-PLC-01'
pm_tm_attr = 'MIR_OH01_01'

if __name__ == '__main__':
  dev_ior = PyTango.DeviceProxy(ior_pm_tm)
  dev_pm = PyTango.DeviceProxy(pm_tm)
  while True:
    #start = time.time()
    #print dev.read_attribute(pm_tm_attr).value
    #end = time.time()
    #if (end - start > 0.5):
    #  print 'took: %s' % end-start
    #  exit(-1)
    state_ior = dev_ior.state()
    state_pm = dev_pm.state()
    if not (state_ior in [PyTango.DevState.ON,PyTango.DevState.ALARM]) or \
       not (state_pm  in [PyTango.DevState.ON,PyTango.DevState.ALARM]):
      print dev_ior.dev_name(), state_ior
      print dev_pm.dev_name(), state_pm
      exit(-1)
    time.sleep(0.5)

