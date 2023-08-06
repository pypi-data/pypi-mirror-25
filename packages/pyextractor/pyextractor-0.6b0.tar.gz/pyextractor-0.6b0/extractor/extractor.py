#!/bin/python3
"""
Copyright 2017 Marlon Petry

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

    1. Redistributions of source code must retain the above copyright notice,
    this list of conditions and the following disclaimer.

    2. Redistributions in binary form must reproduce the above copyright
    notice, this list of conditions and the following disclaimer in the
    documentation and/or other materials provided with the distribution.

    3. Neither the name of the copyright holder nor the names of its
    contributors may be used to endorse or promote products derived from this
    software without specific prior written permission.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
    AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
    IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
    PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
    CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
    EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
                                         PROCUREMENT OF SUBSTITUTE GOODS OR
                                         SERVICES; LOSS OF USE, DATA, OR
                                         PROFITS; OR BUSINESS INTERRUPTION)
    HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
    STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
    ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
    POSSIBILITY OF SUCH DAMAGE.
"""

import requests
import csv
import urllib.request
from io import BytesIO
from urllib.parse import quote
from termcolor import colored, cprint
import textract
import re
import os.path
import yaml
from multiprocessing import Process, Manager,Lock
import traceback
import sys
import argparse
from pygrok import Grok
from collections import OrderedDict



def load_config():
    try:
        if args.config:
            config = args.config
        else:
            config = "config.yml"

        with open(config, 'r') as ymlfile:
            cfg = yaml.load(ymlfile)
        #validate if
        if not 'NUM_WORKERS' in cfg:
            raise Exception("NUM_WORKERS not found in config.yml")

        if not 'patterns' in cfg:
            raise Exception("Patterns not found in config.yml")


        if not 'sequence' in cfg:
            raise Exception("sequence not found in config.yml")


        return cfg
    except Exception as error:
        cprint("ERROR CONFIG " + error,'yellow')
        sys.exit(1)



def download_file(lock,in_queue,results):
    #download file
    while True:
        try:
            data = in_queue.get()
            if data == 'STOP':
                cprint("EXIT",'yellow');
                #Exit Process
                break
            url = data[0]
            percent = data[1]
            pattern = "(?P<urlPath>.*\/)(?P<filename>.*\.[a-zA-Z]{3,4}$)"
            er_filename = re.compile(pattern)
            match_file = er_filename.match(url)
            if match_file:
                urlpath = match_file.group('urlPath')
                filename = match_file.group('filename')
            else:
                raise Exception("Verify URL not found filename")

            url = urlpath+quote(filename)

            #save file in /tmp
            req = urllib.request.Request(url)
            local_file= "/tmp/"+filename
            color_progress1 = colored('[','green')
            color_progress2 = colored(']','green')

            #print(color_progress1, percent,color_progress2,url )
            if not os.path.isfile(local_file):
                with urllib.request.urlopen(req) as response:
                    remoteFile = response.read()
                    file = open(local_file, 'wb')
                    file.write(remoteFile)
            extract_text(local_file,args.lang)
            #lock.acquire()
            process_file(local_file,url,lock)
            #lock.release()
            print(color_progress1, percent,color_progress2,url )
        except Exception as error:
            cprint(error,'yellow')
            traceback.print_exc(file=sys.stdout)
            sys.exit(1)


def extract_text(local_file,lang):
    #extract
    local_file_text = local_file + ".text"
    if not os.path.isfile(local_file_text):
        text = textract.process(local_file,method='tesseract', language=lang)
        file = open(local_file_text,'wb')
        file.write(text)
        file.close()
    return local_file_text

def extract_grok(patterns,text,debug=False):
    result = None
    for p in patterns:
        grok=Grok(p)
        if grok.match(text.rstrip()):
            if debug:
               print(text)
               pattern_color = colored(p,'red')
               matched_color = colored("MATCHED","green")
               coli_color = colored(grok.match(text.rstrip()),'magenta')
               cprint(pattern_color + " " + matched_color + " " + coli_color)
            result = (grok.match(text.rstrip()))

            return result
    return result



def process_file(local_file,url,lock):
    try:
        local_file = local_file+".text"
        file_text = open(local_file,'rb')
        ex = file_text.read()
        text = ex.decode('utf-8')
        extraction=OrderedDict()
        extraction[local_file]=[]

        for line in text.splitlines():
            if line:
                result = extract_grok(cfg['patterns'],line,debug=False)
                if result:
                    extraction[local_file].append(result)
        write_csv(lock,local_file,extraction,url)
        cprint("FINISHED" + local_file,'red')

    except Exception as error:
        cprint(error,'yellow')
        traceback.print_exc(file=sys.stdout)
        sys.exit(1)


