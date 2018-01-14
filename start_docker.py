import re
import subprocess
import argparse
import sys

import errno


def parse_terminal_table(text: str):
    patter_header = '([^\s]+\s*)'
    lines = text.splitlines()
    header = lines[0]
    lines = lines[1:]
    header_details = []
    end = 0
    start = end
    while True:
        match = re.match(patter_header, header, re.IGNORECASE)
        if match:
            word = header[0:match.end(0)]
            header = header[match.end(0):]
            end += match.end(0)
            header_details.append({'header': word.strip(), 'start': start, 'end': end})
            start = end
        else:
            break

    rows = []
    for line in lines:
        rows.append({})
        for detail in header_details:
            rows[-1][detail['header']] = line[detail['start']:detail['end']].strip()

    return rows


def extract_docker_machine_info(tabel_line: dict):
    return tabel_line['NAME'], tabel_line['DRIVER']


def check_docker():
    print('Checking docker ...', end='')
    docker_check = subprocess.run(['docker', '-v'], stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
    code = docker_check.returncode
    out = docker_check.stdout.decode(encoding=sys.stdout.encoding).strip()

    if code != 0 or code is None:
        print(' failed')
        print('There is a problem with your docker installation:')
        print(out)

    print(' is installed (' + out + ')')

    return code


def check_docker_machine():
    print('Checking docker-machine ...', end='')
    docker_check = subprocess.run(['docker-machine', '-v'], stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
    code = docker_check.returncode
    out = docker_check.stdout.decode(encoding=sys.stdout.encoding).strip()

    if code != 0 or code is None:
        print(' failed')
        print('There is a problem with your docker-machine installation:')
        print(out)

    print(' is installed (' + out + ')')

    return code


def get_docker_machines():
    print('Find existing docker machines ...', end='')
    docker_machine = subprocess.run(['docker-machine', 'ls'], stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
    code = docker_machine.returncode
    out = docker_machine.stdout.decode(encoding=sys.stdout.encoding)

    if code != 0:
        print(' failed')
        print('There is an error occurred:')
        print(out)
        print('could not go further.')
        machine_list = []
    else:
        machine_list = parse_terminal_table(out)

        if len(machine_list) == 0:
            print(' no machines found')
        else:
            print(' {} machines found:'.format(len(machine_list)))
            for machine in machine_list:
                print('- Machine {} with driver {} (State: {})'
                      .format(machine['NAME'], machine['DRIVER'], machine['STATE']))

    return code, machine_list


def create_docker_machine(driver: str, name: str):
    print('Try to create new docker machine with name {} and driver {}.'.format(name, driver))
    subproc = subprocess.run(['docker-machine', 'create', '-d', driver, name], shell=True)
    code = subproc.returncode

    if code != 0 or code is None:
        print('There was a problem while creating the docker machine {} with driver {}.'.format(name, driver))
    else:
        print('New docker machine created with name ' + name)

    return code


def start_docker_machine(name: str):
    print('Try to start docker machine: {}'.format(name))
    subproc = subprocess.run(['docker-machine', 'start', name], shell=True)
    code = subproc.returncode

    if code != 0:
        print('A problem occurs while starting the machine.')
    else:
        print('Docker machine {} has started.'.format(name))

    return code


def status_docker_machine(name: str):
    print('Checking status of the docker machine {} ...'.format(name), end='')
    docker_check = subprocess.run(['docker-machine', 'status', name], stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
    code = docker_check.returncode
    out = docker_check.stdout.decode(encoding=sys.stdout.encoding).strip()

    if code != 0 or code is None:
        print(' failed')
        print('There is a problem with your docker-machine:')
        print(out)
        stat = None
    else:
        stat = out.strip()
        print(' is {}'.format(stat))

    return code, stat


def get_docker_containers():
    print('Try to find container ...', end='')
    docker_container = subprocess.run(['docker', 'container', 'ls'], stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
    code = docker_container.returncode
    out = docker_container.stdout.decode(encoding=sys.stdout.encoding)

    if code != 0 or code is None:
        print(' failed')
        print('There is an error occurred:')
        print(out)
        container_list = []
    else:
        raise NotImplemented(out)

    return code, container_list


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Start a simple Docker-Container')
    parser.add_argument('-d', '--driver', choices=['virtualbox', 'hyperv'], default="virtualbox")
    parser.add_argument('-f', '--force', action='store_true')
    parser.add_argument('-m', '--machine', action='store', default=None)

    args = parser.parse_args()

    machine_name = args.driver + 'Default' if args.machine is None else args.machine
    machine_driver = args.driver

    dockerImageName = 'homepage'

    exitcode = check_docker()

    if exitcode != 0:
        exit(exitcode)

    exitcode = check_docker_machine()

    if exitcode != 0:
        exit(exitcode)

    # start/create a docker machine
    exitcode, machines = get_docker_machines()

    if exitcode != 0:
        exit(exitcode)

    if len(machines) == 0:
        exitcode = create_docker_machine(args.driver, machine_name)
        if exitcode != 0:
            exit(exitcode)

    else:
        print('Try to find the best docker machine.')

        wanted_name = list(filter(lambda x: x['NAME'] == machine_name, machines))
        wanted_driver = list(filter(lambda x: x['DRIVER'] == machine_driver, machines))

        if args.machine is None:
            if len(wanted_driver) > 0:
                print('Found docker machine with the driver {}.'.format(machine_driver))
                wanted_running = list(filter(lambda x: x['STATE'] == 'Running', wanted_driver))
                if len(wanted_running) == 0:
                    machine_name, machine_driver = extract_docker_machine_info(wanted_driver[0])
                else:
                    machine_name, machine_driver = extract_docker_machine_info(wanted_running[0])
                print('The docker machine with the name {} will used now.'.format(machine_name))
            else:
                print('No docker machine found with a driver {}.'.format(args.driver))
                if args.force:
                    exitcode = create_docker_machine(machine_driver, machine_name)
                    if exitcode != 0:
                        exit(exitcode)

                else:
                    print('Will use another docker machine.')
                    wanted_running = list(filter(lambda x: x['STATE'] == 'Running', machines))
                    if len(wanted_running) == 0:
                        machine_name, machine_driver = extract_docker_machine_info(machines[0])
                    else:
                        machine_name, machine_driver = extract_docker_machine_info(wanted_running[0])
                    print('The docker machine with the name {} will used now.'.format(machine_name))

        else:
            if len(wanted_name) == 1:
                machine_name, machine_driver = extract_docker_machine_info(wanted_name[0])
                print('Docker machine with name {} found.'.format(machine_name))

            elif len(wanted_name) == 0:
                print('No docker machine found with the name {}.'.format(machine_name))
                if args.force:
                    exitcode = create_docker_machine(machine_driver, machine_name)
                    if exitcode != 0:
                        exit(exitcode)

                else:
                    if len(wanted_driver) > 0:
                        print('Found another docker machine with the driver {}.'.format(args.driver))
                        wanted_running = list(filter(lambda x: x['STATE'] == 'Running', wanted_driver))
                        if len(wanted_running) == 0:
                            machine_name, machine_driver = extract_docker_machine_info(wanted_driver[0])
                        else:
                            machine_name, machine_driver = extract_docker_machine_info(wanted_running[0])
                        print('The docker machine with the name {} will used now.'.format(machine_name))
                    else:
                        print('No docker machine found with a driver {}.'.format(args.driver))
                        print('Will use another docker machine.')
                        wanted_running = list(filter(lambda x: x['STATE'] == 'Running', machines))
                        if len(wanted_running) == 0:
                            machine_name, machine_driver = extract_docker_machine_info(machines[0])
                        else:
                            machine_name, machine_driver = extract_docker_machine_info(wanted_running[0])
                        print('The docker machine with the name {} will used now.'.format(machine_name))

            else:
                print('There are more than one machine with the name, don\'t know what to do.')
                exit(errno.ETOOMANYREFS)

    exitcode, status = status_docker_machine(machine_name)

    if exitcode != 0:
        exit(exitcode)

    if status != 'Running':
        exitcode = start_docker_machine(machine_name)
        if exitcode != 0:
            exit(exitcode)

    # start/create docker container
    print(get_docker_containers())
