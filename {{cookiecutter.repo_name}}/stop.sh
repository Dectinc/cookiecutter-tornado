#!/bin/bash
{{ cookiecutter.project_slug|upper }}_DIR="$( cd "$(dirname "$0")" ; pwd -P )"
{{ cookiecutter.project_slug|upper }}_SCRIPT="{% raw %}${{% endraw %}{{ cookiecutter.project_slug|upper }}_DIR}/run.py"

if [ $(ps -ef | grep {% raw %}${{% endraw %}{{ cookiecutter.project_slug|upper }}_SCRIPT} | grep python | wc -l) -eq 0 ]; then
	echo "{{ cookiecutter.project_slug|title }} not started"
else
	echo "{{ cookiecutter.project_slug|title }} stopping..."
	ps -ef | grep {% raw %}${{% endraw %}{{ cookiecutter.project_slug|upper }}_SCRIPT} | grep python | awk '{print $2}' | xargs kill
	[ $(ps -ef | grep {% raw %}${{% endraw %}{{ cookiecutter.project_slug|upper }}_SCRIPT} | grep python | wc -l) -eq 0 ] && echo "{{ cookiecutter.project_slug|title }} stopped"
fi
