import random
import tornado.web
from typing import Optional, Awaitable


class Test2Handler(tornado.web.RequestHandler):

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def get(self):
        data = {}
        for i in range(random.randrange(1, 10)):
            words = ['testing', 'abc', 'test2', 'another_word', 'cdef', 'jkl']
            key = words[random.randrange(0, 5)]
            value = words[random.randrange(0, 5)]
            data[f'{key}_{i}'] = f'{value}_{i}'
            # randomly add some lists too
            if random.randrange(0, 2):
                data[f'{key}_{i}_{i}'] = []
                for j in range(random.randrange(1, 10)):
                    data[f'{key}_{i}_{i}'].append(f'{value}_{j}_{i}')
        self.write(dict(data))  # using dict sets content type to application/json
        # self.render("render_json.html", data=json.dumps(data))
