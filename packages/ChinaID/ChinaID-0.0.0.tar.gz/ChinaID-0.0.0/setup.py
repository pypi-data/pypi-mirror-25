# Copyright (C) 2017 Pandorym
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from setuptools import setup, find_packages

setup(
    name='ChinaID',
    version='0.0.0',
    description='Verify the Chinese identity card number and obtain the information from it',
    url='https://github.com/Pandorym/ChinaID',

    py_modules=['ChinaID', 'AreaNumber', 'Verification'],

    install_requires=[
        'requests',
        'lxml',
    ],

    author='Pandorym',
    author_email='Pandorym@foxmail.com',
    license='AGPL-3.0',

    packages=find_packages(),
    platforms=['any'],
)
