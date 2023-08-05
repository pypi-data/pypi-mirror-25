import os
import re
import fnmatch
import threading

from pprint import pprint
from stdplus import readfile
from _run_cmd import run

knownHostsLock = threading.Lock()

class SshConfigBlock(list):
    def __init__(self,line,lineNumber):
        list.__init__(self)
        self.line = line
        self.lineNumber = lineNumber

    def __str__(self):
        return "{}{}{}".format(self.line,"\n" if len(self) > 0 else "","\n".join(x.__repr__() for x in self) )

    def __repr__(self):
        return "{}:<{}>{}{}".format(self.lineNumber,self.line,"\n" if len(self) > 0 else "","\n".join(x.__repr__() for x in self) )

class SshConfig(SshConfigBlock):
    def __init__(self):
        SshConfigBlock.__init__(self,'',0)
        self.hosts = {}
    def __str__(self):
        return "\n".join(x.__repr__() for x in self)
    def __repr__(self):
        return "\n".join(x.__repr__() for x in self)

class WithSettings(SshConfigBlock):
    def __init__(self,line,lineNumber):
        SshConfigBlock.__init__(self,line,lineNumber)
        self.settings = {}
    def addSetting(self,setting):
        if not setting.name in self.settings:
            self.settings[setting.name] = []
        self.settings[setting.name].append(setting)
        
class Host(WithSettings):
    def __init__(self,line,lineNumber):
        WithSettings.__init__(self,line,lineNumber)
        m = re.search('^.*Host[ \t]+([^#]*)(#.*)*',line)
        self.name = m.group(1)

class Comment(SshConfigBlock):
    pass

class Match(WithSettings):
    pass

class Setting(SshConfigBlock):
    def __init__(self,line,lineNumber):
        SshConfigBlock.__init__(self,line,lineNumber)
        m = re.search('^[ \t]*([A-Za-z_]*)[ \t]+([^#]*)(#.*)*',line)
        self.name = m.group(1)
        self.value = m.group(2)
        self.comment = m.group(3)

def parseSshConfig(contents):
    lines = contents.split('\n')
    lineNumber = 0
    rootBlock = SshConfig()
    currentBlock = rootBlock
    for line in lines:
        lineNumber += 1
        if 0 == len(line.strip()) or line.startswith('#'):
            currentBlock.append(Comment(line,lineNumber))
        elif line.strip().startswith('Host '):
            currentBlock = Host(line,lineNumber)
            rootBlock.append(currentBlock)
            rootBlock.hosts[currentBlock.name] = currentBlock
        elif line.strip().startswith('Match '):
            currentBlock = Match(line,lineNumber)
            rootBlock.append(currentBlock)
        else:
            setting = Setting(line,lineNumber)
            currentBlock.append(setting)
            if isinstance(currentBlock,Host) or isinstance(currentBlock,Match):
                currentBlock.addSetting(setting)
            
    return rootBlock

def readSshConfig(path=os.path.expanduser('~/.ssh/config')):
    if os.path.exists(path):
        config = readfile(path)
        return parseSshConfig(config)
    return SshConfig()

def getSshHost(sshConfig,host):
    for pattern,settings in sshConfig.hosts.iteritems():
        if fnmatch.fnmatch(host,pattern):
            return settings
        
def resetKnownHost(ip):
    removeKnownHosts([ip])
    keyscanHost(ip)

def resetKnownHosts(ips):
    removeKnownHosts(ips)
    for ip in ips:
        keyscanHost(ip)

def keyscanHost(ip):
    sshConfig = readSshConfig()
    sshHost = getSshHost(sshConfig,ip)
    proxyCommand = ''
    if sshHost and 'ProxyCommand' in sshHost.settings and sshHost.settings['ProxyCommand'] and sshHost.settings['ProxyCommand'][0].value:
        proxyCommand = sshHost.settings['ProxyCommand'][0].value.replace("-W %h:%p",'')    
    global knownHostsLock
    with knownHostsLock:
        run("mkdir -p ~/.ssh && touch ~/.ssh/known_hosts && {} ssh-keyscan -H {} >> ~/.ssh/known_hosts 2> /dev/null".format(proxyCommand, ip))    

def removeKnownHosts(ips):
    if not ips:
        return
    
    args = []
    for ip in ips:
        args.append("-R {}".format(ip))
    global knownHostsLock
    with knownHostsLock:
        if not os.path.exists(os.path.expanduser('~/.ssh/known_hosts')):
            return
        run("ssh-keygen {}".format(" ".join(args)))

