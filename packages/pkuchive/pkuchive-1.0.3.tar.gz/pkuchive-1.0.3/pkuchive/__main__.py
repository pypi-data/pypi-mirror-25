#-*-coding:utf-8-*-
import sys
import getopt
import os
import string
dic = open("/usr/local/pkuchive_data/archive_map.arc", "r")


def procedure(dir_name):
    dir_name = str(dir_name)
    dir_name = dir_name[:4]
    return dict[dir_name]


def version():
    print("")
    print("pkuchive 1.0.1 by Kvar_ispw17 with Python 3.6.2")
    print("email : enkerewpo@gmail.com")


def usage():
    print("\npkuchive usage:")
    print("     -i [dir] : selection the directory that contains your")
    print("                problems code folders")
    print("     -h       : show this helping page")
    print("     -ver     : show the version of pkuchive")


def main():
    opts, args = getopt.getopt(sys.argv[1:], "hi:|ver")
    input_file = ''
    dict = {}
    argc = len(sys.argv)
    for w in range(1000, 4000):
        line = dic.readline()
        if not line:
            break
        str_full = str(line)[:-1]
        A = str(str_full[:4])
        B = str(str_full[5:])
        dict[A] = B
    if(argc == 1):
        usage()
        sys.exit()
    for op, value in opts:
        if op == '-i':
            input_file = value
            path = os.getcwd()
            path += '/'
            path += input_file
            tot = 0
            for dir in os.listdir(path):
                tot = tot + 1
                if(len(str(dir)) > 4):
                    continue
                strf = dict[dir]
                strd = dir + ' ' + strf
                # strd = strd.decode('utf-8')
                os.rename(os.path.join(path, dir), os.path.join(path, strd))
            print ("\nsuccessfully tagged " + str(tot) + " folder(s)")
        elif op == '-h':
            usage()
            sys.exit()
        elif op == '-v':
            version()
            sys.exit()


if __name__ == "__main__":
    sys.exit(main())
