# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals
#import regex

import configparser
from pprint import pprint
from PyInquirer import style_from_dict, Token, prompt
from PyInquirer import Validator, ValidationError

CONFIG_FILENAME = '/etc/everyedge/config.ini'

# Default settings
DEFAULT_NAT_DISCOVERY_SERVER_IP = '2607:5300:201:3100::6a8f'
DEFAULT_NAT_DISCOVERY_SERVER_PORT = '3478'
DEFAULT_NAT_DISCOVERY_CLIENT_IP = '::'
DEFAULT_NAT_DISCOVERY_CLIENT_PORT = '0'
DEFAULT_PYMERANG_SERVER_IP = '2001:760:4016:1200:5054:ff:fe7f:f5a8'
DEFAULT_PYMERANG_SERVER_PORT = '50061'
DEFAULT_TOKEN_FILE = '/etc/everyedge/token'
DEFAULT_PUBLIC_PREFIX_LENGTH = '128'
DEFAULT_SID_PREFIX = 'fc00::/64'
DEFAULT_DEBUG = False
DEFAULT_VERBOSE = False
DEFAULT_DEVICE_CONFIG_FILE = '/etc/everyedge/device-info.json'
DEFAULT_SB_INTERFACE = 'gRPC'
DEFAULT_GRPC_SERVER_IP = '::'
DEFAULT_GRPC_SERVER_PORT = '12345'
DEFAULT_KEEP_ALIVE_INTERVAL = '5'
DEFAULT_DEFAULT_SECURE = False
DEFAULT_KEY = '/etc/everyedge/key'
DEFAULT_QUAGGA_PASSWORD = 'zebra'
DEFAULT_ZEBRA_PORT = '2601'
DEFAULT_OSPF6D_PORT = '2606'
DEFAULT_ENABLE_PROXY_NDP = True
DEFAULT_FORCE_IP6TNL = False
DEFAULT_FORCE_SRH = True
DEFAULT_INCOMING_SR_TRANSPARENCY = 't0'
DEFAULT_OUTGOING_SR_TRANSPARENCY = 't0'
DEFAULT_ALLOW_REBOOT = True
DEFAULT_TOKEN = ''

style = style_from_dict({
    Token.QuestionMark: '#E91E63 bold',
    Token.Selected: '#673AB7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#2196f3 bold',
    Token.Question: '',
})


# class PhoneNumberValidator(Validator):
#     def validate(self, document):
#         ok = regex.match('^([01]{1})?[-.\s]?\(?(\d{3})\)?[-.\s]?(\d{3})[-.\s]?(\d{4})\s?((?:#|ext\.?\s?|x\.?\s?){1}(?:\d+)?)?$', document.text)
#         if not ok:
#             raise ValidationError(
#                 message='Please enter a valid phone number',
#                 cursor_position=len(document.text))  # Move cursor to end


class NumberValidator(Validator):
    def validate(self, document):
        if document.text == '':
            return
        try:
            int(document.text)
        except ValueError:
            raise ValidationError(
                message='Please enter a number',
                cursor_position=len(document.text))  # Move cursor to end


class PortNumberValidator(Validator):
    def validate(self, document):
        if document.text == '':
            return
        try:
            port = int(document.text)
            if port < 0 or port > 65535:
                raise ValidationError(
                    message='Port Number should be in the range [0, 65535]',
                    cursor_position=len(document.text))  # Move cursor to end
        except ValueError:
            raise ValidationError(
                message='Please enter a valid port number',
                cursor_position=len(document.text))  # Move cursor to end


class PrefixLengthValidator(Validator):
    def validate(self, document):
        if document.text == '':
            return
        try:
            port = int(document.text)
            if port < 0 or port > 65535:
                raise ValidationError(
                    message='Prefix length should be in the range [0, 128]',
                    cursor_position=len(document.text))  # Move cursor to end
        except ValueError:
            raise ValidationError(
                message='Please enter a valid prefix length',
                cursor_position=len(document.text))  # Move cursor to end


print('EveryEdge Configuration Wizard')


