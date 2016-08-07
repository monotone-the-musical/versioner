# VERSIONER  - the quick file-backup solution #

Versioner is a utility designed for administrators to quickly and easily backup specific files whilst working from the CLI.

Good admin practice is to backup sensitive files before making any changes, for example:

* cp -p /etc/hosts /etc/hosts.ORIG
* cp -p /etc/sudoers /etc/sudoers.20160223

However this can quickly become the cause for multiple extraneous files lying around your system, sometimes for years. This not only looks untidy, but can become confusing and in some instances even a security risk.

Versioner neatens this practice by copying the files to a "vault", complete with informative meta-data and content checking through file-hash identification. With Versioner you can quickly swap back and forth between different versions of your file, each easily identifiable by backup date-time and optional comments. The backups are kept hidden away in a configurable directory so that your system remains clean.

Other features include:

 - file-content hash checks ensuring only one physical file is backed up, even if you back-up multiple different filenames with the same content
 - vault-checking performed when restoring files, ensuring you don't restore over another file you haven't yet backed up 
 - easy navigation through the "pick" menu, allowing you to choose which file to restore. Or use the --latest flag to quickly restore to the newest version
 - delete versions of files from the vault at any time with the -d flag
 - see vault contents for specific files or directories, or even the entire vault, through the -l flag
 - each time the vault is updated, the previous version of the vault table-of-contents is itself backed up in the vault.

### Dependencies ###

* Python 2.7 or above (incl Python 3)
* pick - https://github.com/wong2/pick (pip install pick)

### Installation ###

* Ensure dependencies are installed (see above)
* If you are installing for Python 3, then you first need to run the following command: mv versioner.py.python3 versioner.py
* Run ./setup.sh as root user from within the script's directory.

### Instructions ###

run 'vs -h' for all syntax

Some examples:

* To backup file.txt in the current dir: vs -b ./file.txt
* To backup file.txt in the current dir with a comment: vs -b ./file.txt -c hello world
* To see backed up versions of existing file.txt in current dir: vs -l ./file.txt
* To see all files backed up in current directory: vs -l .
* To see entire vault contents: vs -l ALL
* To restore backed up version of existing file.txt in current dir: vs -r ./file.txt
* To restore latest backed up version of existing file.txt in current dir: vs -r ./file.txt --latest
* To restore backed up version of existing file.txt in current dir with new name: vs -r ./file.txt -n ./file-restored.txt
* To restore any file that was backed up in current dir (i.e. not sure of the filename): vs -r .
* To restore any file in the vault that matches the string ".txt" (i.e. grep): vs -r .txt
* To restore any file in the vault that matches the string ".doc" to the current directory with new name "restored.doc": vs -r .doc -n ./restored.doc
* To delete a file in the vault for the current directory: vs -d .

### Note ###

* Versioner is not intended as a complete system backup solution, nor is it a complete version-control system (i.e. GIT). It is merely a command-line tool to help with your day-to-day workflow.
* Current version: v1.1

### contact ###

* monotone.the.musical@gmail.com
