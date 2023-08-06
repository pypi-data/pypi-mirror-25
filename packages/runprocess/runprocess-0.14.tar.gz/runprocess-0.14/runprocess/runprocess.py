#!/usr/bin/env python
"""
Take a shell command, run it, return a dictionary with indexes output and exit status
"""
import subprocess
import sys
from gmailer import senderror
from time import sleep
import select

# function to run shell commands results in a dictionary with output and exit status
def runprocess(command, singlestring=False):
    """
    Take a shell command, run it, return a dictionary with indexes output and exit status
    :type command: list
    :param command: the command to execute in form of a list Sample1: ['/bin/ls'], Sample2: ['/bin/ls', '-l', '/tmp' ]
    :type singlestring: boolean
    :param singlestring: is the command beeing passed all one string. If you want to use shell globbing you will need to use this option (Example: ['mv','/var/lib/pgsql/9.1/data/*','/mnt/pgsql'] will not work because of the asterisk, you need to pass a single item list of the string ['mv /var/lib/pgsql/9.1/data/* /mnt/pgsql'] as command and set singlestring to True)

    """
    # the dictionary we will return
    output_dict = {}
    # the actual process making stdout and stderr available
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=singlestring)
    # loop that waits for command to finish
    while(True):
        exit_status = p.poll() #returns None while subprocess is running
        # process is done once exit_status is not None
        if(exit_status is not None):
            # capture the exit status
            output_dict['exit_status'] = exit_status
            # the list where we will store our output
            temp_list = []
            # step through and grab the output
            for line in p.stdout:
                temp_list.append(line)
            # storeout output
            output_dict['output'] =  temp_list
            # return a two key dict with the output and the exit_status 
            return output_dict
        sleep(2)

# function to run shell commands results in a dictionary with output and exit status
def runprocess_realtime(command, singlestring=False):
    """
    Take a shell command, run it, return a dictionary with indexes output and exit status, WARNING: this version (realtime) will use much more cpu as it constantly polls the running process and thus exit right when the process is done.  Only use this if time is critical and cpu isn't
    :type command: list
    :param command: the command to execute in form of a list Sample1: ['/bin/ls'], Sample2: ['/bin/ls', '-l', '/tmp' ]
    :type singlestring: boolean
    :param singlestring: is the command beeing passed all one string. If you want to use shell globbing you will need to use this option (Example: ['mv','/var/lib/pgsql/9.1/data/*','/mnt/pgsql'] will not work because of the asterisk, you need to pass a single item list of the string ['mv /var/lib/pgsql/9.1/data/* /mnt/pgsql'] as command and set singlestring to True)

    """
    # the dictionary we will return
    output_dict = {}
    # the actual process making stdout and stderr available
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=singlestring)
    # loop that waits for command to finish
    while(True):
        exit_status = p.poll() #returns None while subprocess is running
        # process is done once exit_status is not None
        if(exit_status is not None):
            # capture the exit status
            output_dict['exit_status'] = exit_status
            # the list where we will store our output
            temp_list = []
            # step through and grab the output
            for line in p.stdout:
                temp_list.append(line)
            # storeout output
            output_dict['output'] =  temp_list
            # return a two key dict with the output and the exit_status 
            return output_dict


def runprocess_auto_check(command, local_hostname, singlestring=False):
    """
    Take a shell command, run it, return a dictionary with indexes output and exit status, if there's a non-zero exit status send a yelp email and exit script
    :type command: list
    :param command: the command to execute in form of a list Sample1: ['/bin/ls'], Sample2: ['/bin/ls', '-l', '/tmp' ]
    :type local_hostname: str
    :param local_hostname: the hostname of the localmachine
    :param singlestring: is the command beeing passed all one string. If you want to using shell globbing you will need to use this option (Example: ['mv','/var/lib/pgsql/9.1/data/*','/mnt/pgsql'] will not work because of the asterisk, you need to pass a single item list of the string ['mv /var/lib/pgsql/9.1/data/* /mnt/pgsql'] as command and set singlestring to True)

    """

    process_output = runprocess(command, singlestring=singlestring)
    if process_output['exit_status'] != 0:
        # changed local_hostname['output'][0].strip() to local_hostname this should assume a str
        subject_text="command on %s failed " % local_hostname
        body_text = "Command: %s failed on %s. Command resulted in an exit code of %s.  Output follows\n%s" %(' '.join(command), local_hostname, process_output['exit_status'],''.join(process_output['output']))
        senderror(subject_text, body_text)
        print(body_text)        
        sys.exit(1)
    return process_output

