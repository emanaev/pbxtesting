#!/bin/bash
cd $(dirname "$0")
cp yate-conf/* /usr/local/etc/yate/
sip-settings -a add 9164440001@pbx.test test
sip-settings -a add 112@pbx.test test
