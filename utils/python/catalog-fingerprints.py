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

    path_fp = os.path.join(meta, "fingerprints.csv")
    
    crawl = mapzen.whosonfirst.utils.crawl(data, inflate=True)
    writer = None
    
    for feature in crawl:

        props = feature["properties"]
        wof_id = props["wof:id"]
        fp = props["media:fingerprint"]

        row = {
            "wof_id": wof_id,
            "fingerprint": fp,
        }

        if writer == None:

            out = open(path_fp, "w")
            writer = csv.DictWriter(out, fieldnames=row.keys())
            writer.writeheader()

        writer.writerow(row)
