from flask_api import FlaskAPI
import os
import subprocess
import MySQLdb

app = FlaskAPI(__name__)
backIP = '10.200.157.55'
frontIP = '10.200.185.44'
testIP = '10.200.173.19'

@app.route('/request/<string:tier>/<string:mach>/<string:vers>')
def request(tier, mach, vers):
	ret = {'tier' : tier, 'mach' : mach, 'vers' : vers }
	
	print 'enter request'

	cmd = ['sshpass', '-p', 'dfu1357531', 'ssh', 'osru@' + backIP, 'cat', '/home/osru/tier.txt']
	ssh = subprocess.Popen(cmd, stdout=subprocess.PIPE)

	print 'after sshpass tier check'

	for line in ssh.stdout:
		print line
		if(line != tier):
			print 'error: tier not active'
			return "ERROR: tier not active"

	depBundle(mach, vers)
	print ret
	return ret

def depBundle(mach, vers):
	
	if(mach == 'test'):
		
		print 'enter test'
	
                vers = 'backend_' + vers + '.zip'

                myDB = MySQLdb.connect(host="localhost",port=3306,user="deploy",passwd="letMe1n",db="user_info")
                curs = myDB.cursor()
                bundLoc = curs.execute("select location from bundles where name='" + vers + "';")
                myDB.commit()

		print 'after DBQ'

                os.system('scp ' + bundLoc + ' tim@' + testIP + ':/home/tim/bundles/')
                cmd = ['sshpass', '-p', 'Tsuc8223#!', 'ssh', 'time@' + backIP, 'unzip', '/home/tim/bundles/' + vers]
		
		print 'after SCP'

	elif(mach == 'back'):

		vers = 'backend_' + vers + '.zip'

		myDB = MySQLdb.connect(host="localhost",port=3306,user="deploy",passwd="letMe1n",db="user_info")
        	curs = myDB.cursor()
        	curs.execute("select location from bundles where name='" + vers + "';")
        	#myDB.commit()

		#print curs.fetchone()[0]

		os.system('scp ' + curs.fetchone()[0] + ' osru@' + str(backIP) + ':/home/osru/bundles/')
		cmd = ['sshpass', '-p', 'dfu1357531', 'ssh', 'osru@' + backIP, 'unzip', '/home/osru/bundles/' + vers]

	elif(mach == 'front'):

		vers = 'frontend_' + vers + '.zip'

		myDB = MySQLdb.connect(host="localhost",port=3306,user="deploy",passwd="letMe1n",db="user_info")
        	curs = myDB.cursor()
        	bundLoc = curs.execute("select location from bundles where name='" + vers + "';")
        	myDB.commit()

		os.system('scp ' + bundLoc + ' manvi@' + frontIP + ':/home/manvi/bundles/')
		cmd = ['sshpass', '-p', 'babaji', 'ssh', 'manvi@' + frontIP, 'unzip', '/home/manvi/bundles/' + vers]


	#unzip
	ssh = subprocess.Popen(cmd, stdout=subprocess.PIPE)

if(__name__ == '__main__'):
	app.run(host='0.0.0.0', port=5000)
