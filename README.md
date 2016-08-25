# ICArus
A simple tool for viewing and scoring FSL MELODIC ICA/FIX results

This is a tool was built to work with FSL's [Melodic](http://fsl.fmrib.ox.ac.uk/fsl/fslwiki/MELODIC) and [ICAFIX](http://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FIX).
It was created to make the process of evaluating ICA components and FIX classifier labels quicker and less prone to human error.
This is accomplished by re-arranging the material presented in MELODIC's html report pages into one web page per MELODIC ica-output with signal and noise components sorted into separate sections. The signal and noise labels can

## Installation
```sh
git clone https://github.com/edickie/ICArus.git
cd ICArus
sudo python ./setup.py install
```

## Dependancies

While this programs do not require FSL or ICAFIX to be in order to work. 
They are built to work with outputs of these. 
 + **FSL Melodic**[http://fsl.fmrib.ox.ac.uk/fsl/fslwiki/MELODIC] 
 + **ICAFIX**[http://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FIX]

Python dependancies (these will be installed when you install icarus if you don't already have them:
 + pandas
 + numpy 
 + docopt  

## There are two executables:
+[**icarus-report**](#icarus-report) : for generating an html report from one set of labels
+[**icarus-compare**](#icarus-compare) : For generating an html report comparing two sets of labels

### icarus-report 

```
Usage:
  icarus-report [options] <input.feat>...

Arguments:
  <input.feat>  Top directory for the output file structure

Options:
  --html-out FILE          Name [default: qc_icafix.html] (fullpath) to index html file.
  --labelfilename FILE     Name [default: fix4melview_Standard_thr20.txt] of file that contains labels.
  --csvreport FILE         Name of csv output of summary stats.
  --copy-qcdir PATH        Copy out all the qc files and the melodic report to the specified path
  -v,--verbose             Verbose logging
  --debug                  Debug logging in Erin's very verbose style
  -n,--dry-run             Dry run
  --help                   Print help

 DETAILS
 Runs makes an ica qc html page for all specified feat directories.
 Writes an index page with some summary data.

 Default name for --csvreport is "ica_fix_report_<labelfilename>.csv"
 
 QC pages are interactive so that you can click buttons to manually rate signal and noise.
 A text line shows up at the bottom with a command to save your ratings to hand_labels_noise.txt.
```

# Some Examples:

To run ICArus and inspect ICA FIX performance after pre-preprocessing data using FSL's MELODIC GUI and running the ICA FIX with built in Standard.Rdata training set and a threshold of 20.

~~~sh
MELODIC_OUTPUTDIR=/path/to/melodic

cd ${MELODIC_OUTPUTDIR}
## if data preprocessed with melodic, all output directories end in .ica
MELODIC_OUTPUTS=`ls -1d *.ica`
icarus-report ${MELODIC_OUTPUTS}
~~~

If data was preprocessed with FSL FEAT. The input folders will all with ".feat"

~~~sh
FEAT_OUTPUTDIR=/path/to/feat/outputs

cd ${FEAT_OUTPUTDIR}
## if data preprocessed with melodic, all output directories end in .ica
FEAT_OUTPUTS=`ls -1d *.feat`
icarus-report ${FEAT_OUTPUTS}
~~~

If data was preprocessed using the epitome pipeline tool ().
ICArus need to point to at the location of your "fake feat" directories...

~~~sh
## epitome users often has these variables set
EPITOME_OUTPUTS=${DIR_EPITOME}/${DIR_DATA} ## epitome user's usually has these variables set
MODE="MYMODE" #ususally set to the MR scan type

cd ${EPITOME_OUTPUTS}
FEATDIRS=`ls -1d */${MODE}/*/fake*feat`
icarus-report ${FEAT_OUTPUTS}
~~~

To change the labels files to a different label. Say you would like to looks "hand_labels_noise.txt" labels written by a collaborator for building a new fix training set.

~~~sh
icarus-report --labelfilename hand_labels_noise.txt ${FEAT_OUTPUTS}
~~~

For those of us who are preprocessing data on a high performance cluster (or any other computer to big to be portable). We also added an option to copy all the pictures and html pages (i.e. the whole ICArus report structure) into a separate folder. So that it can be moved to another computer or a web-server to allow to for visualization and ratings of the ICA fix results to on a separate computer.

~~~sh
icarus-report --copy-qcdir /path/to/copied/qc/files ${FEAT_OUTPUTS}
~~~

### icarus-compare
```
For generating an html report comparing two sets of labels

Usage:
  icarus_compare [options] <labelname1> <labelname2> <input.ica>...

Arguments:
    <labelname1>       Filename containing first (gold-standard) set of labels
    <labelname2>       Filename containing second set of labels
    <input.ica>        Ica output directories

Options:
  --csvreport FILE         Name of csv output of summary stats.
  -v,--verbose             Verbose logging
  --debug                  Debug logging in Erin's very verbose style
  -n,--dry-run             Dry run
  --help                   Print help

DETAILS
Runs makes an ica qc html page for all specified feat directories.

All report pages have four sections:
  1) False Alarms (labelname1 = signal, labelname2 = noise) - in yellow
  2) Misses (labelname2 = noise, labelname1 = signal) - in purple
  3) Hits (both labeled as signal) - in teal  
  4) Correct Rejections (both labeled as noise) - in orange

Writes an index page with some summary data.

Default name for --csvreport is "compare_<labelname1>_vs_<labelname2>.csv"

QC pages are interactive so that you can click buttons to manually rate signal and noise.
A text line shows up at the bottom with a command to save your ratings to hand_labels_noise.txt.
```
