
import sys
import hashlib
import shutil
import socket
import os
import pwd
import grp
import datetime
import ConfigParser
import re
from os.path import expanduser
from os.path import basename
from pick import pick

# .meta:
# hashval       0
# name          1
# host          2
# uid           3
# gid           4
# perms         5
# versionval    6
# comment       7

blankfile="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"

class loadfile(object):
  def __init__(self,name,newname="",comment=""):

    # configurations
    config = ConfigParser.ConfigParser()
    config.read('/etc/versioner/versioner.cfg')
    tmpvault = config.get('Main', 'vault')
    home = expanduser("~")
    self.vault = tmpvault.replace("~", home)

    versionlabel=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    self.newname=newname
    self.meta=[]
    self.dironly=False
    if os.path.isdir(name):
      self.dironly=True
      name=os.path.abspath(name)
      self.dirname=name
    if os.path.isfile(name):
      name=os.path.abspath(name)
      hashval = gen_hash(name)
      uid = os.stat(name).st_uid
      uid = pwd.getpwuid(uid).pw_name
      gid = os.stat(name).st_gid
      gid = grp.getgrgid(gid)[0]
      perms = os.stat(name).st_mode
    else:
      # name is just the user input. they are restoring a deleted file or could also be a grep string
      hashval = "0"
      uid = "unknown"
      gid = "unknown"
      perms = "unknown"
    if not self.dironly:
      self.meta.append(hashval)
      self.meta.append(name)
      self.meta.append(socket.getfqdn())
      self.meta.append(uid)
      self.meta.append(gid)
      self.meta.append(str(perms))
      self.meta.append(versionlabel)
      self.meta.append(comment)

  def backup(self):
    wrote_hash=False
    wrote_file=False
    check = check_if_exists(self.vault,self.meta)
    if not check[0] or not check[1]: # don't continue if the hash already exists
      fh = open(self.vault+"/versions.table", "a") #append
      for element in self.meta:
        fh.write("%s," % element)
      fh.write("\n")
      fh.close
      wrote_hash=True
    if not check[0]: # if the hash does not exist then backup the physical file
        copyfile(self.meta[1], self.vault+"/versions/"+self.meta[0],self.vault)
        wrote_file=True
    if wrote_hash or wrote_file:
      copyfile(self.vault+"/versions.table", self.vault+"/versions/",self.vault) #backup previous version of table in vault
    return [wrote_hash,wrote_file]

  def list_backups_by_hash(self):
    versionlist=[]
    backedup=False
    with open(self.vault+"/versions.table", "r") as fh:
      filedata = fh.readlines()
    for arecord in filedata:
      check=arecord.split(",")
      if check[0] == self.meta[0]:
        versionlist.append(check[1])
    if len(versionlist) > 0:
      backedup=True
      if (len(versionlist) != 1 and versionlist[0] != self.meta[1]) or (len(versionlist) > 1):
        print ("Known filenames for current version:\n")
        for arecord in versionlist:
          print (" > %s" % (arecord))
        print ("")

  def list_backups_by_name(self):
    versionlist=[]
    backedup=False
    if not os.path.isfile(self.vault+"/versions.table"):
      if not os.path.exists(self.vault):
            os.makedirs(self.vault)
      if not os.path.exists(self.vault+"/versions"):
            os.makedirs(self.vault+"/versions")
      open(self.vault+"/versions.table", 'a+').close()
    with open(self.vault+"/versions.table", "r") as fh:
      filedata = fh.readlines()
    for arecord in filedata:
      check=arecord.split(",")
      if check[1] == self.meta[1]:
        if check[0] == self.meta[0]:
          versionlist.append([check[0],check[1]," X ",check[6],check[7]])
          backedup=True
        else:
          versionlist.append([check[0],check[1],"   ",check[6],check[7]])
    if not backedup and self.meta[0] != "0":
      print ("\nWARNING: Current version not backed up!")
    elif backedup:
      print ("\nFile is backed up!")
    if len(versionlist) > 0:
      print ("\nVersions available:\n")
      for arecord in versionlist:
        if arecord[4] != "":
          print (" > (%s) %s%s - %s" % (arecord[3],basename(arecord[1]),arecord[2],arecord[4]))
        else:
          print (" > (%s) %s%s" % (arecord[3],basename(arecord[1]),arecord[2]))
    print ("")

  def list_backups_for_dir(self): 
    versionlist=[]
    backedup=False
    if not os.path.isfile(self.vault+"/versions.table"):
      sys.exit()
    with open(self.vault+"/versions.table", "r") as fh:
      filedata = fh.readlines()
    for arecord in filedata:
      check=arecord.split(",")
      if os.path.dirname(check[1]) == self.dirname:
        versionlist.append([check[0],check[1],"   ",check[6],check[7]])
    if len(versionlist) > 0:
      print ("\nFiles that have been backed up in %s:\n" % (self.dirname))
      for arecord in versionlist:
        if arecord[4] != "":
          print (" > (%s) %s%s - %s" % (arecord[3],basename(arecord[1]),arecord[2],arecord[4]))
        else:
          print (" > (%s) %s%s" % (arecord[3],basename(arecord[1]),arecord[2]))
    print ("")

  def restore_backups_for_dir(self,delfile=False):
    versionlist=[]
    backedup=False
    if not os.path.isfile(self.vault+"/versions.table"):
      if not os.path.exists(self.vault):
            os.makedirs(self.vault)
      if not os.path.exists(self.vault+"/versions"):
            os.makedirs(self.vault+"/versions")
      open(self.vault+"/versions.table", 'a+').close()
    with open(self.vault+"/versions.table", "r") as fh:
      filedata = fh.readlines()
    for arecord in filedata:
      check=arecord.split(",")
      if os.path.dirname(check[1]) == self.dirname:
        versionlist.append([check[0],check[1],"   ",check[6],check[7],check[5]])
    if len(versionlist) > 0:
      menulist=[]
      for arecord in versionlist:
        menulist.append(" (%s) %s%s %s" % (arecord[3],basename(arecord[1]),arecord[2],arecord[4]))
      menulist.append(" abort")
      if delfile:
        option, index = pick(menulist, "Backups available for deletion from vault:")
      else:
        option, index = pick(menulist, "Backups available for specified directory:")
      if option == " abort":
        print ("\ncancelled\n")
        sys.exit()
      hash_to_restore = ("%s" % (versionlist[index][0]))
      file_to_restore = ("%s" % (versionlist[index][1]))
      file_permissions = ("%s" % (versionlist[index][5]))
      if self.newname:
        file_to_restore=self.newname
      copyfile(self.vault+"/versions/"+hash_to_restore,file_to_restore,self.vault,delfile,hash_to_restore)
      if delfile:
        remove_from_table(self.vault, hash_to_restore, file_to_restore)
        print ("\nFile %s removed from vault." % (file_to_restore))
      else:
        origperm=int(file_permissions)
        os.chmod(file_to_restore, origperm)  # set permissions just in case copy2 didn't do it.
        print ("\nFile %s restored." % (file_to_restore))
    print ("")

  def restore_backup_by_name(self,delfile=False,latest=False):
    versionlist=[]
    backedup=False
    if not os.path.isfile(self.vault+"/versions.table"):
      if not os.path.exists(self.vault):
            os.makedirs(self.vault)
      if not os.path.exists(self.vault+"/versions"):
            os.makedirs(self.vault+"/versions")
      open(self.vault+"/versions.table", 'a+').close()
    with open(self.vault+"/versions.table", "r") as fh:
      filedata = fh.readlines()
    searchstring=re.compile(self.meta[1],re.I)
    for arecord in filedata:
      check=arecord.split(",")
      hit = searchstring.search(check[1])
      if hit:                                   
        if check[0] == self.meta[0]:
          versionlist.append([check[0],check[1]," X ",check[6],check[7],check[5]])
          backedup=True
        else:
          versionlist.append([check[0],check[1],"   ",check[6],check[7],check[5]])
    if len(versionlist) > 0:
      menulist=[]
      for arecord in versionlist:
        menulist.append(" (%s) %s%s %s" % (arecord[3],basename(arecord[1]),arecord[2],arecord[4]))
      menulist.append(" abort")
      if delfile:
        option, index = pick(menulist, "Versions available for removal from vault:")
      else:
        if not latest and len(versionlist) > 1:
          option, index = pick(menulist, "Versions available:")
        else:
          option = ""
          index=0
          if len(versionlist) > 1:
            index = -1 
      if option == " abort":
        print ("\ncancelled\n")
        sys.exit()
      hash_to_restore = ("%s" % (versionlist[index][0]))
      file_to_restore = ("%s" % (versionlist[index][1]))
      file_permissions = ("%s" % (versionlist[index][5]))
      if self.newname:
        file_to_restore=self.newname
      copyfile(self.vault+"/versions/"+hash_to_restore,file_to_restore,self.vault,delfile,hash_to_restore)
      if delfile:
        remove_from_table(self.vault, hash_to_restore, file_to_restore)
        print ("\nFile %s removed from vault." % (file_to_restore))
      else:
        origperm=int(file_permissions)
        os.chmod(file_to_restore, origperm)  # set permissions just in case copy2 didn't do it.
        print ("\nFile %s restored." % (file_to_restore))
    print ("")

  def show_vault_contents(self):
    versionlist=[]
    if not os.path.isfile(self.vault+"/versions.table"):
      if not os.path.exists(self.vault):
            os.makedirs(self.vault)
      if not os.path.exists(self.vault+"/versions"):
            os.makedirs(self.vault+"/versions")
      open(self.vault+"/versions.table", 'a+').close()
    with open(self.vault+"/versions.table", "r") as fh:
      filedata = fh.readlines()
    for arecord in filedata:
      check=arecord.split(",")
      versionlist.append([check[0],check[1],"   ",check[6],check[7]])
    if len(versionlist) > 0:
      print ("\nVault Contents:\n")
      for arecord in versionlist:
        if arecord[4] != "":
          print (" > (%s) %s%s - %s" % (arecord[3],arecord[1],arecord[2],arecord[4]))
        else:
          print (" > (%s) %s%s" % (arecord[3],arecord[1],arecord[2]))
    print ("")

