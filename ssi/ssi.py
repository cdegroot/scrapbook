#!/usr/bin/env python
#
#  I had an old SSI site. I wanted to put the site onto S3. This is
#  my solution. Don't laugh too hard :P
#
import sys, re, os

def process(file, vars = {}):
    input = open(file, "r")
    for line in input.readlines():
        varSearch = re.search('<!--#set var="(.*)" value="(.*)"-->', line)
        if varSearch:
            vars[varSearch.group(1)] = varSearch.group(2)
            continue
        incSearch = re.search('<!--#include virtual="(.*)"-->', line)
        if incSearch:
            nestedFile = incSearch.group(1)
            if nestedFile.startswith('/'):
                nestedFile = os.path.normpath(os.environ['SSI_BASE'] + nestedFile)
            if os.path.exists(nestedFile):
                process(nestedFile, vars)
            continue
        # Lazy. I know for a fact that I don't have more than one #echo per line
        expandedSearch = re.search('^(.*)<!--#echo var="(.*)"-->(.*)$', line)
        if expandedSearch:
            print expandedSearch.group(1),
            key = expandedSearch.group(2)
            if key in vars:
                print vars[key],
            print expandedSearch.group(3)
            continue

        # The Default
        print line,
    input.close()

if __name__ == '__main__':
    process(sys.argv[1])
