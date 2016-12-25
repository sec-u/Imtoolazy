import mmap,os,os.path,sys,subprocess,time,socket
from subprocess import Popen
import _winreg as wreg
PATH= 'alert.ids'
os.chdir(r'D:\Snort\log')
line_number = line_num = counter = 0
compare = ['[**]'];
str1 = ("cmd /c netsh advfirewall firewall add rule name=rule1 dir=in action=block protocol=any remoteip=")
str2 = ("127.0.0.1 ")
str3 = r'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Internet Settings\\ZoneMap\\Domains\\'
str4 = r'SYSTEM\\CurrentControlSet\\Services\\TcpIp\\Parameters\\'
str5 = r'SYSTEM\\CurrentControlSet\\services\\DNS\\Parameters\\'
str6 = r'SYSTEM\\CurrentControlSet\\Services\\AFD\\Parameters\\'
#line_number = int(raw_input('Enter the line number: '))
x = []
empty_line = []
run = True

def lookup(addr):
	try:
		return socket.gethostbyaddr(addr)
	except socket.herror:
		return None, None, None
		
def reverselookup(name):
	try:
		host = socket.gethostbyname(name)
		return host
	except socket.gaierror, err:
		print "cannot resolve hostname: ", name, err

def ipextract():
	f = open('alert.ids', "U")
	i = 1
	for line in f:
		if i == line_number:
			break
		i += 1
	words = line.split() 
	str2= words[1]
	str2 = str2.split(":", 1)[0]
	f.close()
	return str2
	
def dnscheck():
	ip = ipextract()
	print ip
	name,alias,addresslist = lookup(ip)
	ip2 = reverselookup(name)
	winreg(name,'*',0x00000004,0,str3)
	if ip in ip2:
		pass
	else:
		print "Your DNS Cache is poisened!"
		
def synflood():
	winreg(name,'SynAttackProtect',0x00000002,1,str4)
	winreg(name,'TcpMaxPortsExhausted',0x00000005,1,str4)
	winreg(name,'TcpMaxHalfOpen',0x000001F4,1,str4)
	winreg(name,'TcpMaxHalfOpenRetried',0x00000190,1,str4)
	
def icmp():
	winreg(name,'EnableICMPRedirect',0x00000000,1,str4)
	
def snmp():
	winreg(name,'EnableDeadGWDetect',0x00000000,1,str4)
	
def additional():
	winreg(name,'DisableIPSourceRouting',0x00000001,1,str4)
	winreg(name,'EnableMulticastForwarding',0x00000000,1,str4)
	winreg(name,'IPEnableRouter',0x00000000,1,str4)
	winreg(name,'EnableAddrMaskReply',0x00000000,1,str4)
	
def afdprotection():
	winreg(name,'EnableDynamicBacklog',0x00000001,1,str5)
	winreg(name,'MinimumDynamicBacklog',0x00000014,1,str5)
	winreg(name,'MaximumDynamicBacklog',0x00004E20,1,str5)
	winreg(name,'DynamicBacklogGrowthDelta',0x0000000A,1,str5)
	
def winreg(dnsname, regn, rvalue,rpath,str):
	regrule = "".join((str3, dnsname))
	print regrule
	if rpath == 0:
		key = wreg.CreateKey(wreg.HKEY_CURRENT_USER, regrule)
	else:
		key = wreg.CreateKey(wreg.HKEY_LOCAL_MACHINE, regrule)
	wreg.SetValueEx(key, regn, 0, wreg.REG_DWORD, rvalue)

def firewallr():
	global counter
	counter += 1
	wordx = str1.split()
	indexn = str(counter)
	rulename = "".join(("name=rule", indexn))
	wordx[7] = rulename
	wordx = " ".join(wordx)
	wordx = "".join((wordx, ipextract()))
	print wordx
	os.system(wordx)
	return;
	
def emptys():
	if line in ['\n', '\r\n']:
		if any(str(line_num) in i for i in empty_line):
			pass
		else:
			empty_line.extend([str(line_num)])
	
def file_len(fname):
	i = 0
	f = open(fname)
	for i, l in enumerate(f):
		pass
	f.close()
	return i + 1

if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
	while run:	
		last_line = file_len('alert.ids')
		myFile = open('alert.ids', "U")
		for line in myFile.readlines():
			line_num += 1
			emptys()
			if line_num == last_line:
				time.sleep(1)
				break
			if line.find(compare[0]) >= 0:
				line_nums=str(line_num)
				if any(line_nums in s for s in x):
					pass
				else:
					x.extend([line_nums])
					if 'portscan' in line:
						line_number = line_num+2
						firewallr()
					if 'OBFUSCATION' in line:
						line_number = line_num+2
						dnscheck()
					if 'flood' in line:
						line_number = line_num+2
						synflood()
					if 'ddos' in line:
						line_number = line_num+2
						icmp()
					if 'snmp' in line:
						line_number = line_num+2
						snmp()
		time.sleep(1)
		myFile.close()
		line_num = 0
else:
	print "Either file is missing or is not readable"
