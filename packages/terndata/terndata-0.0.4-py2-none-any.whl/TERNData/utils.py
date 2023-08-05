'''
Created on 24 Aug 2017

@author: uqysun6
'''

import numpy
# import copy
# import netCDF4
# import datetime
# import sys
# import xlrd 
# import xlwt
# import dateutil
#from TERNData import constants

# class DataStructure(object):
#     def __init__(self):
#         self.series = {}
#         self.globalattributes = {}
#         self.globalattributes["Functions"] = ""
#         self.mergeserieslist = []
#         self.averageserieslist = []
#         self.returncodes = {"value":0,"message":"OK"}
            
# def nc_read_series(dataset,checktimestep=True,fixtimestepmethod=""):
#     ds = DataStructure()
#     gattrlist=dataset.ncattrs()
#     if len(gattrlist)!=0:
#         for gattr in gattrlist:
#             ds.globalattributes[gattr] = getattr(dataset,gattr)
#             if "time_step" in ds.globalattributes: ts = ds.globalattributes["time_step"]
#     
#     # get a list of the variables in the netCDF file (not their QC flags)
#     varlist = [x for x in dataset.variables.keys() if "_QCFlag" not in x]
#     for ThisOne in varlist:
#         # skip variables that do not have time as a dimension
#         dimlist = [x.lower() for x in dataset.variables[ThisOne].dimensions]
#         if "time" not in dimlist: continue
#         # create the series in the data structure
#         ds.series[unicode(ThisOne)] = {}
#         # get the data and the QC flag
# 
#         data,flag,attr = nc_read_var(dataset,ThisOne)
#         ds.series[ThisOne]["Data"] = data
#         ds.series[ThisOne]["Flag"] = flag
#         ds.series[ThisOne]["Attr"] = attr
#     #dataset.close()
#     # make sure all values of -9999 have non-zero QC flag
#     CheckQCFlags(ds)
#     # get a series of Python datetime objects
#     if "time" in ds.series.keys():
#         time,f,a = GetSeries(ds,"time")
#         get_datetimefromnctime(ds,time,a["units"])
#     else:
#         get_datetimefromymdhms(ds)
#     # round the Python datetime to the nearest second
#     round_datetime(ds,mode="nearest_second")
#     # check the time step and fix it required
#     if checktimestep:
#         if CheckTimeStep(ds):
#             FixTimeStep(ds,fixtimestepmethod=fixtimestepmethod)
#             # update the Excel datetime from the Python datetime
#             get_xldatefromdatetime(ds)
#             # update the Year, Month, Day etc from the Python datetime
#             get_ymdhmsfromdatetime(ds)
#     # tell the user when the data starts and ends
#     ldt = ds.series["DateTime"]["Data"]
#     msg = " Got data from "+ldt[0].strftime("%Y-%m-%d %H:%M:%S")+" to "+ldt[-1].strftime("%Y-%m-%d %H:%M:%S")
# 
#     return ds

def nc_read_var(ncFile,ThisOne):
    """ Reads a variable from a netCDF file and returns the data, the QC flag and the variable
        attribute dictionary.
    """
    # check the number of dimensions
    nDims = len(ncFile.variables[ThisOne].shape)
    if nDims not in [1,3]:
        msg = "nc_read_var: unrecognised number of dimensions ("+str(nDims)
        msg = msg+") for netCDF variable "+ ThisOne
        raise Exception(msg)
    if nDims==1:
        # single dimension
        data = ncFile.variables[ThisOne][:]
        # netCDF4 returns a masked array if the "missing_variable" attribute has been set
        # for the variable, here we trap this and force the array in ds.series to be ndarray
        if numpy.ma.isMA(data): data,dummy = MAtoSeries(data)
        # check for a QC flag
        if ThisOne+'_QCFlag' in ncFile.variables.keys():
            # load it from the netCDF file
            flag = ncFile.variables[ThisOne+'_QCFlag'][:]
        else:
            # create an empty flag series if it does not exist
            nRecs = numpy.size(data)
            flag = numpy.zeros(nRecs,dtype=numpy.int32)
    elif nDims==3:
        # 3 dimensions
        data = ncFile.variables[ThisOne][:,0,0]
        # netCDF4 returns a masked array if the "missing_variable" attribute has been set
        # for the variable, here we trap this and force the array in ds.series to be ndarray
        if numpy.ma.isMA(data): data,dummy = MAtoSeries(data)
        # check for a QC flag
        if ThisOne+'_QCFlag' in ncFile.variables.keys():
            # load it from the netCDF file
            flag = ncFile.variables[ThisOne+'_QCFlag'][:,0,0]
        else:
            # create an empty flag series if it does not exist
            nRecs = numpy.size(data)
            flag = numpy.zeros(nRecs,dtype=numpy.int32)
    # force float32 to float64
    if data.dtype=="float32": data = data.astype(numpy.float64)
    # check for Year, Month etc as int64, force to int32 if required
    if ThisOne in ["Year","Month","Day","Hour","Minute","Second"]:
        if data.dtype=="int64": data = data.astype(numpy.int32)
    # get the variable attributes
    vattrlist = ncFile.variables[ThisOne].ncattrs()
    attr = {}
    if len(vattrlist)!=0:
        for vattr in vattrlist:
            attr[vattr] = getattr(ncFile.variables[ThisOne],vattr)
    return data,flag,attr

