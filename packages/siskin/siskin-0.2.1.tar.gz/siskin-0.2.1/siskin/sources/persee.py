# coding: utf-8
# pylint: disable=F0401,C0111,W0232,E1101,R0904,E1103,C0301

# Copyright 2017 by Leipzig University Library, http://ub.uni-leipzig.de
#                   The Finc Authors, http://finc.info
#                   Robert Schenk, <robert.schenk@uni-leipzig.de>
#                   Martin Czygan, <martin.czygan@uni-leipzig.de>
#
# This file is part of some open source application.
#
# Some open source application is free software: you can redistribute
# it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, either
# version 3 of the License, or (at your option) any later version.
#
# Some open source application is distributed in the hope that it will
# be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
#
# @license GPL-3.0+ <http://spdx.org/licenses/GPL-3.0+>

"""
Persee, refs #3133.
"""

import datetime

import luigi
from gluish.intervals import monthly
from gluish.parameter import ClosestDateParameter
from gluish.utils import shellout

from siskin.task import DefaultTask


class PerseeTask(DefaultTask):
    """ Base task. """
    TAG = '39'

    def closest(self):
        return monthly(self.date)


class PerseeCombined(PerseeTask):
    """
    Harvest and combine.
    """
    date = ClosestDateParameter(default=datetime.date.today())

    def run(self):
        output = shellout("""
            metha-sync http://oai.persee.fr/c/ext/prescript/oai &&
            metha-cat http://oai.persee.fr/c/ext/prescript/oai | pigz -c > {output}
        """)
        luigi.LocalTarget(output).move(self.output().path)

    def output(self):
        return luigi.LocalTarget(path=self.path(ext='xml.gz'))


class PerseeMARC(PerseeTask):
    """
    Custom convert to MARC.
    """
    date = ClosestDateParameter(default=datetime.date.today())

    def requires(self):
        return PerseeCombined(date=self.date)

    def run(self):
        output = shellout("""python {script} <(unpigz -c {input}) {output}""",
                          script=self.assets('39/39_marcbinary.py'),
                          input=self.input().path)
        luigi.LocalTarget(output).move(self.output().path)

    def output(self):
        return luigi.LocalTarget(path=self.path(ext='fincmarc.mrc'))

    def on_success(self):
        """
        Signal for manual update. This is decoupled from the task output,
        because it might be deleted, when imported.
        """
        self.output().copy(self.path(ext='fincmarc.mrc.import'))
