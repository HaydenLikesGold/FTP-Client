# FTP-Client

ftp-client 2.0.0
Published: 13-February-2015

## Introduction
A FTP Python project that follows guidelines from RFC-959. At the start, it was
a class project, but has expanded to have improved design, clarity, and command-line
usage.


## Installation
Nothing all that fancy here, just have python 2.7, clone the repo, and test it out.

## Usage
All you need to provide is the server name, port number, and the path of the file
you wish to retrieve, the ftp-client will do the rest.

Template:
`python ftpclient {server_name} {server_port} {file_path}`

Example Usage:
`python ftpclient ftp.cs.princeton.edu 21 /pub/cs126/nbody/3body.txt`
