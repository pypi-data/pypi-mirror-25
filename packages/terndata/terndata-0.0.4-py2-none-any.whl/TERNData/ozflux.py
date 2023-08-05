'''
Created on 28 Jul 2017

@author: uqysun6
'''

import urllib2
import urllib
import xml.etree.ElementTree as ET
import netCDF4
from thredds_crawler.crawl import Crawl
from TERNData.tree import Tree
import pandas as pd 
#from tkinter import filedialog#python3.6
#import tkFileDialog
import xlsxwriter
from pandas import ExcelWriter
import numpy as np
from netCDF4 import date2num
from TERNData import utils
import datetime
#from os import environ
import os
import constants
from pydap.handlers import netcdf


class Ozflux:
        def __init__(self):
            
                self.url=constants.ROOT+constants.CATALOG

              
                hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
                req=urllib2.Request(self.url,headers=hdr)
                
                f=urllib2.urlopen(req)
            
                self.doc= ET.parse(f)
                self.root=self.doc.getroot()
                self.tree=Tree()
                
                self.parent=constants.NAME
                
                self.siteurlroot=constants.ROOT

        # GET /sites/:site
        @staticmethod
        def listdata(site_name):
            skips=Crawl.SKIPS+[".*.docx"]+ [".*.pdf"]
            urls=[]
                
            if site_name in constants.SITES:                    
                catalog=constants.ROOT+site_name+'/catalog.xml'
                
                crawler=Crawl(catalog,debug=False,skip=skips,select=[".*.nc"])
                
                for d in crawler.datasets:
                        url=[s.get("url") for s in d.services if s.get("service").lower()=="opendap"]
                        urls.append(url[0])
                        #print(url)
                #return dict(enumerate(urls))            
                
            return urls
        
        # GET /sites
        def listCatalog(self):                
                self.tree.add_node(self.parent)
                sites=self.getDatasetCatalogUrl(self,self.root.findall('{http://www.unidata.ucar.edu/namespaces/thredds/InvCatalog/v1.0}dataset')[0],self.parent)
                #self.tree.display(self.parent)
                return sites

        def getCatalogUrl(self):
            return self.url

        @staticmethod
        def getDatasetCatalogUrl(self,doc,parent):
                catalog=doc.findall('{http://www.unidata.ucar.edu/namespaces/thredds/InvCatalog/v1.0}catalogRef')
                sites=[]
                if len(catalog) >0:                  
                    for node in catalog:
                        caturl=self.siteurlroot+node.attrib.get('{http://www.w3.org/1999/xlink}href')
                        self.tree.add_node(caturl,parent)
                        sites.append(caturl)
                return sites
        
        # GET data/:site/:level
        @staticmethod
        def readData(site_name,level):
            url=constants.DATA_URL_ROOT+site_name+'/'+level+'/'+'default/'+site_name+'_'+level+'.nc'
            
            dataset=netCDF4.Dataset(url)
            variables=dataset.variables
            dimensions=dataset.dimensions
            
            return_array = []
            
            #ga=[]
            var=[]
            #dm=[]
            
            #print("Global attributes:\n")
            #for attr in dataset.ncattrs():
                #print (attr+'='+str(getattr(dataset, attr)))
                #ga.append({ attr: getattr(dataset, attr) })
                #temp=[attr,str(getattr(dataset, attr))]
                #ga_dict.append(temp)
                
            
            #print (ga_dict)
            #print("\n")
            #print("Variables: \n"+ ",".join(str(x) for x in variables)+"\n")
            
            for x in variables:
                var.append(str(x))
                
            #print (var_dict)
            #for x in dimensions:
                #dm.append(str(x))
            #print("Dimensions: \n"+",".join(str(x) for x in dimensions)+"\n")
            
            #return_array.append({"Global Attributes": ga})
            #return_array.append({"Variables": var})
            #return_array.append({"Dimensions": dm})
            return var
           
        #GET variables/:site/:level
        @staticmethod
        def readVariables(site_name,level):
            url=constants.DATA_URL_ROOT+site_name+'/'+level+'/'+'default/'+site_name+'_'+level+'.nc'
            dataset=netCDF4.Dataset(url)
            variables=dataset.variables
                
            return_array=[]
            

            for v in variables:
                return_array.append([{"Name":v},{"Dimensions":dataset[v].dimensions},{"Shape":dataset[v].shape}])
