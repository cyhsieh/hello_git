import os, re
from datetime import datetime

class Named:
    def __init__(self):
        self.time = ""
        self.income_sw = False
        self.nowquery = ""
        self.lastquery = ""
        self.result = {}

    def clear(self):
        self.nowquery = ""
        self.lastquery = ""
        self.income_sw = False

    def proc(self, file, filename):
        outfile = open(filename + "_out.csv","w")
        print("Time,Current Query,Avg qps in Last Minute")
        outfile.write("Time,Current Query,Avg qps in Last Minute\n")
        for line in file.readlines():
            if self.income_sw:
                self.lastquery = self.nowquery
                self.nowquery = re.search(r"(\d+)", line).group(1)
                if self.nowquery and self.lastquery:
                    diff = int(self.nowquery) - int(self.lastquery)
                    diff = diff // 60
                    print(self.time + "," + self.nowquery + "," + str(diff))
                    outfile.write(self.time + "," + self.nowquery + "," + str(diff) + "\n")
                else:
                    print(self.time + "," + self.nowquery + ",")
                    outfile.write(self.time + "," + self.nowquery + ",\n")
                self.income_sw = False
            if "Statistics Dump" in line:
                time = re.search(r"\((\d+)\)",line).group(1)
                self.time = datetime.fromtimestamp(float(time)).isoformat(' ',timespec="minutes")
                # print(self.time)
                continue
            if "++ Incoming Requests ++" in line:
                self.income_sw = True
                continue
        # print(self.result)
        outfile.close()

    def proc2(self, file, filename):
        # print("Time,Current Query,Query in Last Minute")
        # outfile.write("Time,Current Query,Query in Last Minute\n")
        self.clear()
        for line in file.readlines():
            if self.income_sw:
                self.lastquery = self.nowquery
                self.nowquery = re.search(r"(\d+)", line).group(1)
                if self.nowquery and self.lastquery:
                    diff = int(self.nowquery) - int(self.lastquery)
                    # print(self.time + "," + self.nowquery + "," + str(diff))
                    # if diff is not "":
                    #     diff = diff // 60
                    diff = diff // 60
                    if self.time in self.result:
                        self.result[self.time] = diff + self.result[self.time]
                    else:
                        self.result[self.time] = diff
                # else:
                    # print(self.time + "," + self.nowquery + ",")
                self.income_sw = False
            if "Statistics Dump" in line:
                time = re.search(r"\((\d+)\)",line).group(1)
                self.time = datetime.fromtimestamp(float(time)).isoformat(' ',timespec="minutes")
                # print(self.time)
                continue
            if "++ Incoming Requests ++" in line:
                self.income_sw = True
                continue
        # print(self.result)
        # outfile.close()
        self.print_result()

    def set_proc2_outfile(self,file):
        self.proc2_filename = file + "_out.csv"

    def print_result(self):
        # print(self.result)
        print(self.proc2_filename)
        with open(self.proc2_filename,"w") as f:
            f.write("Time,Avg QPS in Last Minute")
            for i in self.result:
                print(i,self.result[i], sep=",")
                f.write(i + "," + str(self.result[i]) + "\n")

named = Named()
file = "test"
named.set_proc2_outfile(file)
for i in range(1,3):
    filename = file + str(i)
    if not os.path.exists(filename + ".txt"):
        continue
    f = open(filename + ".txt")
    named.proc2(f, filename)
    f.close()

