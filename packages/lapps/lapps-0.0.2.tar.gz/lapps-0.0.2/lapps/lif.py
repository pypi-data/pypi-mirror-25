# Copyright (c) 2017. The Language Applications Grid
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

import json
from copy import deepcopy
from lapps.discriminators import Uri

class Data:
    '''
    The Data object is the container for all communications between services on
    the Lappsgrid.

    The Data object consists of a discrimintator, a payload, and possibly some
    parameters.
    '''

    def __init__(self, discriminator=None, payload=None):
        if isinstance(discriminator, dict):
            self.discriminator = discriminator['discriminator']
            if self.discriminator == Uri.LIF:
                self.payload = Container(discriminator['payload'])
            else:
                self.payload = discriminator['payload']
        else:
            if discriminator is not None:
                self.discriminator = discriminator
            else:
                self.discriminator = Uri.LIF

            if payload is not None:
                self.payload = payload
            else:
                self.discriminator = Uri.ERROR
                self.payload = 'Default message'

    def as_json(self):
        return Serializer.to_json(self)

    def as_pretty_json(self):
        return Serializer.to_pretty_json(self)


class Text:
    def __init__(self, text=None, language=None):
        if isinstance(text, dict):
            self.value = text['@value']
            if '@language' in text:
                self.language = text['@language']
        else:
            self.value = text
            if language is not None:
                self.language = 'en'


class Container:
    def __init__(self, d=None):
        if d is None:
            self.metadata = {}
            self.views = []
            self.text = Text()
            self.context = 'http://vocab.lappsgrid.org/context-1.0.0.jsonld'
            # self.id = ''
        elif isinstance(d, dict):
            # self.id = d['id']
            self.metadata = deepcopy(d['metadata'])
            if '@context' in d:
                self.context = d['@context']
            else:
                self.context = 'http://vocab.lappsgrid.org/context-1.0.0.jsonld'
            text = d['text']
            self.text = Text()
            if '@value' in text:
                self.text.value = text['@value']
            if '@language' in text:
                self.text.language = text['@language']
            self.views = []
            for v in d['views']:
                self.views.append(View(v))
        else:
            raise Exception('Invalid type: ' + str(d))

    def set_text(self, text):
        self.text.value = text

    def get_text(self):
        return self.text.value

    def set_language(self, lang):
        self.text.language = lang

    def get_language(self):
        return self.text.language

    def new_view(self, id=None):
        if id is None:
            id = self.generate_id()
        if self.find_view(id) is not None:
            raise Exception("A view with the id" + id + " already exists.")

        view = View(id)
        self.views.append(view)
        return view

    def find_view(self, id):
        for view in self.views:
            if view.id == id:
                return view
        return None

    def find_view_by_type(self, type):
        for view in self.views:
            if view.contains(type):
                return view
        return None

    def generate_id(self):
        n = self.views.__len__ + 1
        id = 'v-' + str(n)
        duplicate = self.find_view(self, id)
        while duplicate:
            id = 'v-' + str(++n)
            duplicate = self.find_view(self, id)
        return id


class View:
    def __init__(self, id=None):
        if isinstance(id, dict):
            d = id
            # TODO this is a hack-around until I can determine why the view.id is
            # not being set.
            if 'id' in d:
                self.id = d['id']
            else:
                self.id = 'id'
            self.metadata = d['metadata']
            self.annotations = []
            for a in d['annotations']:
                self.annotations.append(Annotation(a))
        else:
            self.id = id
            self.metadata = {}
            self.annotations = []

    def add_metadata(self, name, value):
        self.metadata[name] = value

    def add_contains(self, type, producer, info):
        if 'contains' in self.metadata:
            contains = self.metadata['contains']
        else:
            contains = {}
            self.metadata['contains'] = contains

        contains[type] = {
            'producer': producer,
            'type': info
        }

    def contains(self, type):
        if not 'contains' in self.metadata:
            return None

        contains = self.metadata['contains']
        if type in contains:
            return contains[type]
        return None

    def new_annotation(self, id, type, start=None, end=None):
        a = Annotation(id, type, start, end)
        self.annotations.append(a)
        return a


class Annotation:
    def __init__(self, ID, type=None, start=None, end=None):
        try:
            basestring
        except:
            basestring=str

        if isinstance(ID, dict):
            #for k,v in id.items():
            #    self.__dict__[k] = v
            a = ID
            self.id = a['id']
            self.start = a['start']
            self.end = a['end']
            self.type = a['@type']
            if 'label' in a:
                self.label = a['label']
            else:
                self.label = None
            if 'features' in a:
                self.features = deepcopy(a['features'])
            else:
                self.features = {}
            if 'metadata' in a:
                self.metadata = deepcopy(a['metadata'])
            else:
                self.metadata = {}
        elif isinstance(ID, basestring):
            self.id = ID
            self.start = start
            self.end = end
            self.label = None
            self.type = type
            self.features = {}
            self.metadata = {}
        elif isinstance(ID, Annotation):
            a = ID
            self.id = a.id
            self.type = a.type
            self.start = a.start
            self.end = a.end
            self.label = a.label
            self.features = deepcopy(a.features)
            self.metadata = deepcopy(a.metadata)
        else:
            raise Exception('Invalid initializer for Annotation ' + str(ID))

    def add_feature(self, name, value):
        self.features[name] = value

    def get_feature(self, name):
        if (name in self.features):
            return self.features[name]
        return None


class Serializer:
    @staticmethod
    def get(o):
        '''
        Most classes can be serialized directly from their __dict__ objects,
        however a few classes are supposed to generate JSON keys that start
        with a '@'. We need to intercept those classes and return a dictionary
        with the proper key (attribute) names.

        :param o: the object to be serialized.
        :return: a dictionary that can be used by json.dump to serialize the
        object to JSON.
        '''
        if isinstance(o, Text):
            t = {}
            t['@value'] = o.value
            if hasattr(o, 'language'):
                t['@language'] = o.language
            return t
        elif isinstance(o, Container):
            t = {}
            t['@context'] = o.context
            t['metadata'] = o.metadata
            t['views'] = o.views
            t['text'] = o.text
            return t
        elif isinstance(o, Annotation):
            a = {}
            a['id'] = o.id
            a['@type'] = o.type
            a['start'] = o.start
            a['end'] = o.end
            a['label'] = o.label
            a['features'] = o.features
            a['metadata'] = o.metadata
            return a
        else:
            return o.__dict__

    @staticmethod
    def to_json(o):
        return json.dumps(o, default=Serializer.get, sort_keys=True)

    @staticmethod
    def to_pretty_json(o):
        return json.dumps(o, default=Serializer.get, sort_keys=True, indent=4)

    @staticmethod
    def parse(text, cls=None):
        map = json.loads(text)
        if cls is None:
            return map
        return cls(map)
