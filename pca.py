import ipyrad
import ipyrad.analysis as ipa
import toyplot.png

import os
import time
import json

def get_job_details():
    """Reads in metadata information about assets used by the algo"""
    job = dict()
    job['dids'] = json.loads(os.getenv('DIDS', None))
    job['metadata'] = dict()
    job['files'] = dict()
    job['algo'] = dict()
    job['secret'] = os.getenv('secret', None)
    algo_did = os.getenv('TRANSFORMATION_DID', None)
    if job['dids'] is not None:
        for did in job['dids']:
            # get the ddo from disk
            filename = '/data/ddos/' + did
            print(f'Reading and printing data file {filename}')
            f = open(filename, 'r')
            print(f.read())
            
            print(f'Reading json from {filename}')
            with open(filename) as json_file:
                ddo = json.load(json_file)
                if ddo is not None:
                    # search for metadata service
                    for service in ddo['service']:
                        if service['type'] == 'metadata':
                            job['files'][did] = list()
                            index = 0
                            for file in service['attributes']['main']['files']:
                                job['files'][did].append(
                                    '/data/inputs/' + did + '/' + str(index))
                                index = index + 1
    if algo_did is not None:
        filename = '/data/ddos/' + algo_did
        print(f'Reading and printing algo file {filename}')
        f = open(filename, 'r')
        print(f.read())
            
        job['algo']['did'] = algo_did
        job['algo']['ddo_path'] = '/data/ddos/' + algo_did
    return job
  
def execute_pca(job_details):
    """Executes the line counter based on inputs"""
    print('Starting compute job with the following input information:')
    print(json.dumps(job_details, sort_keys=True, indent=4))

    """ Now, count the lines of the first file in first did """
    first_did = job_details['dids'][0]
    filename = job_details['files'][first_did][0]
    non_blank_count = 0
    with open(filename) as infp:
        for line in infp:
            if line.strip():
                non_blank_count += 1
    print ('number of non-blank lines found %d' % non_blank_count)
    """ Print that number to output to generate algo output"""
    f = open("/data/outputs/result", "w")
    f.write(str(non_blank_count))
    f.close()
    
    vcffile = filename
    # Create the pca object
    # `quiet=True` indicates we don't care about the details, at this point
    pca = ipa.pca(data=vcffile)
    pca.run()
    img = pca.draw()
    # print(img)

    toyplot.png.render(img[0], "result.png")


if __name__ == '__main__':
    execute_pca(get_job_details())
