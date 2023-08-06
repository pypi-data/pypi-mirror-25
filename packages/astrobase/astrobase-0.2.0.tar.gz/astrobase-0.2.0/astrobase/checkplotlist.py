#!/usr/bin/env python
'''checkplotlist.py - Waqas Bhatti (wbhatti@astro.princeton.edu) - Dec 2016
License: MIT. See LICENSE for full text.

DESCRIPTION
===========

This makes a checkplot file list for use with the checkplot-viewer.html or the
checkplotserver.py webapps. Checkplots are quick-views of object info, finder
charts, light curves, phased light curves, and periodograms used to examine
their stellar variability. These are produced by several functions in the
astrobase.checkplot module:

checkplot.checkplot_png: makes a checkplot PNG for a single period-finding
                         method

checkplot.twolsp_checkplot_png: does the same for two independent period-finding
                                methods

checkplot.checkplot_pickle: makes a checkplot .pkl.gz for any number of
                            independent period-finding methods


USAGE
=====

If you made checkplots in the PNG format (checkplot-*.png)
----------------------------------------------------------

Copy checkplot-viewer.html and checkplot-viewer.js to the
base directory from where you intend to serve your checkplot images from. Then
invoke this command from that directory:

$ checkplotlist png subdir/containing/the/checkplots 'optional-glob*.png'

This will generate a checkplot-filelist.json file containing the file paths to
the checkplots.

You can then run a temporary Python web server from this base directory to
browse through all the checkplots:

$ python -m SimpleHTTPServer # Python 2
$ python3 -m http.server     # Python 3

then browse to http://localhost:8000/checkplot-viewer.html.

If this directory is already in a path served by a web server, then you can just
browse to the checkplot-viewer.html file normally. Note that a file:/// URL
provided to the browser won't necessarily work in some browsers (especially
Google Chrome) because of security precautions.

If you made checkplots in the pickle format (checkplot-*.pkl)
-------------------------------------------------------------

Invoke this command from that directory like so:

$ checkplotlist pkl subdir/containing/the/checkplots

Then, from that directory, invoke the checkplotserver webapp (make sure the
astrobase virtualenv is active, so the command below is in your path):

$ checkplotserver [list of options, use --help to see these]

The webapp will start up a Tornado web server running on your computer and
listening on a local address (default: http://localhost:5225). This webapp will
read the checkplot-filelist.json file to find the checkplots.

Browse to http://localhost:5225 (or whatever port you set in checkplotserver
options) to look through or update all your checkplots. Any changes will be
written back to the checkplot .pkl files, making this method of browsing more
suited to more serious variability searches on large numbers of checkplots.

'''


PROGDESC = '''\
This makes a checkplot file list for use with the checkplot-viewer.html (for
checkplot PNGs) or the checkplotserver.py (for checkplot pickles) webapps.
'''

PROGEPILOG= '''\
SEARCHING FOR CHECKPLOT PNGS OR PICKLES
---------------------------------------
If you have checkplots that don't have 'checkplot' somewhere in their file name,
use the optional checkplot file glob argument to checkplotlist to provide
this:

--search '<filename glob for prefix>'

Make sure to use the quotes around this argument, otherwise the shell will
expand it.

Example: search for checkplots with awesome-object in their filename:

$ checkplotlist png my-project/awesome-objects --search '*awesome-object*'

SORTING CHECKPLOT PICKLES
-------------------------
If you want to sort checkplot pickle files in the output list in some special
way other than the usual filename sort order, this requires an argument on the
commandline of the form:

--sortby '<sortkey>-<asc|desc>'

Here, sortkey is some key in the checkplot pickle. This can be a simple key:
e.g. objectid or it can be a composite key: e.g. varinfo.features.stetsonj.
sortorder is either 'asc' or desc' for ascending/descending sort. The sortkey
must exist in all checkplot pickles.

Example: sort checkplots by their 2MASS J magnitudes in ascending order:

$ checkplotlist pkl my-project/awesome-objects --sortby 'objectinfo.jmag-asc'

Example: sort checkplots by the power of the best peak in their PDM
periodograms:

$ checkplotlist pkl my-project/awesome-objects --sortby 'pdm.nbestlspvals.0-asc'

FILTERING CHECKPLOT PICKLES
---------------------------
You can filter the checkplot pickle files in the output list by using the
--filterby argument. Note that filtering takes place after any requested
sorting.  Provide a filterkey, filteroperator, and filteroperand in the form:

--filterby '<filterkey>-<filteroperator>@<filteroperand>'

Here, filterkey is some key in the checkplot pickle, specified as the sortkey
discussed above. filteroperator is one of the following 2-character strings:

'gt' -> greater than, 'lt' -> less than, 'ge' -> greater than or equal to,
'le' -> less than or equal to, 'eq' -> equal to

filteroperand is the appropriate integer, float, or string for the filterkey and
operator.

Example: get only those checkplots with Stetson J > 0.2:

checkplotlist pkl my-project/awesome-objects --filterby 'varinfo.features.stetsonj-gt@0.2'

Example: get only those checkplots for objects with r < 12.0 and sort these by
power of the best peak in their Lomb-Scargle periodogram:

checkplot pkl my-project/awesome-objects --filterby 'objectinfo.sdssr-lt@12.0' --sortby 'gls.nbestlspvals.0-desc'
'''

