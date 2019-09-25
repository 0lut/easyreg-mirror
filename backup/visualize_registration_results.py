from __future__ import print_function
from __future__ import absolute_import
# from builtins import str
# from builtins import range
from backup.global_variable import is_lung

from data_pre.reg_data_utils import make_dir
#from .config_parser import MATPLOTLIB_AGG
# if MATPLOTLIB_AGG:
#     matplt.use('Agg')

"""
Some utility functions to display the registration results
"""

import matplotlib.pyplot as plt
import numpy as np
import os
from model_pool import utils
from backup import viewers

dpi=500
extension= '.png'
def _show_current_images_1d(iS, iT, iW, iter, vizImage, vizName, phiWarped,visual_param=None, i=0):

    if (vizImage is not None) and (phiWarped is not None):
        sp_s = 231
        sp_t = 232
        sp_w = 233
        sp_p = 235
        sp_v = 236
    elif (vizImage is not None):
        sp_s = 221
        sp_t = 222
        sp_w = 223
        sp_v = 224
    elif (phiWarped is not None):
        sp_s = 221
        sp_t = 222
        sp_w = 223
        sp_p = 224
    else:
        sp_s = 131
        sp_t = 132
        sp_w = 133

    plt.suptitle('Iteration = ' + str(iter))
    plt.setp(plt.gcf(), 'facecolor', 'white')
    plt.style.use('bmh')

    plt.subplot(sp_s)
    plt.plot(utils.t2np(iS))
    plt.title('source image')

    plt.subplot(sp_t)
    plt.plot(utils.t2np(iT))
    plt.title('target image')

    plt.subplot(sp_w)
    plt.plot(utils.t2np(iT),'g',linestyle=':')
    plt.plot(utils.t2np(iS),'r',linestyle='--')
    plt.plot(utils.t2np(iW),linestyle=':')
    plt.title('warped image')

    if phiWarped is not None:
        plt.subplot(sp_p)
        plt.plot(utils.t2np(phiWarped[0,:]))
        plt.title('phi')

    if vizImage is not None:
        plt.subplot(sp_v)
        plt.plot(utils.lift_to_dimension(utils.t2np(vizImage),1))
        plt.title(vizName)

    if visual_param is not None:
        if i==0 and visual_param['visualize']:
            plt.show()
        if visual_param['save_fig']:
            file_name = visual_param['pair_path'][i]
            join_p = lambda pth1,pth2: os.path.join(pth1, pth2)
            make_dir(join_p(visual_param['save_fig_path_byname'], file_name))
            make_dir(join_p(visual_param['save_fig_path_byiter'], visual_param['iter']))
            plt.savefig(join_p(join_p(visual_param['save_fig_path_byname'], file_name),visual_param['iter']+extension), dpi=dpi)
            plt.savefig(join_p(join_p(visual_param['save_fig_path_byiter'], visual_param['iter']), file_name+extension), dpi=dpi)
    else:
        plt.show()


def checkerboard_2d(I0,I1,nrOfTiles=8):
    """
    Creates a checkerboard between two images

    :param I0: image 0, size XxYxZ
    :param I1: image 1, size XxYxZ
    :param nrOfTiles: number of desired tiles in each direction
    :return: returns tiled image
    """
    sz = I0.shape
    tileSize = int( np.array(sz).min()/nrOfTiles )
    nrOfTileXH = int( np.ceil(sz[0]/tileSize)/2+1 )
    nrOfTileYH = int( np.ceil(sz[1]/tileSize)/2+1 )
    cb_grid = np.kron([[1, 0] * nrOfTileYH, [0, 1] * nrOfTileYH] *nrOfTileXH, np.ones((tileSize, tileSize)))
    # now cut it to the same size
    cb_grid=cb_grid[0:sz[0],0:sz[1]]
    cb_image = I0*cb_grid + I1*(1-cb_grid)
    return cb_image

