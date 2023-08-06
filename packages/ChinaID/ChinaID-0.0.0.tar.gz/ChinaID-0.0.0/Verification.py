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


def verification(id_no):
    num = 0
    for i in range(17):
        num += int(id_no[i]) * pow(2, 17 - i, 11)
    r = (12 - num % 11) % 11
    v = 'X' if r == 10 else str(r)
    return True if v == id_no[-1] else False