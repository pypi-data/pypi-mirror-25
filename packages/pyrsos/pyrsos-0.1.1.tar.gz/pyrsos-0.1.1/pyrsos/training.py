import math
import sys

import torch


def sort_batch(lengths, others):
    """
    Sort batch data and labels by length.
    Useful for variable length inputs, for utilizing PackedSequences
    Args:
        lengths (nn.Tensor): tensor containing the lengths for the data
        others (iterable): training data or labels to sort according to lengths

    Returns:

    """
    batch_size = lengths.size(0)

    sorted_lengths, sorted_idx = lengths.sort()
    reverse_idx = torch.linspace(batch_size - 1, 0, batch_size).long()
    sorted_lengths = sorted_lengths[reverse_idx]

    return sorted_lengths, (lst[sorted_idx][reverse_idx] for lst in others)


def epoch_progress(loss, epoch, batch, batch_size,
                   dataset_size, interval=1, ppl=False):
    """
    Print the progress of the training for
    Args:
        loss (float): the average loss for the epoch
        epoch (int): the epoch
        batch (int): the batch
        batch_size (int): the batch size
        dataset_size (int): the training examples in the dataset
        interval (int): how often to update the progress
        ppl (bool): show the average perplexity of the model -> exp(loss)

    Returns:

    """
    batches = math.ceil(float(dataset_size) / batch_size)

    # if interval == 0, then use a sane default
    if interval == 0:
        interval = min([50, math.ceil(batches / 10)])

    if batch % interval != 0 and batch != batches:
        return

    count = batch * batch_size
    bar_len = 40
    filled_len = int(round(bar_len * count / float(dataset_size)))

    log_bar = '=' * filled_len + '-' * (bar_len - filled_len)

    log_losses = ' CE: {:.4f}'.format(loss)

    if ppl:
        log_losses += ', PPL: {:.4f}'.format(math.exp(loss))

    log_epoch = ' Epoch {}'.format(epoch)
    log_batches = ' Batch {}/{}'.format(batch, batches)
    _progress_str = "\r \r {} [{}] {} ... {}".format(log_epoch,
                                                     log_bar,
                                                     log_batches,
                                                     log_losses)
    sys.stdout.write(_progress_str)
    sys.stdout.flush()

    if batch == batches:
        print()
