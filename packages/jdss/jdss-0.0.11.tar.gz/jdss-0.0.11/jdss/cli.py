import argparse
import os
import json
import glob
import requests
from jdss import SummaryReport


def job(args):
    report = SummaryReport()
    section = report.add_section()
    tabs = section.add_tabs()
    for i in range(0, len(args.tabs)):
        tab_contents = args.tabs[i]
        name = 'tab{}'.format(i + 1) if len(args.names) <= i else args.names[i]
        tab = tabs.add_tab(name)
        for files in [glob.glob(f) for f in tab_contents]:
            for file in files:
                file_name = os.path.splitext(os.path.split(file)[-1])[0]
                file_ext = os.path.splitext(os.path.split(file)[-1])[1].lower()
                if file_ext == '.json':
                    with open(file, 'r') as json_file:
                        contents = json.loads(json_file.read())
                    for key in contents:
                        tab.add_field(key, contents[key])
                elif file_ext in ['.png', '.jpeg', '.jpg']:
                    tab.add_field(file_name, '<![CDATA[<img src="{}"/>]]>'.format(file))
    report.write(args.output)


def jobs(args):
    response = requests.get('{}lastBuild/buildNumber'.format(args.url))
    if response.status_code != 200:
        raise Exception('Not ok response received for latest build number. Check the url and credentials')
    last_build_number = int(response.content.decode())

    builds = []
    artifact_keys = set()
    for build_number in range(max(last_build_number - args.history, 1), last_build_number + 1):
        response = requests.get('{}/{}/artifact/{}'.format(args.url, build_number, args.artifact))
        if response.status_code != 200:
            print('WARN: Artifact was not available for build number {}'.format(build_number))
            continue
        try:
            artifact = json.loads(response.content.decode())
        except:
            print('WARN: Artifact was not valid JSON for build number {}'.format(build_number))
            continue
        artifact_keys.add(*artifact.keys())
        builds.append({'build_number': build_number, 'artifact': artifact})

    report = SummaryReport()
    section = report.add_section()
    table = section.add_table()

    header = table.add_row()
    header.add_cell('build')
    for key in artifact_keys:
        header.add_cell(key)

    for build in builds:
        row = table.add_row()
        row.add_cell(build['build_number'], '{}/{}'.format(args.url, build['build_number']))
        for key in artifact_keys:
            if key not in build['artifact']:
                row.add_cell('-')
            else:
                row.add_cell(build['artifact'][key])

    report.write(args.output)


def main()
    parser = argparse.ArgumentParser()
    sub_parsers = parser.add_subparsers()

    jobs_parser = sub_parsers.add_parser('jobs')
    jobs_parser.add_argument('--url', required=True, help='The url of the build job in Jenkins to summarise')
    jobs_parser.add_argument(
        '--artifact',
        required=True,
        help='The name of the artifact that will be used to populate the metadata about head job. This should be a JSON '
             'file containing a list of key value pairs.'
    )
    jobs_parser.add_argument('--history', type=int, default=50, help='The number of historic builds to summarise')
    jobs_parser.add_argument('--output', required=True, help='The output directory into which the summary report XML file should be written')
    jobs_parser.set_defaults(func=jobs)

    job_parser = sub_parsers.add_parser('job')
    job_parser.add_argument(
        '--tabs',
        action='append',
        default=[],
        nargs='*',
        help='This option can  be used multiple times to specify the content of an individual tab. Multiple values can '
             'be provided, each being a file path that is read. If the file contains XML or JSON, the values are parsed '
             'into a field per property. The assumption here is that the file will contain key value pairs - if the '
             'structure is more complicated, nested objects will be ignored. If the file paths provided are PNG or JPEG '
             'files then these will be included in the tab as images.'
    )
    job_parser.add_argument(
        '--names',
        default=[],
        nargs='*',
        help='A list of names to be used when labelling the tabs whose content is provided in `--tabs`. If no names are '
             'provided then the tabs will be labelled tab1, tab2, etc. If more names are provided than tabs then the '
             'extras will be ignored.'
    )
    job_parser.add_argument('--output', required=True, help='The output directory into which the summary report XML file should be written')
    job_parser.set_defaults(func=job)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
