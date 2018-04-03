#!/bin/bash
#ANDROID_SDK="/Users/panic/Development/android-sdk-macosx/tools"
ANDROID_SDK="/Users/panic/Library/Android/sdk/tools"
TMP="/tmp/jobb"
if [ $# -eq 0 ];
then
    echo "Usage $0 zipfile"
fi

rm -rvf $TMP
unzip $1 -d $TMP
$ANDROID_SDK/jobb -d $TMP -o main.1.net.openpanzer.obb -pn net.openpanzer -pv 14

# to emulator: adb push file /storage/sdcard/Android/obb/net.openpanzer
