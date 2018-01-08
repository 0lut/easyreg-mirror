from time import time
import torch
from torch.autograd import Variable
from pipLine.utils import *
from models.networks import SimpleNet

record_path ='../data/records/learning/'
model_path = None
check_point_path = '../data/checkpoints'
reg= 1e-2



def train_model(opt,model, dataloaders,writer):
    since = time()
    experiment_name = opt['tsk_set']['tsk_name']
    period = opt['tsk_set'][('print_step', 10, 'num of steps to print')]
    num_epochs = opt['tsk_set'][('epoch', 100, 'num of epoch')]
    resume_training = opt['tsk_set'][('continue_train', False, 'continue to train')]
    model_path = opt['tsk_set'][('model_path', '', 'if continue_train, given the model path')]
    record_path = opt['tsk_set']['path'][('record_path', '', 'path of record')]
    best_model_wts = model.state_dict()
    best_loss = 0
    model = model.cuda()
    start_epoch = 0
    global_step = {x:0 for x in ['train','val']}
    period_loss = {x: 0. for x in ['train', 'val']}


    if resume_training:
        start_epoch, best_loss =resume_train(model_path, model)
    # else:
    #     model.apply(weights_init)

    for epoch in range(start_epoch, num_epochs):
        print('Epoch {}/{}'.format(epoch, num_epochs - 1))
        print('-' * 10)

        # Each epoch has a training and validation phase
        for phase in ['train', 'val']:
            save_per_epoch = 1
            if phase == 'train':
                model.train(True)  # Set model to training mode
            else:
                model.train(False)  # Set model to evaluate mode

            running_loss = 0.0

            # Iterate over data.
            for data in dataloaders[phase]:
                # get the inputs

                model.set_input(data)
                if phase == 'train':
                    model.optimize_parameters()
                elif phase =='val':
                    model.cal_val_errors()

                loss = model.get_current_errors()

                if epoch % 10 == 0 and save_per_epoch:
                    save_per_epoch = 0
                    appendix = 'epoch_' + str(epoch)
                    #save_result(record_path + phase + '_' + experiment_name+'/', appendix)

                #backward + optimize only if in training phase


                # statistics
                running_loss += loss.data[0]
                period_loss[phase] += loss.data[0]
                # save for tensorboard, both train and val will be saved
                global_step[phase] += 1
                if global_step[phase] > 1 and global_step[phase]%period == 0:
                    period_avg_loss = period_loss[phase] / period
                    writer.add_scalar('loss/'+phase, period_avg_loss, global_step[phase])
                    period_loss[phase] = 0.



            epoch_loss = running_loss / dataloaders['data_size'][phase]
            print('{} Loss: {:.4f}'.format(
                phase, epoch_loss))

            # deep copy the model
            if epoch == 0:
                best_loss = epoch_loss
            is_best =False
            if phase == 'val' and epoch_loss < best_loss:
                is_best = True
                best_loss = epoch_loss
                best_model_wts = model.state_dict()
            # save check point every epoch
            # only train phase would be saved
            if phase == 'val':
                save_checkpoint({'epoch': epoch,'state_dict': model.state_dict(),
                             'best_loss': best_loss}, is_best, check_point_path, 'epoch_'+str(epoch), 'reg_net')

        print()

    time_elapsed = time() - since
    print('Training complete in {:.0f}m {:.0f}s'.format(
        time_elapsed // 60, time_elapsed % 60))
    print('Best val Loss: {:4f}'.format(best_loss))

    # load best model weights
    model.load_state_dict(best_model_wts)
    return model
