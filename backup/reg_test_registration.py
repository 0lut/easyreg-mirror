import matplotlib as matplt
matplt.use('Agg')
import sys,os
sys.path.insert(0,os.path.abspath('.'))
sys.path.insert(0,os.path.abspath('..'))
sys.path.insert(0,os.path.abspath('../model_pool'))
sys.path.insert(0,os.path.abspath('../mermaid'))
print(sys.path)
from backup.global_variable import *
import data_pre.module_parameters as pars
from abc import ABCMeta, abstractmethod
from model_pool.piplines import run_one_task
from data_pre.reg_data_utils import write_list_into_txt, get_file_name, loading_img_list_from_files
import numpy as np

class BaseTask():
    __metaclass__ = ABCMeta
    def __init__(self,name):
        self.name = name

    @abstractmethod
    def save(self):
        pass

class DataTask(BaseTask):
    """
    load the data settings from json
    """
    def __init__(self,name,path='../settings/base_data_settings.json'):
        super(DataTask,self).__init__(name)
        self.data_par = pars.ParameterDict()
        self.data_par.load_JSON(path)


    def save(self, path='../settings/data_settings.json'):
        self.data_par.write_ext_JSON(path)

class ModelTask(BaseTask):
    """
    load the task settings from json
    """
    def __init__(self,name,path='../settings/base_task_settings.json'):
        super(ModelTask,self).__init__(name)
        self.task_par = pars.ParameterDict()
        self.task_par.load_JSON(path)

    def save(self,path= '../settings/task_settings.json'):
        self.task_par.write_ext_JSON(path)



def force_setting(dm, tsm,output_path):
    task_full_path = os.path.join(os.path.join(output_path,'reg'),'res')
    dm.data_par['datapro']['dataset']['prepare_data'] = False
    dm.data_par['datapro']['reg']['max_pair_for_loading'] = [1, 1, -1, 1]
    tsm.task_par['tsk_set']['train'] = False
    tsm.task_par['tsk_set']['save_by_standard_label'] = True
    tsm.task_par['tsk_set']['continue_train'] = False
    tsm.task_par['tsk_set']['reg']['mermaid_net']['using_sym'] = False
    data_json_path = os.path.join(task_full_path, 'cur_data_setting.json')
    tsk_json_path = os.path.join(task_full_path, 'cur_task_setting.json')
    tsm.save(tsk_json_path)
    dm.save(data_json_path)
    tsm.save()
    dm.save()


def init_env(task_full_path,output_path, source_path_list, target_path_list, l_source_path_list=None, l_target_path_list=None):
    """
    :param task_full_path:  the path of a completed task
    :param source_path: path of the source image
    :param target_path: path of the target image
    :param l_source: path of the label of the source image
    :param l_target: path of the label of the target image
    :return: None
    """
    dm_json_path = os.path.join(task_full_path, 'cur_data_setting.json')
    tsm_json_path = os.path.join(task_full_path, 'cur_task_setting.json')
    dm = DataTask('task_reg',dm_json_path)
    tsm = ModelTask('task_reg',tsm_json_path)
    file_num = len(source_path_list)
    assert len(source_path_list) == len(target_path_list)
    if l_source_path_list is not None and l_target_path_list is not None:
        assert len(source_path_list) == len(l_source_path_list)
        file_list = [[source_path_list[i], target_path_list[i],l_source_path_list[i],l_target_path_list[i]] for i in range(file_num)]
    else:
        file_list = [[source_path_list[i], target_path_list[i]] for i in range(file_num)]
    os.makedirs(os.path.join(output_path,'reg/test'),exist_ok=True)
    os.makedirs(os.path.join(output_path,'reg/res'),exist_ok=True)
    pair_txt_path =  os.path.join(output_path,'reg/test/pair_path_list.txt')
    fn_txt_path =   os.path.join(output_path,'reg/test/pair_name_list.txt')
    fname_list = [get_file_name(file_list[i][0])+'_'+get_file_name(file_list[i][1]) for i in range(file_num)]
    write_list_into_txt(pair_txt_path,file_list)
    write_list_into_txt(fn_txt_path,fname_list)
    root_path = output_path
    data_task_name = 'reg'
    cur_task_name = 'res'
    dm.data_par['datapro']['dataset']['output_path'] = root_path
    dm.data_par['datapro']['dataset']['task_name'] = data_task_name
    tsm.task_par['tsk_set']['task_name'] = cur_task_name
    return dm, tsm











#############3
import argparse

parser = argparse.ArgumentParser(description='Registeration demo (include train and test)')

parser.add_argument('--gpu', required=False, type=int, default=2,
                    help='give the id to run the gpu')
parser.add_argument('--llf', required=False, type=bool, default=False,
                    help='run on long leaf')
parser.add_argument('--task_name', required=False, default='reg_lddmm_2step_sym500',
                    help='run on long leaf')
parser.add_argument('--mermaid_net_json_pth', required=False,default='/playpen/zyshen/data/croped_for_reg_debug_3000_pair_oai_reg_inter/reg_lddmm_2step_sym500/mermaid_setting.json',
                    help='run on long leaf')
