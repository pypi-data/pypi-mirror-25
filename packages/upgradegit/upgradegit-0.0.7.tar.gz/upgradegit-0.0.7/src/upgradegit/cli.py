import click
import requirements
import os
import re


@click.command()
@click.option('--file', default='requirements.txt', help='File to upgrade')
@click.option('--branch', default='master', help='Branch to upgrade from')
def upgrade(file, branch):
    lines = []
    with open(file, 'r') as f:
        for req in requirements.parse(f):
            line = ''
            if (req.uri):
                reg = r'([0-9a-z]*)(?=(\s+refs\/heads\/'+branch+'))'
                uri = req.uri.replace('git+ssh://', 'ssh://git@')
                cmd = 'git ls-remote {} {} HEAD'.format(uri, branch)
                result = os.popen(cmd).read()
                result = result.strip()
                results = re.findall(reg, result)
                result = results[0][0]
                print('Setting {} to hash: {}'.format(req.uri, result))
                line = re.sub(r'\.git.*?(?=(#|$))', '.git@'+result, req.line)

            else:
                name = req.name
                spec_op = req.specs[0][0]
                spec_ver = req.specs[0][1]
                line = '{name}{spec_op}{spec_ver}'.format(
                    name=name, spec_op=spec_op, spec_ver=spec_ver)

            lines.append(line)

    with open(file, 'w') as f:
        for line in lines:
            f.write(line+'\n')


if __name__ == '__main__':
    upgrade()
