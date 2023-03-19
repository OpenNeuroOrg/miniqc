import json

import pytest
from typer.testing import CliRunner

from miniqc.__main__ import app

runner = CliRunner()


@pytest.mark.parametrize('allow_dangling', (True, False))
def test_app(example_dataset, allow_dangling):
    args = ['-l', str(example_dataset)]
    if not allow_dangling:
        args = args[1:]

    result = runner.invoke(app, args)

    assert result.exit_code == 1
    errors = json.loads(result.stdout)
    assert len(errors) == 1 if allow_dangling else 2
    assert [
        'sub-01/anat/sub-01_acq-truncated_T2w.nii.gz',
        'FailedCheck',
        'Expected 477 bytes; found 352',
    ] in errors

    if not allow_dangling:
        assert any([err[1] == 'FileNotFoundError' for err in errors])
