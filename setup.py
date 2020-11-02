import os
from pathlib import Path
from setuptools import setup
from setuptools.command.install import install
from shutil import copy2
from subprocess import run


class CustomInstallCommand(install):
    def run(self):
        # install systemd service if running with proper permissions
        install.run(self)
        current_dir = Path(os.path.dirname(os.path.realpath(__file__)))
        service1 = current_dir / 'systemd/watch-motion-videos.service'
        service2 = current_dir / 'systemd/clean-motion-videos.service'
        service3 = current_dir / 'systemd/clean-motion-videos.timer'
        try:
            copy2(service1, '/etc/systemd/system')
            copy2(service2, '/etc/systemd/system')
            copy2(service3, '/etc/systemd/system')
            run(['systemctl', 'daemon-reload'], check=True)
        except PermissionError:
            pass


setup(
    name='motionscripts',
    version='0.0.1',
    description='Scripts to manage Motion Project videos',
    packages=['motionscripts'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: POSIX :: Linux'
    ],
    python_requires='>=3.6',
    install_requires=['watchdog'],
    entry_points={
        'console_scripts': [
            'clean-motion-videos=motionscripts.cleanmotionvideos:main',
        ],
    },
    cmdclass={'install': CustomInstallCommand}
)
