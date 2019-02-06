#!/usr/bin/env python

import os
import sys
import csv
import logging

import mapzen.whosonfirst.utils

if __name__ == "__main__":

    import optparse
    opt_parser = optparse.OptionParser()

    opt_parser.add_option('-r', '--root', dest='root', action='store', default='/usr/local/data/sfomuseum-data-media', help='...')    

    opt_parser.add_option('-v', '--verbose', dest='verbose', action='store_true', default=False, help='Be chatty (default is false)')
    options, args = opt_parser.parse_args()

    if options.verbose:	
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    
    data = os.path.join(options.root, "data")
    meta = os.path.join(options.root, "meta")    

    path_exh = os.path.join(meta, "exhibitions.csv")
            
    crawl = mapzen.whosonfirst.utils.crawl(data, inflate=True)

    lookup = {}
    
    for feature in crawl:

        props = feature["properties"]
        wof_id = props["wof:id"]

        mprops = props["media:properties"]

        # this is way way too brittle and is guaranteed to cause hilarity one day
        # but will suffice for now... (20190107/thisisaaronland)

        print "WHIRRRR %s" % wof_id
        
        depicts = mprops["depicts"]
        depicts = depicts[0]

        count = lookup.get(depicts, 0)
        lookup[depicts] = count + 1

    writer = None

    for exh_id, count in lookup.items():

        row = {
            "wof_id": exh_id,
            "count": count
        }

        if not writer:
            out = open(path_exh, "w")
            writer = csv.DictWriter(out, fieldnames=row.keys())
            writer.writeheader()

        writer.writerow(row)
