#!/bin/bash

set -e

case "$1" in
    python)
        python "${@:2}"
    ;;
    bash)
        bash
    ;;
    *)
        gunicorn log_processor.wsgi --bind 0.0.0.0:8000 --reload
    ;;
esac
