from .cli import command, arg, optarg_cql, arg_filter, arg_parent, arg_cql, arg_message

cw_command = command.sub_commands('cw')

@cw_command('approve', arg_cql, arg_message
    arg('-n', '--name', help="approval name")
)
def cw_approve(config):
    confluence = config.getConfluenceAPI()

    cql = config['cql']

    for page in confluence.getPages(confluence.resolveCQL(cql)):
        if not config.name:
            result = confluence.cwInfo(page,expand='approvals')
            if len(result['approvals']) > 1:
                names = ", ".join([ a['name'] for a in result['approvals'] ])
                raise RuntimeError("please pass --name with one of %s" % (names,))

            assert len(result['approvals']) == 1

            name = result['approvals']['name']

        else:
            name = config.name

        confluence.cwApprove(page, name=name, message=config.get('message', ''))
        
