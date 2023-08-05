import os
from os import path
from cement.core.controller import CementBaseController, expose
from app.services.mock_service import Mock
from app.services import loader_service
from app.services import generator_service

class GenerateController(CementBaseController):
    class Meta:
        label = 'generate'
        description = 'Generate mock data'
        stacked_on = 'base'
        stacked_type = 'nested'
        arguments = [
            (['-l', '--loader'], {
                'action': 'store',
                'dest': 'loader',
                'help': 'Loader to run source through [postman, swagger]'
            }),
            (['-o', '--output'], {
                'action': 'store',
                'dest': 'output_dir',
                'help': 'Mock data output path'
            }),
            (['-t', '--template'], {
                'action': 'store',
                'dest': 'template_name',
                'help': 'Mock template name'
            }),
            (['-c', '--custom-templates-path'], {
                'action': 'store',
                'dest': 'custom_templates_path',
                'help': 'Path location of custom templates'
            }),
            (['-v', '--verbose'], {
                'action': 'store_true',
                'dest': 'verbose',
                'help': 'Verbose output'
            }),
            (['-d', '--domain'], {
                'action': 'store',
                'dest': 'domain',
                'help': 'Domain override'
            }),
            (['extra_arguments'], {
                'action': 'store',
                'nargs': '*'
            })
        ]

    @expose(hide=True)
    def default(self):
        pargs = self.app.pargs
        loader = 'postman'
        if pargs.loader:
            loader = pargs.loader
        if len(pargs.extra_arguments) <=0:
            exit('Missing source')
        source = pargs.extra_arguments[0]
        output_dir = path.join(os.getcwd(), 'mocks')
        if pargs.output_dir:
            output_dir = path.abspath(path.join(os.getcwd(), pargs.output_dir))
        template_name = ''
        if pargs.template_name:
            template_name = pargs.template_name
        templates_path = path.join(path.dirname(path.realpath(__file__)), '../templates/')
        if pargs.custom_templates_path:
            templates_path = pargs.custom_templates_path
        domain = pargs.domain
        mocks = loader_service.load(loader, source)
        res = generator_service.generate(mocks=mocks, template_name=template_name, output_dir=output_dir, templates_path=templates_path, domain=domain)
        print('Generated ' + res['template_name'] + ' at ' + res['output_path'])
