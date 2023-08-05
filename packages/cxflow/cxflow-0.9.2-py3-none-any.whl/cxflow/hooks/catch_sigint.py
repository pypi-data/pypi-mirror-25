"""
Module with the SigintHook which allows to stop the training properly when a sigint is caught.
"""
import logging
import signal

from . import AbstractHook, TrainingTerminated


class CatchSigint(AbstractHook):
    """
    Catch SIGINT signals allowing to stop the training with grace.

    On first sigint finish the current batch and terminate training politely, i.e. trigger all ``after_training`` hooks.
    On second sigint quit immediately with exit code 1


    .. code-block:: yaml
        :caption: register SIGINT catching

        hooks:
          - CatchSigint

    """

    def __init__(self, **kwargs):
        """
        Create new CatchSigint hook.

        :param kwargs: additional ``**kwargs`` are ignored
        """
        super().__init__(**kwargs)

        self._num_sigints = 0
        self._original_handler = None

    def _sigint_handler(self, signum, _) -> None:
        """
        On the first signal, increase the ``self_num_sigints`` counter.
        Quit on any subsequent signal.

        :param signum: SIGINT signal number
        """
        if self._num_sigints > 0:  # not the first sigint
            logging.error('Another SIGINT %s caught - terminating program immediately', signum)
            quit(1)
        else:  # first sigint
            logging.warning('SIGINT %s caught - terminating after the following batch.', signum)
            self._num_sigints += 1

    def before_training(self) -> None:
        """Register the SIGINT signal handler."""
        self._original_handler = signal.getsignal(signal.SIGINT)
        signal.signal(signal.SIGINT, self._sigint_handler)
        self._num_sigints = 0

    def after_batch(self, **_) -> None:
        """
        Stop the training if SIGINT signal was caught

        :raise TrainingTerminated: if an SIGINT signal was caught
        """
        if self._num_sigints > 0:
            logging.warning('Terminating because SIGINT was caught during last batch processing.')
            raise TrainingTerminated('SIGINT caught')

    def after_training(self) -> None:
        """Switch to the original signal handler."""
        signal.signal(signal.SIGINT, self._original_handler)
