#!/usr/bin/python
import sys, re, fileinput

if len(sys.argv) is not 3:
	print "usage:   ./get_dnsmasq_conf.py <IP> <ad_domain_list>"
	print "example: ./get_dnsmasq_conf 192.168.0.8 ad_domain_list.txt"
	exit()

IP = sys.argv[1]

re_file=re.compile("\.(png|gif|jpg|css|htm|html|json)$", re.IGNORECASE)
re_ip=re.compile("^[0-9.]*$")

urls = dict()
for line in fileinput.input(sys.argv[2]):
	if "!" in line:
		continue
	if "," in line:
		continue
	if "#" in line:
		continue
	if "@" in line:
		continue
	if "?" in line:
		continue
	if "*" in line:
		continue
	if "[" in line:
		continue
	if "]" in line:
		continue
	if "/" in line:
		continue
	if "=" in line:
		continue
	if "&" in line:
		continue
	if ":" in line:
		continue

	line = re.sub('\^$','', line.rstrip())
	line = re.sub('^\|','', line.rstrip())
	line = re.sub('^\||','', line.rstrip())
	#line = line.replace("^$third-party","")
	line = re.sub('\^\$third-party$','', line.rstrip())
	
	if "$" in line:
		continue
	if line[0] == '-' or line[0] == '_' or line[0] == '.' or line[0] == '*':
		continue
	line = line.replace("\r","").replace("\n","")
	if line[-1] == '-' or line[-1] == '_' or line[-1] == '.' or line[-1] == '*' or line[-1] == '|':
		continue
	if line[-1] == '-' or line[-1] == '_' or line[-1] == '.' or line[-1] == '*' or line[-1] == '|':
		continue
	if re_ip.match(line) != None:
		continue
	if re_file.match(line) != None:
		continue

	#remove general subdomain
	#line = line.replace("www.","")
	line = re.sub("^www\.", "", line)
	#change top domain
	line = line.replace(".co.kr",".co_kr")
	#get domain name
	parse = [x for x in line.split('.')]
	name = parse[-2]
	#revert top domain
	line = line.replace("co_kr","co.kr")
	#insert url to dict without duplicates
	if name in urls:
		if line not in urls[name]:
			urls[name].append(line)
	else:
		urls[name]=[]
		urls[name].append(line)

for name in sorted(urls.keys()):
	#get urls_to_exclude via exclude sub domain
	#urls[name] = [y[::-1] for y in sorted([x[::-1] for x in urls[name]])]
	urls_to_exclude = []
	#print ""
	#print name
	#print "urls:\t",
	#print urls[name]
	for url in urls[name]:
		u = [s for s in urls[name] if url in s][1:]
		urls_to_exclude = urls_to_exclude + u
		#print "sub[%s]:\t" % url,
		#print u
	urls[name] = [url for url in urls[name] if url not in urls_to_exclude]
	#generate dnsmasq conf file
	for url in sorted(urls[name]):
		#print url
		print "address=/.%s/%s\t#%s" % (url, IP, name)