import os
import torch


class AverageMeter(object):
    """Computes and stores the average and current value"""

    def __init__(self):
        self.count = 0
        self.sum = 0
        self.avg = 0
        self.val = 0

    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count


def accuracy(output, target, topk=(1,)):
    """Computes the precision@k for the specified values of k"""
    maxk = max(topk)
    batch_size = target.size(0)

    _, pred = output.topk(maxk, 1, True, True)
    pred = pred.t()
    correct = pred.eq(target.reshape(1, -1).expand_as(pred))

    res = []
    for k in topk:
        correct_k = correct[:k].reshape(-1).float().sum(0, keepdim=True)
        wrong_k = batch_size - correct_k
        res.append(wrong_k.mul_(100.0 / batch_size))

    return res
    # return res, pred[:1].squeeze(0)


def save_checkpoint(state, is_best, args):
    directory = args.log_dir
    filename = directory + f"/checkpoint_{state['epoch']}.pth"

    if not os.path.exists(directory):
        os.makedirs(directory)

    torch.save(state, filename)

    if is_best:
        filename = directory + "/model_best.pth"
        torch.save(state, filename)
