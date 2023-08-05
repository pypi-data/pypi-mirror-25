from requests import get
import xmltodict

class Update():
    
    template = 'https://dynamicdns.park-your-domain.com/update?host={host}&domain={domain_name}&password={ddns_password}&ip={ip}'
    
    def __init__(self,host, domain_name, password, ip):
        
        self.host = host
        self.domain_name = domain_name
        self.ddns_password = password
        
        self.ip = ip
        self.error = ""
        self.raw_response = ""
        self.formatted_template_to_print_out = ""
        
        
    def update(self):
        
        if not self.host:
            raise ValueError('host cannot be empty')
        if not self.domain_name:
            raise ValueError('domain_name cannot be empty')
        if not self.ddns_password:
            raise ValueError('ddns_password cannot be empty')
        if not self.ip:
            raise ValueError('ip cannot be empty')
        
        uri = self.formatted_template_to_print_out = Update.template.format(host=self.host, domain_name=self.domain_name, ddns_password=self.ddns_password, ip=self.ip)
        result = self.raw_response = get(uri).text
        result = xmltodict.parse(result)
        
        if result['interface-response']['ErrCount'] == "1":
            self.error = result['interface-response']['errors']['Err1']
            return False
        
        return True       
    
    
def myip():
    
    return get('https://ipapi.co/ip/').text