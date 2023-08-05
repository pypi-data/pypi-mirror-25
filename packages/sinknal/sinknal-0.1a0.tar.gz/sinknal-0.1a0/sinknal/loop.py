from tornado.web import RequestHandler, Application
from tornado.ioloop import IOLoop
from multiprocessing import Queue
from Queue import Empty
from subprocess import Popen, PIPE
import re


queue = Queue()
remotes = []
regexes = []
keyfiles = []


class SyncHandler(RequestHandler):
    def post(self):
        ip = self.request.remote_ip

        if ip != '::1' and ip != '127.0.0.1':
            self.write('wot')
            return
        
        path = self.get_body_argument('path', None)

        for rgx in regexes:
            if rgx and not rgx.match(path):
                self.write('wrong path')
                return

        queue.put(path)
        self.write('ok')


def process_queue():
    loop = IOLoop.current()
    try:
        path = queue.get(timeout=1)
        remote = '{0}:{1}'.format(remotes[0], path)
        params = ['rsync', '-av']

        if keyfiles:
            ssh_spec = 'ssh -i "{0}"'.format(keyfiles[0])
            params.append('-e')
            params.append(ssh_spec)

        params.append(path)
        params.append(remote)

        p = Popen(params, stdout=PIPE, stderr=PIPE)
        o, e = p.communicate()
        print(o, e)
    except Empty:
        pass

    loop.add_timeout(1, process_queue)

def mainloop(port=47821, remote=None, regex=None,
             keyfile=None, **kwargs):
    remotes.append(remote)
    regexes.append(regex)
    if keyfile: keyfiles.append(keyfile)
    urls = [(r'/sync', SyncHandler, )]
    app = Application(urls)
    app.listen(port)
    loop = IOLoop.current()
    loop.add_timeout(1, process_queue)
    loop.start()


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', type=int, default=47821, dest='port')
    parser.add_argument('-r', dest='remote', required=True)
    parser.add_argument('-i', dest='keyfile')
    parser.add_argument('-g', dest='regex', type=re.compile,
                        required=True)
    args = parser.parse_args()

    mainloop(port=args.port, remote=args.remote,
             regex=args.regex, keyfile=args.keyfile,
             )


