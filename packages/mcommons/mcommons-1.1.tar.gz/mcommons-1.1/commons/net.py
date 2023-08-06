
from terminal import *
import requests
import socket



try:
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
except:
    try:
        import requests
        from requests.packages.urllib3.exceptions import InsecureRequestWarning
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    except:
        pass



def print_response(r):
    if r.status_code >= 200 and r.status_code < 300:
        print_ok(str(r.status_code) + " ")
    else:
        print_fail("[%s] - %s " % (str(r.status_code), r.text))


def http_post(url, data, headers={}, username=None, password=None, **kwargs):
    try:
        print_info(url + " ..  ")
        headers['User-Agent'] = 'Mozilla'
        r = requests.post(url, data=data, verify=False, auth=(
            username, password), headers=headers, allow_redirects=False, **kwargs)
        if r.status_code > 300 and r.status_code < 400:
            print_ok(" -> " + r.headers['Location'] + "\n")
            return http_post(r.headers['Location'], data=data, headers=headers, username=username, password=password, **kwargs)
        print_response(r)
        return r
    except Exception, e:
        print_fail(str(e))


def http_get(url, username=None, password=None, params=None, **kwargs):
    try:
        print_info(url + " ..  ")
        r = requests.get(url,
                        verify=False,
                        params=params,
                        auth=(username, password) if username != None else None,
                        allow_redirects=False,
                        **kwargs)
        if r.status_code > 300 and r.status_code < 400:
            print_ok(" -> " + r.headers['Location'] + "\n")
            return http_get(r.headers['Location'],  username, password, params, **kwargs)
        print_response(r)
        return r
    except requests.exceptions.ConnectionError:
        print_fail(" connection refused \n")
    except Exception, e:
        print_fail(e.body)
        print_fail(str(e))
        return str(e)


def ping(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.settimeout(2.0)
        s.connect((host, port))
        s.close()
        return True
    except Exception, e:
        s.close()
        return False


def execute_ssh(host, username, password, cmd):
    import paramiko
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.connect(host, username=username, password=password)
    print cmd
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)
    print ssh_stderr.readlines()
    print ssh_stdout.readlines()