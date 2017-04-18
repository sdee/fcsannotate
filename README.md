# fcsannotate

fcsannotate is a package for annotating FCS files with experimental metadata. It contains an API endpoint for annotating FCS files.

The endpoint currently labels the FCS file with the following keywords:

* flow_cytometer: [name of the cytometer]

* labeled_at: [timestamp generated at time of labelling]

## Usage

~~~~
To run server with the endpoint:

python fcsannotate/fcsannotate.py

PUT http://localhost/fcs_data/annotate/ [binary FCS file]

If successful, the endpoint returns a response with a status 200 and a labeled FCS file as a binary in the response body.

Otherwise, it returns a 404 (file missing in request) or 500 status code (most likely, due to error with FCS format).

~~~~

## Tests

~~~~

Unit tests for annotating FCS files:

**python fcsannotate/tests/test_annotate.py**

**Integration tests of annotation endpoint:**

python fcsannotate/tests/test_annotate_endpoint.py

~~~~

## Dependencies

This package relies on Flask ('0.10.1) and was tested with Python: 2.7.1 (there were issues with fcsparser at Python 3.6.1 and Anaconda).

The package also uses a fork of fcsparser from https://github.com/NotableLabs/fcsparser (uses the write_file functionality).  

I had to adjust a couple of imports in fcs_parser/__init__.py to make it work for me locally:

~~~~
from ._version import version as __version__
from .api import parse
~~~~

## Contact

Please email me at sutee.dee@alumni.olin.edu with any questions.