args = parser.parse_args()

tsm = ModelTask('task_reg')
dm = DataTask('task_reg')
if not args.llf:
    root_path = '/playpen/zyshen/data/'
    data_task_name ='reg_debug_labeled_oai_reg_inter' #'reg_debug_3000_pair_oasis3_reg_inter'#
    data_task_name_for_test ='reg_debug_labeled_oai_reg_inter' #'reg_debug_3000_pair_oasis3_reg_inter'#
    data_task_name_for_train ='croped_for_reg_debug_3000_pair_oai_reg_inter' #'reg_debug_3000_pair_oasis3_reg_inter'#
else:
    root_path = '/pine/scr/z/y/zyshen/expri/'
    data_task_name = 'reg_debug_labeled_oai_reg_inter'  # 'reg_debug_3000_pair_oasis3_reg_inter'#
    data_task_name_for_test ='reg_debug_labeled_oai_reg_inter' #'reg_debug_3000_pair_oasis3_reg_inter'#
    data_task_name_for_train = 'croped_for_reg_debug_3000_pair_oai_reg_inter'  # 'reg_debug_3000_pair_oasis3_reg_inter'#

cur_program_path = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
data_output_path = os.path.join(root_path,data_task_name_for_test)
train_path = os.path.join(root_path,data_task_name_for_train)


###################


read_img_list_from_txt=True
img_list_txt_path = os.path.join(root_path,'reg_debug_labeled_oai_reg_inter/test/pair_path_list.txt') #'/playpen/zyshen/debugs/get_val_and_debug_res/test.txt'
if not read_img_list_from_txt:
    source_path_list = ['/playpen/zyshen/debugs/9002116_20060804_SAG_3D_DESS_RIGHT_11269909_image.nii.gz']
    target_path_list = ['/playpen/zyshen/debugs/9002116_20050715_SAG_3D_DESS_RIGHT_10423916_image.nii.gz']
    l_source_path_list = ['/playpen/zyshen/debugs/9002116_20060804_SAG_3D_DESS_RIGHT_11269909_prediction_step1_batch6_16_reflect.nii.gz']
    l_target_path_list = ['/playpen/zyshen/debugs/9002116_20050715_SAG_3D_DESS_RIGHT_10423916_prediction_step1_batch6_16_reflect.nii.gz']
else:
    source_path_list, target_path_list,l_source_path_list,l_target_path_list = loading_img_list_from_files(img_list_txt_path)




#todo   not change here
refer_task = 'refer_reg_adpt_lddamm_wkw_formul_025_1_omt_2step_200sym_allinterp_prew_bd_mask20'
task_full_path = os.path.join(data_output_path,refer_task)
    #'/playpen/zyshen/data/reg_debug_labeled_oai_reg_inter/test_intra_mermaid_net_500thisinst_10reg_double_loss_step3_jacobi'

    #'/playpen/zyshen/data/reg_debug_3000_pair_oai_reg_intra/vm_miccal_setting_zeroboundary_withbothlambda100sigma002withenlargedflowreg'
    #'/playpen/zyshen/data/reg_debug_labeled_oai_reg_inter/test_intra_mermaid_net_500thisinst_10reg_double_loss_step3_jacobi'
""" the path of the setting from a completed task"""


task_name = args.task_name
mermaid_net_json_pth = args.mermaid_net_json_pth
output_path = os.path.join(data_output_path,task_name)#rdmm_iter_omt2_accumiter_absw_maskmpow3_b2_fixed#rdmm_iter_omt025_accumiter_absw_zero_vel_bound_b2
dm, tsm = init_env(task_full_path,output_path,source_path_list,target_path_list,l_source_path_list,l_target_path_list)
optional_setting_on = True
tsm.task_par['tsk_set']['gpu_ids'] = args.gpu


if is_oai:
    img_sz = [160,384,384]
    input_resize_factor = [80./160.,192./384.,192./384]
    spacing = [1. / (img_sz[i] * input_resize_factor[i]-1) for i in range(len(img_sz))]
dm.data_par['datapro']['dataset']['img_size'] =img_sz#[160,384,384] #[193, 193, 229]
dm.data_par['datapro']['reg']['input_resize_factor'] =input_resize_factor#[96. / 193., 96. / 193, 112. / 229.]
dm.data_par['datapro']['dataset']['spacing'] =spacing#[96. / 193., 96. / 193, 112. / 229.]
tsm.task_par['tsk_set']['input_resize_factor'] =  dm.data_par['datapro']['reg']['input_resize_factor']
tsm.task_par['tsk_set']['img_size'] =  dm.data_par['datapro']['dataset']['img_size']
tsm.task_par['tsk_set']['spacing'] =  dm.data_par['datapro']['dataset']['spacing']


