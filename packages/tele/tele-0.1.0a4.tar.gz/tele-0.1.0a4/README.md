# Tele

**WARNING: This is alpha software. Use at own risk.**

Tele is a library for reporting metrics from PyTorch. You may want to use it
to:

* Print out loss, accuracy, etc every epoch
* Log metrics to a file
* Display samples and graph metrics with a display server

## Usage

### Meters

```python
import tele.meter
```

Meters hold values that you are interested in monitoring. If you're interested
in monitoring or visualising something, it should be put into a meter.

### Outputs

```python
import tele.console    # Print metrics to stdout
import tele.folder     # Write metrics to files
import tele.showoff    # Send metrics to a Showoff server
```

Outputs are destinations for meter values. Examples include text console output,
files on disk, and remote display servers.

An output will typically consist of multiple cells. Each cell displays values
from one or more meter.