questions = [
    {
        'type': 'input',
        'name': 'nat_discovery_server_ip',
        'message': f'Hostname or IP address of a STUN server [{DEFAULT_NAT_DISCOVERY_SERVER_IP}]:',
    },
    {
        'type': 'input',
        'name': 'nat_discovery_server_port',
        'message': f'Port of a STUN server [{DEFAULT_NAT_DISCOVERY_SERVER_PORT}]:',
        'validate': PortNumberValidator,
    },
    {
        'type': 'input',
        'name': 'nat_discovery_client_ip',
        'message': f'Client IP address to use for the STUN test [{DEFAULT_NAT_DISCOVERY_CLIENT_IP}]:',
    },
    {
        'type': 'input',
        'name': 'nat_discovery_client_port',
        'message': f'Client port to use for the STUN test [{DEFAULT_NAT_DISCOVERY_CLIENT_PORT}]:',
        'validate': PortNumberValidator,
    },
    {
        'type': 'input',
        'name': 'pymerang_server_ip',
        'message': f'Hostname or IP address of the EveryWAN controller [{DEFAULT_PYMERANG_SERVER_IP}]:',
    },
    {
        'type': 'input',
        'name': 'pymerang_server_port',
        'message': f'gRPC port of the EveryWAN controller [{DEFAULT_PYMERANG_SERVER_PORT}]:',
        'validate': PortNumberValidator,
    },
    {
        'type': 'input',
        'name': 'token_file',
        'message': f'Path to the EveryEdge token [{DEFAULT_TOKEN_FILE}]:',
    },
    {
        'type': 'input',
        'name': 'public_prefix_length',
        'message': f'Public prefix length [{DEFAULT_PUBLIC_PREFIX_LENGTH}]:',
        'validate': PrefixLengthValidator,
    },
    {
        'type': 'input',
        'name': 'sid_prefix',
        'message': f'SID Prefix [{DEFAULT_SID_PREFIX}]:',
    },
    {
        'type': 'confirm',
        'name': 'debug',
        'message': 'Debug mode [yes]' if DEFAULT_DEBUG else 'Debug mode [no]',
        'default': DEFAULT_DEBUG,
    },
    {
        'type': 'confirm',
        'name': 'verbose',
        'message': 'Verbose mode [yes]' if DEFAULT_VERBOSE else 'Verbose mode [no]',
        'default': DEFAULT_VERBOSE,
    },
    {
        'type': 'input',
        'name': 'device_config_file',
        'message': f'Path to the JSON configuration file of the device [{DEFAULT_DEVICE_CONFIG_FILE}]:',
    },
    {
        'type': 'input',
        'name': 'sb_interface',
        'message': f'Southbound Interface to use to interact with the controller [{DEFAULT_SB_INTERFACE}]:',
    },
    {
        'type': 'input',
        'name': 'grpc_server_ip',
        'message': f'gRPC server IP address [{DEFAULT_GRPC_SERVER_IP}]:',
    },
    {
        'type': 'input',
        'name': 'grpc_server_port',
        'message': f'gRPC server port [{DEFAULT_GRPC_SERVER_PORT}]:',
        'validate': PortNumberValidator,
    },
    {
        'type': 'input',
        'name': 'keep_alive_interval',
        'message': f'Interval between two consecutive keep alive messages [{DEFAULT_KEEP_ALIVE_INTERVAL}]:',
        'validate': NumberValidator,
    },
    {
        'type': 'confirm',
        'name': 'secure',
        'message': f'Enable gRPC secure mode? [{DEFAULT_DEFAULT_SECURE}]:',
        'default': False,
    },
    {
        'type': 'input',
        'name': 'key',
        'message': f'Path to the TLS key [{DEFAULT_KEY}]:',
    },
    {
        'type': 'input',
        'name': 'quagga_password',
        'message': f'FRR password [{DEFAULT_QUAGGA_PASSWORD}]:',
    },
    {
        'type': 'input',
        'name': 'zebra_port',
        'message': f'zebra port [{DEFAULT_ZEBRA_PORT}]:',
        'validate': PortNumberValidator,
    },
    {
        'type': 'input',
        'name': 'ospf6d_port',
        'message': f'ospf6d port [{DEFAULT_OSPF6D_PORT}]:',
        'validate': PortNumberValidator,
    },    
    {
        'type': 'confirm',
        'name': 'enable_proxy_ndp',
        'message': 'Enable proxy NDP? [yes]' if DEFAULT_ENABLE_PROXY_NDP else 'Enable proxy NDP? [no]',
        'default': True,
    },
    {
        'type': 'confirm',
        'name': 'force_ip6tnl',
        'message': 'Force ip6 tunnels? [yes]' if DEFAULT_FORCE_IP6TNL else 'Force ip6 tunnels? [no]',
        'default': False,
    },
    {
        'type': 'confirm',
        'name': 'force_srh',
        'message': 'Force SRH [yes]' if DEFAULT_FORCE_SRH else 'Force SRH? [no]',
        'default': False,
    },
    {
        'type': 'list',
        'name': 'incoming-sr-transparency',
        'message': f'Incoming SR Transparency:',
        'choices': ['t0', 't1', 'op'],
        'default': 0,
    },
    {
        'type': 'list',
        'name': 'outgoing-sr-transparency',
        'message': f'Outgoing SR Transparency:',
        'choices': ['t0', 't1', 'op'],
        'default': 0,
    },
    {
        'type': 'confirm',
        'name': 'allow-reboot',
        'message': 'Allow reboot? [yes]' if DEFAULT_ALLOW_REBOOT else 'Allow reboot? [no]',
        'default': DEFAULT_ALLOW_REBOOT,
    },
    {
        'type': 'input',
        'name': 'token',
        'message': f'Token:'
    }
]

