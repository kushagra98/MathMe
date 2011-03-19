#!/usr/bin/env bash
#using getopts

genpot(){
    intltool-extract --type="gettext/glade" num.ui
    xgettext -k_ -kN_ -o po/MathMe.pot mathme.py mynum.py
    printf "Done!\n"
}

#FIXME add a new set of commands for each locale in merge() an genmo()
merge(){
    printf "Merging old translations with new tepmplate...\n"
    msgmerge po/es.po po/MathMe.pot -o po/es.po
}

genmo(){
    printf "Generating mo files...\n"
    msgfmt po/es.po -o po/es.mo
    cp po/es.mo locale/es/LC_MESSAGES/mx.ipn.esimez.guslez.MathMe.mo
    printf "Done!\n"
}

usage(){
    printf "OPTIONS:\n -p to create translation template\n -m to merge old po files with new template\n -b to generate mo files\n -h this help\n" >&2
    exit 2
}

ARG=

while getopts 'pmbh' OPTION
    do
    case $OPTION in
        p)
            ARG=0
            ;;
            
        m)
            ARG=1
            ;;
            
        b)
            ARG=2
            ;;
            
        h)
            usage
            ;;
      esac
    done
    
if [ "$ARG" ]
    then
        if [ $ARG = 0 ]; then
            genpot
        elif [ $ARG = 1 ]; then
            merge
        elif [ $ARG = 2 ]; then
            genmo
        fi
else
    usage
fi