import os
import os.path
import sys
import glob
import json
import argparse

# suppress warnings
import warnings
warnings.filterwarnings('ignore')

# to turn a list of keys into a dict address
# from https://stackoverflow.com/a/14692747
# used to walk a checkplotdict for a specific key in the structure
from functools import reduce
from operator import getitem

from astrobase import checkplot
import numpy as np
import multiprocessing as mp


######################
## HELPER FUNCTIONS ##
######################

def dict_get(datadict, keylist):
    '''
    This gets the requested key by walking the datadict.

    '''
    return reduce(getitem, keylist, datadict)



def key_worker(task):
    '''
    This gets the required keys from the requested file.

    '''
    cpf, keys = task


    cpd = checkplot._read_checkplot_picklefile(cpf)

    resultkeys = []

    for k in keys:

        try:
            resultkeys.append(dict_get(cpd, k))
        except:
            resultkeys.append(np.nan)

    return resultkeys


############
## CONFIG ##
############

FILTEROPS = {'eq':'==',
             'gt':'>',
             'ge':'>=',
             'lt':'<',
             'le':'<='}



##########
## MAIN ##
##########

def main():

    ####################
    ## PARSE THE ARGS ##
    ####################

    aparser = argparse.ArgumentParser(
        epilog=PROGEPILOG,
        description=PROGDESC,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    aparser.add_argument(
        'cptype',
        action='store',
        choices=['pkl','png'],
        type=str,
        help=("type of checkplot to search for: pkl -> checkplot pickles, "
              "png -> checkplot PNGs")
    )
    aparser.add_argument(
        'cpdir',
        action='store',
        type=str,
        help=("directory containing the checkplots to process")
    )
    aparser.add_argument(
        '--search',
        action='store',
        default='*checkplot*',
        type=str,
        help=("file glob prefix to use when searching for checkplots "
              "(the extension is added automatically - .png or .pkl)")
    )
    aparser.add_argument(
        '--sortby',
        action='store',
        type=str,
        help=("the sort key and order to use when sorting")
    )
    aparser.add_argument(
        '--filterby',
        action='store',
        type=str,
        help=("the filter key and condition to use when filtering")
    )
    aparser.add_argument(
        '--splitout',
        action='store',
        type=int,
        default=5000,
        help=("if there are more than SPLITOUT objects in "
              "the target directory (default: %(default)s), "
              "checkplotlist will split the output JSON into multiple files. "
              "this helps keep the webapps responsive.")
    )
    aparser.add_argument(
        '--outprefix',
        action='store',
        type=str,
        help=("a prefix string to use for the output JSON file(s). "
              "use this to separate out different sort orders, for example. "
              "if this isn't provided, but sortby is, will use that to "
              "figure out the output files' prefixes")
    )

    args = aparser.parse_args()

    checkplotbasedir = args.cpdir
    fileglob = args.search
    splitout = args.splitout
    outprefix = args.outprefix if args.outprefix else None

    # see if there's a sorting order
    if args.sortby:
        sortkey, sortorder = args.sortby.split('-')
        if outprefix is None:
            outprefix = args.sortby
    else:
        sortkey, sortorder = None, None

    # see if there's a filter condition
    if args.filterby:
        filterkey, filtercondition = args.filterby.split('-')
        if outprefix is None:
            outprefix = args.filterby
        else:
            outprefix = '%s-%s' % (args.filterby, outprefix)
    else:
        filterkey, filtercondition = None, None


    if args.cptype == 'pkl':
        checkplotext = 'pkl'
    elif args.cptype == 'png':
        checkplotext = 'png'
    else:
        print("unknown format for checkplots: %s! can't continue!"
              % args.cptype)
        sys.exit(1)


    #######################
    ## NOW START WORKING ##
    #######################

    currdir = os.getcwd()

    checkplotglob = os.path.join(checkplotbasedir,
                                 '%s.%s' % (fileglob, checkplotext))

    print('searching for checkplots: %s' % checkplotglob)

    searchresults = glob.glob(checkplotglob)

    if searchresults:

        print('found %s checkplot files in %s, '
              'making checkplot-filelist.json...' %
              (len(searchresults), checkplotbasedir))

        # see if we should sort the searchresults in some special order
        # this requires an arg on the commandline of the form:
        # '<sortkey>-<asc|desc>'
        # where sortkey is some key in the checkplot pickle:
        #   this can be a simple key: e.g. objectid
        #   or it can be a composite key: e.g. varinfo.varfeatures.stetsonj
        # and sortorder is either 'asc' or desc' for ascending/descending sort

        # we only support a single condition conditions are of the form:
        # '<filterkey>-<condition>@<operand>' where <condition> is one of: 'ge',
        # 'gt', 'le', 'lt', 'eq' and <operand> is a string, float, or int to use
        # when applying <condition>
        if (sortkey and sortorder) or (filterkey and filtercondition):

            keystoget = []

            # handle sorting
            if (sortkey and sortorder):

                print('sorting checkplot pickles by %s in order: %s...' %
                      (sortkey, sortorder))

                # dereference the sort key
                sortkeys = sortkey.split('.')

                # if there are any integers in the sortkeys strings, interpret
                # these to mean actual integer indexes of lists or integer keys
                # for dicts this allows us to move into arrays easily by
                # indexing them
                sortkeys = [(int(x) if x.isdecimal() else x) for x in sortkeys]

                keystoget.append(sortkeys)

            # handle filtering
            if (filterkey and filtercondition):

                print('filtering checkplot pickles by %s using: %s...' %
                      (filterkey, filtercondition))

                # dereference the filter key
                filterkeys = filterkey.split('.')
                filterkeys = [(int(x) if x.isdecimal() else x)
                              for x in filterkeys]

                keystoget.append(filterkeys)


            # launch the key retrieval
            pool = mp.Pool()
            tasks = [(x, keystoget) for x in searchresults]
            keytargets = pool.map(key_worker, tasks)

            pool.close()
            pool.join()

            # now that we have keys, we need to use them
            # keys will be returned in the order we put them into keystoget
            if len(keystoget) == 2:

                sorttargets = [x[0] for x in keytargets]
                filtertargets = [x[1] for x in keytargets]
            elif (len(keystoget) == 1 and
                  (sortkey and sortorder) and
                  (not(filterkey and filtercondition))):
                sorttargets = keytargets
                filtertargets = None
            elif (len(keystoget) == 1 and
                  (filterkey and filtercondition) and
                  (not(sortkey and sortorder))):
                sorttargets = None
                filtertargets = keytargets

            # turn the search results into an np.array before we do
            # sorting/filtering
            searchresults = np.array(searchresults)


            # first, take care of sort keys
            sortdone = False

            if sorttargets:

                sorttargets = np.ravel(np.array(sorttargets))

                sortind = np.argsort(sorttargets)
                if sortorder == 'desc':
                    sortind = sortind[::-1]

                # sort the search results in the requested order
                searchresults = searchresults[sortind]
                sortdone = True

            # second, take care of any filters
            filterok = False

            if filtertargets:

                filtertargets = np.ravel(np.array(filtertargets))

                # don't forget to also sort the filtertargets in the same order
                # as sorttargets so we can get the correct objects to filter.
                if (sortdone):
                    filtertargets = filtertargets[sortind]

                # figure out the filter condition: <condition>@<operand> where
                # <condition> is one of: 'ge', 'gt', 'le', 'lt', 'eq' and
                # <operand> is a string, float, or int to use when applying
                # <condition>

                try:

                    foperator, foperand = filtercondition.split('@')
                    foperator = FILTEROPS[foperator]

                    # we'll do a straight eval of the filter
                    # yes: this is unsafe

                    filterstr = (
                        'np.isfinite(filtertargets) & (filtertargets %s %s)' %
                        (foperator, foperand)
                    )
                    filterind = eval(filterstr)

                    # apply the filter
                    filterresults = searchresults[filterind]

                    if filterresults.size > 0:

                        print('filter applied: %s -> objects found: %s ' %
                              (args.filterby, filterresults.size))
                        searchresults = filterresults
                        filterok = True

                    else:
                        print('WRN! filter failed! %s -> ZERO objects found!' %
                              (args.filterby, ))
                        print('WRN! not applying failed filter')

                except Exception as e:

                    print('ERR! could not understand filter spec: %s'
                          '\nexception was: %s' %
                          (args.filterby, e))
                    print('WRN! not applying broken filter')

            # all done with sorting and filtering
            # turn the searchresults back into a list
            searchresults = searchresults.tolist()

            # if there's no special sort order defined, use the usual sort order
            # at the end after filtering
            if not(sortkey and sortorder):

                print('WRN! no special sort key and order/'
                      'filter key and condition specified, '
                      'sorting checkplot pickles '
                      'using usual alphanumeric sort...')

                searchresults = sorted(searchresults)
                sortkey = 'filename'
                sortorder = 'asc'


        nchunks = int(len(searchresults)/splitout) + 1

        searchchunks = [searchresults[x*splitout:x*splitout+splitout] for x
                        in range(nchunks)]

        if nchunks > 1:
            print('WRN! more than %s checkplots in final list, '
                  'splitting into %s chunks' % (splitout, nchunks))


        # if the filter failed, zero out filterkey
        if not filterok:
            filterkey = None
            foperator, foperand = None, None

        # generate the output
        for chunkind, chunk in enumerate(searchchunks):

            # figure out if we need to split the JSON file
            outjson = os.path.abspath(
                os.path.join(
                    currdir,
                    '%scheckplot-filelist%s.json' % (
                        ('%s-' % outprefix if outprefix is not None else ''),
                        ('-%02i' % chunkind if len(searchchunks) > 1 else ''),
                    )
                )
            )

            # ask if the checkplot list JSON should be updated
            if os.path.exists(outjson):

                answer = input('There is an existing '
                               'checkplot list file in this '
                               'directory:\n    %s\nDo you want to '
                               'overwrite it completely? (default: no) [y/n] ' %
                               outjson)

                # if it's OK to overwrite, then do so
                if answer and answer == 'y':

                    with open(outjson,'w') as outfd:
                        print('WRN! completely overwriting '
                              'existing checkplot list %s' % outjson)
                        outdict = {'checkplots':chunk,
                                   'nfiles':len(chunk),
                                   'sortkey':sortkey,
                                   'sortorder':sortorder,
                                   'filterkey':filterkey,
                                   'filtercondition':'%s %s' % (foperator,
                                                                foperand)}
                        json.dump(outdict,outfd)

                # if it's not OK to overwrite, then
                else:

                    # read in the outjson, and add stuff to it for objects that
                    # don't have an entry
                    print('only updating existing checkplot list '
                          'file with any new checkplot pickles')

                    with open(outjson,'r') as infd:
                        indict = json.load(infd)

                    # update the checkplot list, sortorder, and sortkey only
                    indict['checkplots'] = chunk
                    indict['nfiles'] = len(chunk)
                    indict['sortkey'] = sortkey
                    indict['sortorder'] = sortorder
                    indict['filterkey'] = filterkey
                    indict['filtercondition'] = '%s %s' % (foperator,
                                                           foperand)

                    # write the updated to back to the file
                    with open(outjson,'w') as outfd:
                        json.dump(indict, outfd)

            # if this is a new output file
            else:

                with open(outjson,'w') as outfd:
                    outdict = {'checkplots':chunk,
                               'nfiles':len(chunk),
                               'sortkey':sortkey,
                               'sortorder':sortorder,
                               'filterkey':filterkey,
                               'filtercondition':'%s %s' % (foperator,
                                                            foperand)}
                    json.dump(outdict,outfd)

            if os.path.exists(outjson):
                print('checkplot file list written to %s' % outjson)
            else:
                print('ERR! writing the checkplot file list failed!')

    else:

        print('ERR! no checkplots found in %s' % checkplotbasedir)


if __name__ == '__main__':
    main()
