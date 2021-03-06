import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from utils.output import load_runs, set_plot_style

NETWORKS_NAMES = ['ff', 'snn', 'cnn']

if __name__ == '__main__':
    # Set plot style
    set_plot_style()

    # ========================= Extreme Learning ===========================
    for net in NETWORKS_NAMES:
        data = load_runs(f'extreme-{net}*')
        data.sort_values(['settings.train_hidden_1', 'settings.train_hidden_2'], inplace=True)

        data['nb_states'] = (data['settings.max_value'] - data['settings.min_value']) / data[
            'settings.inaccuracy_value']
        data['bits'] = np.log2(data['nb_states'])

        x = np.arange(len(data))
        width = 0.35  # the width of the bars

        fig, ax = plt.subplots()
        rects2 = ax.barh(x + width / 2, data['results.accuracy_ideal'], width, label='ideal')
        rects1 = ax.barh(x - width / 2, data['results.accuracy_low_resolution'], width,
                         label=f'low resolution ({data["bits"][0]} bits)')

        plt.yticks(x, (lab for lab in zip(data["settings.train_hidden_1"], data["settings.train_hidden_2"])))
        plt.title(f'Impact of not trainable layers on accuracy\n({data["network_info.name"][0]})')
        plt.xlabel('Accuracy')
        plt.ylabel('Hidden layer trained (1, 2)')
        ax.legend()
        plt.show(block=False)

    # ========================== Inaccuracy Value ==========================

    # Load selected runs files
    data = load_runs('inaccuracy_value*')

    data['nb_states'] = (data['settings.max_value'] - data['settings.min_value']) / data['settings.inaccuracy_value']
    data['bits'] = np.log2(data['nb_states'])

    sns.lineplot(data=data, x='bits', y='results.accuracy_low_resolution', hue='network_info.name')
    plt.title('Evolution of the testing accuracy depending of\nweights resolution')
    plt.xlabel('Resolution (bits)')
    plt.ylabel('Accuracy')
    plt.ylim([0, 1])
    plt.legend(title='Networks')
    plt.show(block=False)

    # ============================= Min / Max ==============================
    data = load_runs('weight_limits*ff*')
    data['diff'] = data['settings.max_value'] - data['settings.min_value']
    data['bits'] = np.round(np.log2(data['diff'] / data['settings.inaccuracy_value']))

    sns.lineplot(data=data, x='diff', y='results.accuracy_low_resolution', hue='bits')
    plt.title('Evolution of the testing accuracy depending of\nweights min / max and resolution (FeedForward)')
    plt.xlabel('Max - Min Weight value')
    plt.ylabel('Accuracy')
    plt.ylim([0, 1])
    plt.legend(title='Number of bits')
    plt.show(block=False)

    data = load_runs('weight_limits*cnn*')
    data['diff'] = data['settings.max_value'] - data['settings.min_value']
    data['bits'] = np.round(np.log2(data['diff'] / data['settings.inaccuracy_value']))

    sns.lineplot(data=data, x='diff', y='results.accuracy_low_resolution', hue='bits')
    plt.title('Evolution of the testing accuracy depending of\nweights min / max and resolution (CNN)')
    plt.xlabel('Max - Min Weight value')
    plt.ylabel('Accuracy')
    plt.ylim([0, 1])
    plt.legend(title='Number of bits')
    plt.show(block=False)

    data = load_runs('weight_limits*snn*')
    data['diff'] = data['settings.max_value'] - data['settings.min_value']
    data['bits'] = np.round(np.log2(data['diff'] / data['settings.inaccuracy_value']))

    sns.lineplot(data=data, x='diff', y='results.accuracy_low_resolution', hue='bits')
    plt.title('Evolution of the testing accuracy depending of\nweights min / max and resolution (SNN)')
    plt.xlabel('Max - Min Weight value')
    plt.ylabel('Accuracy')
    plt.ylim([0, 1])
    plt.legend(title='Number of bits')
    plt.show(block=False)

    # ============================== Nb Epoch ==============================
    data = load_runs('nb_epoch*')

    sns.lineplot(data=data, x='settings.nb_epoch', y='results.accuracy_low_resolution', hue='network_info.name')
    sns.lineplot(data=data, x='settings.nb_epoch', y='results.accuracy_ideal', hue='network_info.name',
                 dashes=[(2, 2), (2, 2)])
    plt.title('Evolution of the testing accuracy depending of\nthe number of training epoch')
    plt.xlabel('Number of training epoch')
    plt.ylabel('Accuracy')
    plt.legend(title='Networks')
    plt.show(block=False)

    # =========================== Nb Parameters ============================
    data = load_runs('size_hidden*')

    # ideal
    sns.lineplot(data=data, x='network_info.total_params', y='results.accuracy_ideal', hue='network_info.name')
    plt.title('Evolution of the testing accuracy depending of the number\n'
              'of parameters on the hidden layers (ideal)')
    plt.xlabel('Total number of parameters')
    plt.ylabel('Accuracy')
    plt.xlim([0, 115135])
    plt.ylim([0, 1])
    plt.legend(title='Networks')
    plt.show(block=False)

    # low_resolution
    sns.lineplot(data=data, x='network_info.total_params', y='results.accuracy_low_resolution', hue='network_info.name')
    plt.title('Evolution of the testing accuracy depending of the number\n'
              'of parameters on the hidden layers (low_resolution)')
    plt.xlabel('Total number of parameters')
    plt.ylabel('Accuracy')
    plt.xlim([0, 115135])
    plt.ylim([0, 1])
    plt.legend(title='Networks')
    plt.show(block=False)
