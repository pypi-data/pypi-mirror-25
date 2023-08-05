"""
This script is intended to be run on an Amazon ECS container, so information for
the job either needs to be provided in environment variables (e.g., the
REACH version and path) or loaded from S3 (e.g., the list of PMIDs).
"""
from __future__ import absolute_import, print_function, unicode_literals
from builtins import dict, str

if __name__ == '__main__':
    from indra.tools.reading import run_reach_on_pmids as rr
    import boto3
    import botocore
    import os
    import sys
    import pickle
    import logging

    logger = logging.getLogger('run_reach_on_pmids_aws')

    client = boto3.client('s3')
    bucket_name = 'bigmech'
    basename = sys.argv[1]
    pmid_list_key = 'reading_results/%s/pmids' % sys.argv[1]
    tmp_dir = sys.argv[2]
    num_cores = int(sys.argv[3])
    start_index = int(sys.argv[4])
    end_index = int(sys.argv[5])
    path_to_reach = os.environ.get('REACH_JAR_PATH')
    reach_version = os.environ.get('REACH_VERSION')
    if path_to_reach is None or reach_version is None:
        print('REACH_JAR_PATH and/or REACH_VERSION not defined, exiting.')
        sys.exit(1)

    try:
        pmid_list_obj = client.get_object(Bucket=bucket_name, Key=pmid_list_key)
    # Handle a missing object gracefully
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] =='NoSuchKey':
            logger.info('Could not find PMID list file at %s, exiting' %
                        pmid_list_key)
            sys.exit(1)
        # If there was some other kind of problem, re-raise the exception
        else:
            raise e
    # Get the content from the object
    pmid_list_str = pmid_list_obj['Body'].read().decode('utf8').strip()
    pmid_list = [line.strip() for line in pmid_list_str.split('\n')]

    # Run the REACH reading pipeline
    (stmts, content_types) = rr.run(pmid_list, tmp_dir, num_cores, start_index,
                                    end_index, False, False, path_to_reach,
                                    reach_version, cleanup=False, verbose=True)
    # Pickle the content types to S3
    ct_key_name = 'reading_results/%s/content_types/%d_%d.pkl' % \
                  (basename, start_index, end_index)
    logger.info("Saving content types for %d papers to %s" %
                (len(stmts), ct_key_name))
    ct_bytes = pickle.dumps(content_types)
    client.put_object(Key=ct_key_name, Body=ct_bytes, Bucket=bucket_name)
    # Pickle the statements to a bytestring
    pickle_key_name = 'reading_results/%s/stmts/%d_%d.pkl' % \
                      (basename, start_index, end_index)
    logger.info("Saving stmts for %d papers to %s" %
                (len(stmts), pickle_key_name))
    stmts_bytes = pickle.dumps(stmts)
    client.put_object(Key=pickle_key_name, Body=stmts_bytes,
                      Bucket=bucket_name)


