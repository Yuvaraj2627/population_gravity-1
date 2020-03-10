"""
Process population projection by step for the popultation_gravity model

@author   Chris R. Vernon
@email:   chris.vernon@pnnl.gov

License:  BSD 2-Clause, see LICENSE and DISCLAIMER files

"""

import logging
import os
import time

from population_gravity.downscale_projection import pop_projection


class ProcessStep:
    """Process population downscaling for a single time step

    :param cfg:                 Configuration file object
    :param yr:                  Target year (YYYY) for a time step

    """

    def __init__(self, cfg, yr, alpha_urban, beta_urban, alpha_rural, beta_rural, rural_pop_proj_n, urban_pop_proj_n):

        # start time
        td = time.time()

        logging.info("\tDownscaling year:  {}".format(yr))

        self.cfg = cfg
        self.yr = yr

        if self.yr == self.cfg.projection_start_year:

            # run downscaling
            pop_projection(self.cfg, self.cfg.historical_urban_pop_raster, self.cfg.historical_rural_pop_raster,
                           alpha_urban, beta_urban, alpha_rural, beta_rural, rural_pop_proj_n, urban_pop_proj_n,
                           self.yr)

        else:

            prev_step = self.yr - self.cfg.time_step

            # TODO: switch to read from memory instead of file
            urban_raster = os.path.join(self.cfg.output_directory,
                                        "{}_1km_{}_urban_{}.tif".format(self.cfg.state_name, self.cfg.scenario, prev_step))
            rural_raster = os.path.join(self.cfg.output_directory,
                                        "{}_1km_{}_rural_{}.tif".format(self.cfg.state_name, self.cfg.scenario, prev_step))

            pop_projection(self.cfg, urban_raster, rural_raster, alpha_urban, beta_urban, alpha_rural, beta_rural,
                           rural_pop_proj_n, urban_pop_proj_n, self.yr)

        logging.info("Downscaling for year {} completed in {} minutes.".format(yr, (time.time() - td) / 60))