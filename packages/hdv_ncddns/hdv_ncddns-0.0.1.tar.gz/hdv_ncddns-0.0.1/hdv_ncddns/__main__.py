from hdv_ncddns import Update
from colorama import Fore, Style
import argparse

parser = argparse.ArgumentParser(description='Namecheap.com dynamic DNS updater')
parser.add_argument("--config", help="path of configuration python script", type=str)
parser.add_argument("--password", help="Password of dynamic DNS", type=str)
parser.add_argument("--host", help="Subdomain name", type=str)
parser.add_argument("--domain_name", help="Domain name WITHOUT subdomain", type=str)
parser.add_argument("--ip", help="IP address", type=str)
parser.add_argument("-v", '--verbose', nargs='?',const=True, default=False,help="Output detail information")
args = parser.parse_args()

def main():
    
    if args.config:
        config = args.config
        #reset params
        import os.path
#         if not os.path.isfile(config):
#             print('{config} is not a file'.format(config=config))
#             return False
        import importlib.machinery
        params = importlib.machinery.SourceFileLoader('config', config).load_module()
    else:
        params = args
        
    def output(verbose, result):
        
        if not verbose:
            return
        
        import xmltodict
        import json
        
        res = result
        res = json.dumps(xmltodict.parse(res)['interface-response'], indent=4)
        print(Fore.GREEN)
        print('URI: ' + update.formatted_template_to_print_out)
        print(Fore.CYAN)
        print('Response from API:')
        print(res)
        print(Style.RESET_ALL)
        
    try:
        update = Update(
            host=params.host, 
            domain_name=params.domain_name,
            password=params.password, 
            ip=params.ip
            )
        result = update.update()
    except Exception as e:
        print(Fore.RED + 'Error:' +  str(e))
        print(Style.RESET_ALL)
        return False
        
    if not result:
        print(Fore.RED + 'Error from API:' +  update.error)
        print(Style.RESET_ALL)
        output(params.verbose, update.raw_response)
        return False
    
    output(params.verbose, update.raw_response)
    return True
    
if __name__ == '__name__':
    #main()
    pass
    
