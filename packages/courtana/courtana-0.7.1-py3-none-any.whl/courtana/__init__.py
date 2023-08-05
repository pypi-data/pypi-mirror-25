# import logging

from .experiment import Experiment

# FIXME should load config from a file and have different
# levels for DEV and PROD
#
# NEVER basicConfig() IN A LIBRARY!!!
#
# logging.basicConfig(
#     level=logging.DEBUG,
#     format='%(levelname)-8s %(name)-24s %(message)s',
# )

__all__ = ['GENDER_COLOR', 'Experiment']
__version__ = '0.7.1'


GENDER_COLOR = {'f': '#dd1c77', 'm': '#3182bd'}