#             
            return return_array    

        # GET /sites/:site/:level/:var/   
        @staticmethod
        def getVarAttribute(site_name,level,varname):
            url=constants.DATA_URL_ROOT+site_name+'/'+level+'/'+'default/'+site_name+'_'+level+'.nc'
            dataset=netCDF4.Dataset(url)
            var=dataset.variables[varname]
            
            results=[]
            for attr in var.ncattrs():
                results.append({attr:str(getattr(var, attr))})
                #print (attr+"="+str(getattr(var, attr)))
            return results
        
        # GET /sites/:site/:level/:var/:time
        @staticmethod
        def getTimeInfo(site_name,level,varname):
            url=constants.DATA_URL_ROOT+site_name+'/'+level+'/'+'default/'+site_name+'_'+level+'.nc'
            dataset=netCDF4.Dataset(url)
            var=dataset.variables[varname]
            
            t=dataset.variables["time"]
            
            first=netCDF4.num2date(t[0],t.units)
            last=netCDF4.num2date(t[-1],t.units)
            
            info=[]
            info.append({"Start Date":first.strftime('%Y-%m-%d %H:%M:%S')})
            info.append({"End Date":last.strftime('%Y-%m-%d %H:%M:%S')})
            info.append({"Time step": str(getattr(dataset,"time_step"))})
            
            return info
        # GET /test/sites/:site/:level/:var/:time   
        @staticmethod
        def getTimeSeries(site_name,level,varname):
            url=constants.DATA_URL_ROOT+site_name+'/'+level+'/'+'default/'+site_name+'_'+level+'.nc'
            dataset=netCDF4.Dataset(url)
            var=dataset.variables[varname]
            
            t=dataset.variables["time"]
            dtime=netCDF4.num2date(t[:],t.units)
            
            first=netCDF4.num2date(t[0],t.units)
            last=netCDF4.num2date(t[-1],t.units)
            
            istart=netCDF4.date2index(first,t,select='nearest')
            istop=netCDF4.date2index(last,t,select='nearest')
            
            d=dataset[varname].dimensions
    
            if d==1:
                hs=var[istart:istop]
            else:          
#                 lat=dataset.variables["latitude"][:]
#                 lon=dataset.variables["longitude"][:]
#                 
#                 lati=getattr(dataset, "latitude")
#                 loni=getattr(dataset, "longitude")
#                 
#                 ix=Ozflux.near(lon,loni)
#                 iy=Ozflux.near(lat,lati)
                hs=var[istart:istop,0,0]
                
            tim=dtime[istart:istop]
            
            ts=pd.Series(hs,index=tim,name=varname)
            
            return ts
                
        # GET /subsets/:site/:level/:var/:fromdate/:todate/:format
        @staticmethod
        def getTemporalSubset(site_name,level,var,fromdate,todate,output):
            catalogUrl=constants.DATA_URL_ROOT+site_name+'/'+level+'/'+'default/'+site_name+'_'+level+'.nc'
            dataset=netCDF4.Dataset(catalogUrl,"r")     
     

#            ds_l=utils.nc_read_series(dataset)
            
