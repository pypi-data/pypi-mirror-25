import sys
from pathlib import Path

import daiquiri

from scheduler import session


def setup(verbosity):
    log_file = Path(session.folders['solution'], 'scheduler.log')
    try:
        log_file.unlink()
    except FileNotFoundError:
        pass

    daiquiri.setup(
        level='DEBUG',
        outputs=(
            daiquiri.output.Stream(sys.stdout, level=verbosity.upper()),
            daiquiri.output.File(log_file, level='DEBUG'))
    )