if optional_setting_on:
    """ the following settings are optional, if you want do something different than the loaded setting"""
    ############################### general settings ##########################

    tsm.task_par['tsk_set']['network_name'] ='mermaid'
    tsm.task_par['tsk_set']['model'] = 'reg_net'
    tsm.task_par['tsk_set']['batch_sz'] = 2  # multi sample registration is only for mermaid based methods, for other methods should always be 1
    tsm.task_par['tsk_set']['model_path'] ='/playpen/zyshen/data/croped_for_reg_debug_3000_pair_oai_reg_inter/reg_lddmm_2step_sym500/checkpoints/epoch_85_'
        #'/playpen/zyshen/data/croped_for_reg_debug_3000_pair_oai_reg_inter/reg_adpt_lddamm_wkw_formul_025_1_omt_2step_200sym_minstd_005_allinterp_maskv_epdffix/checkpoints/epoch_170_'
    # '/playpen/zyshen/data/croped_for_reg_debug_3000_pair_oai_reg_inter/reg_adpt_lddamm_wkw_formul_025_1_omt_2step_500sym_allinterp_prew_new/checkpoints/epoch_145_'
        #'/playpen/zyshen/data/croped_for_reg_debug_3000_pair_oai_reg_inter/reg_svf_reg10_old_2step/checkpoints/epoch_130_'
        #'/playpen/zyshen/data/reg_debug_3000_pair_oai_reg_inter/train_intra_mermaid_net_500thisinst_10reg_double_loss_jacobi/checkpoints/epoch_110_'
        #'/playpen/zyshen/data/croped_for_reg_debug_3000_pair_oai_reg_inter/reg_svf_baseline_continue_rk4_old/checkpoints/epoch_100_'
        #'/playpen/zyshen/data/reg_debug_3000_pair_oai_reg_inter/debug_oneadpt_lddmm/checkpoints/epoch_120_'
    #"/playpen/zyshen/data/reg_debug_3000_pair_oai_reg_inter/train_intra_mermaid_net_500thisinst_10reg_double_loss_jacobi/checkpoints/epoch_170_"
        #'/playpen/zyshen/data/reg_debug_3000_pair_oai_reg_intra/vm_miccal_setting_zeroboundary_withbothlambda100sigma002withenlargedflowreg/checkpoints/epoch_270_'
    #'/playpen/zyshen/data/reg_debug_3000_pair_oai_reg_intra/train_intra_mermaid_net_500inst_10reg_double_loss_jacobi/checkpoints/epoch_110_'
        #'/playpen/zyshen/data/reg_debug_3000_pair_oai_reg_inter/vm_cvprwithregfixnccandtraindata_fixedregfixedncc_reg2/checkpoints/epoch_200_'
        #'/playpen/zyshen/data/reg_debug_3000_pair_oai_reg_intra/train_affine_net_sym_lncc/checkpoints/epoch_1070_'

    ###############################  for mermaid network registration ##########################
    tsm.task_par['tsk_set']['reg']['mermaid_net']['optimize_momentum_network']=False
    tsm.task_par['tsk_set']['reg']['mermaid_net']['using_multi_step']=True
    tsm.task_par['tsk_set']['reg']['mermaid_net']['num_step']=2
    tsm.task_par['tsk_set']['reg']['mermaid_net']['using_affine_init']=True
    tsm.task_par['tsk_set']['reg']['mermaid_net']['mermaid_net_json_pth'] = os.path.join(cur_program_path, mermaid_net_json_pth)

    affine_path = os.path.join(train_path,'train_affine_net_sym_lncc/checkpoints/epoch_1070_')
    tsm.task_par['tsk_set']['reg']['mermaid_net']['affine_init_path']=affine_path
    tsm.task_par['tsk_set']['reg']['affine_net']['affine_net_iter']=7


    ################################  for mermaid optimization registration ######################################3
    tsm.task_par['tsk_set']['reg']['mermaid_iter']={}
    """ settings for the mermaid optimization version, we only provide parameter that may different in longitudinal and cross subject task"""
    tsm.task_par['tsk_set']['reg']['mermaid_iter']['affine']={}
    """ settings for the mermaid-affine optimization version"""
    tsm.task_par['tsk_set']['reg']['mermaid_iter']['affine']['sigma'] =np.sqrt(0.5)
    """ for optimization-based mermaid recommand np.sqrt(1./batch_sz) for longitudinal, recommand np.sqrt(0.5/batch_sz) for cross-subject """
    """ for optimization-based mermaid recommand np.sqrt(1.) for longitudinal, recommand np.sqrt(0.5) for cross-subject """
    tsm.task_par['tsk_set']['reg']['mermaid_iter']['nonp_model_name']= 'lddmm_adapt_smoother_map'#'lddmm_shooting_map' #'lddmm_adapt_smoother_map'
    tsm.task_par['tsk_set']['reg']['mermaid_iter']['mermaid_affine_json']= os.path.join(cur_program_path,'model_pool/cur_settings_affine_tmp.json')
    tsm.task_par['tsk_set']['reg']['mermaid_iter']['mermaid_nonp_json'] =mermaid_net_json_pth#os.path.join(cur_program_path,mermaid_net_json_pth)

force_setting(dm,tsm,output_path)


run_one_task()