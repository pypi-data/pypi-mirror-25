from __future__ import absolute_import, print_function, unicode_literals

import os
import json
import random
import tempfile
import contextmanager
import apache_beam as beam

from apache_beam.options.pipeline_options import PipelineOptions, SetupOptions
from dojo.runners.job import JobRunner


@contextmanager
def authed(auth):
    with tempfile.NamedTemporaryFile() as auth_file:
        auth_file.write(json.dumps(auth))
        auth_file.flush()
        os.fsync(auth_file.fileno())
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = auth_file.name
        yield


class DirectBeamRunner(JobRunner):

    def run(self, job, config):
        project_id = config['cloud']['project']

        dataset_name = job.config['name'].replace('_', '-')
        '%s--%s-%s' % (project_id, dataset_name, random.randint(1, 1000))

        options = PipelineOptions()
        setup_options = options.view_as(SetupOptions)
        setup_options.save_main_session = True
        setup_options.setup_file = os.path.join(os.getcwd(), 'setup.py')

        job.setup()

        with authed(job.secrets['store']['connection']):
            pipeline = beam.Pipeline(runner=str('direct'), options=options)

            job.run(pipeline)

            result = pipeline.run()
            result.wait_until_finish()
            job.teardown()
