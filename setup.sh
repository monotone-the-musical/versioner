
mkdir -p /usr/local/bin/versioner

cp ./vs.py /usr/local/bin/versioner/

cp ./versioner.py /usr/local/bin/versioner/

mkdir -p /etc/versioner

cp ./versioner.cfg /etc/versioner/

echo "python /usr/local/bin/versioner/vs.py \$@" > /usr/local/bin/vs

chmod 755 /usr/local/bin/vs

clear
echo ; echo ; echo "VERSIONER INSTALLED !!!" ; echo ; echo
vs -h
echo ; echo
