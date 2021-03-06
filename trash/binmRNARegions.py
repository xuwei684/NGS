#!/usr/bin/env python
# -*- coding: utf-8 -*-
#from __future__ import division, with_statement
'''
Copyright 2013, 陈同 (chentong_biology@163.com).  
===========================================================
'''
__author__ = 'chentong & ct586[9]'
__author_email__ = 'chentong_biology@163.com'
#=========================================================
'''
Functionla description
'''

import sys
import os
from time import localtime, strftime 
timeformat = "%Y-%m-%d %H:%M:%S"
from optparse import OptionParser as OP

def cmdparameter(argv):
    if len(argv) == 1:
        cmd = 'python ' + argv[0] + ' -h'
        os.system(cmd)
        sys.exit(1)
    desc = ""
    usages = "%prog -i file"
    parser = OP(usage=usages)
    parser.add_option("-i", "--input-file", dest="filein",
        metavar="FILEIN", help="A standard bed file with \
six columns. Strand information will be considered. \
Extra columns will be ignored.")
    parser.add_option("-n", "--number-bins", dest="nBins",
        metavar="20", default="20", 
        help="The numbers bins in regions")
    parser.add_option("-s", "--strand", dest="strand",
        default=1, help="Consider strand information or not. \
Default TRUE. Strings or numbers that represent FALSE can turn \
off this parameter.")
    parser.add_option("-v", "--verbose", dest="verbose",
        default=0, help="Show process information")
    parser.add_option("-d", "--debug", dest="debug",
        default=False, help="Debug the program")
    (options, args) = parser.parse_args(argv[1:])
    assert options.filein != None, "A filename needed for -i"
    return (options, args)
#--------------------------------------------------------------------


def getBinsType(typeL, nBin, gene, strand):
    #add sort operation
    typeL.sort(key=lambda x:int(x[1]))
    type_len = sum([int(i[2])-int(i[1]) for i in typeL])
    size = type_len / nBin
    #if size < 2:
    size = size + 1
    #if size == 1:
    #    size = 2
    #elif size == 0:
    #    size = 1
    if strand == '+':
        cnt = 0
        time = 1
    elif strand == '-':
        cnt = nBin + 1
        time = -1
    else:
        print >>sys.stderr, "Wrong strand type %s" % strand
    remain = 0
    lenTypeL = len(typeL)
    for index in range(lenTypeL):
        i = typeL[index]
        start = int(i[1])
        while True:
            if remain == 0:
                cnt += 1 * time
                end = start + size
            else:
                end = start + remain
                remain = 0
            #if index != lenTypeL -1: 
            if end  <= int(i[2]):
                tmpL = [i[0], str(start), str(end), \
                    gene+'.'+str(cnt), i[4], i[5]]
                print '\t'.join(tmpL)
                start = end
            else:
                remain = end - int(i[2])
                tmpL = [i[0], str(start), i[2], \
                    gene+'.'+str(cnt), i[4], i[5]]
                print '\t'.join(tmpL)
                start = int(i[2])
                break
            #------------------------------------------------
            if start >= int(i[2]):
                break
        #--------------------------------------------------
    #--------------------------------------------------
    if strand == '+':
        for i in range (cnt, nBin):
            lastCnt = int(tmpL[3].split('.')[-1])
            lastCnt += 1
            tmpL[3] = gene+'.'+str(lastCnt)
            print '\t'.join(tmpL)
    else:
        for i in range (cnt, 1, -1):
            lastCnt = int(tmpL[3].split('.')[-1])
            lastCnt -= 1
            assert lastCnt >= 1, "%s\t%d\t%d" % (type, cnt, lastCnt)
            tmpL[3] = gene+'.'+str(lastCnt)
            print '\t'.join(tmpL)
    #-----------------------------------------------------

#---------------------------------------

def getBins(aDict, nBins, strandD):
    for gene, innerL in aDict.items():
        if not strandD:
            getBinsType(innerL, nBins, gene, '+')
        else:
            getBinsType(innerL, nBins, gene, strandD[gene])
#-----------------------------------------------------------
def main():
    options, args = cmdparameter(sys.argv)
    #-----------------------------------
    file = options.filein
    nBins = int(options.nBins)
    verbose = options.verbose
    debug = options.debug
    strand = options.strand
    #-----------------------------------
    if file == '-':
        fh = sys.stdin
    else:
        fh = open(file)
    #--------------------------------
    aDict = {}
    strandD = {}
    for line in fh:
        lineL = line.split()
        gene = lineL[3]
        #keyL = lineL[3].split('.')
        #gene = keyL[0]
        #type = keyL[1]
        if gene not in aDict:
            aDict[gene] = [lineL]
        #---------------------------------
        if strand:
            strandD[gene] = lineL[5]
        #if type in aDict[gene]:
        #    aDict[gene][type].append(lineL)
        #else:
        #    aDict[gene][type] = [lineL]
    #-------------END reading file----------
    #----close file handle for files-----
    if file != '-':
        fh.close()
    #-----------end close fh-----------
    #print aDict['NM_027855_3']
    #print aDict
    getBins(aDict, nBins, strandD)
    #---------------------------------------
    if verbose:
        print >>sys.stderr,\
            "--Successful %s" % strftime(timeformat, localtime())
if __name__ == '__main__':
    startTime = strftime(timeformat, localtime())
    main()
    endTime = strftime(timeformat, localtime())
    fh = open('python.log', 'a')
    print >>fh, "%s\n\tRun time : %s - %s " % \
        (' '.join(sys.argv), startTime, endTime)
    fh.close()



