###############################################################################
#                                                                             #
#    This program is free software: you can redistribute it and/or modify     #
#    it under the terms of the GNU General Public License as published by     #
#    the Free Software Foundation, either version 3 of the License, or        #
#    (at your option) any later version.                                      #
#                                                                             #
#    This program is distributed in the hope that it will be useful,          #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of           #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            #
#    GNU General Public License for more details.                             #
#                                                                             #
#    You should have received a copy of the GNU General Public License        #
#    along with this program. If not, see <http://www.gnu.org/licenses/>.     #
#                                                                             #
###############################################################################

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import sys
import logging

from biolib.common import (make_sure_path_exists,
                           check_dir_exists,
                           check_file_exists,
                           query_yes_no,
                           remove_extension)


class OptionsParser():
    def __init__(self):
        """Initialization"""
        
        self.logger = logging.getLogger('timestamp')
        self.reporter = logging.getLogger('no_timestamp')

    def draw(self, options):
        """Draw command"""

        check_file_exists(options.assembly_file)
        make_sure_path_exists(options.output_dir)
        
        bin = Bin(options.assembly_file, 
                    options.output_dir,
                    options.min_contig_len,
                    options.cpus)
        bin.check_on_path(options)
        bin.coverage(options.bam_files, options.cov_file)
        bin.run(options)
            
        self.logger.info('Done.')

    def parse_options(self, options):
        """Parse user options and call the correct pipeline(s)"""

        if(options.subparser_name == 'draw'):
            self.draw(options)
        else:
            self.logger.error('Unknown DrawM command: ' + options.subparser_name + '\n')
            sys.exit()

        return 0
