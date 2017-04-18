# fcsannotate

fcsannotate is a package for annotating FCS files with experimental metadata. It contains an API endpoint for annotating FCS files.

The endpoint currently labels the FCS file with the following keywords:

* flow_cytometer: [name of the cytometer]

* labeled_at: [timestamp generated at time of labelling]

## Usage

~~~~
To run server with the endpoint:

python fcsannotate/fcsannotate.py

PUT /fcs_data/annotate/ [binary FCS file]

The enpoint returns a labeled FCS as binary in the response body.

~~~~

## Tests

~~~~

Unit tests on annotation of FCS files:

python fcsannotate/tests/test_annotate.py

Integration tests of annotation endpoint:

python fcsannotate/tests/test_annotate_endpoint.py

~~~~

## Dependencies

This package relies on Flask and was tested with Python: 2.7.1 (there were issues with fcsparser at Python 3.6.1 and Anaconda).

The package also uses a fork of fcsparser from https://github.com/NotableLabs/fcsparser (uses the write_file functionality). The repo is included as the fcsparser directory because I had to adjust a couple of imports in fcs_parser/__init__.py.
## Contact

Please email me at sutee.dee@alumni.olin.edu with any questions.
