from optparse import OptionParser
import subprocess as sub
import os
import json

def do_command(cmd):
    p = sub.Popen(cmd,stdout=sub.PIPE,
                      stderr=sub.PIPE,
                      shell=True)

    output,errors = p.communicate()
    ret_code = p.returncode
    print output, errors
    if ret_code != 0: print "".join(["***\n" for i in xrange(1)])
    return ret_code

def get_cmd(path, action, exclude_dirs, dry_run):
    
    cwd = os.getcwd()
    cwd_dir = cwd.split("/")[-1]

    d=''
    exclude=''
    if len(exclude_dirs)>0:
        exclude = "--exclude-from ./.exclude.txt"
        with open(".exclude.txt",'w') as F:
            for f in exclude_dirs:
                F.write("%s\n"%f)

    if dry_run:
        d='n'
    if action=="PULL": 
        #cmd = 'rsync -arvz%s %s/%s %s'%(d, path, cwd_dir, cwd)
        cmd = 'rsync --progress %s -arvz%s %s/ %s/'%(exclude, d, path, cwd)
    elif action =="PUSH":
        cmd = 'rsync --progress %s -arvz%s %s/ %s/'%(exclude, d, cwd, path)
    else:
        print "no action"
        exit(1)
    return cmd

def sync(remote_info, action, dry_run):
    
    remote_path = remote_info['remote_path']
    exclude_dirs = remote_info['exclude_dirs']

    cmd = get_cmd(remote_path, action, exclude_dirs, dry_run)
    print ">%s\n%s"%(action,cmd)
    return do_command(cmd)

def read_info(): 
    if not os.path.exists(".pysync.info"):
        with open(".pysync.info",'w') as F:
            json.dump({"remote_path":None, "exclude_dirs":[]},F)
    
    with open(".pysync.info") as F:
        remote_info = json.load(F)

    return remote_info


def prompt(msg=""):
    choice = raw_input("%s continue [y/n]"%(msg))
    
    if choice.upper()=="Y":
        return
    else:
        exit(1)

def write_info(remote_info):
    with open(".pysync.info",'w') as F:
        remote_info = json.dump(remote_info,F)


if __name__=="__main__":
    usage_txt = "pysync [options] PUSH|PULL"
    opts = OptionParser(usage=usage_txt)
    opts.add_option('','-f',dest='force',
                        default=False,
                        action='store_true',
                        help="skip dry run")
    
    opts.add_option('','--set_remote_path',
                        dest='remote_path',
                        default=None,
                        help="set remote path")
    
    opts.add_option('','--add_exclude_path',
                        dest='exclude_path',
                        default=None,
                        help="add exclude path")
    
    (o,args) = opts.parse_args()
        
    remote_info = read_info() 
    
    if o.remote_path:
        remote_info["remote_path"]=o.remote_path
        sync(remote_info, "PUSH", dry_run=True) 
        sync(remote_info, "PULL", dry_run=True)
        prompt(msg="dry run complete")
        write_info(remote_info)
    elif o.exclude_path:
        remote_info["exclude_dirs"].append(o.exclude_path)
        sync(remote_info, "PUSH", dry_run=True) 
        sync(remote_info, "PULL", dry_run=True)
        prompt(msg="dry run complete")
        write_info(remote_info)
    else:    
        if len(args)!=1 or not (args[0].upper()=="PUSH" or args[0].upper()=="PULL"):
            opts.print_help()
            exit(1)
        elif remote_info['remote_path'] == None:
            print "no remote path setup.\
                        Run pysync --setup <remote_path>\
                        or pysync --help for more options"
            exit(1) 

        action = args[0].upper()

        if sync(remote_info, action, dry_run=True)==0:
            prompt("dry run complete")
            sync(remote_info, action, dry_run=False)

            
    

