from __future__ import absolute_import, print_function, unicode_literals

import os
import json
import tempfile
import subprocess
import contextmanager

from dojo.runners.job import JobRunner


@contextmanager
def authed(auth):
    with tempfile.NamedTemporaryFile() as auth_file:
        auth_file.write(json.dumps(auth))
        auth_file.flush()
        os.fsync(auth_file.fileno())
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = auth_file.name
        yield


class DirectMLEngineRunner(JobRunner):

    def run(self, job, config):
        job.setup()
        with authed(job.secrets['store']['connection']):
            options = []
            for input_key, input_path in job.input_paths().items():
                options += ['--%s_uri' % (input_key, ), job.store.as_uri(input_path)]
            options += ['--output_uri', job.store.as_uri(job.output_path('models'))]
            for key, value in job.config['trainer'].items():
                if key not in ['module', ]:
                    options += ['--%s' % (key, ), str(value)]
            subprocess.check_call([
                'gcloud', 'ml-engine', 'local', 'train',
                '--module-name', job.config['trainer']['module'],
                '--package-path', config['package'],
                '--distributed',
                '--'
            ] + options)
