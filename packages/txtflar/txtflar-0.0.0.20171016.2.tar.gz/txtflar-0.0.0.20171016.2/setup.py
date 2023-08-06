# -*- coding: utf-8 -*-
#
# Copyright (C) 2015 Luis López <luis@cuarentaydos.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301,
# USA.


from setuptools import setup
import txtflar

with open("requirements.txt") as fh:
    pkgs = fh.readlines()

pkgs = [x.strip() for x in pkgs]
pkgs = [x for x in pkgs if x and x[0] != '#']

version = '.'.join([str(x) for x in txtflar.version])

setup(
    name='txtflar',
    version=version,
    author='Luis López',
    author_email='luis@cuarentaydos.com',
    packages=['txtflar'],
    scripts=[],
    url='https://github.com/ldotlopez/txtflar',
    license='LICENSE.txt',
    description=(
        'TeXT file language-aware rename'
        'Automatically rename subtitles (and text files) based on the '
        'language of its contents'
    ),
    long_description=open('README').read(),
    install_requires=pkgs,
)