def check_if_exists(vault,localmetadata):
  hashexists=False
  fileexists=False
  if not os.path.isfile(vault+"/versions.table"):
    if not os.path.exists(vault):
          os.makedirs(vault)
    if not os.path.exists(vault+"/versions"):
          os.makedirs(vault+"/versions")
    open(vault+"/versions.table", 'a+').close()
  with open(vault+"/versions.table", "r") as fh:
    filedata = fh.readlines()
  for arecord in filedata:
    check=arecord.split(",")
    if (check[0] == localmetadata[0]) and (check[1] == localmetadata[1]):
      hashexists=True
      fileexists=True
    elif check[0] == localmetadata[0]:
      hashexists=True
  return [hashexists,fileexists]

def copyfile(sourcefile,destfile,vault,delfile=False,filehashval=blankfile):
  if delfile:
    hashcount = 0
    with open(vault+"/versions.table","r") as inputfile:
      for line in inputfile:
        check=line.split(",")
        if check[0] == filehashval:
            hashcount += 1
      inputfile.close()
    if hashcount == 1:
      os.remove(sourcefile)
  else:
    if os.path.isfile(destfile):
      okhash = False
      okname = False
      BUF_SIZE = 65536  # read in 64k blocks
      sha256 = hashlib.sha256()
      filehashval = gen_hash(destfile)
      with open(vault+"/versions.table","r") as inputfile:
        for line in inputfile:
          check=line.split(",")
          if check[0] == filehashval:
            okhash = True
          if check[1] == destfile:
            okname = True
      inputfile.close()
      if not okhash or not okname:
        print ("\nWARNING: Current version not backed up!")
        tocontinue = raw_input("\nContinue anyway? (y|N): ").lower()
        if tocontinue != "y":
          print ("\nAborting...\n")
          sys.exit()
    shutil.copy2(sourcefile, destfile)

def remove_from_table(vault, hashvalue, filename):
  with open(vault+"/versions.table","r") as inputfile:
    with open(vault+"/versions.table.updated","a") as outputfile: 
      for line in inputfile:
        check=line.split(",")
        if check[0]!=hashvalue or check[1]!=filename:
          outputfile.write(line)
  inputfile.close()
  outputfile.close()
  os.rename(vault+"/versions.table.updated",vault+"/versions.table")

def gen_hash(somefile):
  filehashval = blankfile
  BUF_SIZE = 65536  # read in 64k blocks
  sha256 = hashlib.sha256()
  with open(somefile, 'rb') as f:
    while True:
      data = f.read(BUF_SIZE)
      if not data:
        break
      sha256.update(data)
      filehashval = ("{0}".format(sha256.hexdigest()))
  return filehashval
