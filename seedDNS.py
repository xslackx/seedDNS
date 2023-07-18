#!/usr/bin/env python3
import requests, zipfile, asyncio, os, subprocess, socket


def getTop1m():
    topAlexa = {
        "new": "http://s3.amazonaws.com/alexa-static/top-1m.csv.zip",
        "deprecated": "https://s3.amazonaws.com/alexa-static/top-1m.csv.zip"
    }

    fZip = {
        "new": topAlexa["new"].split("/")[-1], 
        "deprecated": "old." + topAlexa["deprecated"].split("/")[-1]
    }

    if not os.access(fZip["new"], os.R_OK):
        with open(fZip["new"], "wb+") as topCsv:
            print("Getting the content... \n")
            zip = requests.get(topAlexa["new"], timeout=300, allow_redirects=True)
            print("Saving data response.\n")
            topCsv.write(zip.content)
            topCsv.close()    
            print("File: " + fZip["new"] + ", Download: OK\n")
    else:
        print(f"Found {fZip['new']} file\n")

    with zipfile.ZipFile(fZip["new"], "r") as zip:
        print("Zip content\n")
        zip.printdir()
        zip.extractall()
    zipname = zip.namelist()[0]

    return zipname

def clsFile(fn, nn):
    print("Renaming file to: " + nn + "\n")
    os.rename(fn, nn)
    cmd = f"sed -i '1,8d' {nn}"
    print("Remove MOTD\n")
    with subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True) as motd:
        motd.stdout.read()

    cmd = "sed -i 's/^[0-9]\{1,\},//g' " + f"{nn}"
    print("Remove index numbers\n")
    with subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True) as numbers:
        numbers.stdout.read()
    
    if motd.returncode == 0 and numbers.returncode == 0:
        return nn

async def pumpDig(fn, dns, mode, type, engine):
    
    with open(fn, "r") as sites:
        let=sites.read()
    lista = let.split("\n")
    limit = len(lista) - 1
    del let

    if engine == "dig":
        for i in range(0, limit):
            cmd=f"dig @{dns} {lista[i]} {type}"
            if mode == 0:
                await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE)
            elif mode == 1:
                with subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True) as dig:
                    dig.stdout.read()
    elif engine == "sock":
        async def sk(h):
            socket.gethostbyname(h)

        del type
        tk = [] 
        for i in range(0, limit):
            if mode == 0:
                tk.append(asyncio.create_task(f'sk("{lista[i]}")'))
                #asyncio.create_task(sk(lista[i]))
            if mode == 1:
                socket.gethostbyname(f"{lista[i]}")

        if len(tk) > 1:
            asyncio.create_task(tk)

    

# Example usage
#dnsTopFileName = getTop1m()
#TopFileName = "alexatop1m.txt"
#FileCleanJunks = clsFile(dnsTopFileName, TopFileName)
#dnsServer = "172.17.0.2"
#queryType = ['ANY', 'MX', 'NS', 'AAAA', 'A', 'DNSKEY', 'DS', 'SRV']
#print("DigPump\n")
#mode 0 = async very fast 
#mode 1 = for slow
# In engine define which tool use, dig or internal library, 
# internal library support only simple A query
#asyncio.run(pumpDig(FileCleanJunks, dnsServer, 0, queryType[0], "sock"))