#            ldt_l=ds_l.series["DateTime"]["Data"]
 
            ###########################
            data,flag,attr=utils.nc_read_var(dataset, "time")
            
            fdate=datetime.datetime.strptime(fromdate,"%Y-%m-%d %H:%M:%S")
            fdate=Ozflux.roundtime(fdate)   
            fnc_time=netCDF4.date2num(fdate,"days since 1800-01-01 00:00:00.0",calendar="gregorian")
            
            tdate=datetime.datetime.strptime(todate,"%Y-%m-%d %H:%M:%S")
            tdate=Ozflux.roundtime(tdate)   
            tnc_time=netCDF4.date2num(tdate,"days since 1800-01-01 00:00:00.0",calendar="gregorian")
            
            si_l=np.where(data==fnc_time)[0][0]
            ei_l=np.where(data==tnc_time)[0][0]
            #######################
            
                 
            #si_l=utils.GetDateIndex(ldt_l,fromdate)
            #ei_l=utils.GetDateIndex(ldt_l,todate)
                
            
            variable_list = var.split(',')

            df,attr = Ozflux.read_netcdf(dataset,si_l,ei_l+1,variable_list)
            
            if output=="csv":                
                Ozflux.save_csvfile(df,dataset,fromdate,todate)
            elif output=="xlsx":
                Ozflux.save_csvfile_xlsx(df,dataset,fromdate,todate)                
            else:
                Ozflux.save_netcdf4(df,variable_list,dataset,fromdate,todate)
 
            dataset.close()
            
            
        @staticmethod
        def roundtime(dt):
            min_est=dt.minute
            sec_est=dt.second
            
            if sec_est !=0:
                dt=dt.replace(second=0)
                
            if min_est >30:
                add_mins=60 - min_est
            elif min_est==0:
                add_mins=0
            else:
                add_mins= 30 - min_est
                
            return dt+datetime.timedelta(minutes=add_mins)
        
        @staticmethod
        def read_netcdf(dataset,si_l,ei_l,variable_list=[]):
                nc_file=dataset
                
                attr = {}
                attr["global"] = {}
                attr["variable"] = {}
        
                gattrlist = nc_file.ncattrs()
                if len(gattrlist)!=0:
                    for item in gattrlist:
                        attr["global"][item] = getattr(nc_file,item)
        
                time = nc_file.variables["time"][:]
                time_units = getattr(nc_file.variables["time"],"units")
                dt = list(netCDF4.num2date(time[si_l:ei_l],time_units))
                latitude=str(getattr(nc_file,"latitude"))
                longitude=str(getattr(nc_file,"longitude"))
                
                if len(variable_list)==0:
                    variable_list = nc_file.variables.keys()
                else:
                    flag_list = []
                    for item in variable_list: flag_list.append(item+"_QCFlag")
                    variable_list = variable_list+flag_list
                data = {}
        
                for item in variable_list:
                    ndims = len(nc_file.variables[item].shape)
                    data["latitude"]=latitude
                    data["longitude"]=longitude
                    if ndims==1:
                        data[item] = nc_file.variables[item][si_l:ei_l]
                    elif ndims==3:
                        data[item] = nc_file.variables[item][si_l:ei_l,0,0]
                    else:
                        raise Exception("unrecognised number of dimensions for variable"+str(item))
        
                    vattrlist = nc_file.variables[item].ncattrs()
                    if len(vattrlist)!=0:
                        attr["variable"][item] = {}
                        for vattr in vattrlist:
                            attr["variable"][item][vattr] = getattr(nc_file.variables[item],vattr)
  
      
                df = pd.DataFrame(data,index=dt)
                return df,attr    
            
        @staticmethod
        def save_csvfile(df,dataset,fromdate,todate):
#             if "DISPLAY" in environ:
#                 f = tkFileDialog.asksaveasfile(mode='w', defaultextension=".csv")
#             else:
            s=constants.HTTP_ROOT+"From "+fromdate+" To "+todate+".csv"
            f=open(s,"w")
            
            if f is None:
                return 
            
#             canopyHeight=str(getattr(dataset, "canopy_height"))
#             dataPolicy="OzFlux (http://data.ozflux.org.au/portal/site/licenceinfo.jspx)"
#             dataURL=str(getattr(dataset,"data_url"))
#             elevation=str(getattr(dataset,"elevation"))
#             institution=str(getattr(dataset,"institution"))
#             landcover=""
#             landuse=""
#             latitude=str(getattr(dataset,"latitude"))
#             longitute=str(getattr(dataset,"longitude"))
#             timezone=str(getattr(dataset,"time_zone"))
#             licenseType=str(getattr(dataset,"license_type"))
#             licenseUrl=str(getattr(dataset,"license_url"))
#             measurementHeight=str(getattr(dataset,"tower_height"))
#             metadataUrl=str(getattr(dataset,"metadata_url"))
#             piEmail=""
#             piName=str(getattr(dataset,"site_pi"))
#             siteName=str(getattr(dataset,"site_name"))
#             soilType=str(getattr(dataset,"soil"))
#             swc1Depth=""
#             ts1Depth=""
#             citation=str(getattr(dataset,"citation"))
#             reference=str(getattr(dataset,"references"))
#             
#             dic={"CanopyHeight":canopyHeight,
#                  "DataPolicy":dataPolicy,
#                  "DataURL":dataURL,
#                  "Elevation":elevation,
#                  "Institution":institution,
#                  "LandCover":landcover,
#                  "LandUse":landuse,
#                  "Latitude":latitude,
#                  "Longitude":longitute,
#                  "TimeZone":timezone,
#                  "LicenseType":licenseType,
#                  "LicenseURL":licenseUrl,
#                  "MeasurementHeight":measurementHeight,
#                  "MetadataURL":metadataUrl,
#                  "PIEmail":piEmail,
#                  "PIName":piName,
#                  "SiteName":siteName,
#                  "SoilType":soilType,
#                  "SWC1Depth":swc1Depth,
#                  "TS1Depth":ts1Depth,
#                  "Citation":citation,
#                  "Reference":reference
#                  } 
            dic=Ozflux.get_global_attr(dataset)

                
            
            for key in dic.keys():
                name=key
                val=dic[key]
                row=name+","+val+"\n"
                f.write(row)
                
            f.write("\n")
            df.to_csv(f)
            f.close() 
            
            print ("Subsets created, use below url to download the file:"+ "\n"+ constants.HTTP_HOST+"downloads/"+"From "+fromdate+" To "+todate+".csv")

        @staticmethod                    
        def save_netcdf4(df,varlist,dataset,fromdate,todate):