def _show_current_images_2d_no_map(iS, iT, iW, iter, vizImage, vizName, visual_param=None, i=0):

    if (vizImage is not None):
        sp_s = 231
        sp_t = 232
        sp_w = 233
        sp_c = 234
        sp_v = 235
    else:
        sp_s = 221
        sp_t = 222
        sp_w = 223
        sp_c = 224

    plt.suptitle('Iteration = ' + str(iter))
    plt.setp(plt.gcf(), 'facecolor', 'white')
    plt.style.use('bmh')

    plt.subplot(sp_s)
    plt.imshow(utils.t2np(iS),cmap='gray')
    plt.colorbar()
    plt.title('source image')

    plt.subplot(sp_t)
    plt.imshow(utils.t2np(iT),cmap='gray')
    plt.colorbar()
    plt.title('target image')

    plt.subplot(sp_w)
    plt.imshow(utils.t2np(iW),cmap='gray')
    plt.colorbar()
    plt.title('warped image')

    plt.subplot(sp_c)
    plt.imshow(checkerboard_2d(utils.t2np(iW),utils.t2np(iT)),cmap='gray')
    plt.colorbar()
    plt.title('checkerboard')

    if vizImage is not None:
        plt.subplot(sp_v)
        plt.imshow(utils.lift_to_dimension(utils.t2np(vizImage),2),cmap='gray')
        plt.colorbar()
        plt.title(vizName)

    if visual_param is not None:
        if i==0 and visual_param['visualize']:
            plt.show()
        if visual_param['save_fig']:
            file_name = visual_param['pair_path'][i]
            join_p = lambda pth1,pth2: os.path.join(pth1, pth2)
            make_dir(join_p(visual_param['save_fig_path_byname'], file_name))
            make_dir(join_p(visual_param['save_fig_path_byiter'], visual_param['iter']))
            plt.savefig(join_p(join_p(visual_param['save_fig_path_byname'], file_name),visual_param['iter']+extension), dpi=dpi)
            plt.savefig(join_p(join_p(visual_param['save_fig_path_byiter'], visual_param['iter']), file_name+extension), dpi=dpi)
    else:
        plt.show()

def _show_current_images_2d_map(iS, iT, iW,iSL,iTL, iWL, iter, vizImage, vizName, phiWarped, visual_param=None, i=0):
    if iSL is not None and iTL is not None:
        sp_s = 331
        sp_t = 332
        sp_w = 333
        sp_c = 334
        sp_p = 335
        sp_v = 336
        sp_ls = 337
        sp_lt = 338
        sp_lw = 339

    elif (vizImage is not None) and (phiWarped is not None):
        sp_s = 231
        sp_t = 232
        sp_w = 233
        sp_c = 234
        sp_p = 235
        sp_v = 236
    elif (vizImage is not None):
        sp_s = 231
        sp_t = 232
        sp_w = 233
        sp_c = 234
        sp_v = 235
    elif (phiWarped is not None):
        sp_s = 231
        sp_t = 232
        sp_w = 233
        sp_c = 234
        sp_p = 235
    else:
        sp_s = 221
        sp_t = 222
        sp_w = 223
        sp_c = 224

    font = {'size': 10}

    plt.suptitle('Iteration = ' + str(iter))
    plt.setp(plt.gcf(), 'facecolor', 'white')
    plt.style.use('bmh')

    plt.subplot(sp_s).set_axis_off()
    plt.imshow(utils.t2np(iS), cmap='gray')
    plt.colorbar().ax.tick_params(labelsize=3)
    plt.title('source image', font)

    plt.subplot(sp_t).set_axis_off()
    plt.imshow(utils.t2np(iT), cmap='gray')
    plt.colorbar().ax.tick_params(labelsize=3)
    plt.title('target image', font)

    plt.subplot(sp_w).set_axis_off()
    plt.imshow(utils.t2np(iW), cmap='gray')
    plt.colorbar().ax.tick_params(labelsize=3)
    plt.title('warped image', font)

    plt.subplot(sp_c).set_axis_off()
    plt.imshow(checkerboard_2d(utils.t2np(iW), utils.t2np(iT)), cmap='gray')
    plt.colorbar().ax.tick_params(labelsize=3)
    plt.title('checkerboard', font)

    if phiWarped is not None:
        plt.subplot(sp_p).set_axis_off()
        plt.imshow(utils.t2np(iW),cmap='gray')

        plt.contour(utils.t2np(phiWarped[0, :, :]), np.linspace(-1, 1, 20), colors='r', linestyles='solid',
                    linewidths=0.5)
        plt.contour(utils.t2np(phiWarped[1, :, :]), np.linspace(-1, 1, 20), colors='r', linestyles='solid',
                    linewidths=0.5)

        plt.colorbar().ax.tick_params(labelsize=3)
        plt.title('warped image + grid', font)

    if vizImage is not None:
        plt.subplot(sp_v).set_axis_off()
        plt.imshow(utils.lift_to_dimension(utils.t2np(vizImage),2), cmap='gray')
        plt.colorbar().ax.tick_params(labelsize=3)
        plt.title(vizName, font)


    if iSL is not None and iTL is not None:
        plt.subplot(sp_ls).set_axis_off()
        plt.imshow(utils.t2np(iSL), cmap='gray')
        plt.title('Source Label', font)

        plt.subplot(sp_lt).set_axis_off()
        plt.imshow(utils.t2np(iTL), cmap='gray')
        plt.title('Target Label', font)

        plt.subplot(sp_lw).set_axis_off()
        plt.imshow(utils.t2np(iWL), cmap='gray')
        plt.title('Warped Label', font)


    if visual_param is not None:
        if i==0 and visual_param['visualize']:
            plt.show()
        if visual_param['save_fig']:
            file_name = visual_param['pair_path'][i]
            join_p = lambda pth1,pth2: os.path.join(pth1, pth2)
            make_dir(join_p(visual_param['save_fig_path_byname'], file_name))
            make_dir(join_p(visual_param['save_fig_path_byiter'], visual_param['iter']))
            plt.savefig(join_p(join_p(visual_param['save_fig_path_byname'], file_name),visual_param['iter']+extension), dpi=dpi)
            plt.savefig(join_p(join_p(visual_param['save_fig_path_byiter'], visual_param['iter']), file_name+extension), dpi=dpi)
            plt.clf()
    else:
        plt.show()


