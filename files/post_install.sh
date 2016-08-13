
pip install pick

mkdir -p /usr/local/bin/versioner

cp ./files/vs.py /usr/local/bin/versioner/

mkdir -p /etc/versioner

cp ./files/versioner.cfg /etc/versioner/

echo "python /usr/local/bin/versioner/vs.py \$@" > /usr/local/bin/vs

chmod 755 /usr/local/bin/vs

clear
echo ; echo ; echo "VERSIONER INSTALLED !!!" ; echo ; echo
vs -h
echo ; echo
