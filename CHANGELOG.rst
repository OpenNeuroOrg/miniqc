
.. _changelog-23.1.1:

23.1.1 — 2024-07-23
===================

Changed
-------

- Updated package metadata and test configuration.
- Minor updates to CI.

.. _changelog-23.1.0:

23.1.0 — 2023-06-18
===================

Added
-----

- Accept individual files as inputs.

Changed
-------

- Tweaked Dockerfile for faster build and smaller image.
- Streamline CI configuration, testing multiple Python versions in each
  job.
- Test on Windows, normalize paths to POSIX for reporting.

.. _changelog-23.0.1:

23.0.1 — 2023-06-10
===================

Added
-----

- Build Docker image and push to GHCR

Changed
-------

- Small updates to type annotations.
- Reduced Docker image size.

.. _changelog-23.0.0:

23.0.0 — 2023-03-19
===================

Initial release of miniQC.

Added
-----

- Verify expected file lengths of NIfTI-1/2 images
- Extensible structure for mapping file matches to checks
- BIDS-Apps protocol (output and analysis level optional)
- JSON output to ``stdout``
