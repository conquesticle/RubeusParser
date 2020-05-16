import re, csv, os, sys


def parse_rubeus_output(directory,outfile="rubeus_output.csv"):
    files = list()
    fieldnames = ['domain','samaccountname','encryption']

    for rub_file in os.listdir(directory):
        if rub_file.endswith(".txt"):
            files.append(rub_file)

    for rub_file in files:
        print("Reading {0}".format(rub_file))
        domain = rub_file.split(".txt")[0]
        with open(r'{0}\{1}'.format(directory,rub_file),'r') as file:
            body = file.read()
        results = [{'domain':domain,"samaccountname":x[0],"encryption":x[1].replace(", ","|")} for x in re.findall(r"\[\*\]\sSamAccountName\s*:\s*(\S+?)[\r\n\s].+?\[\*\]\sSupported\sETypes\s+:\s+([\s\S]+?)[\r\n]",body,re.DOTALL)]
        print("Found {0} results".format(len(results)))
        with open(r'{0}\{1}'.format(directory,outfile),'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile,fieldnames=fieldnames)
            if os.stat(r'{0}\{1}'.format(directory,outfile)).st_size == 0:
                writer.writeheader()
            writer.writerows(results)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        args = [r"{0}".format(arg) for arg in sys.argv[1:]]
        parse_rubeus_output(*args)
