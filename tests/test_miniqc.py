import json
from pathlib import Path

import pytest
from typer.testing import CliRunner

from miniqc.__main__ import app

runner = CliRunner()


@pytest.mark.parametrize('allow_dangling', (True, False))
def test_app(example_dataset: Path, allow_dangling: bool) -> None:
    args = ['-l', str(example_dataset)]
    if not allow_dangling:
        args = args[1:]

    result = runner.invoke(app, args)

    assert result.exit_code == 1
    errors: list[list[str]] = json.loads(result.stdout)
    assert len(errors) == 1 if allow_dangling else 2
    assert [
        'sub-01/anat/sub-01_acq-truncated_T2w.nii.gz',
        'FailedCheck',
        'Expected 477 bytes; found 352',
    ] in errors

    if not allow_dangling:
        assert any([err[1] == 'FileNotFoundError' for err in errors])


@pytest.mark.parametrize(
    'file, allow_dangling, exit_code',
    (
        ('sub-01_acq-good_T1w.nii.gz', False, 0),
        ('sub-01_acq-truncated_T2w.nii.gz', False, 1),
        ('sub-01_acq-dangling_T2w.nii.gz', False, 1),
        ('sub-01_acq-dangling_T2w.nii.gz', True, 0),
    ),
)
def test_single_file(
    example_dataset: Path,
    file: str,
    allow_dangling: bool,
    exit_code: bool,
) -> None:
    args = ['-l', str(example_dataset / 'sub-01' / 'anat' / file)]
    if not allow_dangling:
        args = args[1:]

    result = runner.invoke(app, args)

    assert result.exit_code == exit_code
    errors: list[list[str]] = json.loads(result.stdout)
    assert len(errors) == exit_code