def origin_url_filename(f,url,sequence,row_csv):
    """
        Function to write when origin is filename or url
    """
    for hk in sequence['titles']:
        hk_dict = sequence[hk]
        origin = hk_dict['origin']
        if origin == 'url':
            row_csv[hk] = url
        elif origin == 'filename':
            if 'pattern_regex' in hk_dict:
                matchFilename = re.compile(".*\/(?P<file>.*[a-zA-Z]{3,4})")
                mfile = matchFilename.match(f)
                if mfile:
                    f_name = mfile.group('file')
                    lookup_re = re.compile(hk_dict['pattern_regex'])
                    result = lookup_re.match(f_name)
                    if result:
                        row_csv[hk] = result.group(hk)
                    else:
                        row_csv[hk] = 'NONE'
                else:
                    raise Exception('Filename Not Found to ' + f + ' in '+hk)


def create_ordereddict(sequence):

    #create ordered dict from list
    oddict = []
    for e in sequence['titles']:
        oddict.append((e,'NONE'))

    ordered_keys = OrderedDict(oddict)
    return ordered_keys


def write_csv(lock,f,extraction,url):


    flag_file_exist = False
    if os.path.exists(args.out):
        flag_file_exist = True

    sequence = cfg['sequence']

    file_csv = open(args.out,'a')


    ordered_keys = create_ordereddict(sequence)

    output_csv = csv.DictWriter(file_csv, ordered_keys,delimiter=';')
    if not flag_file_exist:
        #Write HEAD csv necessary because threadsm otherwise write everytime
        output_csv.writerow(dict((fn,fn) for fn in ordered_keys.keys()))

    row_csv = ordered_keys


    origin_url_filename(f,url,sequence,row_csv)


    flag_save = False
    for e in extraction[f]:

        k = list(e.keys())
        seq = sequence[k[0]]

        #Valida se eh o momento de salvar os dados no arquivo
        if 'save' in seq:
            flag_save = seq['save']


        #conforme a sequencia busca a referencia no dictionary
        if k[0] in e:
            if DEBUG:
                print(k[0],'in',e)
            if 'pattern' in seq:
                print(e[k[0]],seq['pattern'])
                result = extract_grok(seq['pattern'],e[k[0]].rstrip(),debug=False)

                if DEBUG:
                    cprint(result,'green')
            else:
                result = e

                if DEBUG:
                    cprint(e,'magenta')
            #i#if DEBUG:
            #    cprint(result,'green')

            if result:
                for k,v in result.items():
                    if DEBUG:
                        cprint("ADD " + str(k) + ":" + str(v) + " to row_csv",'yellow')
                    row_csv[k] =v
        else:
            if DEBUG:
                print("NOT",k[0],'in',e)


        if flag_save:
            if DEBUG:
                cprint(">>>>SAVE<<<<",'blue')
                print(row_csv)
            output_csv.writerow(row_csv)

            if DEBUG:
                cprint(">>>>SAVE<<<<",'blue')

            row_csv = create_ordereddict(sequence)
            origin_url_filename(f,url,sequence,row_csv)
            flag_save = False


    file_csv.close()
    #ock.release()






def main():
    global cfg, args,DEBUG

    parser = argparse.ArgumentParser(description='Extractor is program to '\
                                     'extract text from pdf,images using grok'\
                                     'patterns')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--linkFile', help='File with links to pdfs or imgs')
    group.add_argument('--url',help='Single Doc to extract')
    parser.add_argument('--out',help='csv file to save output',required=True)
    parser.add_argument('--config', help='Path to config.yml')
    parser.add_argument('--lang',help='language of text', required=True)

    args = parser.parse_args()


    cfg = load_config()
    if 'DEBUG' in cfg:
        DEBUG = cfg['DEBUG']


    if os.path.exists(args.out):
        cprint("Already exists --out "+ args.out, 'yellow')
        sys.exit(0)


    if args.linkFile:
        with open(args.linkFile,encoding='utf-8-sig') as linksfile:
            data = []
            for line in linksfile:
                data.append(line)
            total = len(data)
    elif args.url:
        data = []
        data.append(args.url)
        total = len(data)

    NUM_WORKERS = cfg['NUM_WORKERS']
    pool = []
    manager = Manager()
    results = manager.list()
    work = manager.Queue(NUM_WORKERS)
    lock = Lock()
    for i in range(NUM_WORKERS):
        process = Process(target=download_file,args=(lock,work,results))
        process.start()
        pool.append(process)

    i = 1;
    for url in data:
        data = [url,"%.2f" % ((i*100)/total)]
        work.put(data )
        i = i+1

    for i in range(NUM_WORKERS):
        work.put('STOP')

    for p in pool:
        p.join()




if __name__=="__main__":

    main()

