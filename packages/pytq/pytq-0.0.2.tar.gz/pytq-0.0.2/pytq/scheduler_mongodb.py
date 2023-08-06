#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pickle

try:
    from pytq.scheduler import Task, BaseDBTableBackedScheduler
except:  # pragma: no cover
    from pytq.scheduler import Task, BaseDBTableBackedScheduler


class MongoDBScheduler(BaseDBTableBackedScheduler):
    """

    :param collection: :class:`pymongo.Collection` instance.
    """
    collection = None

    def __init__(self, logger=None, collection=None):
        super(MongoDBScheduler, self).__init__(logger=logger)

        if collection is not None:
            self.collection = collection
        self._col = self.collection

        # link encode method
        try:
            self.user_encode(None)
            self._encode = self.user_encode
        except NotImplementedError:
            self._encode = self._default_encode
        except:
            self._encode = self.user_encode

        # link decode method
        try:
            self.user_decode(None)
            self._decode = self.user_decode
        except NotImplementedError:
            self._decode = self._default_decode
        except:
            self._decode = self.user_decode

    @property
    def collection(self):
        """
        Back-end mongodb collection.
        """
        raise NotImplementedError

    def _default_encode(self, obj):
        return pickle.dumps(obj)

    def user_encode(self, obj):
        """
        (Optional) User defined serializer for output_data.

        :returns: bytes or string.

        **中文文档**

        用于对处理结果序列化的函数。默认使用pickle。
        """
        raise NotImplementedError

    def _encode(self, obj):
        raise NotImplementedError

    def _default_decode(self, bytes_or_str):
        return pickle.loads(bytes_or_str)

    def user_decode(self, bytes_or_str):
        """
        (Optional) User defined deserializer for output_data.

        :returns: python object.

        **中文文档**

        用于对处理结果反序列化的函数。默认使用pickle。
        """
        raise NotImplementedError

    def _decode(self, bytes_or_str):
        raise NotImplementedError

    def _default_is_duplicate(self, task):
        """
        Check if ``task.id`` presents in the collection.
        """
        return self._col.find_one({"_id": task.id}) is not None

    def _get_finished_id_set(self):
        """
        It's Primary key value set.
        """
        return set([
            doc["_id"] for doc in self._col.find({}, {"_id": True})
        ])

    def _default_post_process(self, task):
        """
        Save output_data into ``out`` field.
        """
        self._col.update(
            {"_id": task.id},
            {"$set": {"out": self._encode(task.output_data)}},
            upsert=True,
        )

    def __len__(self):
        return self._col.find().count()

    def __iter__(self):
        for doc in self._col.find():
            yield doc["_id"]

    def clear_all(self):
        self._col.remove({})

    def get_output(self, input_data):
        key = self.user_hash_input(input_data)
        return self._decode(self._col.find_one({"_id", key})["out"])

    def items(self):
        for doc in self._col.find():
            yield (doc["_id"], self._decode(doc["out"]))
