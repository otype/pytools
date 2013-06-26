# -*- coding: utf-8 -*-
"""

    pybuildr

    created by hgschmidt on 18.03.2013, 13:28 CET
    
    Copyright (c) 2012 apitrary

"""
import riak
import logging
from pytools.pybuildr.exceptions import RiakObjectIdNotProvidedException
from pytools.pybuildr.exceptions import RiakObjectNotFoundException


class RiakRepository(object):
    """
        Processor to handle the GET request.
    """

    def __init__(self, riak_host, riak_pb_port, bucket_name, riak_rq, riak_wq):
        """
            Simple init method ...
        """
        super(RiakRepository, self).__init__()
        self.riak_client = riak.RiakClient(host=riak_host, port=riak_pb_port, transport_class=riak.RiakPbcTransport)
        self.bucket_name = bucket_name
        self.bucket = self.riak_client.bucket(self.bucket_name).set_r(riak_rq).set_w(riak_wq)

    def fetch(self, object_id):
        """
            Retrieve a single object with given object ID from Riak
        """
        if object_id is None:
            logging.error('No object ID provided! Object ID required.')
            raise RiakObjectIdNotProvidedException()

        # Fetch the data from the Riak bucket
        single_object = self.bucket.get(object_id).get_data()
        logging.debug('Object with ID {} fetched.'.format(object_id))

        # No object retrieved? Key must be invalid.
        if single_object is None:
            logging.error('Object with given id={} not found!'.format(object_id))
            raise RiakObjectNotFoundException()

        return single_object

    def fetch_all(self):
        """
            This is a helper function to run a map/reduce search call retrieving all objects within
            this entity's bucket.

            Used in GET (EntityHandlers).
        """
        query = riak.RiakMapReduce(self.riak_client).add(self.bucket_name)
        query.map('''function(v) {
                        var data = JSON.parse(v.values[0].data);
                        if(v.key != '_init') {
                            return [{"id": v.key, "data": data}];
                        }
                        return [];
                    }''')
        result = None
        try:
            result = query.run()
        except Exception, e:
            logging.error(e.message)

        return result

    def add(self, object_id, data):
        """
            Create a object in database. But only, if the object_id doesn't exist, yet.
        """
        return self.bucket.new(object_id, data).store()

    def update(self, object_id, data):
        """
            Update a given object in database
        """
        return self.add(object_id=object_id, data=data)

    def remove(self, object_id):
        """
            Remove an object from Riak
        """
        obj = self.bucket.get(object_id)
        if obj:
            return obj.delete()

    def search(self, search_query):
        """
            Search within this entity's bucket.

            Used in GET (EntityHandlers).
        """
        search_query = self.riak_client.search(self.bucket_name, search_query)
        logging.debug('search_query: {}'.format(search_query))
        search_response = []
        for result in search_query.run():
            # Getting ``RiakLink`` objects back.
            obj = result.get()
            obj_data = obj.get_data()
            kv_object = {'_id': result._key, '_data': obj_data}
            search_response.append(kv_object)

        return search_response