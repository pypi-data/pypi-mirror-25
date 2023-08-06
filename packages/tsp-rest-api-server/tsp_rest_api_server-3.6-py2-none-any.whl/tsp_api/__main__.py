from optparse import OptionParser

CONFIG_TEMPLATE = """
DOMAIN = {
    'maps': {
        'additional_lookup': {
            'url': 'regex("[\w]+")',
            'field': 'title',
        },
        'schema': {
            'title': {
                'type':'string'
            },
            'routes': {
                'type':'list',
                'schema': {
                    'type':'dict',
                    'schema': {
                        'origin': {'type':'string'},
                        'destiny': {'type':'string'},
                        'distance': {'type':'float'}
                    }
                }
            }
        }
    }

}

MONGO_HOST = %(default_key)r
MONGO_PORT = 27017
MONGO_DBNAME = 'tsp_rest_api_server'

RESOURCE_METHODS = ['GET', 'POST']
XML = False

"""


def generate_settings(parser, options, args):
    output = CONFIG_TEMPLATE % dict(
        default_key='0.0.0.0',
    )

    with open('settings.py', "a+") as a_file:
        a_file.write(output)
        a_file.close()
    return


def runserver(parser, options, args):
    from api import app
    app.debug = True
    app.run()


COMMANDS = {
    'runserver': runserver,
    'settings': generate_settings,
}


def main():
    # Parse options
    parser = OptionParser(usage="Usage: %prog runserver")
    (options, args) = parser.parse_args()

    # Find command
    try:
        command = args[0]
    except IndexError:
        parser.print_help()
        return

    if COMMANDS:
        if command in COMMANDS:
            COMMANDS[command](parser, options, args)
        else:
            parser.error("Unrecognised command: " + command)


if __name__ == '__main__':
    main()
