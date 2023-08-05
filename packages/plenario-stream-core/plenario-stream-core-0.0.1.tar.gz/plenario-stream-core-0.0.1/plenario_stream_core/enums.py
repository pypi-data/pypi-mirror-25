from enum import Enum


class JobState(Enum):
    """Represents the different possible states of an ongoing job.

    :attr Queued: job has been submitted to the kinesis stream
    :attr Received: job has been received by a worker
    :attr Error: in handling the job, a worker encountered an error
    :attr Success: job was completed successfully by a worker
    """

    New = 'new'
    Queued = 'queued'
    Received = 'received'
    Error = 'error'
    Success = 'success'

    @classmethod
    def from_string(cls, string: str):
        for item in cls:
            if item.value == string:
                return item
        raise ValueError('{} is not a valid value'.format(string))

    def __str__(self) -> str:
        return self.value
