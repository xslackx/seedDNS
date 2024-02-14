#!bin/env python3
from seedDNSabc import seedDNS as abcseed
from zipfile import ZipFile as zp
from os import access, R_OK, listdir
from requests import get
from subprocess import Popen, PIPE
from csv import reader
from time import sleep
from random import randint
from asyncio import create_subprocess_shell

class seedDNS(abcseed):
    def __init__(self) -> None:
        self.tops_1m: list = [
            "http://s3-us-west-1.amazonaws.com/umbrella-static/top-1m.csv.zip",
            "http://downloads.majestic.com/majestic_million.csv"
        ]
        self.tops_hist_dir: dict = {"type": str, "location": str}
        super().__init__()
        
    def top1m(self):
        for self.fp_url in self.tops_1m:
            self.fp_name = self.fp_url.split('/')[-1]
            self.type = None            
            if not access(self.fp_name, R_OK):
                with open(self.fp_name, "wb+") as self.zip:
                    self.blob = get(self.fp_url, timeout=300, allow_redirects=True)
                    self.zip.write(self.blob.content)
                    self.zip.close()
                with Popen(f'file {self.fp_name}', stdout=PIPE, shell=True) as self.typefile:
                    self.type = self.typefile.stdout.read().decode()
                    if self.type.split()[1] == 'Zip':     
                        with zp(self.fp_name, "r") as csv:
                            csv.extractall()
        
    def fmtfile(self):
        self.top_list = []
        for self.has_csv_file in listdir():
            self.index = None
            try:
                if self.has_csv_file.split('.')[1] == 'csv' and self.has_csv_file.split('.')[-1] == 'csv':
                    with open(self.has_csv_file, newline='') as self.csv_file:
                        self.csv = reader(self.csv_file, delimiter=',')
                        if self.has_csv_file.split('.')[0] == 'majestic_million':
                            self.index = 2
                        else: 
                            self.index = 1
                        for self.row in self.csv:
                            self.top_list.append(self.row[self.index])
            except:
                pass
            
        if len(self.top_list) > 10:
            self.tops = list(set(self.top_list))
            with open('data/tops_compiled.txt', 'w') as self.local_save:
                for self.item in self.tops:
                    self.local_save.write(self.item+"\n")
                
    async def consult(self, dns, mode, type_msg):
        with open('data/tops_compiled.txt', 'r') as self.sites:
            self.items = self.sites.read()
        self.items = self.items.split('\n')
        self.items_len = len(self.items)
        
        if not dns:
            self.dns = '127.0.0.1'
        else:
            self.dns = dns
        
        if not type_msg:
            self.type_msg = 'ANY'
        else:
            self.type_msg = type_msg

        for self.index in range(0, self.items_len):
            cmd=f"dig @{self.dns} {self.items[self.index]} {self.type_msg}"
            if mode == 0:
                await create_subprocess_shell(cmd, stdout=PIPE, shell=True)
                sleep(randint(0,10))
            elif mode == 1:
                with Popen(cmd, stdout=PIPE, shell=True) as dig_cmd:
                    dig_cmd.stdout.read()
                sleep(randint(0,10))