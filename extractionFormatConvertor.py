#!/usr/bin/python

#  This script is used to convert dependency file with CoNLL format
#  to extraction file that could be used in Basilisk.
#
#   Author: Haibo Ding
#   Email: haibonlp@gmail.com
#   Data: July 2013
#



import sys
import os


def readStopWords(stopfile):
  In = open(stopfile)
  stopdict = {}
  for line in In.readlines():
    line = line.strip()
    if len(line) > 0:
      stopdict[line]=1
  In.close()
  return stopdict


def extractOneFile(infile, stopDict, Out):
  IN = open(infile)
  sentlist = []
  sent = []
  for line in IN.readlines():
    line = line.strip()
    if len(line) > 0:
      sent.append(line)
    else:
      sentlist.append(sent)
      sent = []
  IN.close()
  if len(sent) > 0:
    sentlist.append(sent)

#  print 'sent size : ', len(sentlist)

  for sent in sentlist:
    if len(sent) > 0:
      for line in sent:
        terms = line.split()
        if len(terms) != 10 :
          print 'Error  term size  :      ', line
          continue
        tId = terms[0].strip()
        word = terms[1].strip()
        pos = terms[4].strip()
        dId = int(terms[6].strip())
        dpTag = terms[7].strip()

        if dId != 0 :
          dId = dId -1
          dpline = sent[dId]
          dpTerms = dpline.split()
          if len(dpTerms) != 10:
            print 'Error  terms size  :   ', dpline
            continue
          dpWord = dpTerms[1].strip()
          dpPos = dpTerms[4].strip()
          if pos.startswith('NN') and  not stopDict.has_key(word):
            dpPattern = word + ' *  ' + '<GDep>:' + '<'+ dpTag + '>:<dependent>:' +  dpWord
            Out.write( dpPattern + '\n')
          if dpPos.startswith('NN') and not stopDict.has_key(dpWord):
            dpPattern = dpWord + ' * ' + '<GDep>:' + '<'+dpTag + '>:<head>:' + word
            Out.write( dpPattern + '\n')




def extract(listfile, stopfile, outfile):
  stopDict = readStopWords(stopfile)
  IN = open(listfile)
  Out = open(outfile, 'w')

  filelist = IN.readlines()
  indir = filelist[0].strip()

  for line in filelist[1:]:
    line = line.strip()
    if len(line) > 0:
      infile = indir + line
      print infile
      extractOneFile(infile,stopDict ,Out)

  IN.close()
  Out.close()




if __name__ == '__main__':
  if len(sys.argv) != 4:
    print 'usage :  ./program   datalistfile   stopfile   outputfile'
    os.exit()
  listfile = sys.argv[1]
  stopfile = sys.argv[2]
  outfile = sys.argv[3]
  extract(listfile, stopfile, outfile)






