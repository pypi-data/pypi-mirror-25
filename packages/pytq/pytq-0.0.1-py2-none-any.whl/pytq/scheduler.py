#!/usr/bin/env python
# -*- coding: utf-8 -*-

import types
from multiprocessing import cpu_count
from multiprocessing.dummy import Pool

try:
    from .task import Task
    from .per_class_logger import ClassWithLogger
    from .util.fingerprint import hash_data
    from .pkg.sfm.exception_mate import get_last_exc_info
except:  # pragma: no cover
    from pytq.task import Task
    from pytq.per_class_logger import ClassWithLogger
    from pytq.util.fingerprint import hash_data
    from pytq.pkg.sfm.exception_mate import get_last_exc_info


class BaseScheduler(ClassWithLogger):
    """
    All Scheduler has to inherit from this base class.
    """

    def __init__(self, logger=None):
        super(BaseScheduler, self).__init__(logger=logger)

        # link hash input method
        try:
            self.user_hash_input(None)
            self._hash_input = self.user_hash_input
        except NotImplementedError:
            self._hash_input = self._default_hash_input
        except:
            self._hash_input = self.user_hash_input

        # link duplicate test method
        try:
            self.user_is_duplicate(None)
            self._is_duplicate = self.user_is_duplicate
        except NotImplementedError:
            self._is_duplicate = self._default_is_duplicate
        except:
            self._is_duplicate = self.user_is_duplicate

        # link pre process method
        try:
            self.user_pre_process(None)
            self._pre_process = self.user_pre_process
        except NotImplementedError:
            self._pre_process = self._default_pre_process
        except:
            self._pre_process = self.user_pre_process

        # link post process method
        try:
            self.user_post_process(None)
            self._post_process = self.user_post_process
        except NotImplementedError:
            self._post_process = self._default_post_process
        except:
            self._post_process = self.user_post_process

    def _default_hash_input(self, input_data):
        """
        Default hash method to get a identical fingerprint for input data.

        By default its: pickle the data and md5 it.

        This method will be used when :meth:`BaseScheduler.user_hash_input`
        are not defined.

        :returns: fingerprint for ``input_data``
        :rtype: string.
        """
        return hash_data(input_data)

    def user_hash_input(self, input_data):
        """
        (Optional) Get identical fingerprint for input data.

        :returns: fingerprint for ``input_data``
        :rtype: string.
        """
        raise NotImplementedError

    def _hash_input(self, input_data):
        """
        The real hashing method will be called.

        :returns: fingerprint for ``input_data``
        :rtype: string.
        """
        raise NotImplementedError

    def user_is_duplicate(self, task):
        """
        (Optional) Check if a task is duplicate.

        :param task:
        :return: return True, when it's a duplicate item.
        :rtype: boolean.
        """
        raise NotImplementedError

    def _default_is_duplicate(self, task):
        """
        Default duplicate test method, always not duplicate.

        :param task:
        :return:
        """
        return False  # Alwasy not duplicate

    def _is_duplicate(self, task):
        """
        The real duplicate test method will be called.

        :returns: boolean. return True, when it's a duplicate item.
        """
        raise NotImplementedError

    def _remove_duplicate(self, input_data_queue):
        """
        Remove duplicate input_data.

        :param input_data_queue:
        :returns: task_queue.
        :rtype: types.GeneratorType.

        **中文文档**

        移除那些重复的输入数据。
        """
        is_generator = isinstance(
            input_data_queue, types.GeneratorType)

        if not is_generator:
            left_counter = len(input_data_queue)

        nth_counter = 0
        for input_data in input_data_queue:
            if is_generator:
                left_counter = None
            else:
                left_counter -= 1

            task = Task(
                id=self._hash_input(input_data),
                input_data=input_data,
                nth_counter=nth_counter,
                left_counter=left_counter,
            )

            if not self._is_duplicate(task):
                nth_counter += 1
                yield task

    _default_batch_pre_process = _remove_duplicate
    """
    A method will be called to pre process task queue before doing any real
    per task process. Usually it can be duplicate filter, statistic check.
    """

    def user_pre_process(self, task):
        """
        (Optional) Defines the action that before the
        :meth:`BaseScheduler.user_process() been called.

        :param task: :class:`pytq.task.Task` instance.
        """
        raise NotImplementedError

    def _default_pre_process(self, task):
        """
        Default behavior of user_pre_process, do nothing.
        """
        pass

    def _pre_process(self, task):
        """
        The real method will be called for pre_process.
        """
        raise NotImplementedError

    def user_post_process(self, task):
        """
        (Optional) Defines the action that after the
        :meth:`BaseScheduler.user_process() been called.

        :param task: :class:`pytq.task.Task` instance.
        """
        raise NotImplementedError

    def _default_post_process(self, task):
        """
        Default behavior of user_post_process, do nothing.
        """
        pass

    def _post_process(self, task):
        """
        The real method will be called for post_process.
        """
        raise NotImplementedError

    def user_process(self, input_data):
        """
        (Required) Defines the logic that process the input_data, returns
        output_data

        :param input_data:
        :return: the output_data
        """
        raise NotImplementedError

    def _process(self, task):
        """
        The real processing method will be called.

        **中文文档**

        处理数据。包含, 哈希, 处理, 标记完成三个步骤
        """
        self.info(task.progress_msg())

        try:
            if task.pre_process is None:
                self._pre_process(task)
            else:
                task._pre_process()

            output_data = self.user_process(task.input_data)
            task.output_data = output_data

            if task.post_process is None:
                self._post_process(task)
            else:
                task._post_process()

            self.info("Success!", 1)
        except Exception as e:
            self.info("Failed due to: %r" % get_last_exc_info(), 1)

    def _do_single_process(self, task_queue):
        """
        Execute single thread process.

        :param task_queue: task queue/list.
        """
        for task in task_queue:
            self._process(task)

    def _do_multi_process(self, task_queue):
        """
        Execute multi thread process.

        :param task_queue: task queue/list.
        """
        pool = Pool(processes=cpu_count())
        pool.map(self._process, task_queue)

    def do(self,
           input_data_queue,
           pre_process=None,
           multiprocess=False):
        """
        Do the real work.

        :param input_data_list: list of input data (or generator).
        :param quick_remove_duplicate: apply remove finished item (duplicate)
          filter  before we start the real work.
        :param multiprocess: trigger to use multiprocess.
        """
        if pre_process is None:
            task_queue = self._default_batch_pre_process(input_data_queue)
        else:
            task_queue = pre_process(input_data_queue)

        try:
            self.info("\nHas %s items todo." % len(input_data_queue))
        except:
            self.info("\nHas UNKNOWN items todo")

        if multiprocess:
            self._do_multi_process(task_queue)
        else:
            self._do_single_process(task_queue)

        self.info("Complete!")

    def clear_all(self):
        """
        Clear all data.

        **中文文档**

        重置Filter至初始状态。
        """
        raise NotImplementedError

    def __len__(self):
        raise NotImplementedError

    def __iter__(self):
        raise NotImplementedError

    def get(self, id):
        """
        Get output data by fingerprint of input_data.

        **中文文档**

        根据输入的指纹, 直接获得已经完成的输出数据。
        """
        raise NotImplementedError

    def get_output(self, input_data):
        """
        Get output data of the input_data.

        **中文文档**

        根据输入的数据, 直接获得已经完成的输出的数据。
        """
        return self.get(self._hash_input(input_data))

    def keys(self):
        return iter(self)

    def items(self):
        for key in self:
            yield (key, self.get(key))


class BaseDBTableBackedScheduler(BaseScheduler):
    """
    Scheduler that use database table as backend storage.

    - Task.id as primary_key
    - Other column / field for input_data, output_data storage.
    """

    def _get_finished_id_set(self):
        """
        (Required) A method that returns all saved id set.
        (For all processed input_data)

        :returns: a id set.
        :rtype: set.
        """
        raise NotImplementedError

    def _default_batch_pre_process(self, input_data_queue):
        finished_id_set = self._get_finished_id_set()

        is_generator = isinstance(input_data_queue, types.GeneratorType)
        # if its generator, then left_counter always be None
        if not is_generator:
            left_counter = len(input_data_queue)

        nth_counter = 0
        for input_data in input_data_queue:
            if is_generator:
                left_counter = None
            else:
                left_counter -= 1

            id = self._hash_input(input_data)
            if id not in finished_id_set:
                nth_counter += 1
                task = Task(
                    id=id,
                    input_data=input_data,
                    nth_counter=nth_counter,
                    left_counter=left_counter,
                )
                yield task
