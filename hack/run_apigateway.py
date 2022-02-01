#  Copyright (c) 2020.
#
#  Metaprov.com

def main():
     import subprocess
     p = subprocess.Popen('kubectl get pods -n modela-system', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
     for line in p.stdout.readlines():
         sline = str(line)
         if "modela-api-gateway" in sline:
            parts = sline.split()
            pod = str(parts[0][0:])
            cmd = "kubectl port-forward  " + pod + " 3000:8080 -n modela-system"
            print("running " + cmd)
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            retval = p.wait()
            print("port ret val" + str(retval))
     retval = p.wait()


if __name__== "__main__":
  main()