def MAtoSeries(Series):
    WasMA = False
    if numpy.ma.isMA(Series):
        WasMA = True
        Series = numpy.ma.filled(Series,float(-9999))
    return Series, WasMA

# def CheckQCFlags(ds):
#     # force any values of -9999 with QC flags of 0 to have a QC flag of 8
#     for ThisOne in ds.series.keys():
#         data = numpy.ma.masked_values(ds.series[ThisOne]["Data"],-9999)
#         flag = numpy.ma.masked_equal(numpy.mod(ds.series[ThisOne]["Flag"],10),0)
#         mask = data.mask&flag.mask
#         index = numpy.ma.where(mask==True)[0]
#         ds.series[ThisOne]["Flag"][index] = numpy.int32(8)
#     # force all values != -9999 to have QC flag = 0, 10, 20 etc
#     for ThisOne in ds.series.keys():
#         index = numpy.where((abs(ds.series[ThisOne]['Data']-numpy.float64(-9999))>0.0000001)&
#                             (numpy.mod(ds.series[ThisOne]["Flag"],10)!=0))
#         ds.series[ThisOne]["Flag"][index] = numpy.int32(0)
        
        
# def GetSeries(ds,ThisOne,si=0,ei=-1,mode="truncate"):
#     """ Returns the data, QC flag and attributes of a series from the data structure."""
#     # number of records
#     if "nc_nrecs" in ds.globalattributes:
#         nRecs = int(ds.globalattributes["nc_nrecs"])
#     else:
#         nRecs = len(ds.series[ThisOne]["Data"])
#     # check the series requested is in the data structure
#     if ThisOne in ds.series.keys():
#         # series is in the data structure
#         if isinstance(ds.series[ThisOne]['Data'],list):
#             # return a list if the series is a list
#             Series = list(ds.series[ThisOne]['Data'])
#         elif isinstance(ds.series[ThisOne]['Data'],numpy.ndarray):
#             # return a numpy array if series is an array
#             Series = ds.series[ThisOne]['Data'].copy()
#         # now get the QC flag
#         if 'Flag' in ds.series[ThisOne].keys():
#             # return the QC flag if it exists
#             Flag = ds.series[ThisOne]['Flag'].copy()
#         else:
#             # create a QC flag if one does not exist
#             Flag = numpy.zeros(nRecs,dtype=numpy.int32)
#         # now get the attribute dictionary
#         if "Attr" in ds.series[ThisOne].keys():
#             Attr = GetAttributeDictionary(ds,ThisOne)
#         else:
#             Attr = MakeAttributeDictionary()
#     else:
#         # make an empty series if the requested series does not exist in the data structure
#         Series,Flag,Attr = MakeEmptySeries(ds,ThisOne)
#     # tidy up
#     if ei==-1: ei = nRecs - 1
#     if mode=="truncate":
#         # truncate to the requested start and end indices
#         si = max(0,si)                  # clip start index at 0
#         ei = min(nRecs,ei)              # clip end index to nRecs
#         Series = Series[si:ei+1]        # truncate the data
#         Flag = Flag[si:ei+1]            # truncate the QC flag
#     elif mode=="pad":
#         # pad with missing data at the start and/or the end of the series
#         if si<0 and ei>nRecs-1:
#             # pad at the start
#             Series = numpy.append(float(-9999)*numpy.ones(abs(si),dtype=numpy.float64),Series)
#             Flag = numpy.append(numpy.ones(abs(si),dtype=numpy.int32),Flag)
#             # pad at the end
#             Series = numpy.append(Series,float(-9999)*numpy.ones((ei-(nRecs-1)),dtype=numpy.float64))
#             Flag = numpy.append(Flag,numpy.ones((ei-(nRecs-1)),dtype=numpy.int32))
#         elif si<0 and ei<=nRecs-1:
#             # pad at the start, truncate the end
#             Series = numpy.append(float(-9999)*numpy.ones(abs(si),dtype=numpy.float64),Series[:ei+1])
#             Flag = numpy.append(numpy.ones(abs(si),dtype=numpy.int32),Flag[:ei+1])
#         elif si>=0 and ei>nRecs-1:
#             # truncate at the start, pad at the end
#             Series = numpy.append(Series[si:],float(-9999)*numpy.ones((ei-(nRecs-1)),numpy.float64))
#             Flag = numpy.append(Flag[si:],numpy.ones((ei-(nRecs-1)),dtype=numpy.int32))
#         elif si>=0 and ei<=nRecs-1:
#             # truncate at the start and end
#             Series = Series[si:ei+1]
#             Flag = Flag[si:ei+1]
#         else:
#             msg = 'GetSeries: unrecognised combination of si ('+str(si)+') and ei ('+str(ei)+')'
#             raise ValueError(msg)
#     elif mode=="mirror":
#         # reflect data about end boundaries if si or ei are out of bounds
#         if si<0 and ei>nRecs-1:
#             # mirror at the start
#             Series = numpy.append(numpy.fliplr([Series[1:abs(si)+1]])[0],Series)
#             Flag = numpy.append(numpy.fliplr([Flag[1:abs(si)+1]])[0],Flag)
#             # mirror at the end
#             sim = 2*nRecs-1-ei
#             eim = nRecs-1
#             Series = numpy.append(Series,numpy.fliplr([Series[sim:eim]])[0])
#             Flag = numpy.append(Flag,numpy.fliplr([Flag[sim:eim]])[0])
#         elif si<0 and ei<=nRecs-1:
#             # mirror at start, truncate at end
#             Series = numpy.append(numpy.fliplr([Series[1:abs(si)+1]])[0],Series[:ei+1])
#             Flag = numpy.append(numpy.fliplr([Flag[1:abs(si)+1]])[0],Flag[:ei+1])
#         elif si>=0 and ei>nRecs-1:
#             # truncate at start, mirror at end
#             sim = 2*nRecs-1-ei
#             eim = nRecs
#             Series = numpy.append(Series[si:],numpy.fliplr([Series[sim:eim]])[0])
#             Flag = numpy.append(Flag[si:],numpy.fliplr([Flag[sim:eim]])[0])
#         elif si>=0 and ei<=nRecs-1:
#             # truncate at the start and end
#             Series = Series[si:ei+1]
#             Flag = Flag[si:ei+1]
#         else:
#             msg = 'GetSeries: unrecognised combination of si ('+str(si)+') and ei ('+str(ei)+')'
#             raise ValueError(msg)            
#     else:
#         raise ValueError("GetSeries: unrecognised mode option "+str(mode))
#     return Series,Flag,Attr        


