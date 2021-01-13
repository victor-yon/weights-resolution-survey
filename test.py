import torch
from torch.nn import Module
from torch.utils.data import DataLoader, Dataset

from utils.logger import logger


def test(test_dataset: Dataset, network: Module) -> None:
    logger.info('Start network testing...')

    # Turn on the inference mode of the network
    network.eval()

    # Use the pyTorch data loader
    test_loader = DataLoader(test_dataset, batch_size=16, shuffle=True, num_workers=4)
    nb_batch = len(test_loader)

    nb_correct = 0
    nb_total = 0
    # Diable gradient for performances
    with torch.no_grad():
        # Iterate batches
        for i, data in enumerate(test_loader):
            logger.debug(f'Start testing batch {i + 1:03}/{nb_batch} ({i / nb_batch * 100:05.2f}%)')
            # Get the inputs: data is a list of [inputs, labels]
            inputs, labels = data

            # Forward
            outputs = network(inputs)
            _, predicted = torch.max(outputs, 1)  # Get the index of the max value for each image of the batch

            # Count the result
            nb_total += len(labels)
            nb_correct += torch.eq(predicted, labels).sum()

    logger.info(f'Test overall accuracy: {nb_correct / nb_total * 100:05.2f}%')

    logger.info('Network testing competed')