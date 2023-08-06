#Author: Partha
import sys
import tornado.ioloop
import tornado.web
import sockjs.tornado
import json

class BaseHandler(tornado.web.RequestHandler):

    def get(self):
        if self.request.path.endswith("/read/"):
            return self.read()

    def post(self):
        self.user = self.get_argument('user', None)
        count = self.get_argument('count', 0)
        try:
            data = self.get_argument('data', None)
        except:
            data = json.loads(self.get_argument('data', None))

        if self.request.path.endswith("/read/"):
            return self.read(data, count)
        if self.request.path.endswith("/unread/"):
            return self.unread(data, count)
        if self.request.path.endswith("/deleted/"):
            return self.deleted(data, count)

    def send(self):
        if self.user is not None:
            for tab in MessageConnection.tabs[self.user]:
                tab.send(self.payload)
            self.finish()
        
    
class ProcessNotify(BaseHandler):

    def read(self, data, count):
        self.payload = {
            'count':count,
            'node': 'PROCESS',
            'action':'READ',
            'data': json.loads(data)
        }
        return self.send()

    def unread(self, data, count):
        self.payload = {
            'count':count,
            'node': 'PROCESS',
            'action':'UNREAD',
            'data': json.loads(data)
        }
        return self.send()
        

    def deleted(self, data, count):
        self.payload = {
            'count':count,
            'node': 'PROCESS',
            'action':'DELETED',
            'data': json.loads(data)
        }
        return self.send()
        

class MessageNotify(BaseHandler):
    
    def read(self, data, count):
        self.payload = {
            'count':count,
            'node': 'MESSAGE',
            'action':'READ',
            'data': json.loads(data)
        }
        return self.send()

    def unread(self, data, count):
        self.payload = {
            'count':count,
            'node': 'MESSAGE',
            'action':'UNREAD',
            'data': json.loads(data)
        }
        return self.send()
        

    def deleted(self, data, count):
        self.payload = {
            'count':count,
            'node': 'MESSAGE',
            'action':'DELETED',
            'data': json.loads(data)
        }
        return self.send()


class Backdoor(BaseHandler):

    def read(self, *args, **kwargs):
        
        return None

    def write(self, *args, **kwargs):
        import pdb;pdb.set_trace()


class MessageConnection(sockjs.tornado.SockJSConnection):
    """ Wrapping the Data with Connection """

    tabs = {
        
    }

    def on_message(self, user):
        """ Storing the object with username together """
        try:
            data = json.loads(user)
            print data
            if data.get('type', None) == 'position':
                if getattr(self, 'tabdata', None) is None:
                    self.tabdata = []
                self.tabdata.append({'x':data['x'], 'y':data['y']})
                print data['x'], data['y']

                if data['user'] is not None:
                    for tab in MessageConnection.tabs[data['user']]:
                        tab.send(data)
                    self.finish()
            if data.get('type', None) == 'click':
                # import pdb;pdb.set_trace()
                if getattr(self, 'tabdata', None) is None:
                    self.tabdata = []
                self.tabdata.append({'x':data['x'], 'y':data['y'], 'ele':data['ele']})
                print data['x'], data['y'], 

                if data['user'] is not None:
                    for tab in MessageConnection.tabs[data['user']]:
                        tab.send(data)
                    self.finish()
            if data.get('type', None) == 'html':
                if getattr(self, 'tabdata', None) is None:
                    self.tabdata = []
                self.tabdata.append({'html':data['html']})

                if data['user'] is not None:
                    for tab in MessageConnection.tabs[data['user']]:
                        tab.send(data)
                    self.finish()
        except:
            print "Connected User:", user
            if user not in self.tabs.keys():
                self.tabs[user] = []
            self.tabs[user].append(self)
        

    def on_close(self):
        """ Removing the User object from the respective user """
        for tab in self.tabs:
            if tab['tab_id'] == self:
                self.tabs.remove(tab)
                break


if __name__ == "__main__":
    import logging
    logging.getLogger().setLevel(logging.DEBUG)


    # 1. Create Message router
    MessageRouter = sockjs.tornado.SockJSRouter(MessageConnection, '/notify')

    # 2. Create Tornado application
    app = tornado.web.Application(
            [(r"/notify/process/read/", ProcessNotify)] +
            [(r"/notify/process/unread/", ProcessNotify)] +
            [(r"/notify/process/deleted/", ProcessNotify)] +
            [(r"/notify/message/read/", MessageNotify)] +
            [(r"/notify/message/unread/", MessageNotify)] +
            # [(r"/notify/backdoor/read/", Backdoor)] + 
            [(r"/notify/message/deleted/", MessageNotify)] + MessageRouter.urls
    )

    # 3. Make Tornado app listen on port 8080
    app.listen(sys.argv[1])

    # 4. Start IOLoop
    tornado.ioloop.IOLoop.instance().start()
