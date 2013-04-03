#!/bin/bash

set -u
set -e

basedir="${HOME}/git/arcade"
logfilename="${HOME}/arcade_log"

launcher_index=0
while :
do
    launcher_log="$(${basedir}/launcher.py -f -i ${launcher_index} || exit 1)"
    launcher_index="$(echo "${launcher_log}" | awk -F '=' '/INDEX/ {print $2}')"
    launcher_title="$(echo "${launcher_log}" | awk -F '=' '/TITLE/ {print $2}')"
    launcher_command="$(echo "${launcher_log}" | awk -F '=' '/COMMAND/ {print $2}')"
    test "${launcher_command}" && test "${launcher_index}" || break
    echo "command ${launcher_command}"
    echo "$(date) ${launcher_command}" >> "${logfilename}"
    echo "index ${launcher_index}"
    ${launcher_command} &
    pid=$!
    ${basedir}/killer.py || break
    ps -p $pid >/dev/null 2>&1 || kill -9 $pid
    echo "$(date) QUIT" >> "${logfilename}"
done

