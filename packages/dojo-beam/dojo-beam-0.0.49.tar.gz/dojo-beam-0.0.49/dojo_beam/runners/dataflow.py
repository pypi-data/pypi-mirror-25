from __future__ import absolute_import, print_function, unicode_literals

import os
import json
import tempfile
import random
import contextmanager
import apache_beam as beam

from apache_beam.options.pipeline_options import PipelineOptions, SetupOptions, \
    GoogleCloudOptions, WorkerOptions
from dojo.runners.job import JobRunner


@contextmanager
def authed(auth):
    with tempfile.NamedTemporaryFile() as auth_file:
        auth_file.write(json.dumps(auth))
        auth_file.flush()
        os.fsync(auth_file.fileno())
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = auth_file.name
        yield


class DataflowBeamRunner(JobRunner):

    def run(self, job, config):
        job.setup()
        project_id = config['cloud']['project']

        dataset_name = job.config['name'].replace('_', '-')
        job_id = '%s--%s-%s' % (project_id, dataset_name, random.randint(1, 1000))

        options = PipelineOptions()
        setup_options = options.view_as(SetupOptions)
        setup_options.save_main_session = True
        setup_options.setup_file = os.path.join(os.getcwd(), 'setup.py')

        if 'cloud' in job.config and 'dataflow' in job.config['cloud']:
            worker_options = options.view_as(WorkerOptions)
            for key, value in job.config['cloud']['dataflow'].items():
                setattr(worker_options, key, value)

        gc_options = options.view_as(GoogleCloudOptions)
        gc_options.project = project_id
        gc_options.job_name = job_id
        gc_options.staging_location = job.store.as_uri(job.output_path('staging'))
        gc_options.temp_location = job.store.as_uri(job.output_path('temp'))

        with authed(job.secrets['store']['connection']):
            pipeline = beam.Pipeline(runner=str('dataflow'), options=options)

            job.run(pipeline)
            result = pipeline.run()
            result.wait_until_finish()
            job.store.teardown()