def runprocess_realtime_auto_check(command, local_hostname, singlestring=False):
    """
    Take a shell command, run it, return a dictionary with indexes output and exit status, if there's a non-zero exit status send a yelp email and exit script WARNING: this version (realtime) will use much more cpu as it constantly polls the running process and thus exit right when the process is done.  Only use this if time is critical and cpu isn't
    :type command: list
    :param command: the command to execute in form of a list Sample1: ['/bin/ls'], Sample2: ['/bin/ls', '-l', '/tmp' ]
    :type local_hostname: str
    :param local_hostname: the hostname of the localmachine
    :param singlestring: is the command beeing passed all one string. If you want to using shell globbing you will need to use this option (Example: ['mv','/var/lib/pgsql/9.1/data/*','/mnt/pgsql'] will not work because of the asterisk, you need to pass a single item list of the string ['mv /var/lib/pgsql/9.1/data/* /mnt/pgsql'] as command and set singlestring to True)

    """

    process_output = runprocess_realtime(command, singlestring=singlestring)
    if process_output['exit_status'] != 0:
        # changed local_hostname['output'][0].strip() to local_hostname this should assume a str
        subject_text="command on %s failed " % local_hostname
        body_text = "Command: %s failed on %s. Command resulted in an exit code of %s.  Output follows\n%s" %(' '.join(command), local_hostname, process_output['exit_status'],''.join(process_output['output']))
        senderror(subject_text, body_text)
        print(body_text)        
        sys.exit(1)
    return process_output


# function to run shell commands results in a dictionary with output and exit status
def runprocess_full(command, singlestring=False, timeout=0):
    """
    Take a shell command, run it, return a dictionary keys for stdout, stderr and exit status
    :type command: list
    :param command: the command to execute in form of a list Sample1: ['/bin/ls'], Sample2: ['/bin/ls', '-l', '/tmp' ]
    :type singlestring: boolean
    :param singlestring: is the command beeing passed all one string. If you want to use shell globbing you will need to use this option (Example: ['mv','/var/lib/pgsql/9.1/data/*','/mnt/pgsql'] will not work because of the asterisk, you need to pass a single item list of the string ['mv /var/lib/pgsql/9.1/data/* /mnt/pgsql'] as command and set singlestring to True)
    :type timeout: int
    :param timeout: is the number of seconds before we should timeout (0 is infinite and also the default)

    """
    # the dictionary we will return
    output_dict = {}
    # insert the command into output_dict
    if isinstance(command, str):
        command_printout = command
    if isinstance(command, list):
        command_printout = ' '.join(command)
    output_dict['command'] = command_printout
    # the actual process making stdout and stderr available
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=singlestring)

    # set our timeout
    if timeout == 0:
        max_loops = float('inf')
    else:
        # divide by 2 because we sleep for 2 seconds at the end of the loop
        max_loops = timeout // 2

    # establish current_number_of_loops
    current_number_of_loops = 0

    # loop that waits for command to finish or timeout is reached
    while(current_number_of_loops <= max_loops):
        exit_status = p.poll() #returns None while subprocess is running
        # process is done once exit_status is not None
        if(exit_status is not None):
            # capture the exit status
            output_dict['exit_status'] = exit_status
            # the list where we will store our output
            stdout_list = []
            # step through and grab the output
            for line in p.stdout:
                stdout_list.append(line)
            # storeout output
            output_dict['stdout'] =  stdout_list

            # the list where we will store our output
            stderr_list = []
            # step through and grab the output
            for line in p.stderr:
                stderr_list.append(str(line))
            # storeout output
            output_dict['stderr'] =  stderr_list

            # timeout 
            output_dict['timeout_reached'] = False

            # return a two key dict with the output and the exit_status 
            return output_dict
        current_number_of_loops += 1
        sleep(2)
    # if we get here that means we reached the timeout
    timeout_message = 'timeout of: %d seconds reached' % timeout
    output_dict['exit_status'] = 666
    output_dict['stderr'] = timeout_message
    output_dict['stdout'] = timeout_message
    output_dict['timeout_reached'] = True
    return(output_dict)



