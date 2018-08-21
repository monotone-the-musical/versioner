#!/bin/sh

rm -f /usr/bin/vs
rm -f /usr/local/bin/vs # remove legacy
rm -rf /usr/local/bin/versioner
rm -rf /etc/versioner
rm -rf ~/.vault

pip uninstall versioner
pip uninstall pick # remove legacy

exit
