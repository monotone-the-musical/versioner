
import versioner
import argparse

# parameters
parser = argparse.ArgumentParser(description='Versioner - the quick file-backup solution')

parser.add_argument('-b','--backup', nargs='+', metavar='filename', 
                  help='Backup the specified file', 
                  required=False)
parser.add_argument('-c','--comment', nargs='+', metavar='comment', 
                  help='Optional comment when backing up a file (only valid with -b flag)', 
                  required=False)
parser.add_argument('-l','--listbackups', nargs='+', metavar='filename|dirname|ALL', 
                  help='List available backed up versions of specified file or directory. Specify ALL to show entire vault contents', 
                  required=False)
parser.add_argument('-a','--all', help='List all contents of vault', required=False)
parser.add_argument('-r','--restore', nargs='+', metavar='filename|dirname', 
                  help='Restore a backed up version of the file, or choose from a list of backed up files in specified directory', 
                  required=False)
parser.add_argument('-n','--name', nargs='+', metavar='newfilename', 
                  help='Optional new filename when restoring a file (only valid with -r flag)', 
                  required=False)
parser.add_argument('-d','--delete', nargs='+', metavar='filename|dirname', 
                  help='Delete a file from the vault, or choose from a list of files to remove for specified directory', 
                  required=False)
parser.add_argument('--latest', action='store_true', 
                  help='Restore latest version of specified file without prompting (only valid when restoring a specific file with -r flag)', 
                  required=False)

args = parser.parse_args()

# main code
if args.backup:
  if args.comment:
    args.comment = ' '.join(args.comment)
  else:
    args.comment = ""
  args.backup = ' '.join(args.backup)
  thefile = versioner.loadfile(args.backup,"",args.comment)
  wrote = thefile.backup()
  if not wrote[0] and not wrote[1]:
    print ("\n%s already backed up.\n" % (thefile.meta[1]))
  elif not wrote[1]:
    print ("\n%s contents already backed up but new filename noted.\n" % (thefile.meta[1]))
  else:
    print ("\n%s backed up.\n" % (thefile.meta[1]))
elif args.listbackups:
  args.listbackups = ' '.join(args.listbackups)
  thefile = versioner.loadfile(args.listbackups)
  if thefile.dironly:
    thefile.list_backups_for_dir()
  elif thefile.meta[1] == "ALL":
    thefile.show_vault_contents()
  else:
    thefile.list_backups_by_name()
    if thefile.meta[0] != "0":
      thefile.list_backups_by_hash()
elif args.restore:
  args.restore = ' '.join(args.restore)
  if args.name:
    args.name = ' '.join(args.name)
  else:
    args.name = ""
  thefile = versioner.loadfile(args.restore,args.name)
  if thefile.dironly:
    thefile.restore_backups_for_dir()
  else:
    if args.latest:
      thefile.restore_backup_by_name(False,True)
    else:
      thefile.restore_backup_by_name()
elif args.delete:
  args.delete = ' '.join(args.delete)
  thefile = versioner.loadfile(args.delete)
  if thefile.dironly:
    thefile.restore_backups_for_dir(True)
  else:
    thefile.restore_backup_by_name(True)

