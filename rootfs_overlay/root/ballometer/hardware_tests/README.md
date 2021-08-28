# Hardware Tests

The tests in this directory are inteded to be executed on the physical ballometer device.
Their main purpose is to check if all components such as sensors and buttons work as one would roughly expect.

Begin by adding the main ballometer directory to the python path:

```bash
cd /root/ballometer
export PYTHONPATH="$PWD"
```

Then run all the tests with:

```bash
python hardware_tests/test_all.py
```