answers = prompt(questions, style=style)

print('Resolving defaults')
if answers['nat_discovery_server_ip'] == '':
    answers['nat_discovery_server_ip'] = DEFAULT_NAT_DISCOVERY_SERVER_IP
if answers['nat_discovery_server_port'] == '':
    answers['nat_discovery_server_port'] = DEFAULT_NAT_DISCOVERY_SERVER_PORT
if answers['nat_discovery_client_ip'] == '':
    answers['nat_discovery_client_ip'] = DEFAULT_NAT_DISCOVERY_CLIENT_IP
if answers['nat_discovery_client_port'] == '':
    answers['nat_discovery_client_port'] = DEFAULT_NAT_DISCOVERY_CLIENT_PORT
if answers['pymerang_server_ip'] == '':
    answers['pymerang_server_ip'] = DEFAULT_PYMERANG_SERVER_IP
if answers['pymerang_server_port'] == '':
    answers['pymerang_server_port'] = DEFAULT_PYMERANG_SERVER_PORT
if answers['token_file'] == '':
    answers['token_file'] = DEFAULT_TOKEN_FILE
if answers['public_prefix_length'] == '':
    answers['public_prefix_length'] = DEFAULT_PUBLIC_PREFIX_LENGTH
if answers['sid_prefix'] == '':
    answers['sid_prefix'] = DEFAULT_SID_PREFIX
if answers['device_config_file'] == '':
    answers['device_config_file'] = DEFAULT_DEVICE_CONFIG_FILE
if answers['sb_interface'] == '':
    answers['sb_interface'] = DEFAULT_SB_INTERFACE
if answers['grpc_server_ip'] == '':
    answers['grpc_server_ip'] = DEFAULT_GRPC_SERVER_IP
if answers['grpc_server_port'] == '':
    answers['grpc_server_port'] = DEFAULT_GRPC_SERVER_PORT
if answers['keep_alive_interval'] == '':
    answers['keep_alive_interval'] = DEFAULT_KEEP_ALIVE_INTERVAL
if answers['key'] == '':
    answers['key'] = DEFAULT_KEY
if answers['quagga_password'] == '':
    answers['quagga_password'] = DEFAULT_QUAGGA_PASSWORD
if answers['zebra_port'] == '':
    answers['zebra_port'] = DEFAULT_ZEBRA_PORT
if answers['ospf6d_port'] == '':
    answers['ospf6d_port'] = DEFAULT_OSPF6D_PORT
if answers['incoming-sr-transparency'] == '':
    answers['incoming-sr-transparency'] = DEFAULT_INCOMING_SR_TRANSPARENCY
if answers['outgoing-sr-transparency'] == '':
    answers['outgoing-sr-transparency'] = DEFAULT_OUTGOING_SR_TRANSPARENCY

# Remove token from the configuration
token = answers.pop('token')

# Save the token to a separate file
print('Saving the token to %s:' % answers['token_file'])
TOKEN_FILENAME = answers['token_file']
with open(TOKEN_FILENAME, 'w') as tokenfile:
  tokenfile.write(token)


print('Generating configuration:')
pprint(answers)
config = configparser.ConfigParser()
config['DEFAULT'] = answers

print('Saving configuration to file %s' % CONFIG_FILENAME)
with open(CONFIG_FILENAME, 'w') as configfile:
  config.write(configfile)
