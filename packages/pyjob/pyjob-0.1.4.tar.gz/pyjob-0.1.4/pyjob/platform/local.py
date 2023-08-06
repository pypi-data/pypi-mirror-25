# MIT License
#
# Copyright (c) 2017 Felix Simkovic
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Module to store local job management code"""

__author__ = "Felix Simkovic"
__date__ = "09 May 2017"
__version__ = "0.1"

import collections
import logging
import multiprocessing
import random
import time

from pyjob import cexec
from pyjob.platform.platform import LocalPlatform

logger = logging.getLogger(__name__)

SERVER_INDEX = collections.defaultdict(dict)


class Worker(multiprocessing.Process):
    """Simple manual worker class to execute jobs in the queue"""

    def __init__(self, queue, kill_switch, directory=None, permit_nonzero=False):
        """Instantiate a new worker

        Parameters
        ----------
        queue : obj
           An instance of a :obj:`Queue <multiprocessing.Queue>`
        kill_switch : obj
           An instance of a :obj:`Event <multiprocessing.Event>`
        directory : str, optional
           The directory to execute the jobs in
        permit_nonzero : bool, optional
           Allow non-zero return codes [default: False]

        """
        super(Worker, self).__init__()
        self.queue = queue
        self.kill_switch = kill_switch
        self.directory = directory
        self.permit_nonzero = permit_nonzero

    def run(self):
        """Method representing the process's activity"""
        for job in iter(self.queue.get, None):
            if self.kill_switch.is_set():
                continue
            else:
                stdout = cexec([job], directory=self.directory,
                               permit_nonzero=self.permit_nonzero)
                with open(job.rsplit('.', 1)[0] + '.log', 'w') as f_out:
                    f_out.write(stdout)


class LocalJobServer(LocalPlatform):
    """A local server to execute jobs via the multiprocessing module
    
    Examples
    --------

    The most basic example of a :obj:`LocalJobServer` is to run scripts across one or
    more processors on a local machine. This can be achieved with the following example.

    >>> from pyjob.misc import make_python_script
    >>> from pyjob.platform import LocalJobServer
    >>> scripts = [
    ...     make_python_script(["import sys;", "print('hello');", "sys.exit(0);"])
    ...     for _ in range(3)
    ... ]
    >>> LocalJobServer.sub(scripts, nproc=2)

    This will create three Python script files and execute them by calling :func:`sub <LocalJobServer.sub>`.
    
    Sometimes you might want to submit many jobs where you know that some are going to fail. In this 
    case, you can also use the :obj:`LocalJobServer` and provide the ``permit_nonzero`` keyword argument,
    which will allow non-zero return codes from commands.

    """

    @staticmethod
    def kill(jobid):
        """Remove a job from the local process list
        
        Parameters
        ----------
        jobid : int
           The job id to remove
        
        """
        if jobid in SERVER_INDEX:
            SERVER_INDEX[jobid]["kill_switch"].set()
            while any(wk.is_alive() for wk in SERVER_INDEX[jobid]["workers"]):
                continue
            logger.debug("Terminated job %d", jobid)
            SERVER_INDEX.pop(jobid)
        else:
            logger.debug("Job %d not in queue", jobid)

    @staticmethod
    def stat(jobid):
        """Obtain information about a job id
        
        Parameters
        ----------
        jobid : int
           The job id to remove
        
        """
        if jobid in SERVER_INDEX and any(wk.is_alive() for wk in SERVER_INDEX[jobid]["workers"]):
            return {'job_number': jobid, 'status': "Running"}
        else:
            return {}

    @staticmethod
    def sub(command, directory=None, nproc=1, permit_nonzero=False, *args, **kwargs):
        """Submission function for local job submission via ``multiprocessing``
        
        Parameters
        ----------
        command : list
           A list with the final command
        directory : str, optional
           The directory to execute the jobs in
        nproc : int, optional
           The number of processors to use
        permit_nonzero : bool, optional
           Allow non-zero return codes [default: False]
        runtime : int, optional
           The maximum runtime of the job in seconds

        """
        queue = multiprocessing.Queue()
        kill_switch = multiprocessing.Event()
        workers = []
        for _ in range(nproc):
            wp = Worker(queue, kill_switch, directory=directory,
                        permit_nonzero=permit_nonzero)
            wp.start()
            workers.append(wp)
        for cmd in command:
            queue.put(cmd)
        for _ in range(nproc):
            queue.put(None)
        queue.close()
        time.sleep(0.1)
        while True:
            jobid = random.randint(1, 1000)
            if jobid not in SERVER_INDEX:
                break
        SERVER_INDEX[jobid] = {
            "queue": queue,
            "kill_switch": kill_switch,
            "workers": workers
        }
        return jobid
