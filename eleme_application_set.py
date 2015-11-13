 # -*- coding: utf-8 -*-
class ElemeApplication(object):
    """docstring for ElemeApplication"""
    def __init__(self, consumer_key, consumer_secret):
        super(ElemeApplication, self).__init__()
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret


eleme_application_set = {}

# 测试application
eleme_application_set['test'] = ElemeApplication('0170804777', '87217cb263701f90316236c4df00d9352fb1da76')

# 内部测试
eleme_application_set['inner_test'] = ElemeApplication('6409615053', '6735297989472acfc0786fdcd1bae74cf091b94c')

# 来一火
eleme_application_set['lai_yi_huo'] = ElemeApplication('8702401614', 'f14e904c28241ec1e250ad59d19f66c3692a15f6')

# 乐食送
eleme_application_set['le_shi_song'] = ElemeApplication('4763079303', '18002eb8fd29fba30b41c64c823856053d17bf6d')

# KFC
eleme_application_set['kfc'] = ElemeApplication('0684243596', '5144c5ea18cc21dc43391ef105db8865d26e9579')

# 望湘园
eleme_application_set['wang_xiang_yuan'] = ElemeApplication('8933682027', 'c0c0dbc81e2606e355bb4104350c4d61fc3575bc')

# Napos test
eleme_application_set['napos_test'] = ElemeApplication('3795355456', 'ecd3760554778a4c29770fa57b5018f285775f6c')

# 华润
eleme_application_set['hua_run'] = ElemeApplication('3285241516', 'b54bfaccb6d53943d56458cbee909d4759609d9d')

# 江南小厨
eleme_application_set['jiang_nan_xiao_chu'] = ElemeApplication('6682128232', 'a3fb25490da53d5858531514507394134249f286')

# 72街
eleme_application_set['72_jie'] = ElemeApplication('7246948075', 'b454e56f67006bd978e287f0bc6d173022419681')


# 百胜集团测试
eleme_application_set['bai_sheng_group_test'] = ElemeApplication('3415271303', '73a2d6ef564eaec33c5c9bca35a6d272d290e829')

# 必胜宅测试
eleme_application_set['bsz'] = ElemeApplication('4828053019', '0fbd45311558ba8ed12763c11f1f9b414d4c136f')

# 北京领结科技
eleme_application_set['beijing_lingjie'] = ElemeApplication('8116514933', '7ba07482c95568603c36081900e25139d5419ece')

# 棒约翰
eleme_application_set['bang_yue_han'] = ElemeApplication('1455298157', 'e5e9ac9ac29d6cf8e223d66c029c2456332041a3')

# 药快好
eleme_application_set['yao_kuai_hao'] = ElemeApplication('0197812924', '4f24c012da67247905d54157517b1e7adc959636')

# 小南国点点送
eleme_application_set['xiaonanguo_diandian_song'] = ElemeApplication('8981539574', '9b30ced2a5ded9f5a4c772713233cf32e9a4e02a')

# 达美乐测试
eleme_application_set['damino_test'] = ElemeApplication('4375344250', '903173d7e4ae8eebd439e480cf8815264532a870')

# 达美乐
eleme_application_set['damino'] = ElemeApplication('0787448651', '4913802c84ba6dfeaeed87953f4d933b3afd7438')
