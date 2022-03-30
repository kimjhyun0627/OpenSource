#!/bin/bash

while read value1; do 
    continue
done < num1.txt
while read value2; do 
    continue
done < num2.txt

res=0

if [ $# -le 0 ]; then
    echo "....none operator parameter...."
    echo "1)add"
    echo "2)sub"
    echo "3)div"
    echo "4)mul"
    read -p "select menu : " select

    if [ "$select" -eq 1 ]; then
        param=add
        res=$(("$value1" + "$value2"))
    elif [ "$select" -eq 2 ]; then
        param=sub
        res=$(("$value1" - "$value2"))
    elif [ "$select" -eq 3 ]; then
        param=div
        res=$(("$value1" / "$value2"))
    elif [ "$select" -eq 4 ]; then
        param=mod
        res=$(("$value1" % "$value2"))
    fi

    echo "num1 : $value1"
    echo "num2 : $value2"
    echo "op : $param"
    echo "result : $res"
else
    if [ "$1" = "add" ]; then
        param=add
        res=$(("$value1" + "$value2"))
    elif [ "$1" = "sub" ]; then
        param=sub
        res=$(("$value1" - "$value2"))
    elif [ "$1" = "div" ]; then
        param=div
        res=$(("$value1" / "$value2"))
    elif [ "$1" = "mod" ]; then
        param=mod
        res=$(("$value1" % "$value2"))
    fi

    echo "num1 : $value1"
    echo "num2 : $value2"
    echo "op : $param"
    echo "result : $res"
fi

exit