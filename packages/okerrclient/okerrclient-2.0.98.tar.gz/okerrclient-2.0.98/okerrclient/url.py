import okerrclient.taskseq as ts
import requests

class UrlTaskProcessor(ts.TaskProcessor):
    chapter = 'URL operations'

class GetUrl(UrlTaskProcessor):
    help = 'get HTTP document'
    
    
    tpconf={
        'url': []
    }
    
    # store_argline='n'
    # parse_args=False

    defargs = {
        'url':'', 
        'redirect': '1',
        'verify': '1',
        'user': '',
        'pass': '',
        }
    
    def validate_url(self, url):
        
        if '*' in self.tpconf['url']:
            return True
        
        for prefix in self.tpconf['url']:
            if url.startswith(prefix):
                return True
        
        return False
        
    def run(self,ts,data,args):
        out = dict()

        url = args['url']
        
        
        if not self.validate_url(url):
            ts.stop()
            return None
            
        if args['redirect'] == '1':
            redir = True
        else:
            redir = False

        if args['verify'] == '1':
            verify = True
        else:
            verify = False

        if args['user'] and args['pass']:
            auth = (args['user'], args['pass'])
        else:
            auth = None

        try:        
            r = requests.get(url, allow_redirects=redir, verify=verify, auth=auth, timeout=5)        
        except requests.exceptions.RequestException as e:
            ts.oc.log.error('GETURL exception {} {}'.format(type(e), str(e)))
            ts.stop()
            return None 
            
        
        for field in ['status_code', 'text']:
            out[field] = getattr(r,field, None)
        
        for header in r.headers:
            out['h_'+header] = r.headers[header]
        
        return out
        
GetUrl('GETURL',ts.TaskSeq)            

