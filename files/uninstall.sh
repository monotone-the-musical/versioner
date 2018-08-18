#!/bin/sh

rm -f /usr/bin/vs
rm -rf /usr/local/bin/versioner
rm -rf /etc/versioner
rm -rf ~/.vault

pip uninstall versioner

exit
