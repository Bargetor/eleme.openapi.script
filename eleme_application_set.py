 # -*- coding: utf-8 -*-
class ElemeApplication(object):
    """docstring for ElemeApplication"""
    def __init__(self, consumer_key, consumer_secret):
        super(ElemeApplication, self).__init__()
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret


eleme_application_set = {}

#测试application
eleme_application_set['test'] = ElemeApplication('0170804777', '87217cb263701f90316236c4df00d9352fb1da76')