def _show_current_images_2d(iS, iT, iW,iSL, iTL,iWL, iter, vizImage, vizName, phiWarped, visual_param=None, i=0):

    if phiWarped is not None:
        _show_current_images_2d_map(iS, iT, iW, iSL, iTL, iWL, iter, vizImage, vizName, phiWarped, visual_param, i)
    else:
        _show_current_images_2d_no_map(iS, iT, iW, iter, vizImage, vizName, visual_param, i)


def _show_current_images_3d(iS, iT, iW,iSL, iTL,iWL, iter, vizImage, vizName, phiWarped, visual_param=None, i=0,extraImage=None, extraName= None):
    if iSL is not None and iTL is not None:
        phiw_a = 3
        if vizImage is None and extraImage is None:
            fig, ax = plt.subplots(7, 3)
            iSL_a = 4
            iTL_a = 5
            iWL_a = 6
        elif extraImage is None:
            fig, ax = plt.subplots(8, 3)
            vizi_a = 4
            iSL_a = 5
            iTL_a = 6
            iWL_a = 7
        else:
            if is_lung:
                fig, ax = plt.subplots(9, 3,figsize=(6,15))
            else:
                fig, ax = plt.subplots(3,9, figsize=(14,5))
            vizi_a = 4
            ext_a = 5
            iSL_a = 6
            iTL_a = 7
            iWL_a = 8
    elif (phiWarped is not None) and (vizImage is not None):
        fig, ax = plt.subplots(5,3)
        phiw_a = 3
        vizi_a = 4
    elif (phiWarped is not None):
        fig, ax = plt.subplots(4,3)
        phiw_a = 3
    elif (vizImage is not None):
        fig, ax = plt.subplots(4,3)
        vizi_a = 3
    else:
        fig, ax = plt.subplots(3,3)

    plt.suptitle('Iteration = ' + str(iter))
    plt.setp(plt.gcf(), 'facecolor', 'white')
    plt.style.use('bmh')
    #plt.subplots_adjust(top=0.99, bottom=0.01, hspace=0.15, wspace=0.04)

    ivsx = viewers.ImageViewer3D_Sliced(ax[0][0], utils.t2np(iS), 0, 'source X', True)
    ivsy = viewers.ImageViewer3D_Sliced(ax[1][0], utils.t2np(iS), 1, 'source Y', True)
    ivsz = viewers.ImageViewer3D_Sliced(ax[2][0], utils.t2np(iS), 2, 'source Z', True)

    ivtx = viewers.ImageViewer3D_Sliced(ax[0][1], utils.t2np(iT), 0, 'target X', True)
    ivty = viewers.ImageViewer3D_Sliced(ax[1][1], utils.t2np(iT), 1, 'target Y', True)
    ivtz = viewers.ImageViewer3D_Sliced(ax[2][1], utils.t2np(iT), 2, 'target Z', True)

    ivwx = viewers.ImageViewer3D_Sliced(ax[0][2], utils.t2np(iW), 0, 'warped X', True)
    ivwy = viewers.ImageViewer3D_Sliced(ax[1][2], utils.t2np(iW), 1, 'warped Y', True)
    ivwz = viewers.ImageViewer3D_Sliced(ax[2][2], utils.t2np(iW), 2, 'warped Z', True)

    if phiWarped is not None:
        ivwxc = viewers.ImageViewer3D_Sliced_Contour(ax[0][phiw_a], utils.t2np(iW), utils.t2np(phiWarped), 0, 'warped X', True)
        ivwyc = viewers.ImageViewer3D_Sliced_Contour(ax[1][phiw_a], utils.t2np(iW), utils.t2np(phiWarped), 1, 'warped Y', True)
        ivwzc = viewers.ImageViewer3D_Sliced_Contour(ax[2][phiw_a], utils.t2np(iW), utils.t2np(phiWarped), 2, 'warped Z', True)

    if vizImage is not None:
        ivvxc = viewers.ImageViewer3D_Sliced(ax[0][vizi_a], utils.lift_to_dimension(utils.t2np(vizImage), 3), 0, vizName + ' X', True)
        ivvyc = viewers.ImageViewer3D_Sliced(ax[1][vizi_a], utils.lift_to_dimension(utils.t2np(vizImage), 3), 1, vizName + ' Y', True)
        ivvzc = viewers.ImageViewer3D_Sliced(ax[2][vizi_a], utils.lift_to_dimension(utils.t2np(vizImage), 3), 2, vizName + ' Z', True)
    if extraImage is not None:
        ivexc = viewers.ImageViewer3D_Sliced(ax[0][ext_a], utils.lift_to_dimension(utils.t2np(extraImage), 3), 0, extraName + ' X', True)
        iveyc = viewers.ImageViewer3D_Sliced(ax[1][ext_a], utils.lift_to_dimension(utils.t2np(extraImage), 3), 1, extraName + ' Y', True)
        ivezc = viewers.ImageViewer3D_Sliced(ax[2][ext_a], utils.lift_to_dimension(utils.t2np(extraImage), 3), 2, extraName + ' Z', True)

    if iSL is not None and iTL is not None:
        ivslxc = viewers.ImageViewer3D_Sliced(ax[0][iSL_a], utils.lift_to_dimension(utils.t2np(iSL), 3), 0,
                                              'Lsource X', True, True)
        ivslyc = viewers.ImageViewer3D_Sliced(ax[1][iSL_a], utils.lift_to_dimension(utils.t2np(iSL), 3), 1,
                                              'Lsource Y', True, True)
        ivslzc = viewers.ImageViewer3D_Sliced(ax[2][iSL_a], utils.lift_to_dimension(utils.t2np(iSL), 3), 2,
                                              'Lsource Z', True, True)
        ivtlxc = viewers.ImageViewer3D_Sliced(ax[0][iTL_a], utils.lift_to_dimension(utils.t2np(iTL), 3), 0,
                                              'LTarget X', True, True)
        ivtlyc = viewers.ImageViewer3D_Sliced(ax[1][iTL_a], utils.lift_to_dimension(utils.t2np(iTL), 3), 1,
                                              'LTarget Y', True, True)
        ivtlzc = viewers.ImageViewer3D_Sliced(ax[2][iTL_a], utils.lift_to_dimension(utils.t2np(iTL), 3), 2,
                                              'LTarget Z', True, True)
        ivwlxc = viewers.ImageViewer3D_Sliced(ax[0][iWL_a], utils.lift_to_dimension(utils.t2np(iWL), 3), 0,
                                              'LWarped X', True, True)
        ivwlyc = viewers.ImageViewer3D_Sliced(ax[1][iWL_a], utils.lift_to_dimension(utils.t2np(iWL), 3), 1,
                                              'LWarped Y', True, True)
        ivwlzc = viewers.ImageViewer3D_Sliced(ax[2][iWL_a], utils.lift_to_dimension(utils.t2np(iWL), 3), 2,
                                              'LWarped Z', True, True)


    if visual_param is not None:
        if i==0 and visual_param['visualize']:
            plt.show()
        if visual_param['save_fig']:
            file_name = visual_param['pair_path'][i]
            join_p = lambda pth1,pth2: os.path.join(pth1, pth2)
            make_dir(join_p(visual_param['save_fig_path_byname'], file_name))
            make_dir(join_p(visual_param['save_fig_path_byiter'], visual_param['iter']))
            plt.savefig(join_p(join_p(visual_param['save_fig_path_byname'], file_name),visual_param['iter']+extension), dpi=dpi)
            plt.savefig(join_p(join_p(visual_param['save_fig_path_byiter'], visual_param['iter']), file_name+extension), dpi=dpi)
            plt.close('all')
    else:
        plt.show()
        plt.clf()


