#!/usr/bin/env python
"""
Mash good and bad ica output pics together into on html page of sanity check qc.

Usage:
  ica_comparelabels_viewer.py [options] <labelname1> <labelname2> <input.ica>...

Arguments:
    <labelname1>       Filename containing first set of labels
    <labelname2>       Filename containing second set of labels
    <input.ica>        Ica output directories

Options:
  --csvreport FILE         Name of csv output of summary stats.
  -v,--verbose             Verbose logging
  --debug                  Debug logging in Erin's very verbose style
  -n,--dry-run             Dry run
  --help                   Print help

DETAILS
Takes the images from the ICA report and combines them into webpages sorted as good and bad.
Written by Erin W Dickie, November 12, 2015
"""
from docopt import docopt
import pandas as pd
import numpy as np
import os
import subprocess
import glob
import sys

arguments       = docopt(__doc__)
featdirs        = arguments['<input.ica>']
icalabels1       = arguments['<labelname1>']
icalabels2       = arguments['<labelname2>']
csvfilename     = arguments['--csvreport']
VERBOSE         = arguments['--verbose']
DEBUG           = arguments['--debug']
DRYRUN          = arguments['--dry-run']

### Erin's little function for running things in the shell
def docmd(cmdlist):
    "sends a command (inputed as a list) to the shell"
    if DEBUG: print ' '.join(cmdlist)
    if not DRYRUN: subprocess.call(cmdlist)

def write_html_section(featdir, htmlhandle, IClist,SectionClass, SectionTitle):
    htmlhandle.write('<h2>'+SectionTitle+'</h2>')
    for IC in IClist:
        ## determine absolute and relative paths to the web page ica report data
        pic1 = os.path.join(featdir,'filtered_func_data.ica','report','IC_'+ str(IC) +'_thresh.png')
        pic2 = os.path.join(featdir,'filtered_func_data.ica','report','t'+ str(IC) +'.png')
        icreport = os.path.join(featdir,'filtered_func_data.ica','report','IC_'+ str(IC) +'.html')
        pic1relpath = os.path.relpath(pic1,os.path.dirname(htmlhandle.name))
        pic2relpath = os.path.relpath(pic2,os.path.dirname(htmlhandle.name))
        icreppath = os.path.relpath(icreport,os.path.dirname(htmlhandle.name))
        ## write it to the html
        htmlhandle.write('<p class="{}">\n'.format(SectionClass))
        htmlhandle.write('<a href="{}"><img src="{}"></a>\n'.format(icreppath,pic1relpath))
        htmlhandle.write('<a href="{}"><img src="{}">{}</a><br>\n'.format(icreppath,pic2relpath,icreppath))
        htmlhandle.write('<input type="radio" name="IC{}" value="Signal"'.format(IC))
        if (SectionClass == "SignalNoise") or (SectionClass == "SignalSignal"): htmlhandle.write(' checked="checked"')
        htmlhandle.write('> Signal')
        htmlhandle.write('<input type="radio" name="IC{}" value="Noise"'.format(IC))
        if (SectionClass == "NoiseSignal") or (SectionClass == "NoiseNoise"): htmlhandle.write(' checked="checked"')
        htmlhandle.write('> Noise')
        htmlhandle.write('</p>\n')


def get_SignalandNoise(inputdir, inputlabelfile, numICs) :
    labelpath = os.path.join(inputdir,inputlabelfile)
    if os.path.isfile(labelpath):
        a=open(labelpath,'rb')
        lines = a.readlines()
        if lines:
            first_line = lines[:1]
            last_line = lines[-1]

        bad_ica = last_line.split(',')
        for i in range(len(bad_ica)):
            bad_ica[i] = bad_ica[i].replace('[','')
            bad_ica[i] = bad_ica[i].replace(']','')
            bad_ica[i] = bad_ica[i].replace(' ','')
            bad_ica[i] = bad_ica[i].replace('\n','')

        ## if bad icas are empty, set the empty list, if not set to mat to int
        if bad_ica == ['']:
            bad_ica = []
        else:
            bad_ica = map(int,bad_ica)
            if max(bad_ica) > numICs:
                print("We have a problem, more labels in {} than ICs".format(inputlabelfile))
                print("Number of ICs: {}".format(numICs))
                print("Labeled Bad ICs {}".format(bad_ica))

    else:
        sys.exit("IC labels file {} not found".format(labelpath))

    good_ica = list(set(range(1,numICs+1)) - set(bad_ica))
    return(good_ica,bad_ica)

