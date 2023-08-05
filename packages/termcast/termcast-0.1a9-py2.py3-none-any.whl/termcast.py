#!/usr/bin/python
"""Script to execute the terminal sharing."""

import io
import os
import sys
import time
import uuid
import json
import argparse
import platform
import traceback
import subprocess

from threading import Thread
from distutils import spawn

import requests
from websocket import create_connection

class Host(object):
    """Stores the host domain"""

    def __init__(self, domain, ssl=True):
        self._ssl = ssl
        self._domain = domain

    def ws(self):
        """Return the host as a websocket reference"""
        return 'ws%s://%s/' % ('s' if self._ssl else '', self._domain)

    def http(self):
        """Return the host as a http reference"""
        return 'http%s://%s/' % ('s' if self._ssl else '', self._domain)


def stream(host, session, fifo, output, tmux_socket):
    """Handle all the bidirectional traffic"""

    #TODO: This should be in a config file.
    buffer_size = 1024

    url = host.ws() + session['id']
    ws = create_connection(url)

    out = open(output, 'w', 1)
    template = ' ' + host.http() + '%s [%d viewing]\n'
    out.write(template % (session['id'], 0))

    def listener():
        """Listen to the few messages we care about coming back down the websocket."""
        while True:
            try:
                received = json.loads(ws.recv())
                if received['type'] == 'viewcount':
                    out.write(template % (session['id'], received['body']))
                if received['type'] == 'snapshot_request':
                    snapshot = subprocess.check_output(['tmux', '-S',
                                                        tmux_socket,
                                                        'capture-pane',
                                                        '-pe']).decode(sys.stdout.encoding)
                    snapshot = snapshot.rstrip('\n').replace('\n', '\r\n')
                    j = json.dumps({'type': 'snapshot',
                                    'token': session['token'],
                                    'body': snapshot,
                                    'target': received['requester'] })
                    ws.send(j)

            except Exception:
                #TODO: Handle exceptions with more nuance.
                out.write('Connection interrupted :(\n')
                traceback.print_exc()
                time.sleep(30)

    listener_thread = Thread(target=listener)
    listener_thread.daemon = True
    listener_thread.start()

    def keep_alive():
        """Websockets just love to die, esp. with ill-configured web servers. Keep small
        volumes of traffic flowing to stay active."""
        while True:
            try:
                ws.send(json.dumps({'type': 'keepAlive'}))
            except Exception:
                #TODO: Handle exceptions with more nuance.
                out.write('Connection interrupted :(\n')
            time.sleep(30)

    keep_alive_thread = Thread(target=keep_alive)
    keep_alive_thread.daemon = True
    keep_alive_thread.start()

    ws.send(json.dumps({'type': 'registerPublisher',
                        'token': session['token'],
                        'body': ''}))

    with io.open(fifo, 'r+b', 0) as typescript_fifo:
        data_to_send = bytearray()
        while True:
            read_data = bytearray(typescript_fifo.read(buffer_size))
            data_to_send += read_data
            if len(read_data) < buffer_size:
                j = json.dumps({'type': 'stream',
                                'token': session['token'],
                                'body': data_to_send.decode('utf-8', 'replace')})
                ws.send(j)
                data_to_send = bytearray()

def system_dependency_is_available(dependency):
    """Checks that a specified dependency is available on this machine."""
    return spawn.find_executable(dependency)

def check_requirements():
    """We need to have a few things installed on the system:
     - tmux
     - script
    """
    assert system_dependency_is_available('tmux')
    assert system_dependency_is_available('script')

def do_the_needful():
    """Main method - parse arguments, generate temp. files, get stuff done."""
    check_requirements()

    parser = argparse.ArgumentParser()
    parser.add_argument('--width', type=int, default=None)
    parser.add_argument('--height', type=int, default=None)
    parser.add_argument('--token', default=None)
    parser.add_argument('--session', default=None)
    args = parser.parse_args()

    unique_id = uuid.uuid4()

    prefix = '/tmp/termcast.'

    fifo = prefix + 'fifo.%s' % unique_id
    tmux_config = prefix + 'tmux_config.%s' % unique_id
    output = prefix + 'output.%s' % unique_id
    tmux_socket = prefix + 'socket.%s' % unique_id

    width, height = args.width, args.height
    if width is None:
        width = subprocess.check_output(['tput', 'cols']).strip().decode(sys.stdout.encoding)
    if height is None:
        height = subprocess.check_output(['tput', 'lines']).strip().decode(sys.stdout.encoding)

    with open(tmux_config, 'w') as tmux_config_file:
        tmux_config_file.write('\n'.join([
            "set-option -g status-left-length 70",
            "set -s escape-time 0",
            "set -g status-left '#(tail -n1 %s)'" % output,
            "set -g status-right ''",
            "set -g status-interval 1",
            "set -g default-terminal 'screen-256color'",
            "set -g force-width %s" % width,
            "set -g force-height %s" % height,
            "set-option -g status-position top",
            "set-window-option -g window-status-current-format ''",
            "set-window-option -g window-status-format ''"]))

    # This gubbins sets up the fifo
    subprocess.call(['mkfifo', fifo])

    # Get the session details
    host = Host('termcast.me', ssl=True)
    if args.session is not None and args.token is not None:
        session = {'id': args.session,
                   'token': args.token,
                   'width': width,
                   'height': height}
    else:
        try:
            session = requests.get(host.http() + 'init?width=%s&height=%s&idGenerator=dictionary'
                                   % (width, height)).json()
        except Exception as e:
            #TODO: Handle this exception with more nuance
            sys.stderr.write('Unable to make HTTP connection to %s :(\n' % host.http())
            traceback.print_exc()
            exit(1)

    stream_thread = Thread(target=stream, args=(host, session, fifo, output, tmux_socket))
    stream_thread.daemon = True
    stream_thread.start()

    if platform.system() == 'Darwin':
        flush = '-F'
    else:
        flush = '-f'

    subprocess.call(['tmux', '-S', tmux_socket, '-2', '-f', tmux_config,
                     'new', 'script', '-q', '-t0', flush, fifo])

    # Tidy up after ourselves.
    for mess in [fifo, tmux_config, output, tmux_socket]:
        os.remove(mess)

    print("You have disconnected from your broadcast session.")
    print("To reconnect, run:")
    print("")
    print("termcast --session %s --token %s --width %s --height %s" % (session['id'], 
                                                                       session['token'],
                                                                       session['width'],
                                                                       session['height']))

if __name__ == "__main__":
    do_the_needful()
