mkdir /home/databak

yum install -y nfs-utils
mkdir /home/maintainer
mount -t nfs 103.250.15.28:/home/maintainer /home/maintainer

echo ". /home/maintainer/profile.sh" >> ~/.bash_profile

ssh-keygen 
ssh-copy-id -i ~/.ssh/id_rsa.pub root@210.245.214.242
ssh-copy-id -i ~/.ssh/id_rsa.pub root@210.245.214.246
ssh-copy-id -i ~/.ssh/id_rsa.pub root@43.243.51.24
