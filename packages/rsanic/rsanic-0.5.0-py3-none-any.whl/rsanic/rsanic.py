#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys
import importlib
import logging
from datetime import date
from datetime import datetime
from sanic import Sanic
from sanic.response import json, html, text
from sanic.exceptions import NotFound
from sanic.log import log
from jinja2 import Environment, FileSystemLoader
from jinja2.bccache import FileSystemBytecodeCache
from markdown import markdown


class Rsanic:

    _routes = {}
    _app = None
    _workers = 1
    _config = {}

    def __init__(self, config=None, routes=None, name=None, error_handler=None, workers=1):
        self._config = config
        self._workers = workers
        print("--")
        print(log.level)
        print(logging.NOTSET)
        print("--")
        if not logging.root.handlers and (log.level == logging.NOTSET):
            formatter = logging.Formatter(
                "%(levelname)s: %(message)s")
            handler = logging.StreamHandler()
            handler.setFormatter(formatter)
            log.addHandler(handler)
            log.setLevel(logging.INFO)
        log.info('\n\t\t>>>>>>>>>>>>>> RSANIC loading... <<<<<<<<<<<<<')

        log.info('Defining sanic app: %s\t', name)
        app = Sanic(name=name, error_handler=error_handler)
        if 'public' in self._config:
            log.info('Adding static folder %s at /public\t', self._config['public'])
            app.static('/public', self._config['public'])

        log.info('Adding routes:',)
        for route in routes:
            url = route[1]
            try:
                return_type = route[3]
                return_type = return_type.lower()
            except (KeyError, IndexError):
                return_type = 'html'
            self._routes[url] = {'controller': route[2], 'return_type': return_type}
            if route[0].__class__ is dict:
                methods = route[0]
            else:
                methods = {route[0]}
            log.info('Methods: %s, URI: %s, Controller: %s, Return Type: %s', methods, route[1], route[2], return_type)
            app.add_route(self.dispatcher, route[1], methods=methods)
        @app.exception(NotFound)
        def ignore_404s(request, exception):
            pass

        self.app = app
        log.info('RSANIC loaded')

    def run(self):
        self.app.run(
            host=self._config['host'],
            port=self._config['port'],
            debug=self._config['debug'],
            workers=self._workers,
            log_config=self._config['logging_config']
        )

    async def dispatcher(self, request, **args):
        sys.path.append(self._config['app_dir'] + '/controllers')
        url_path = request.path
        if 'log_access' in self._config and self._config['log_access']:
            log.info('%s\t%s\t %s', request.ip, datetime.now(), url_path)

        route_data = self.app.router.get(request)
        for key, value in route_data[2].items():
            url_path = url_path.replace(value, '<' + key + '>')
        try:
            handler = self._routes[url_path]
        except KeyError:
            handler = {'controller': self._config['not_found_method'], 'return_type': self._config['default_return_type']}
        try:
            return_type = handler['return_type']
        except KeyError:
            return_type = self._config.default_return_type
        handler_parts = handler['controller'].rsplit(".", 1)
        module_path = handler['controller']
        controller_obj = getattr(importlib.import_module(module_path), handler_parts[1].title())
        controller = controller_obj(config=self._config, request=request)
        await controller.application_global()
        await controller.controller_global()
        controller_response = await controller.invoke(args)
        await controller.close()
        if return_type == 'html':
            return html(await self.html_response(handler, controller_response, 0))
        if return_type == 'md':
            return html(await self.html_response(handler, controller_response, 1))
        elif return_type == 'json':
            return json(controller_response)
        else:
            return text(controller_response)

    async def html_response(self, handler, controller_response, is_markdown):
        file_ext = '.html'
        if is_markdown:
            file_ext = '.md'
        jinja = self.get_jinja()
        jinja.globals['config'] = self._config
        template_path = handler['controller'].replace('.', '/') + file_ext
        template = jinja.get_template(template_path)
        controller_html = template.render(**controller_response)
        if is_markdown:
            controller_html = markdown(controller_html)
        del controller_response['data']
        app_data = controller_response
        app_data['app_content'] = controller_html
        app_template = '_default.html'
        if 'app_template' in controller_response:
            app_template = '_' + controller_response['app_template'] + '.html'
        main_template = jinja.get_template(app_template)

        return main_template.render(**app_data)

    def get_jinja(self):
        bcc = FileSystemBytecodeCache()
        loader = FileSystemLoader(self._config['app_dir'] + '/templates')
        jinja = Environment(bytecode_cache=bcc, loader=loader, autoescape=True, auto_reload=False)
        jinja.filters['date'] = JinjaFilters.date
        jinja.filters['split'] = JinjaFilters.split_space
        jinja.filters['string'] = JinjaFilters.string
        return jinja


class JinjaFilters:
    @staticmethod
    def date(value, format='%y-%m-%d %H:%i:%s'):
        value = date.fromtimestamp(value)
        return value.strftime(format)

    @staticmethod
    def split_space(my_str):
        return my_str.strip().split()

    @staticmethod
    def string(my_str):
        return str(my_str)
