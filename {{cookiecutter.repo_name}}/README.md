# {{ cookiecutter.project_name }}

## Project structure

- `data`
    - `config`: all configurations
    - `model`: model and feature files
- `{{cookiecutter.project_slug}}`
    - `handlers`: API handlers, based on [Tornado](https://github.com/tornadoweb/tornado) web framework
    - `service`: business services
        - `exception`: exception definitions
    - `util`:
        - constant.py: predefined constants
        - decorators.py
        - paths.py: predefined file paths
    - urls.py: API dispatching configuration of [Tornado](https://github.com/tornadoweb/tornado)
- `tests`: unit tests
- run.py: entrypoint of all services, such as Tornado web service and {{ cookiecutter.project_slug }} service
- settings.py: initializing configuration of service

## References

- [OpenCV VideoCapture](https://docs.opencv.org/2.4/modules/highgui/doc/reading_and_writing_images_and_video.html)
- [Tornado](https://github.com/tornadoweb/tornado)