# def GetAttributeDictionary(ds,ThisOne):
#     attr = {}
#     # if series ThisOne is in the data structure
#     if ThisOne in ds.series.keys():
#         attr = ds.series[ThisOne]['Attr']
#     else:
#         attr = MakeAttributeDictionary()
#     return copy.deepcopy(attr)


# def MakeAttributeDictionary(**kwargs):
#     """
#     Purpose:
#      Make an attribute dictionary.
#     Usage:
#      attr_new = qcutils.MakeAttributeDictionary(long_name = "some string",attr_exist)
#      where long_name is an attribute to be written to the new attribute dictionary
#            attr_exist is an existing attribute dictionary
#     Author: PRI
#     Date: Back in the day
#     """
#     default_list = ["ancillary_variables","height","instrument","long_name","serial_number","standard_name",
#                     "units","valid_range"]
#     attr = {}
#     for item in kwargs:
#         if isinstance(item, dict):
#             for entry in item: attr[entry] = item[entry]
#         else:
#             attr[item] = kwargs.get(item,"not defined")
#         if item in default_list: default_list.remove(item)
#     if len(default_list)!=0:
#         for item in default_list:
#             if item == "valid_range":
#                 attr[item] = str(-1E35 )+","+str(1E35 )
#             else:
#                 attr[item] = "not defined"
#     attr["missing_value"] = -9999
#     return copy.deepcopy(attr)
# 
# def get_datetimefromnctime(ds,time,time_units):
#     """
#     Purpose:
#      Create a series of datetime objects from the time read from a netCDF file.
#     Usage:
#      qcutils.get_datetimefromnctime(ds,time,time_units)
#     Side effects:
#      Creates a Python datetime series in the data structure
#     Author: PRI
#     Date: September 2014
#     """
#     ts = int(ds.globalattributes["time_step"])
#     nRecs = int(ds.globalattributes["nc_nrecs"])
#     dt = netCDF4.num2date(time,time_units)
#     ds.series[unicode("DateTime")] = {}
#     ds.series["DateTime"]["Data"] = list(dt)
#     ds.series["DateTime"]["Flag"] = numpy.zeros(nRecs)
#     ds.series["DateTime"]["Attr"] = {}
#     ds.series["DateTime"]["Attr"]["long_name"] = "Datetime in local timezone"
#     ds.series["DateTime"]["Attr"]["units"] = "None"
#     
# def get_datetimefromymdhms(ds):
#     ''' Creates a series of Python datetime objects from the year, month,
#     day, hour, minute and second series stored in the netCDF file.'''
#     SeriesList = ds.series.keys()
#     if 'Year' not in SeriesList or 'Month' not in SeriesList or 'Day' not in SeriesList or 'Hour' not in SeriesList or 'Minute' not in SeriesList or 'Second' not in SeriesList:
#         return
#     nRecs = get_nrecs(ds)
#     ts = ds.globalattributes["time_step"]
#     ds.series[unicode('DateTime')] = {}
#     ds.series['DateTime']['Data'] = [None]*nRecs
#     if "Microseconds" in ds.series.keys():
#         microseconds = ds.series["Microseconds"]["Data"]
#     else:
#         microseconds = numpy.zeros(nRecs,dtype=numpy.float64)
#     for i in range(nRecs):
#         #print i,int(ds.series['Year']['Data'][i]),int(ds.series['Month']['Data'][i]),int(ds.series['Day']['Data'][i])
#         #print i,int(ds.series['Hour']['Data'][i]),int(ds.series['Minute']['Data'][i]),int(ds.series['Second']['Data'][i])
#         ds.series['DateTime']['Data'][i] = datetime.datetime(int(ds.series['Year']['Data'][i]),
#                                                        int(ds.series['Month']['Data'][i]),
#                                                        int(ds.series['Day']['Data'][i]),
#                                                        int(ds.series['Hour']['Data'][i]),
#                                                        int(ds.series['Minute']['Data'][i]),
#                                                        int(ds.series['Second']['Data'][i]),
#                                                        int(microseconds[i]))
#     ds.series['DateTime']['Flag'] = numpy.zeros(nRecs)
#     ds.series['DateTime']['Attr'] = {}
#     ds.series['DateTime']['Attr']['long_name'] = 'Date-time object'
#     ds.series['DateTime']['Attr']['units'] = 'None'
# 
# def get_nrecs(ds):
#     if 'nc_nrecs' in ds.globalattributes.keys():
#         nRecs = int(ds.globalattributes['nc_nrecs'])
#     elif 'NumRecs' in ds.globalattributes.keys():
#         nRecs = int(ds.globalattributes['NumRecs'])
#     else:
#         series_list = ds.series.keys()
#         nRecs = len(ds.series[series_list[0]]['Data'])
#     return nRecs
#     
# def MakeEmptySeries(ds,ThisOne):
#     nRecs = int(ds.globalattributes['nc_nrecs'])
#     Series = float(-9999)*numpy.ones(nRecs,dtype=numpy.float64)
#     Flag = numpy.ones(nRecs,dtype=numpy.int32)
#     Attr = MakeAttributeDictionary()
#     return Series,Flag,Attr    
# 
# 
# def round_datetime(ds,mode="nearest_timestep"):
#     """
#     Purpose:
#      Round the series of Python datetimes to the nearest time based on mode
#     Usage:
#      qcutils.round_datetime(ds,mode=mode)
#      where;
#       mode = "nearest_second" rounds to the nearesy second
#       mode = "nearest_timestep" rounds to the nearest time step
#     Author: PRI
#     Date: February 2015
#     """
#     # local pointer to the datetime series
#     ldt = ds.series["DateTime"]["Data"]
#     # check which rounding option has been chosen
#     if mode.lower()=="nearest_timestep":
#         # get the time step
#         if "time_step" in ds.globalattributes:
#             ts = int(ds.globalattributes["time_step"])
#         else:
#             ts = numpy.mean(get_timestep(ds)/60)
#             ts = roundtobase(ts,base=30)
#             ds.globalattributes["time_step"] = ts
#         # round to the nearest time step
#         rldt = [rounddttots(dt,ts=ts) for dt in ldt]
#     elif mode.lower()=="nearest_second":
#         # round to the nearest second
#         rldt = [rounddttoseconds(dt) for dt in ldt]
#     else:
#         # unrecognised option for mode, return original datetime series
#         rldt = ds.series["DateTime"]["Data"]
#     # replace the original datetime series with the rounded one
#     ds.series["DateTime"]["Data"] = rldt
#     
# def get_timestep(ds):
#     """
#     Purpose:
#      Return an array of time steps in seconds between records
#     Useage:
#      dt = qcutils.get_timestep(ds)
#     Author: PRI
#     Date: February 2015
#     """
#     # local pointer to the Python datetime series
#     ldt = ds.series["DateTime"]["Data"]
#     # time step between records in seconds
#     dt = numpy.array([(ldt[i]-ldt[i-1]).total_seconds() for i in range(1,len(ldt))])
#     return dt    
# 
# def roundtobase(x,base=5):
#     return int(base*round(float(x)/base))
# 
# def rounddttots(dt,ts=30):
#     dt += datetime.timedelta(minutes=int(ts/2))
#     dt -= datetime.timedelta(minutes=dt.minute % int(ts),seconds=dt.second,microseconds=dt.microsecond)
#     return dt 
# 
# def rounddttoseconds(dt):
#     dt += datetime.timedelta(seconds=0.5)
#     dt -= datetime.timedelta(seconds=dt.second % 1,microseconds=dt.microsecond)
#     return dt
# 
# def CheckTimeStep(ds):
#     """
#     Purpose:
#      Checks the datetime series in the data structure ds to see if there are
#      any missing time stamps.
#      This function returns a logical variable that is true if any gaps exist
#      in the time stamp.
#     Useage:
#      has_gaps = CheckTimeSTep(ds)
#      if has_gaps:
#          <do something about missing time stamps>
#     Author: PRI
#     Date: April 2013
#     """
#     # set the has_gaps logical
#     has_gaps = False
#     # get the number of records
#     nRecs = int(ds.globalattributes["nc_nrecs"])
#     # get the time step
#     ts = int(ds.globalattributes["time_step"])
#     # time step between records in seconds
#     dt = get_timestep(ds)
#     # indices of elements where time step not equal to default
#     index = numpy.where(dt!=ts*60)[0]
#     # check to see if ww have any time step problems
#     if len(index)!=0:
#         has_gaps = True        
#     return has_gaps
# 
# # def FixTimeStep(ds,fixtimestepmethod="round"):
# #     """
# #     Purpose:
# #      Fix problems with the time stamp.
# #     Useage:
# #      qcutils.FixTimeStep(ds,fixtimestepmethod=fixtimestepmethod)
# #     Author: PRI
# #     Date: April 2013
# #     Modified:
# #      February 2015 - split check and fix functions into different routines
# #     """
# #     # get the number of records
# #     nRecs = int(ds.globalattributes["nc_nrecs"])
# #     # get the time step
# #     ts = int(ds.globalattributes["time_step"])
# #     # time step between records in seconds
# #     dt = get_timestep(ds)
# #     dtmin = numpy.min(dt)
# #     dtmax = numpy.max(dt)
# #     if dtmin < ts*60:
# #         # duplicate or overlapping times found
# #         RemoveDuplicateRecords(ds)
# #         dt = get_timestep(ds)
# #         dtmin = numpy.min(dt)
# #         dtmax = numpy.max(dt)
# #         #log.info("After RemoveDuplicateRecords:"+str(dtmin)+" "+str(dtmax))
# #     if numpy.min(numpy.mod(dt,ts*60))!=0 or numpy.max(numpy.mod(dt,ts*60))!=0:
# #         # non-integral time steps found
# #         # indices of elements where time step not equal to default
# #         index = numpy.where(numpy.min(numpy.mod(dt,ts*60))!=0 or numpy.max(numpy.mod(dt,ts*60))!=0)[0]
# #         FixNonIntegralTimeSteps(ds,fixtimestepmethod=fixtimestepmethod)
# #         dt = get_timestep(ds)
# #         dtmin = numpy.min(dt)
# #         dtmax = numpy.max(dt)
# #         #log.info("After FixNonIntegralTimeSteps:"+str(dtmin)+" "+str(dtmax))
# #     if dtmax > ts*60:
# #         # time gaps found
# #         FixTimeGaps(ds)
# #         dt = get_timestep(ds)
# #         dtmin = numpy.min(dt)
# #         dtmax = numpy.max(dt)
# #         #log.info("After FixTimeGaps: "+str(dtmin)+" "+str(dtmax))
#         
# # def get_xldatefromdatetime(ds):
# #     '''
# #     Purpose:
# #      Returns a list of xldatetime (floating point number represent decimal days
# #      since 00:00 1/1/1900) from a list of Python datetimes
# #     Usage:
# #      qcutils.get_xldatefromdatetime(ds)
# #     Assumptions:
# #      The Excel datetime series ("xlDateTime") exists in the data structure ds.
# #     Author: PRI
# #     '''
# #     # get the datemode of the original Excel spreadsheet
# #     if "xl_datemode" in ds.globalattributes.keys():
# #         datemode = int(ds.globalattributes["xl_datemode"])
# #     else:
# #         datemode = int(0)
# #     nRecs = int(ds.globalattributes["nc_nrecs"])
# #     # get the Excel datetime series, flag and attributes
# #     if "xlDateTime" in ds.series.keys():
# #         xldt_org,xldt_flag,xldt_attr = GetSeriesasMA(ds,"xlDateTime")
# #     else:
# #         xldt_flag = numpy.zeros(nRecs,dtype=numpy.int32)
# #         xldt_attr = MakeAttributeDictionary(long_name="Date/time in Excel format",units="days since 1899-12-31 00:00:00")
# #     # get a local pointer to the Python DateTime series in ds
# #     ldt = ds.series["DateTime"]["Data"]
# #     # get a list of Excel datetimes from the Python datetime objects
# #     xldate = [xlrd.xldate.xldate_from_datetime_tuple((ldt[i].year,
# #                                                       ldt[i].month,
# #                                                       ldt[i].day,
# #                                                       ldt[i].hour,
# #                                                       ldt[i].minute,
# #                                                       ldt[i].second),
# #                                                       datemode) for i in range(0,len(ldt))]
# #     xldt_new = numpy.ma.array(xldate, dtype=numpy.float64)
# #     # overwrite the existing Excel datetime series
# #     CreateSeries(ds,"xlDateTime",xldt_new,Flag=xldt_flag,Attr=xldt_attr)
#     
# # def get_ymdhmsfromdatetime(ds):
# #     '''
# #     Purpose:
# #      Gets the year, month, day, hour, minute and second from a list of
# #      Python datetimes.  The Python datetime series is read from
# #      the input data structure and the results are written back to the
# #      data structure.
# #     Usage:
# #      qcutils.get_ymdhmsfromdatetime(ds)
# #     Assumptions:
# #      None
# #     Author: PRI
# #     '''
# #     nRecs = int(ds.globalattributes["nc_nrecs"])
# #     dt = ds.series["DateTime"]["Data"]
# #     flag = numpy.zeros(nRecs,dtype=numpy.int32)
# #     Year = numpy.array([dt[i].year for i in range(0,nRecs)]).astype(numpy.int32)
# #     Month = numpy.array([dt[i].month for i in range(0,nRecs)]).astype(numpy.int32)
# #     Day = numpy.array([dt[i].day for i in range(0,nRecs)]).astype(numpy.int32)
# #     Hour = numpy.array([dt[i].hour for i in range(0,nRecs)]).astype(numpy.int32)
# #     Minute = numpy.array([dt[i].minute for i in range(0,nRecs)]).astype(numpy.int32)
# #     Second = numpy.array([dt[i].second for i in range(0,nRecs)]).astype(numpy.int32)
# #     Hdh = numpy.array([float(Hour[i])+float(Minute[i])/60. for i in range(0,nRecs)]).astype(numpy.float64)
# #     Ddd = numpy.array([(dt[i] - datetime.datetime(Year[i],1,1)).days+1+Hdh[i]/24. for i in range(0,nRecs)]).astype(numpy.float64)
# #     CreateSeries(ds,'Year',Year,Flag=flag,Attr=MakeAttributeDictionary(long_name='Year',units='none'))
# #     CreateSeries(ds,'Month',Month,Flag=flag,Attr=MakeAttributeDictionary(long_name='Month',units='none'))
# #     CreateSeries(ds,'Day',Day,Flag=flag,Attr=MakeAttributeDictionary(long_name='Day',units='none'))
# #     CreateSeries(ds,'Hour',Hour,Flag=flag,Attr=MakeAttributeDictionary(long_name='Hour',units='none'))
# #     CreateSeries(ds,'Minute',Minute,Flag=flag,Attr=MakeAttributeDictionary(long_name='Minute',units='none'))
# #     CreateSeries(ds,'Second',Second,Flag=flag,Attr=MakeAttributeDictionary(long_name='Second',units='none'))
# #     CreateSeries(ds,'Hdh',Hdh,Flag=flag,Attr=MakeAttributeDictionary(long_name='Decimal hour of the day',units='none'))
# #     CreateSeries(ds,'Ddd',Ddd,Flag=flag,Attr=MakeAttributeDictionary(long_name='Decimal day of the year',units='none'))    
# #     
# 
# # def CreateSeries(ds,Label,Data,FList=None,Flag=None,Attr=None):
# #     """
# #     Purpose:
# #      Create a series (1d array) of data in the data structure.
# #      If the series already exists in the data structure, data values and QC flags will be
# #      overwritten but attributes will be preserved.  However, the long_name and units attributes
# #      are treated differently.  The existing long_name will have long_name appended to it.  The
# #      existing units will be overwritten with units.
# #      This utility is the prefered method for creating or updating a data series because
# #      it implements a consistent method for creating series in the data structure.  Direct
# #      writes to the contents of the data structure are discouraged (unless PRI wrote the code:=P).
# #     Usage:
# #      Fsd,flag,attr = qcutils.GetSeriesasMA(ds,"Fsd")
# #       ... do something to Fsd here ...
# #      qcutils.CreateSeries(ds,"Fsd",Fsd,Flag=flag,Attr=attr)
# #     Author: PRI
# #     Date: Back in the day
# #     """
# #     ds.series['_tmp_'] = {}                       # create a temporary series to avoid premature overwrites
# #     # put the data into the temporary series
# #     if numpy.ma.isMA(Data):
# #         ds.series['_tmp_']['Data'] = numpy.ma.filled(Data,float(-9999))
# #     else:
# #         ds.series['_tmp_']['Data'] = numpy.array(Data)
# #     # copy or make the QC flag
# #     if Flag is None:
# #         ds.series['_tmp_']['Flag'] = MakeQCFlag(ds,FList)
# #     else:
# #         ds.series['_tmp_']['Flag'] = Flag.astype(numpy.int32)
# #     # do the attributes
# #     ds.series['_tmp_']['Attr'] = {}
# #     if Label in ds.series.keys():                 # check to see if the series already exists
# #         for attr in ds.series[Label]['Attr']:     # if it does, copy the existing attributes
# #             if attr in Attr and ds.series[Label]['Attr'][attr]!=Attr[attr]:
# #                 ds.series['_tmp_']['Attr'][attr] = Attr[attr]
# #             else:
# #                 ds.series['_tmp_']['Attr'][attr] = ds.series[Label]['Attr'][attr]
# #         for attr in Attr:
# #             if attr not in ds.series['_tmp_']['Attr'].keys():
# #                 ds.series['_tmp_']['Attr'][attr] = Attr[attr]
# #     else:
# #         for item in Attr:
# #             ds.series['_tmp_']['Attr'][item] = Attr[item]
# #     ds.series[unicode(Label)] = ds.series['_tmp_']     # copy temporary series to new series
# #     del ds.series['_tmp_']                        # delete the temporary series
#     
#     
#     
# # def RemoveDuplicateRecords(ds):
# #     """ Remove duplicate records."""
# #     # the ds.series["DateTime"]["Data"] series is actually a list
# #     for item in ["DateTime","DateTime_UTC"]:
# #         if item in ds.series.keys():
# #             ldt,ldt_flag,ldt_attr = GetSeries(ds,item)
# #             # ldt_nodups is returned as an ndarray
# #             ldt_nodups,idx_nodups = numpy.unique(numpy.array(ldt),return_index=True)
# #             # now get ldt_nodups as a list
# #             ldt_nodups = ldt_nodups.tolist()
# #             # and put it back into the data structure
# #             ds.series[item]["Data"] = ldt_nodups
# #             ds.series[item]["Flag"] = ldt_flag[idx_nodups]
# #     # get a list of the series in the data structure
# #     series_list = [item for item in ds.series.keys() if '_QCFlag' not in item]
# #     # remove the DateTime
# #     for item in ["DateTime","DateTime_UTC"]:
# #         if item in series_list: series_list.remove(item)
# #     # loop over the series in the data structure
# #     for ThisOne in series_list:
# #         data_dups,flag_dups,attr = GetSeriesasMA(ds,ThisOne)
# #         data_nodups = data_dups[idx_nodups]
# #         flag_nodups = flag_dups[idx_nodups]
# #         CreateSeries(ds,ThisOne,data_nodups,Flag=flag_nodups,Attr=attr)
# #     ds.globalattributes['nc_nrecs'] = len(ds.series["DateTime"]["Data"])      
#     
# # def FixNonIntegralTimeSteps(ds,fixtimestepmethod=""):
# #     """
# #     Purpose:
# #      Fix time steps that are not an integral number of the default time step.
# #      The default time step is read from the "time_step" global attribute which is read from
# #      the L1 control file and written to the L1 netCDF file.
# #      The most common cause of non-integral time steps is drift in logger time stamp or
# #      rounding errors in Excel's treatment of datetimes.
# #     Usage:
# #      FixNonIntegralTimeSteps(ds)
# #     Called By: CheckTimeStep
# #     Author: PRI
# #     Date: February 2015
# #     To do:
# #      Implement [I]nterpolate
# #     """
# #     ts = int(ds.globalattributes["time_step"])
# #     ldt = ds.series["DateTime"]["Data"]
# #     dt_diffs = numpy.array([(ldt[i]-rounddttots(ldt[i],ts=ts)).total_seconds() for i in range(1,len(ldt))])
# #     ans = fixtimestepmethod
# #     if ans=="": ans = raw_input("Do you want to [Q]uit, [I]nterploate or [R]ound? ")
# #     if ans.lower()[0]=="q":
# #         print ("Quiting ...")
# #         sys.exit()
# #     if ans.lower()[0]=="i":
# #         print ("Interpolation to regular time step not implemented yet ...")
# #         sys.exit()
# #     if ans.lower()[0]=="r":        
# #         ldt_rounded = [rounddttots(dt,ts=ts) for dt in ldt]
# #         rdt = numpy.array([(ldt_rounded[i]-ldt_rounded[i-1]).total_seconds() for i in range(1,len(ldt))])
# #         # replace the existing datetime series with the datetime series rounded to the nearest time step
# #         ds.series["DateTime"]["Data"] = ldt_rounded
# #     ds.globalattributes['nc_nrecs'] = len(ds.series["DateTime"]["Data"])      
#     
# # def FixTimeGaps(ds):
# #     """
# #     Purpose:
# #      Fix gaps in datetime series found by CheckTimeStep.
# #     Useage:
# #      has_gaps = CheckTimeStep(ds)
# #      if has_gaps:
# #          FixTimeGaps(ds)
# #     Author: PRI
# #     Date: April 2013
# #     Modified:
# #      September 2014 - rewrite for clarity and efficiency
# #      February 2015 - and again ...
# #     """
# #     ts = int(ds.globalattributes["time_step"])
# #     #ldt_gaps,ldt_flag,ldt_attr = GetSeries(ds,"DateTime")
# #     ldt_gaps = ds.series["DateTime"]["Data"]
# #     # generate a datetime list from the start datetime to the end datetime
# #     ldt_start = ldt_gaps[0]
# #     ldt_end = ldt_gaps[-1]
# #     ldt_nogaps = [result for result in perdelta(ldt_start,ldt_end,datetime.timedelta(minutes=ts))]
# #     # update the global attribute containing the number of records
# #     nRecs = len(ldt_nogaps)
# #     ds.globalattributes['nc_nrecs'] = nRecs
# #     # find the indices of the no-gap data in the original data
# #     idx_gaps = FindIndicesOfBInA(ldt_gaps,ldt_nogaps)
# #     # update the series of Python datetimes
# #     ds.series['DateTime']['Data'] = ldt_nogaps
# #     org_flag = ds.series['DateTime']['Flag'].astype(numpy.int32)
# #     ds.series['DateTime']['Flag'] = numpy.ones(nRecs,dtype=numpy.int32)
# #     ds.series['DateTime']['Flag'][idx_gaps] = org_flag
# #     # get a list of series in the data structure
# #     series_list = [item for item in ds.series.keys() if '_QCFlag' not in item]
# #     # remove the datetime-related series from data structure
# #     datetime_list = ["DateTime","DateTime_UTC"]
# #     for item in datetime_list:
# #         if item in series_list: series_list.remove(item)
# #     # now loop over the rest of the series in the data structure
# #     for ThisOne in series_list:
# #         data_nogaps = numpy.ones(nRecs,dtype=numpy.float64)*float(-9999)
# #         flag_nogaps = numpy.ones(nRecs,dtype=numpy.int32)
# #         data_gaps,flag_gaps,attr = GetSeriesasMA(ds,ThisOne)
# #         data_nogaps[idx_gaps] = data_gaps
# #         flag_nogaps[idx_gaps] = flag_gaps
# #         CreateSeries(ds,ThisOne,data_nogaps,Flag=flag_nogaps,Attr=attr)
#         
# 
# # def GetSeriesasMA(ds,ThisOne,si=0,ei=-1,mode="truncate"):
# #     """
# #     Purpose:
# #      Returns a data series and the QC flag series from the data structure.
# #     Usage:
# #      data,flag,attr = qcutils.GetSeriesasMA(ds,label,si=0,ei=-1)
# #     where the arguments are;
# #       ds    - the data structure (dict)
# #       label - label of the data series in ds (string)
# #       si    - start index (integer), default 0
# #       ei    - end index (integer), default -1
# #     and the returned values are;
# #       data - values for the requested series in ds
# #              (numpy masked array, float64)
# #       flag - QC flag for the requested series in ds
# #              (numpy masked array, int32)
# #       attr - attribute dictionary for series
# #     Example:
# #      The code snippet below will return the incoming shortwave data values
# #      (Fsd) and the associated QC flag (f) as numpy masked arrays;
# #       ds = qcio.nc_read_series("HowardSprings_2011_L3.nc")
# #       Fsd,f,a = qcutils.GetSeriesasMA(ds,"Fsd")
# #     Author: PRI
# #     """
# #     Series,Flag,Attr = GetSeries(ds,ThisOne,si=si,ei=ei,mode=mode)
# #     Series,WasND = SeriestoMA(Series)
# #     return Series,Flag,Attr        
# 
# def MakeQCFlag(ds,SeriesList):
#     flag = []
#     if len(SeriesList)<=0:
#         #log.info('  MakeQCFlag: no series list specified')
#         pass
#     if len(SeriesList)==1:
#         if SeriesList[0] in ds.series.keys():
#             flag = ds.series[SeriesList[0]]['Flag'].copy()
# 
#     if len(SeriesList)>1:
#         for ThisOne in SeriesList:
#             if ThisOne in ds.series.keys():
#                 if len(flag)==0:
#                     #flag = numpy.ones(numpy.size(ds.series[ThisOne]['Flag']))
#                     flag = ds.series[ThisOne]['Flag'].copy()
#                 else:
#                     tmp_flag = ds.series[ThisOne]['Flag'].copy()      # get a temporary copy of the flag
#                     index = numpy.where(numpy.mod(tmp_flag,10)==0)    # find the elements with flag = 0, 10, 20 etc
#                     tmp_flag[index] = 0                               # set them all to 0
# 
#     return flag.astype(numpy.int32)    
# 
# def perdelta(start, end, delta):
#     """
#     Yields an iterator of datetime objects from start to end with time step delta.
#     """
#     curr = start
#     while curr <= end:
#         yield curr
#         curr += delta
# 
# def FindIndicesOfBInA(a,b):
#     """
#     Purpose:
#      Find the indices of elements in b that also occur in a.
#      The routine is intended for use only with lists of Python datetime
#      values.  This ensures the input series are monotonically increasing
#      (though this is not a requirement) and contain no duplicates (which
#      is required, or at least not handled).
#     Limitations:
#      Argument a is converted to a set to greatly speed the comparison
#      of b elements with a.  This means that duplicates in a will be
#      dropped and hence only 1 index will be returned for each value
#      in b.
#     Usage:
#      indices = qcutils.FindIndicesOfBInA(a,b)
#      where a is a list of Python datetime objects
#            b is a list of Python datetime objects
#            indices is a list of indices in b where the elements of b
#                 also occur in a
#     Author: PRI
#     Date: July 2015
#     Comments: Replaces find_indices used up to V2.9.3.
#     """
#     if len(set(a))!=len(a):
#         msg = " FindIndicesOfBInA: first argument contains duplicate values"
#     tmpset = set(a)
#     indices = [i for i,item in enumerate(b) if item in tmpset]
#     return indices        
# 
# def SeriestoMA(Series):
#     """
#     Convert a numpy ndarray to a masked array.
#     Useage:
#      Series, WasND = SeriestoMA(Series)
#      where:
#       Series (input)    is the data series to be converted.
#       WasND  (returned) is a logical, True if the input series was an ndarray
#       Series (output)   is the input series convered to a masked array.
#     """
#     WasND = False
#     if not numpy.ma.isMA(Series):
#         WasND = True
#         Series = numpy.ma.masked_where(abs(Series-numpy.float64(-9999))<0.0000001,Series)
#     return Series, WasND
# 
# def GetDateIndex(dts,date,ts=30,default=0,match='exact'):
#     try:
#         if len(date)!=0:
#             i = dts.index(dateutil.parser.parse(date))
#         else:
#             if default==-1:
#                 i = len(dts)-1
#             else:
#                 i = default
#     except ValueError:
#         if default==-1:
#             i = len(dts)-1
#         else:
#             i = default
#     if match=="exact":
#         # if an exact match is required, do nothing
#         pass
#     elif match=="startnextmonth":
#         # get to the start of the next day
#         while abs(dts[i].hour+float(dts[i].minute)/60-float(ts)/60)>0.0000001:
#             i = i + 1
#         while dts[i].day!=1:
#             i = i + int(float(24)/(float(ts)/60))
#     elif match=='startnextday':
#         while abs(dts[i].hour+float(dts[i].minute)/60-float(ts)/60)>0.0000001:
#             i = i + 1
#     elif match=="startnexthour":
#         # check the time step value
#         if int(ts)!=60:
#             # if the time step is 60 then it is always the start of the next hour
#             # we assume here that the time period ends on the datetime stamp
#             while dts[i].minute!=ts:
#                 # iterate until the minutes equal the time step
#                 i = i + 1
#     elif match=='endpreviousmonth':
#         while abs(dts[i].hour+float(dts[i].minute)/60)>0.0000001:
#             i = i - 1
#         while dts[i].day!=1:
#             i = i - int(float(24)/(float(ts)/60))
#     elif match=='endpreviousday':
#         while abs(dts[i].hour+float(dts[i].minute)/60)>0.0000001:
#             i = i - 1
#     elif match=="endprevioushour":
#         # check the time step value
#         if int(ts)!=60:
#             # if the time step is 60 then it is always the end of the previous hour
#             # we assume here that the time period ends on the datetime stamp
#             while dts[i].minute!=0:
#                 # iterate until the minutes equal 0
#                 i = i - 1
# 
#     return i