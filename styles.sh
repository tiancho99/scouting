#!/bin/sh

file='scss/'$1'.scss'
echo $file
if [ -f $file ]
then
    echo 'hola'
    sass --watch /mnt/c/Users/tianc/Desktop/scouting/scss/$1.scss /mnt/c/Users/tianc/Desktop/scouting/app/static/css/$1.css
else 
    touch scss/$1.scss
    sass  /mnt/c/Users/tianc/Desktop/scouting/scss/$1.scss /mnt/c/Users/tianc/Desktop/scouting/app/static/css/$1.css
    sass --watch /mnt/c/Users/tianc/Desktop/scouting/scss/$1.scss /mnt/c/Users/tianc/Desktop/scouting/app/static/css/$1.css
fi