#!/bin/bash
ansible-shell dev,prod 'pip install site-discovery -U' | grep -E '(installed|up-to-date|CHANGED)'
