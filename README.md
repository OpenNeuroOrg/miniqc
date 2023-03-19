# miniqc

[![PyPI - Version](https://img.shields.io/pypi/v/miniqc.svg)](https://pypi.org/project/miniqc)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/miniqc.svg)](https://pypi.org/project/miniqc)

-----

**Table of Contents**

- [Installation](#installation)
- [Usage](#usage)
- [Testing](#testing)
- [License](#license)

## Installation

```console
pip install miniqc
```

## Usage

`miniqc` is a [BIDS-App](https://bids-apps.neuroimaging.io/), so can be run
as follows:

```
miniqc /path/to/dataset /output participant
```

Because miniqc does not currently generate any outputs or modify its behavior
based on analysis level, output directory and analysis level are optional.

This tool is meant as a CLI application and does not provide a public API.

### Example

```console
$ miniqc tests/data/bids_dataset
[
  [
    "sub-01/anat/sub-01_acq-truncated_T2w.nii.gz",
    "FailedCheck",
    "Expected 477 bytes; found 352"
  ],
  [
    "sub-01/anat/sub-01_acq-dangling_T2w.nii.gz",
    "FileNotFoundError",
    "[Errno 2] No such file or directory: 'tests/data/bids_dataset/sub-01/anat/sub-01_acq-dangling_T2w.nii.gz'"
  ]
]
```

### Outputs

The output of this tool is a JSON array of arrays, each of length 3.
The each sub-array contains the failed file (relative to dataset root),
the type of error (`"FailedCheck"` for miniqc-defined failures, or any Python
exceptions raised while checking the file).

## Testing

With the [hatch](https://hatch.pypa.io) project management tool installed:

```console
hatch run test:cov
```

Alternately, just run `pytest`, although you will need the dependencies installed.

## License

`miniqc` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
