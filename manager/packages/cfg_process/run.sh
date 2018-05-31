#!/bin/bash

script_name='cfg_process'

cd ~/manager/packages/${script_name}
start() {
    loc_User=`whoami`
    ps xu -U $loc_User -u $loc_User | grep python | grep "${script_name}.py" | grep -v grep > /dev/null
    if [ $? != 0 ]
    then
        python3 ${script_name}.py &
        echo "${script_name} ............................... [start]"
    else
        echo "${script_name} ............................... [running]"
    fi
}

stop() {
    loc_User=`whoami`
    ps xu -U $loc_User -u $loc_User | grep perl | grep "${script_name}.py" | grep -v grep > /dev/null
    if [ $? = 0 ]
    then
        ps xu -U $loc_User -u $loc_User | grep python | grep ${script_name}.py | grep -v grep | awk '{print $2}' | xargs kill
        echo "${script_name} ............................... [stop]"
    else
        echo "${script_name} ............................... [no run]"
    fi
}

case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        stop
        start
        ;;
esac
