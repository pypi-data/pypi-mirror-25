Module metadata definitions and the modulemd library
====================================================

This repository contains simple module metadata template and the corresponding
library for the manipulation thereof.

`spec.yaml <https://pagure.io/modulemd/blob/master/f/spec.yaml>`_:
        This file serves two roles -- it is the input for tools generating the
        actual module (such as pungi-modularization) and it is also present in
        the resulting repository, available to its consumers (such as
        fm-metadata-service).  For practical reasons, it is written in YAML.
        See comments in the template for details.

modulemd:
        A python library for manipulation of the proposed module metadata format.
        API documentation is available at http://modulemd.readthedocs.org/.
