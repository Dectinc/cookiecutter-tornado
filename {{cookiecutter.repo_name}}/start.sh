#!/bin/bash
echo "{{ cookiecutter.project_slug|title }} starting..."
{{ cookiecutter.project_slug|upper }}_DIR="$( cd "$(dirname "$0")" ; pwd -P )"
PYTHON=$(which python3)
LOG_DIR={% raw %}${{% endraw %}{{ cookiecutter.project_slug|upper }}_DIR}/data/logs
mkdir -p ${LOG_DIR}

if [ -e ${LOG_DIR}/{{ cookiecutter.project_slug }}.log ]; then
    mv ${LOG_DIR}/{{ cookiecutter.project_slug }}.log ${LOG_DIR}/{{ cookiecutter.project_slug }}-`date +'%Y%m%d_%H%M%S'`.log
fi
nohup ${PYTHON} {% raw %}${{% endraw %}{{ cookiecutter.project_slug|upper }}_DIR}/run.py --profile=dev --debug=False --log=warn > ${LOG_DIR}/{{ cookiecutter.project_slug }}.log 2>&1 &
echo "{{ cookiecutter.project_slug|title }} started"
