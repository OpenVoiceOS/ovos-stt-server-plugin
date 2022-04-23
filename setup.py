#!/usr/bin/env python3
from setuptools import setup


PLUGIN_ENTRY_POINT = (
    'ovos-stt-plugin-server = ovos_stt_plugin_server:OVOSHTTPServerSTT',
    'ovos-stt-plugin-server-streaming = ovos_stt_plugin_server:OVOSHTTPStreamServerSTT'
)

setup(
    name='ovos-stt-plugin-server',
    version='0.0.2a1',
    description='ovos stt server plugin for mycroft',
    url='https://github.com/OpenVoiceOS/ovos-stt-server-plugin',
    author='JarbasAi',
    author_email='jarbasai@mailfence.com',
    license='Apache-2.0',
    packages=['ovos_stt_plugin_server'],
    install_requires=['ovos-plugin-manager'],
    zip_safe=True,
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Text Processing :: Linguistic',
        'License :: OSI Approved :: Apache Software License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='mycroft OpenVoiceOS OVOS plugin stt',
    entry_points={'mycroft.plugin.stt': PLUGIN_ENTRY_POINT}
)
