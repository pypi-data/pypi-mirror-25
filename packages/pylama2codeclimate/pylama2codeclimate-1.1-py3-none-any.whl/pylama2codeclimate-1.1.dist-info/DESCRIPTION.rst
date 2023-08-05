pylama2codeclimate
==================

Converts the (parsable) pylama output to codeclimate.json format.
This was written with the intention of using pylama to analyse python programs and report the output to gitlab ci code quality feature:
https://docs.gitlab.com/ee/user/project/merge_requests/code_quality_diff.html

It can be used in a gitlab-ci.yml stage like:

::

    codequality:
      stage: test
      script:
        - pip3 install pylama2codeclimate pylama
        - pylama --format parsable | pylama2codeclimate > codeclimate.json
      artifacts:
        when: always
        paths: [codeclimate.json]