# function to run shell commands results in a dictionary with output and exit status
def runprocess_full_realtime(command, singlestring=False):
    """
    Take a shell command, run it, return a dictionary keys for stdout, stderr and exit status WARNING: this version (realtime) will use much more cpu as it constantly polls the running process and thus exit right when the process is done.  Only use this if time is critical and cpu isn't
    :type command: list
    :param command: the command to execute in form of a list Sample1: ['/bin/ls'], Sample2: ['/bin/ls', '-l', '/tmp' ]
    :type singlestring: boolean
    :param singlestring: is the command beeing passed all one string. If you want to use shell globbing you will need to use this option (Example: ['mv','/var/lib/pgsql/9.1/data/*','/mnt/pgsql'] will not work because of the asterisk, you need to pass a single item list of the string ['mv /var/lib/pgsql/9.1/data/* /mnt/pgsql'] as command and set singlestring to True)

    """
    # the dictionary we will return
    output_dict = {}
    # the actual process making stdout and stderr available
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=singlestring)
    # loop that waits for command to finish
    while(True):
        exit_status = p.poll() #returns None while subprocess is running
        # process is done once exit_status is not None
        if(exit_status is not None):
            # capture the exit status
            output_dict['exit_status'] = exit_status
            # the list where we will store our output
            stdout_list = []
            # step through and grab the output
            for line in p.stdout:
                stdout_list.append(line)
            # storeout output
            output_dict['stdout'] =  stdout_list

            # the list where we will store our output
            stderr_list = []
            # step through and grab the output
            for line in p.stderr:
                stderr_list.append(line)
            # storeout output
            output_dict['stderr'] =  stderr_list

            # return a two key dict with the output and the exit_status 
            return output_dict


def runprocess_full_auto_check(command, local_hostname, singlestring=False, timeout=0):
    """
    Take a shell command, run it, return a dictionary with indexes stdout, stderr and exit_status, if there's a non-zero exit status send a yelp email and exit script
    :type command: list
    :param command: the command to execute in form of a list Sample1: ['/bin/ls'], Sample2: ['/bin/ls', '-l', '/tmp' ]
    :type local_hostname: str
    :param local_hostname: the hostname of the localmachine
    :param singlestring: is the command beeing passed all one string. If you want to using shell globbing you will need to use this option (Example: ['mv','/var/lib/pgsql/9.1/data/*','/mnt/pgsql'] will not work because of the asterisk, you need to pass a single item list of the string ['mv /var/lib/pgsql/9.1/data/* /mnt/pgsql'] as command and set singlestring to True)
    :type timeout: int
    :param timeout: is the number of seconds before we should timeout (0 is infinite and also the default)

    """
    process_output_dict = runprocess_full(command, singlestring=singlestring, timeout=timeout)
    if process_output_dict['exit_status'] != 0:
        subject_text="command on %s failed " % local_hostname
        body_text = "Command: %s failed on %s. Command resulted in an exit code of %s.  Output follows\n\nstdout:\n%s\n\nstderr:\n%s" %(process_output_dict['command'], local_hostname, process_output_dict['exit_status'],process_output_dict['stdout'],process_output_dict['stderr'])
        senderror(subject_text, body_text)
        print(body_text)        
        sys.exit(1)
    return process_output_dict

def runprocess_full_realtime_auto_check(command, local_hostname, singlestring=False):
    """
    Take a shell command, run it, return a dictionary with indexes stdout, stderr and exit_status, if there's a non-zero exit status send a yelp email and exit script WARNING: this version (realtime) will use much more cpu as it constantly polls the running process and thus exit right when the process is done.  Only use this if time is critical and cpu isn't
    :type command: list
    :param command: the command to execute in form of a list Sample1: ['/bin/ls'], Sample2: ['/bin/ls', '-l', '/tmp' ]
    :type local_hostname: str
    :param local_hostname: the hostname of the localmachine
    :param singlestring: is the command beeing passed all one string. If you want to using shell globbing you will need to use this option (Example: ['mv','/var/lib/pgsql/9.1/data/*','/mnt/pgsql'] will not work because of the asterisk, you need to pass a single item list of the string ['mv /var/lib/pgsql/9.1/data/* /mnt/pgsql'] as command and set singlestring to True)

    """
    process_output_dict = runprocess_full_realtime(command, singlestring=singlestring)
    if process_output_dict['exit_status'] != 0:
        subject_text="command on %s failed " % local_hostname
        body_text = "Command: %s failed on %s. Command resulted in an exit code of %s.  Output follows\n\nstdout:\n%s\n\nstderr:\n%s" %(process_output_dict['command'], local_hostname, process_output_dict['exit_status'],process_output_dict['stdout'],process_output_dict['stderr'])
        senderror(subject_text, body_text)
        print(body_text)        
        sys.exit(1)
    return process_output_dict

def get_hostname():
    """Returns a string of the local hostname
    """
    hostname_cmd = 'hostname'
    hostname_cmd_output = runprocess_full(hostname_cmd, singlestring=False)
    hostname = hostname_cmd_output['stdout'][0]
    return hostname