def write_featdir_html(featdir, htmlpath,
                       labelbasename1, labelbasename2,
                       signalnoise, noisesignal, signalsignal, noisenoise,
                       htmltitle):

    handlablefile = os.path.join(featdir, "hand_labels_noise.txt")
    handlabelrelpath = os.path.relpath(handlablefile,os.path.dirname(htmlpath))
    htmlpage = open(htmlpath,'w')
    htmlpage.write('<HTML><TITLE>'+htmltitle+'</TITLE>')
    htmlpage.write('<head>\n')
    htmlpage.write('<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.0/jquery.min.js"></script>')
    htmlpage.write('<style>\n')
    htmlpage.write('body { background-color:#333333; '
                    'font-family: futura,sans-serif;color:white;\n'
                    'text-align: center;}\n')
    htmlpage.write('p.SignalSignal {background-color:#009999;}\n')
    htmlpage.write('p.NoiseNoise {background-color:#ff4000;}\n')
    htmlpage.write('p.SignalNoise {background-color:#ffbf00;}\n')
    htmlpage.write('p.NoiseSignal {background-color:#990099;}\n')
    htmlpage.write('img {width:800; display: block;margin-left: auto;margin-right: auto }\n')
    htmlpage.write('h2 {color:white; }\n')
    htmlpage.write('</style></head>\n')
    htmlpage.write('<BODY>\n')
    htmlpage.write('<form action="{}" method="post" id="main">\n'.format(handlabelrelpath))
    htmlpage.write('<h1>Components for '+ featdir +'</h1>')

    ## Signal for both
    write_html_section(featdir, htmlpage, signalnoise, "SignalNoise",
                        "Signal in {} Noise in {}".format(labelbasename1, labelbasename2))

    ## add a break
    htmlpage.write('<br>\n')

    ## Signal for both
    write_html_section(featdir, htmlpage, noisesignal, "NoiseSignal",
                        "Noise in {} Signal in {}".format(labelbasename1, labelbasename2))

    ## add a break
    htmlpage.write('<br>\n')

    ## Signal for both
    write_html_section(featdir, htmlpage, signalsignal,"SignalSignal","Signal in both")

    ## add a break
    htmlpage.write('<br>\n')

    ## Signal for both
    write_html_section(featdir, htmlpage, noisenoise,"NoiseNoise","Noise in both")

    ## finish the file
    htmlpage.write('<br>\n')
    htmlpage.write('<input type="submit" name="submit" value="Show/Update Labels"></br>\n</form>\n')
    htmlpage.write('<br><h3>To write handlabels copy this line into the terminal:</h3>\n')
    htmlpage.write('<br><p>echo "<span id="output"></span>')
    htmlpage.write('" > ' + handlablefile + '</p><br>\n')

    htmlpage.write('<script type="text/javascript">\n')
    htmlpage.write('$("#main").submit(function(e) {\n')
    htmlpage.write('  e.preventDefault();\n')
    htmlpage.write('  var handlabels = "[";\n')

    IClist= range(1, len(signalsignal) + len(noisenoise) + len(signalnoise) + len(noisesignal) +1)
    for IC in IClist:
        htmlpage.write('  if ($("input[name=IC' + str(IC) +']:checked").val() == "Noise") ')
        htmlpage.write('{handlabels += "'+ str(IC) +', ";}\n')

    htmlpage.write('  handlabels = handlabels.substring(0,handlabels.length - 2) + "]";\n')
    htmlpage.write('  $("#output").text(handlabels);\n});\n</script>\n')

    htmlpage.write('</BODY>\n</HTML>\n')
    htmlpage.close() # you can omit in most cases as the destructor will call it


## inputdir='/home/edickie/analysis/colin_fix/featprep/H002_NY_imitate.feat'
## icalabels='hand_labels_noise.txt'
if DEBUG: print arguments


## naming convention for individual html files from labelname
labelbasename1 = os.path.splitext(icalabels1)[0]
labelbasename2 = os.path.splitext(icalabels2)[0]

## Start the index html file
htmlindexfile = "compare_{}_vs_{}_report.html".format(labelbasename1,labelbasename2)
htmlindex = open(htmlindexfile,'w')
htmlindex.write('<HTML><TITLE> ICA FIX qc index </TITLE>\n'
                '<head>\n<style>\n'
                'body { background-color:#333333; '
                'font-family: futura,sans-serif;'
                'color:white;text-align: center;}\n'
                'a:link {color:#99CCFF;}\n'
                'a:visited  {color: #AC58FA;}\n'
                'table { margin: 25px auto; '
                '        border-collapse: collapse;'
                '        text-align: left;'
                '        width: 98%; '
                '        border: 1px solid grey;'
                '        border-bottom: 2px solid #00cccc;} \n'
                'th {background: #00cccc;\n'
                'color: #fff;'
                'text-transform: uppercase;};'
                'td {border-top: thin solid;'
                '    border-bottom: thin solid;}\n'
                '</style></head>\n')


