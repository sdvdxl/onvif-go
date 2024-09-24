#!/usr/bin/env python3

import dataclasses
import pathlib
import re
import subprocess


# license header to use for generated go files
HEADER = '''\
// -*- Mode: Go; indent-tabs-mode: t -*-
//
// Copyright (C) 2022 Intel Corporation
//
// SPDX-License-Identifier: Apache-2.0

// Code generated by gen_commands.py DO NOT EDIT.

'''

BASE_MODULE_NAME = 'github.com/IOTechSystems/onvif'

SERVICE_NAMES = [
    'analytics',
    'device',
    'event',
    'imaging',
    'media',
    'media2',
    'ptz',
    'recording',
    'search',
    'replay',
    "Subscription"
]


@dataclasses.dataclass
class FunctionsGenerator:
    service_name: str
    input_file: pathlib.Path
    output_file: pathlib.Path
    commands = []

    @staticmethod
    def make_function(cmd):
        return '''\
type %sFunction struct{}

func (_ *%sFunction) Request() interface{} {
\treturn &%s{}
}
func (_ *%sFunction) Response() interface{} {
\treturn &%sResponse{}
}

''' % (cmd, cmd, cmd, cmd, cmd)

    def run(self):
        self.commands = []
        with open(self.input_file) as f:
            with open(self.output_file, 'w') as w:
                w.write(HEADER)
                w.write(f'package {self.service_name}\n\n')

                while line := f.readline():
                    if m := re.search(r'type ([^ ]+)Response struct', line):
                        cmd = m.group(1)
                        if cmd.endswith('Fault'):
                            continue  # skip Fault responses
                        self.commands.append(cmd)

                self.commands = sorted(self.commands)
                for cmd in self.commands:
                    print(f'{self.service_name}.{cmd}')
                    w.write(FunctionsGenerator.make_function(cmd))

    def write_func_map(self, w):
        w.write('var %sFunctionMap = map[string]Function{\n' % self.proper_name)
        for cmd in self.commands:
            w.write('\t%s: &%s.%sFunction{},\n' % (cmd, self.service_name, cmd))
        w.write('}\n\n')

    @property
    def proper_name(self):
        return (self.service_name[0].upper() + self.service_name[1:]).replace('Ptz', 'PTZ')


@dataclasses.dataclass
class MainGenerator:
    root_dir: pathlib.Path
    generators = []
    unique_cmds = set()

    def _generate_mappings(self):
        with open(self.root_dir.joinpath('mappings.go'), 'w') as w:
            w.write(HEADER)
            w.write('package onvif\n\n')
            w.write('import (\n')
            for service_name in SERVICE_NAMES:
                w.write(f'\t"{BASE_MODULE_NAME}/{service_name}"\n')
            w.write(')\n\n')

            for generator in self.generators:
                generator.write_func_map(w)

    def _generate_names(self):
        with open(self.root_dir.joinpath('names.go'), 'w') as w:
            w.write(HEADER)
            w.write('package onvif\n\n')
            w.write('// Onvif WebService\n')
            w.write('const (\n')
            for gen in self.generators:
                w.write(f'\t{gen.proper_name}WebService = "{gen.proper_name}"\n')
            w.write(')\n\n')

            for gen in self.generators:
                w.write(f'// WebService - {gen.proper_name}\n')
                w.write('const (\n')
                for cmd in gen.commands:
                    if cmd not in self.unique_cmds:
                        w.write(f'\t{cmd} = "{cmd}"\n')
                    self.unique_cmds.add(cmd)
                w.write(')\n\n')

    def run(self):
        for service_name in SERVICE_NAMES:
            gen = FunctionsGenerator(service_name,
                                     self.root_dir.joinpath(f'{service_name}/types.go'),
                                     self.root_dir.joinpath(f'{service_name}/function.go'))
            gen.run()
            self.generators.append(gen)

        self._generate_mappings()
        self._generate_names()


def main():
    root_dir = pathlib.Path(__file__).parent.parent.resolve()
    main_gen = MainGenerator(root_dir)
    main_gen.run()

    print('\n\nFormatting generated files...')
    try:
        subprocess.check_call(['go', 'fmt', str(root_dir) + "/..."])
    except OSError as e:
        print(f"\n\033[31;1mError occurred while trying to format generated files: {e}\033[0m")
        print("\033[33;1mPlease run 'go fmt ./...' manually to cleanup generated code formatting!\033[0m")


if __name__ == '__main__':
    main()
