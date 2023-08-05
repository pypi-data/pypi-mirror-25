'''
Created on 28 Jul 2017

@author: uqysun6
'''
import os
import urllib
import xml.etree.ElementTree as ET
import netCDF4
from thredds_crawler.crawl import Crawl
from TERNData.tree import Tree
import xarray
 
class Auscover:
        def __init__(self):
                self.url="http://tern-auscover.science.uq.edu.au/thredds/catalog.xml"
                #self.url="http://dapds00.nci.org.au/thredds/catalogs/rr9/emast_tern-aggregations.xml"

                f=urllib.urlopen(self.url)
                self.doc= ET.parse(f)
                self.root=self.doc.getroot()
                self.tree=Tree()
                
                self.parent="Auscover"


        @staticmethod
        def listdata(catalog):
                skips=Crawl.SKIPS+[".*.docx"]+ [".*.pdf"]
                crawler=Crawl(catalog,debug=False,skip=skips,select=[".*.nc"])
                
                urls=[]
                for d in crawler.datasets:
                        url=[s.get("url") for s in d.services if s.get("service").lower()=="opendap"]
                        print(url)
                        urls.append(url)
                return urls[0:2]
                
        @staticmethod
        def combinenc(catalog):
            urls=Auscover.listdata(catalog)
            
            datasets=[xarray.open_dataset(url[0]) for url in urls]
            
            merged=xarray.concat(datasets,'x')
            merged.to_netcdf('all-data.nc')
                            
        def listCatalog(self):
                self.tree.add_node(self.root.attrib.get('name'))
                self.getDatasetCatalogUrl(self,self.root,self.root.attrib.get('name'))
                self.tree.display(self.root.attrib.get('name'))

        def getCatalogUrl(self):
            return self.url

        @staticmethod
        def getDatasetCatalogUrl(self,doc,parent):
                for node in doc.findall('{http://www.unidata.ucar.edu/namespaces/thredds/InvCatalog/v1.0}dataset'):
                            
                        catalog=node.findall('{http://www.unidata.ucar.edu/namespaces/thredds/InvCatalog/v1.0}catalogRef')
                        if len(catalog)==0:
                                self.tree.add_node(node.attrib.get('name'),parent)
                                self.getDatasetCatalogUrl(self,node,node.attrib.get('name'))

                        else:
                                self.tree.add_node(node.attrib.get('name'),parent)
                                for cat in catalog:
                                        self.tree.add_node(cat.attrib.get('{http://www.w3.org/1999/xlink}href'),node.attrib.get('name'))

        @staticmethod
        def readData(catalogUrl):
            url=catalogUrl
            dataset=netCDF4.Dataset(url)
            variables=dataset.variables
            dimensions=dataset.dimensions
            
            print("Global attributes:\n")
            for attr in dataset.ncattrs():
                print (attr+'='+str(getattr(dataset, attr)))
                
            print("\n")
            print("Variables: \n"+ ",".join(str(x) for x in variables)+"\n")

            print("Dimensions: \n"+",".join(str(x) for x in dimensions)+"\n")
            

            
            
        @staticmethod
        def getVarAttribute(catalogUrl,varname):
            url=catalogUrl
            dataset=netCDF4.Dataset(url)
            var=dataset.variables[varname]
            for attr in var.ncattrs():
                print (attr+"="+str(getattr(var, attr)))
            