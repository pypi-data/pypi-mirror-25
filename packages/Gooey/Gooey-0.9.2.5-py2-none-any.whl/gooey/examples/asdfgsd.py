from __future__ import print_function
from gooey import Gooey, GooeyParser


@Gooey(program_name="Main")
def parse_args():
    parser = GooeyParser()

    subparsers = parser.add_subparsers(help='options', dest='subparser_name')

    a_fields = subparsers.add_parser('a')
    a_fields.add_argument('Links',
                        action='store',
                        default='',
                        widget='FileChooser',
                        help='')

    b_fields = subparsers.add_parser('b')
    b_fields.add_argument('Request_Date',
                        action='store',
                        default='',
                        help='')

    c_fields = subparsers.add_parser('c')
    c_fields.add_argument('Combined_File',
                        action='store',
                        default='',
                        widget='FileChooser',
                        help='')

    args = parser.parse_args()
    return args

if __name__ == '__main__':

    conf = parse_args()

    if conf.subparser_name == 'a':
        print ('Ran A')
    elif conf.subparser_name == 'b':
        print ('Ran B')
    elif conf.subparser_name == 'c':
        print ('Ran C')
