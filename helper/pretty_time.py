

def secToMMSS(sec):
	return ':'.join([(str(i) if len(str(i))>1 else '0'+str(i)) for i in  divmod(int(sec), 60)])
