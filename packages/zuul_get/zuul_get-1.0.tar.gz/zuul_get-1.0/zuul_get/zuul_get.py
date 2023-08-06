#!/usr/bin/env python
# Copyright 2016, Major Hayden
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""Gets the URLs to monitor a running OpenStack Zuul job."""
import argparse

import requests

from terminaltables import AsciiTable


ZUUL_URLS = {
    '2': 'http://zuul.openstack.org/status.json',
    '3': 'http://zuulv3.openstack.org/status.json'
}


def search_for_job(json_data, review_number):
    """Do a deep search through json for our review's CI jobs."""
    for pipeline in json_data.get('pipelines'):
        for change_queue in pipeline.get('change_queues'):
            for heads in change_queue.get('heads'):
                for job in heads:
                    if job['id'] is not None:
                        review, _ = job['id'].split(',')
                        if review == review_number:
                            return job['jobs']
    return None


def get_jobs(review_number, zuul_version=2):
    """Create a dictionary of jobs."""
    r = requests.get(
        ZUUL_URLS[zuul_version],
        verify=False,
    )
    json_data = r.json()

    job_data = search_for_job(json_data, review_number)

    if job_data is None:
        return None

    return job_data


def job_started(jobdata):
    """Determine if job has started."""
    return jobdata['start_time'] is not None


def job_finished(jobdata):
    """Determine if job has finished."""
    return jobdata['end_time'] is not None


def get_short_url(url):
    """Generate short URL for test results."""
    baseurl = "https://is.gd/create.php"
    params = {
        'format': 'simple',
        'url': url,
    }
    r = requests.post(baseurl, data=params)
    return r.text


def make_table(review_number, running_jobs, args, zuul_version):
    """Create table output."""
    table_header = 'Zuulv{} Jobs for {}'.format(zuul_version, review_number)
    table_data = [[table_header, '']]
    for running_job in running_jobs:

        if not job_started(running_job):
            # Job hasn't started yet
            jobinfo = [
                running_job['name'],
                'Queued',
                ''
            ]
        elif job_started(running_job) and not job_finished(running_job):
            # Job is in progress
            if 'stream.html' in running_job['url']:
                url = (
                    "http://zuulv3.openstack.org/"
                    "{}".format(running_job['url'])
                )
            else:
                url = running_job['url']
            jobinfo = [
                running_job['name'],
                'Running',
                url
            ]
        elif job_finished(running_job):
            # Job is done
            jobinfo = [
                running_job['name'],
                running_job['result'].title()
            ]
            if args.shorten:
                jobinfo.append(get_short_url(running_job['report_url']))
            else:
                jobinfo.append(running_job['report_url'])

        table_data.append(jobinfo)

    table = AsciiTable(table_data)
    print(table.table)


def run():
    """Handle the operations of the script."""
    parser = argparse.ArgumentParser(
        usage='%(prog)s',
        description="Gets URLs to monitor OpenStack Zuul gate jobs",
        epilog='Licensed "Apache 2.0"'
    )
    parser.add_argument(
        'review_number',
        action='store',
        nargs=1,
        help="Gerrit review number (six digits)",
    )
    parser.add_argument(
        '-s', '--shorten',
        action='store_true',
        default=True,
        help="Shorten URLs using is.gd"
    )
    args = parser.parse_args()

    review_number = ''.join(args.review_number)

    for zuul_version in sorted(ZUUL_URLS.keys()):
        running_jobs = get_jobs(review_number, zuul_version)

        if running_jobs is None:
            msg = "Couldn't find any jobs for review {} in Zuulv{}"
            print(msg.format(review_number, zuul_version))
            continue

        make_table(review_number, running_jobs, args, zuul_version)


if __name__ == "__main__":
    run()