htmltitle="{} vs {}".format(labelbasename1,labelbasename2)

## check that the csvreport exists
if not csvfilename:
    csvfilename = "compare_{}_vs_{}_report.csv".format(labelbasename1,labelbasename2)

## load the pandas dataframe
csvreport = pd.DataFrame({ 'featdir' : pd.Categorical(featdirs),
                           'NumSignalNoise' : np.empty([len(featdirs)], dtype=int),
                           'NumNoiseSignal' : np.empty([len(featdirs)], dtype=int),
                           'NumSignalSignal' : np.empty([len(featdirs)], dtype=int),
                           'NumNoiseNoise' : np.empty([len(featdirs)], dtype=int),
                           'Accuracy' : np.empty([len(featdirs)], dtype=float),
                           'Precision' : np.empty([len(featdirs)], dtype=float),
                           'numICs' : np.empty([len(featdirs)], dtype=int)})
#csvreport = loadreportcsv(csvfilename,featdirs)
#csvreport.labelfile = icalabels

## add the title
htmlindex.write('<h1>ICA FIX labels comparison index</h1>')
htmlindex.write('<h2>Labels: {} and {}</h2>'.format(labelbasename1, labelbasename2))

## add the table header
htmlindex.write('<table>'
                '<tr><th>Path</th>')
htmlindex.write('<th>{} Signal ICs</th>'.format(labelbasename1))
htmlindex.write('<th>{} Signal ICs</th>'.format(labelbasename2))
htmlindex.write('<th>Accuracy</th>'
                '<th>Precision</th>'
                '<th>Total ICs</th></tr>')

for featdir in featdirs:

    ## get the number of ICA components from the report length
    ICpngs = glob.glob(os.path.join(featdir,'filtered_func_data.ica','report','IC_*_thresh.png'))
    numICs = len(ICpngs)

    ## get the signal and noise components from both files
    signal1, noise1 = get_SignalandNoise(featdir, icalabels1, numICs)
    signal2, noise2 = get_SignalandNoise(featdir, icalabels2, numICs)

    ## get the signal and noise components from both files
    signalnoise = list(set(signal1).intersection(noise2))
    noisesignal = list(set(noise1).intersection(signal2))
    signalsignal = list(set(signal1).intersection(signal2))
    noisenoise = list(set(noise1).intersection(noise2))

    ## write the featdir's html file
    featdirhtml = os.path.join(featdir,"compare_{}_to_{}_report.html".format(labelbasename1,labelbasename2))
    write_featdir_html(featdir,
                       featdirhtml,
                       labelbasename1,
                       labelbasename2,
                       signalnoise,
                       noisesignal,
                       signalsignal,
                       noisenoise,
                        "Compare {} vs {} ICA labels".format(labelbasename1, labelbasename2))

    ## print relative link to index
    featdir_relpath = os.path.relpath(featdirhtml,os.path.dirname(htmlindex.name))
    featdir_relname = os.path.dirname(featdir_relpath)

    htmlindex.write('<tr>') ## table new row
    htmlindex.write('<td>') ## first data cell
    htmlindex.write('<a href="{}">{}</a>'.format(featdir_relpath,featdir_relname))
    htmlindex.write('</td>') ## end of cell

    ## print basic stats - % excluded, total IC's number kept, total IC
    NumSignal1 = len(signal1)
    NumSignal2 = len(signal2)
    Accuracy = (float((len(signalsignal) + len(noisenoise)))/float(numICs))*100
    if ( NumSignal2 + NumSignal1) > 0 :
        Precision = float(len(signalsignal))/float((len(signalsignal)+len(noisesignal)))*100
    else:
        Precision = 100
    htmlindex.write("<td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td>".format(NumSignal1,NumSignal2,format(Accuracy, '.1f'),format(Precision, '.1f'),numICs))
    htmlindex.write('</tr>')

    ## write this info to csvreport
    idx = csvreport[csvreport.featdir == featdir].index[0]
    csvreport.loc[idx,'NumSignalNoise'] = len(signalnoise)
    csvreport.loc[idx,'NumNoiseSignal'] = len(noisesignal)
    csvreport.loc[idx,'NumSignalSignal'] = len(signalsignal)
    csvreport.loc[idx,'NumNoiseNoise'] = len(noisenoise)
    csvreport.loc[idx,'Accuracy'] = Accuracy
    csvreport.loc[idx,'Precision'] = Precision
    csvreport.loc[idx,'numICs'] = numICs

## finish the file
htmlindex.write('</table>\n')
htmlindex.write('</BODY></HTML>\n')
htmlindex.close() # you can omit in most cases as the destructor will call it

## write the results out to a file
csvreport.to_csv(csvfilename, sep=',', index = False)
