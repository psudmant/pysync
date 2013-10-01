from optparse import OptionParser
import subprocess as sub
import os


def do_command(cmd):
    p = sub.Popen(cmd,stdout=sub.PIPE,
                      stderr=sub.PIPE,
                      shell=True)

    output,errors = p.communicate()
    ret_code = p.returncode
    print output, errors
    if ret_code != 0: print "".join(["***\n" for i in xrange(1)])
    return ret_code

def get_cmd(path, action, dry_run):
    
    cwd = os.getcwd()
    cwd_dir = cwd.split("/")[-1]

    d=''
    if dry_run:
        d='n'
    if action=="PULL": 
        cmd = 'rsync -arvz%s %s/%s %s'%(d, path, cwd_dir, cwd)
    else:
        cmd = 'rsync -arvz%s %s %s'%(d, cwd, path)
    return cmd

def sync(remote_path, action, dry_run):

    cmd = get_cmd(remote_path, action, dry_run)
    print ">%s\n%s"%(action,cmd)
    return do_command(cmd)


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
    (o,args) = opts.parse_args()
        
    if o.remote_path:
        try:
            with open(".pysync.info",'w') as F:
                remote_path=o.remote_path
                sync(remote_path, "PUSH", dry_run=True) 
                sync(remote_path, "PULL", dry_run=True)
                F.write("%s\n"%o.remote_path)
        except IOError:
            print "IOERROR"
    else:
        if len(args)!=1 or not (args[0].upper()=="PUSH" or args[0].upper()=="PULL"):
            opts.print_help()
            exit(1)
        
        action = args[0]

        try:
            with open(".pysync.info") as F:
                remote_path = F.readline().rstrip() 
                if sync(remote_path, action, dry_run=True)==0:
                    choice = raw_input("dry run complete - continue [y/n]")
                    if choice.upper() == "Y":
                        sync(remote_path, action, dry_run=False)

        except IOError:
            print "no remote path setup. Run pysync --setup <remote_path>"
            
    

