#!/bin/bash

set -u
set -e

launcher_index=0
while :
do
    launcher_log="$(./launcher.py -f -i ${launcher_index})"
    launcher_index="$(echo "${launcher_log}" | awk -F '=' '/INDEX/ {print $2}')"
    launcher_title="$(echo "${launcher_log}" | awk -F '=' '/TITLE/ {print $2}')"
    launcher_command="$(echo "${launcher_log}" | awk -F '=' '/COMMAND/ {print $2}')"
    test "${launcher_command}" && test "${launcher_index}" || break
    echo "command ${launcher_command}"
    echo "index ${launcher_index}"
    ${launcher_command} &
    pid=$!
    ./killer.py && kill $pid
done

