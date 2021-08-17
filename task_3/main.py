import logging
from abc import ABC, abstractmethod

import time
import os

from psutil import virtual_memory


class TestClass(ABC):
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.logger = self.create_logger(name)
        self.logger.info(f'Test id: {self.id} name: {self.name} start')

    @staticmethod
    def create_logger(name):
        # create logger
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)

        # create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                                      datefmt='%Y-%m-%d %H:%M:%S')

        # create console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        # create file handler
        fl = logging.FileHandler(name + '.log', encoding='UTF8')
        fl.setLevel(logging.INFO)

        # add formatter
        ch.setFormatter(formatter)
        fl.setFormatter(formatter)

        # add ch to logger
        logger.addHandler(ch)
        logger.addHandler(fl)

        # 'application' code
        # logger.info('info message')
        return logger

    @abstractmethod
    def prepare(self):
        self.logger.info(f'Test id: {self.id} name: {self.name} prepare')

    @abstractmethod
    def run(self):
        self.logger.info(f'Test id: {self.id} name: {self.name} run')

    @abstractmethod
    def clean_up(self):
        self.logger.info(f'Test id: {self.id} name: {self.name} clean_up')

    def execute(self):
        try:
            self.prepare()
            self.run()
            self.clean_up()
        except Exception as e:
            self.logger.exception(f'Test id: {self.id} name: {self.name} exception {e}')


class TestCase1(TestClass):
    def __init__(self, id, name):
        super().__init__(id, name)

    def prepare(self):
        super().prepare()
        time_ = int(time.time())
        if time_ % 2 != 0:
            raise Exception(f'time: {time_}')

    def run(self):
        super().run()
        home_directory = os.path.expanduser("~")
        list_dir = os.listdir(home_directory)
        # for f in list_dir:
        #     print(f)
        self.logger.info(f'Test id: {self.id} name: {self.name} from {home_directory} files: {list_dir}')

    def clean_up(self):
        super().clean_up()


class TestCase2(TestClass):
    def __init__(self, id, name):
        super().__init__(id, name)

    def prepare(self):
        super().prepare()
        mem = virtual_memory()
        # print(int(mem.total))
        self.logger.info(f'Test id: {self.id} name: {self.name} memory {mem}')
        if mem.total < 1024 ** 3:
            raise Exception(f'memory {mem} < {1024 ** 3}')

    def run(self):
        super().run()
        if not os.path.exists('test'):
            with open('test', 'wb') as f:
                f.write(os.urandom(1024*1024))

    def clean_up(self):
        super().clean_up()
        os.remove('test')


if __name__ == '__main__':
    test_1 = TestCase1(1, 'Test_1')
    test_1.execute()

    test_2 = TestCase2(2, 'Test_2')
    test_2.execute()