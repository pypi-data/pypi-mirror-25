"""Setup file for handling packaging and distribution."""
from setuptools import setup, find_packages

result_handlers = [
    "db = rotest.core.result.handlers.db_handler:DBHandler",
    "xml = rotest.core.result.handlers.xml_handler:XMLHandler",
    "tags = rotest.core.result.handlers.tags_handler:TagsHandler",
    "excel = rotest.core.result.handlers.excel_handler:ExcelHandler",
    "dots = rotest.core.result.handlers.stream.dots_handler:DotsHandler",
    "tree = rotest.core.result.handlers.stream.tree_handler:TreeHandler",
    "remote = rotest.core.result.handlers.remote_db_handler:RemoteDBHandler",
    "loginfo = rotest.core.result.handlers.stream.log_handler:LogInfoHandler",
    "artifact = rotest.core.result.handlers.artifact_handler:ArtifactHandler",
    "logdebug = "
    "rotest.core.result.handlers.stream.log_handler:LogDebugHandler",
    "signature = "
    "rotest.core.result.handlers.signature_handler:SignatureHandler",
    "full = "
    "rotest.core.result.handlers.stream.stream_handler:EventStreamHandler",
]

setup(
    name='rotest',
    version="2.4.0",
    description="Resource oriented testing framework",
    long_description=open("README.rst").read(),
    license="MIT",
    author="gregoil",
    author_email="gregoil@walla.co.il",
    url="https://github.com/gregoil/rotest",
    keywords="testing system django unittest",
    install_requires=['django>=1.7,<1.8',
                      'ipdb',
                      'ipdbugger>=1.1.0',
                      'lxml',
                      'xlwt',
                      'twisted',
                      'psutil',
                      'colorama',
                      'termcolor',
                      'xmltodict',
                      'jsonschema',
                      'basicstruct'],
    entry_points={"rotest.result_handlers": result_handlers},
    packages=find_packages("src"),
    package_dir={"": "src"},
    package_data={'': ['*.xls', '*.xsd', '*.json', '*.css', '*.xml', '*.rst']},
    zip_safe=False
)
