Table of Contents
_________________

1 HPCLI
.. 1.1 CLI Usage
.. 1.2 SDK Usage
.. 1.3 Workflow


1 HPCLI
=======

  A command-line tool and SDK for highlyprobable.com


1.1 CLI Usage
~~~~~~~~~~~~~

  ,----
  | ➜  foobar hpcli --help
  | HighlyProbable-cli.
  | 
  | Usage:
  |   hpcli login
  |   hpcli create-account
  |   hpcli create-project [<template-type>] [<project-name>]
  |   hpcli config-project (<project-name>)
  |   hpcli run [<project-name>] [<custom-docker-image>] [--use-remote=<use-remote>]
  |   hpcli remote deploy [<project-name>]
  |   hpcli remote upload [<project-name>]
  |   hpcli remote create [<project-name>]
  |   hpcli remote start [<project-name>]
  |   hpcli remote stop [<project-name>]
  |   hpcli remote ping [<project-name>]
  | 
  | Options:
  |   -h --help     Show this screen.
  |   --use-remote=<use-remote>  Use a remote url for the code source eg: s3://foo.bar.baz [default: None]
  | 
  | Templates:
  | - python3-generic
  `----


1.2 SDK Usage
~~~~~~~~~~~~~

  ,----
  | from hpcli.sdk.base import API as HP
  | 
  | input_data = {"text": "Hello world!"}
  | hp = HP('ab758a/detect-language', api_key='your_api_key').post(input_data)
  | # hp: ['en', -23.71974611282348]
  `----


1.3 Workflow
~~~~~~~~~~~~

  1. Create a project:
  `hpcli create-project`
  1. Run the project:
  `hpcli run $project-name`
