**Tool is Back In Development…err hopefully**
This has peaked my interest again. Ive learned quite a bit more (Although not as much as I would like) about since I wrote this. I have an idea. for a new delivery system. Hopefully I get around to fixing it. 

-----

This is a simple backup script primarily for linux (May work on others such as Mac and windows as long as you dont use mysql. However it has not been tested). I thought about just using 1 set of username variables, but this long list gives you flexibility and the ability to use multiple backup options (maybe Ill put this in a seperate file). Features include:

- Custom selection of multiple files and folder paths
- Mysql Dumps (currently via a sub process but will be upgraded to mysqlDB soon)
- Tar.gz or zip backups
- FTP and SFTP support
- DropBox support
- Amazon S3 support
- Google Drive support

Future plans:

- Upgrade to mysqldb and stop using sub processes
- Email selected address completion or error message (Pipe it to mail in linux for now)
- File management
-- Meaning the script will control how many files are kept on the server and disk at a given time. (Meaning only, lets say 5 backups will be kept on the remote server no matter where that be)
- Change over to 1 big class in transferProg.py
- box.net support


Scratched Plans (Unless someone really really wants it)

- Windows Sky Drive support (This is probably not possible)
- Samba
- NFS