def show_current_images(iter, iS, iT, iW,iSL=None, iTL=None, iWL=None, vizImages=None, vizName=None, phiWarped=None, visual_param=None,extraImages=None, extraName= None):
    """
    Visualizes the current images during registration
    
    :param iter: iteration number 
    :param iS: source image BxCxXxYxZ (only displays B=0,C=0)
    :param iT: target image BxCxXxYxZ (only displays B=0,C=0)
    :param iW: warped image BxCxXxYxZ (only displays B=0,C=0)
    :param vizImage: custom visualization image XxYxZ
    :param vizName: name for this image
    :param phiWarped: warped map BxdimxXxYxZ (only displays B=0)
    """
    """
    Show current 2D registration results in relation to the source and target images
    :param iter: iteration number
    :param iS: source image
    :param iT: target image
    :param iW: current warped image
    :return: no return arguments
    """

    dim = iS.ndimension()-2

    if visual_param is not None:
        if visual_param['save_fig'] == True:
            save_fig_num = min(visual_param['save_fig_num'], len(visual_param['pair_path']))
            print("num {} of pair would be saved in {}".format(save_fig_num,visual_param['save_fig_path']))
        else:
            save_fig_num = 1
    else:
        save_fig_num = 1


    for i in range(save_fig_num):
        iSF = iS[i,0,...]
        iTF = iT[i,0,...]
        iWF = iW[i,0,...]
        iSLF = None
        iTLF = None
        iWLF = None

        if vizImages is not None:
            vizImage = vizImages[i,...]
        else:
            vizImage = None

        if extraImages is not None:
            extraImage = extraImages[i,0,...]
        else:
            extraImage = None


        if phiWarped is not None:
            pwF = phiWarped[i,...]
        else:
            pwF = None

        if iSL is not None and iTL is not None:
            iSLF = iSL[i, 0, ...]
            iTLF = iTL[i, 0, ...]
            iWLF = iWL[i, 0, ...]

        if dim==1:
            _show_current_images_1d(iSF, iTF, iWF, iter, vizImage, vizName, pwF, visual_param, i)
        elif dim==2:
            _show_current_images_2d(iSF, iTF, iWF,iSLF,iTLF,iWLF, iter, vizImage, vizName, pwF, visual_param, i)
        elif dim==3:
            _show_current_images_3d(iSF, iTF, iWF, iSLF, iTLF, iWLF, iter, vizImage, vizName, pwF, visual_param, i,extraImage, extraName)
        else:
            raise ValueError( 'Debug output only supported in 1D and 3D at the moment')

        '''
        plt.show(block=False)
        plt.draw_all(force=True)
    
        print( 'Click mouse to continue press any key to exit' )
        wasKeyPressed = plt.waitforbuttonpress()
        if wasKeyPressed:
            sys.exit()
        '''