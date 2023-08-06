from subprocess import *
import subprocess
import sh

from terminal import *


def stream_process_results(p, prefix=''):
    out = ""
    while True:
        line = p.stdout.readline()
        if not line:
            p.poll()
            print_info("[%s] " % prefix)
            print_ok(line + "\n")
            if p.returncode == 0:
                print_info(prefix + " ")
                print_ok("[0]\n")
            else:
                print_info(prefix + " ")
                print_fail("[%s]" % p.returncode + "\n")

            print


def print_process_result(p, prefix='', full=False):

    while True:
        line = p.stdout.readline()
        if not line:
            p.poll()
            if p.returncode == 0:
                print_info(prefix + " ")
                print_ok("[0]\n")
                if full:
                    print out
            else:
                print_info(prefix + " ")
                print_fail("[%s]" % p.returncode + "\n")
                print out
            return out
        out += line + "\n"


def print_process(p, prefix=''):
    out = ""
    while True:
        line = p.stdout.readline()
        if not line:
            p.poll()
            if p.returncode == 0:
                print_info(prefix + " ")
                print_ok("[0]\n")
            else:
                print_info(prefix + " ")
                print_fail("[%s]" % p.returncode + "\n")
            return out
        out += line + "\n"




def execute(command, async=False):
    print_info("executing " + white(command) + " .. ")
    p = Popen(command, stdout=subprocess.PIPE, shell=True, env=os.environ)
    if async:
        call_async(print_process_result, [p, command])
    else:
        return print_process(p, command)



def ansible_playbook(playbook, host, inventory=None, extra_vars=None, group=None, private_key_file=None, remote_user=None):
    print_info("running play %s on %s" % (playbook, host))
    ansible = sh.Command('ansible-playbook')
    args = [playbook, "-l", host]
    if inventory != None:
        args.append("-i")
        args.append(inventory)
    if extra_vars != None:
        for k, v in extra_vars.items():
            args.append('-e')
            args.append("%s=%s" % (k, v))

    print args

    def out(line):
        sys.stdout.write(blue(playbook) + gray("/" + host) + " " + line)
    ansible(args, _out=out, _err=out)
