#!/usr/bin/env python3

from ring_api import client

if __name__ == "__main__":
    cli = client.Client()
    #cli.start_dring()      # TODO make thread
    cli.start_restserver()
