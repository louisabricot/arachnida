import argparse
import sys
import validators

LEVEL_MIN_VAL = 1
LEVEL_MAX_VAL = 100

def url_type(arg):
    """ Type function for argparse - validates the url """ 
    
    validation = validators.url(arg, public=True)
    if validation:
        return arg
    else:
        raise argparse.ArgumentTypeError("Must be a valid url")

def range_limited_int_type(arg):
    """ Type function for argparse - an integer within some predefined bounds """

    try:
        n = integer(arg)
    except ValueError:
        raise argparse.ArgumentTypeError("Must be an integer number")
    if n < LEVEL_MIN_VAL or n > LEVEL_MAX_VAL:
        raise argparse.ArgumentTypeError("Argument must be < " +
        str(LEVEL_MAX_VAL) + "and > " + str(LEVEL_MIN_VAL))
    return n
        
def main():
    parser = argparse.ArgumentParser(
                        description='Extracts images from the provided url',
                        epilog='Developed by louisabricot')
    
    parser.add_argument(
        'url',
        type=url_type,
        help='The website\'s url'
    )
    
    parser.add_argument(
        '--recursive',
        '-r',
        action='store_true',
        required='-l' in sys.argv,
        help='Recursive download'
    )
    
    parser.add_argument(
        '--level',
        '-l',
        type=range_limited_int_type,
        default=5,
        help='The maximum depth level of the recursive download. Default is 5'
    )

    parser.add_argument(
        '-p',
        type=str,
        default='./data/',
        help='The path where the downloaded files will be saved. Default is ./data/'
    )
    
    args = parser.parse_args()
    print('Hello ' + args.url + 'level: ' + repr(args.level), 'data storage ' +
    args.p)

if __name__ == "__main__":
    main()
