import re
import json
import argparse
import fileinput


class ParerError(Exception):
    pass

# Example pylama outputs
"""
main.py:22:1: [W] W0611 'logger.domainlogging' imported but unused [pyflakes]
file1.py:58:1: [E] E0602 undefined name 'SetupNamedSized' [pyflakes]
file2.py:149:1: [C] C901 'QueueListener._monitor' is too complex (11) [mccabe]
file2.py:94:1: [W] W0612 local variable 'ret' is assigned to but never used [pyflakes]
"""

parser = re.compile(r'^(?P<path>.*?):(?P<line>\d+?):(?P<column>\d+?): \[(?P<severity>\S)\] (?P<check_name>\S+?) (?P<description>.+) \[(?P<checker>\S+)\]$')


def issue(check_name, description, categories, location,
          content=None, trace=None, remediation_points=None, severity=None, fingerprint=None, engine_name=None):
    """
    CodeClimate Issue: https://github.com/codeclimate/spec/blob/master/SPEC.md#issues
    :param str  check_name: Required. A unique name representing the static analysis check that emitted this issue.
    :param str  description: Required. A string explaining the issue that was detected.
    :param list categories: Required. At least one category indicating the nature of the issue being reported.
    :param dict location: Required. A Location object representing the place in the source code where the issue was discovered.
    :param str  content: Optional. A markdown snippet describing the issue, including deeper
                explanations and links to other resources.
    :param str  trace: Optional. A Trace object representing other interesting source code locations related to this issue.
    :param str  remediation_points: Optional. An integer indicating a rough estimate of how long
                           it would take to resolve the reported issue.
    :param str  severity: Optional. A Severity string (info, minor, major, critical, or blocker)
                 describing the potential impact of the issue found.
    :param str  fingerprint: Optional. A unique, deterministic identifier for the specific issue
                    being reported to allow a user to exclude it from future analyses.
    :param str  engine_name: Optional. name of the code climate engine reporting this result.
    :return: dict
    """
    _issue = {
      "type": "issue",
      "check_name": check_name,
      "description": description,
      "categories": categories,
      "location": location
    }

    for arg in 'content', 'trace', 'remediation_points', 'severity', 'fingerprint', 'engine_name':
        if locals()[arg] is not None:
            _issue[arg] = locals()[arg]

    return _issue


def process(line):
    match = re.match(parser, line)
    if not match:
        raise ParerError("could not parse:%s", line)

    details = match.groupdict()

    positions = dict(
        begin=dict(
            line=int(details['line']),
            column=int(details['column'])
        ),
        end=dict(
            line=int(details['line']),
            column=-1
        )
    )
    lines = dict(
        begin=int(details['line']),
        end=int(details['line'])
    )
    location = dict(path=details['path'].replace('\\', '/'),
                    #positions=positions,
                    lines=lines
                    )

    # info, minor, major, critical, or blocker
    severity = dict(E='major',
                    W='minor').get(details['severity'], 'E')

    _issue = issue(
        check_name=details['check_name'],
        description=details['description'],
        categories=[details['checker']],
        location=location,
        severity=severity,
        engine_name=details['checker']
    )

    return json.dumps(_issue) + ','


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', default='-', help='an integer for the accumulator')
    args = parser.parse_args()
    infile = args.i

    print('[')
    buffer = ''

    for line in fileinput.input(infile):
        if buffer:
            print(buffer)
        buffer = process(line)
    if buffer.endswith(','):
        buffer = buffer[:-1]
    print(buffer)
    print(']')


if __name__ == '__main__':
    main()
