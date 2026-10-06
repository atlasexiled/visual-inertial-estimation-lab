# Visual–inertial estimation lab

A hands-on Python study lab progressing from numerical foundations to monocular
visual odometry and camera–IMU estimation. Core algorithms are learning exercises.

**Start with [Week 1](exercises/week01/README.md).** The three function bodies are
intentionally unfinished; their tests define the expected behavior.

## Setup

Activate an existing `.venv` with `source .venv/bin/activate`, or create an
isolated environment using the commands below.

Use Python 3.12 (setup verified with 3.12.3). From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest tests/test_setup.py -q
python -m pytest tests/test_week01.py -q
```

The setup tests should pass. Exercise tests initially fail with
`NotImplementedError`; implement the functions one at a time. Tests run directly
against `src/` through the pytest configuration, so no package installation is
needed yet.

If your shell sources ROS 2, its `PYTHONPATH` also exposes ROS pytest plugins
inside a virtual environment. The pytest configuration disables `launch_testing`
and `launch_ros` for this lab, preventing unrelated ROS imports such as `yaml`
from breaking test discovery. No ROS installation is needed for these exercises.

## Study materials

- [30-week curriculum](docs/curriculum.md)
- [Progress checklist](docs/progress.md)
- [Frame and unit conventions](docs/conventions.md)
- [Week 1 instructions](exercises/week01/README.md)
- [Week 1 implementation](src/vielab/foundations.py)
- [Week 1 report](reports/week01.md)

Ask for hints when stuck, then request a review of your saved implementation.
You implement the algorithms and explain your reasoning in conversation. The
assistant writes and runs tests, documents findings, and updates progress.
Running existing tests yourself is optional; no test writing or Markdown editing
is assigned to you. Advance after the implementation and understanding are verified.
Large datasets and generated experiment outputs stay outside Git.
