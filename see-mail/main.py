#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import webapp2

# this is for displaying HTML
from webapp2_extras import jinja2

# BaseHandler subclasses RequestHandler so that we can use jinja
class BaseHandler(webapp2.RequestHandler):

    @webapp2.cached_property
    def jinja2(self):
        # Returns a Jinja2 renderer cached in the app registry.
        return jinja2.get_jinja2(app=self.app)

        # This will call self.response.write using the specified template and context.
        # The first argument should be a string naming the template file to be used. 
        # The second argument should be a pointer to an array of context variables
        #  that can be used for substitutions within the template
    def render_response(self, _template, **context):
        # Renders a template and writes the result to the response.
        context = {}
        rv = self.jinja2.render_template(_template, **context)
        self.response.write(rv)


class MainHandler(BaseHandler):
    def get(self):
	context = {}
        self.render_response('index.html', **context)
        
    def post(self):
        context = {}
        self.render_response('index.html', **context)
        
class friend1Length(BaseHandler):
    def get(self):
	context = {}
        self.render_response('friend1-length.html', **context)
        
    def post(self):
        context = {}
        self.render_response('friend1-length.html', **context)

class friend1Keywords(BaseHandler):
    
    def get(self):
	#defines default search to be a
        context = {}
        self.render_response('friend1-keywords.html', **context)
        
    def post(self):
        context = {}
        self.render_response('friend1-keywords.html', **context)
        

class About(BaseHandler):
    
    def get(self):
	#defines default search to be a
        context = {}
        self.render_response('about.html', **context)
        
    def post(self):
        context = {}
        self.render_response('about.html', **context)

class friend1(BaseHandler):
    
    def get(self):
	#defines default search to be a
        context = {}
        self.render_response('friend1.html', **context)
        
    def post(self):
        context = {}
        self.render_response('friend1.html', **context)


        
class Resources(BaseHandler):
    
    def get(self):
	#defines default search to be a
        context = {}
        self.render_response('resources.html', **context)
        
    def post(self):
        context = {}
        self.render_response('resources.html', **context)

    

app = webapp2.WSGIApplication([('/', MainHandler),
                            ('/friend1-length', friend1Length),
                            ('/friend1-keywords', friend1Keywords),
                            ('/about', About),
                            ('/friend1', friend1),
                            
                            ('/resources', Resources),
                            
                            ], debug=True)