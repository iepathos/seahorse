#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tornado.ioloop
from body.soul import make_app

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
