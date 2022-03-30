#!/bin/bash

echo ....create temp directory....
mkdir temp

echo ....copy files to temp directory....
cp num1.txt temp
cp num2.txt temp

echo "1)add"
echo "2)sub"
echo "3)div"
echo "4)mul"
read -p "select menu : " select

if [ "$select" -eq 1 ]; then
    param="add"
elif [ "$select" -eq 2 ]; then
    param="sub";
elif [ "$select" -eq 3 ]; then
    param="div";
elif [ "$select" -eq 4 ]; then
    param="mod";
fi

echo "....$param selected...."

echo ....run calculator....
chmod +x cal.sh
./cal.sh $param