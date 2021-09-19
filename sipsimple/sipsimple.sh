#!/bin/bash
sip-settings -a add $SIP_USER@$SIP_SERVER $SIP_PASSWORD
sip-settings -a default $SIP_USER@$SIP_SERVER
sip-audio-session -S -b $*
