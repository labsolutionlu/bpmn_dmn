from distutils.core import setup
from setuptools import setup, find_packages

setup(
  name              = 'bpmn_dmn',
  packages          = find_packages(),
  version           = '0.1.2',
  description       = 'A library to execute BPMN Workflows and DMN Decision Tables',
  author            = 'Denny Weinberg',
  author_email      = 'denny.weinberg@labsolution.lu',
  url               = 'https://github.com/labsolutionlu/bpmn_dmn',
  download_url      = 'https://github.com/labsolutionlu/bpmn_dmn/archive/0.1.zip',
  keywords          = ['bpmn', 'dmn', 'camunda'],
  classifiers       = [],
  install_requires  = ['SpiffWorkflow'],
  zip_safe          = True,
)