#             if "DISPLAY" in environ:
#                 f = tkFileDialog.asksaveasfile(mode='w', defaultextension=".nc")
#             else:
            s=constants.HTTP_ROOT+"From "+fromdate+" To "+todate+".nc"
            f=open(s,"w")
            
            if f is None:
                return    
            ncFile=netCDF4.Dataset(f.name,'w')
              
            globalattr=Ozflux.get_global_attr(dataset)
            
            ncFile.setncatts(globalattr)

            variables=varlist
            ncFile.createDimension('time',len(df.index))
            ndim=ncFile.createVariable('time',dataset.variables['time'].dtype,('time',))
            
            for ncattr in dataset.variables['time'].ncattrs():
                ndim.setncattr(ncattr, dataset.variables['time'].getncattr(ncattr))
 
            dateindex=[]
            for idx,t in enumerate(df.index.values):
                tt=pd.to_datetime(t)
                dateindex.append(date2num(tt,units='days since 1800-01-01 00:00:00.0',calendar='gregorian'))

                
            ncFile.variables['time'][:]=dateindex
            
            for item in variables:
                nvar=ncFile.createVariable(item,dataset.variables[item].dtype,('time'))
                for ncattr in dataset.variables[item].ncattrs():
                    nvar.setncattr(ncattr,dataset.variables[item].getncattr(ncattr))
                ncFile.variables[item][:]=df.iloc[:][item].values
                
            ncFile.close()
            
            print ("Subsets created,use below url to download the file:"+ "\n"+ constants.HTTP_HOST+"downloads/"+"From "+fromdate+" To "+todate+".nc")
        @staticmethod
        def get_global_attr(dataset):
            dic={}
            for k in dataset.ncattrs():
                dic[k]=str(getattr(dataset, k))
            return dic
            

        @staticmethod
        def save_csvfile_xlsx(df,dataset,fromdate,todate):
#             if "DISPLAY" in environ:
#                 f = tkFileDialog.asksaveasfile(mode='w', defaultextension=".xlsx")
#             else:
            s=constants.HTTP_ROOT+"From "+fromdate+" To "+todate+".xlsx"
            f=open(s,"w")            
            
            if f is None:
                return 

            workbook=xlsxwriter.Workbook(f)
            worksheetattr=workbook.add_worksheet("Attr")
            
            dic=Ozflux.get_global_attr(dataset)                
            
            #global attributes
            row=1
            col=0
            worksheetattr.write(0,0,'Global attributes')
            for key in dic.keys():
                worksheetattr.write(row, col,    key)
                worksheetattr.write(row, col+1,  dic[key])
                row+=1
            
            writer=ExcelWriter(f,engine='xlsxwriter')
            writer.book=workbook

            #data
            datacols=[c for c in df.columns if c.lower()[-6:]!='qcflag']
            
            dfdata=df[datacols]
            dfdata.to_excel(writer,'Data')               

            #qc
            dfflag=df.filter(like="_QCFlag")
            dfflag.to_excel(writer,'QCFlag') 

            #close writer and workbook
            writer.save()
            writer.close()
            workbook.close()
            
            #close file
            f.close()
            print ("Subsets created,use below url to download the file:"+ "\n"+ constants.HTTP_HOST+"downloads/"+"From "+fromdate+" To "+todate+".xlsx")
            
