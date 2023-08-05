# Simple ESPER command line tool
# Allows reading and writing of ESPER variables

import os
import sys
import requests
import argparse
import signal

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, '../VERSION')) as version_file:
    version = version_file.read().strip()

def signal_handler(signal, frame):
        sys.exit(0)

def main(argv):
    prog='esper-tool'
        
    # Register handler
    signal.signal(signal.SIGINT, signal_handler)
    
    parser = argparse.ArgumentParser(prog=prog)

    # Verbose, because sometimes you want feedback
    parser.add_argument('-v','--verbose', help="Verbose output", default=False, action='store_true')
    parser.add_argument('--version', action='version', version='%(prog)s ' + version)
    
    # Sub parser for write,read
    subparsers = parser.add_subparsers(title='commands', dest='command', description='Available Commands', help='Type '+prog+' [command] -h to see additional options')

    # Write arguments
    parser_write = subparsers.add_parser('write', help='[-o <offset>] [-d <json value/array>]  <url> <mid> <vid>')
    parser_write.add_argument('-d','--data', help="JSON data to write")
    parser_write.add_argument('-f','--file', type=argparse.FileType('r'), help="JSON file to write from")    
    parser_write.add_argument('-o','--offset', default='0',dest='offset', help='offset to write to')
    
    # Read arguments
    parser_read = subparsers.add_parser('read', help='[-o <offset>] [-l <length>] <url> <mid> <vid>')
    parser_read.add_argument('-o','--offset', default='0', help='element offset to read from')
    parser_read.add_argument('-l','--len', default='0', help='elements to read')

    parser_upload = subparsers.add_parser('upload', help='[-f <file>] <url> <mid> <vid>')
    parser_upload.add_argument('-f','--file', required='true', type=argparse.FileType('rb'), help="binary file to upload")    
    parser_upload.add_argument('-r','--retry', default='3', help='number of retries to attempt')
    
    # positional arguments
    parser.add_argument("url", help="Node URL. ie: 'http://<hostname>:<port>'")
    parser.add_argument("mid", help="Module Id or Key")
    parser.add_argument("vid", help="Variable Id or Key")

    # Put the arguments passed into args
    args = parser.parse_args()

    # Strip trailing / off args.url
    if(args.url[-1:] == '/'):
        args.url = args.url[0:-1]
    
    # if url is missing 'http', add it
    if(args.url[0:7] != 'http://'):
        args.url = 'http://' + args.url

    # Keys should always be lower case
    args.mid = args.mid.lower()
    args.vid = args.vid.lower()

    try: 
        # Handle write
        if(args.command == 'write'): 
            querystring = {'mid': args.mid, 'vid': args.vid, 'offset': args.offset}

            # if -d is set, we will write what is passed on the command line
            # ESPER is expecting either a JSON array [], a JSON string " ", or a single JSON primitive
            if args.data is not None:
                payload = args.data

            # if -f is set, we will write in file that contains JSON in the above format
            elif args.file is not None:
                with args.file as upload_file:
                    payload = upload_file.read()
            else:
                # No data specified to send on write, just bail out. Argparser should ensure this branch never gets reached
                print "No data specified to send, exitting\n"
                # It didn't fail, so return 0 
                sys.exit(0) 
            
            # Send POST request
            r = requests.post(args.url + '/write_var', params=querystring, data=payload)
            if(r.status_code == 200):
                if(args.verbose): 
                    err = r.json()
                    print 'Successfully wrote data'
                    print '\tModule: ' + str(err['mid']) + '\n\tVariable: ' + str(err['id']) + '\n\tTimestamp: ' + str(err['ts']) + '\n\tWrite count: ' + str(err['wc']) + '\n\tStatus: ' + str(err['stat'])
                sys.exit(0)
            else:
                if(args.verbose): 
                    err = r.json()
                    print '\tStatus: ' + str(err['error']['status']) + '\n\tCode: ' + str(err['error']['code']) + '\n\tMeaning: ' + err['error']['meaning'] + '\n\tMessage: ' + err['error']['message'] + '\n'
                sys.exit(1)
        # Handle read
        elif(args.command == 'read'): 
            querystring = {'mid': args.mid, 'vid': args.vid, 'offset': args.offset, 'len': args.len, 'dataOnly':'y'}
            # Send GET request
            r = requests.get(args.url + '/read_var', params=querystring)
            if(r.status_code == 200): 
                print(r.content)
                sys.exit(0)
            else:
                if(args.verbose): 
                    err = r.json()
                    print '\tStatus: ' + str(err['error']['status']) + '\n\tCode: ' + str(err['error']['code']) + '\n\tMeaning: ' + err['error']['meaning'] + '\n\tMessage: ' + err['error']['message'] + '\n'
                sys.exit(1)
        # Handle file uploading
        elif(args.command == 'upload'):
            # Get var info first, need to know max chunk size of file to send
            with args.file as upload_file:
                querystring = {'mid': args.mid, 'vid': args.vid }
                r = requests.get(args.url + '/read_var', params=querystring)
                if(r.status_code == 200):
                    # Var found, lets see what we got!
                    vinfo = r.json()
                    # Always use the 'max_req_size', otherwise certain flash devices like EPCQs may have issue with multiple chunks to the same block..
                    chunk_size = vinfo['max_req_size']
                    # Get the size of the file and then return to the start
                    upload_file.seek(0, os.SEEK_END)
                    file_size = upload_file.tell()
                    upload_file.seek(0, os.SEEK_SET)
                    
                    if(args.verbose): 
                        print('Chunk size: ' + str(chunk_size))
                        print('File size: ' + str(file_size))
                        print "Uploading [%-50s]" % " ",
                        
                    # Get the first chunk of the file
                    payload = upload_file.read(chunk_size)
                    chunk_size = len(payload)
                    file_offset = 0
                    retry_count = 0
                    max_retries = args.retry
                    while(chunk_size > 0):
                        sys.stdout.flush()
                        # transmit payload using binary methods
                        querystring = {'mid': args.mid, 'vid': args.vid, 'offset': file_offset, 'len': chunk_size, 'binary': 'y'}
                        r = requests.post(args.url + '/write_var', params=querystring, data=payload)

                        # Did we transfer successfully?
                        if(r.status_code == 200):
                            # update offset to write to, based on last chunk_size written
                            file_offset += chunk_size
                            # Grab the next binary chunk
                            payload = upload_file.read(chunk_size)
                            # update chunk_size to match what was actually grabbed (may be less if chunk_size was less than remaining length)
                            chunk_size = len(payload)
                                                    
                            if(args.verbose):
                                strCompleteness = '#' * int(file_offset / float(file_size) * 50)
                                print "\rUploading [%-50s]" % strCompleteness,
                        # Retry up to X times
                        elif(retry_count < max_retries):
                            retry_count += 1
                            print "\nUpload attempt failed, retrying..."
                        else:
                            print "Failed to upload " + os.path.basename(upload_file.name) 
                            sys.exit(1)

                    if(args.verbose):
                        print "\nDone uploading " + os.path.basename(upload_file.name)

                    # All done uploading file, exit
                    sys.exit(0)

                else:
                    if(args.verbose):
                        err = r.json()
                        print '\tStatus: ' + str(err['error']['status']) + '\n\tCode: ' + str(err['error']['code']) + '\n\tMeaning: ' + err['error']['meaning'] + '\n\tMessage: ' + err['error']['message'] + '\n'
                    sys.exit(1)
        else:
            # No options selected, this should never be reached
            sys.exit(0) 
    
    except requests.exceptions.Timeout:
        # Maybe set up for a retry, or continue in a retry loop
        print 'Timed out attempting to communicate with ' + args.url + "\n"
        sys.exit(1)
    except requests.exceptions.TooManyRedirects:
        # Tell the user their URL was bad and try a different one
        print 'Timed out attempting to communicate with ' + args.url + "\n"
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        # catastrophic error. bail.
        print "Unknown error occured ( "
        print e
        print " )\n"
        sys.exit(1)

