import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt


sns.set_context('poster')
sns.set_color_codes()
plot_kwds = {'alpha' : 0.25, 's' : 80, 'linewidths':0}

channel_labels = {1: 'BR Klassik',
                2: 'Bayern 1',
                3: 'Bayern 3',
                4: 'B5 Aktuell',
                5: 'Puls',
                6: 'WDR2',
                }


def plot_clusters(self, data, algorithm, args, kwds):
    start_time = time.time()
    labels = algorithm(*args, **kwds).fit_predict(data)
    end_time = time.time()
    palette = sns.color_palette('deep', np.unique(labels).max() + 1)
    colors = [palette[x] if x >= 0 else (0.0, 0.0, 0.0) for x in labels]
    plt.scatter(data.T[0], data.T[1], c=colors, **plot_kwds)
    frame = plt.gca()
    plt.axis('off')
    plt.title('Clusters found by {}'.format(str(algorithm.__name__)), fontsize=20)
    # plt.text(0.1, 0.9, 'Clustering took {:.2f} s'.format(end_time - start_time), ha='center', va='center', transform=ax.transAxes, fontsize=14)
    plt.show()


def plot_real_clusters(self, data, target, label=None, title=None):
    palette = sns.color_palette('deep', np.unique(target).max() + 1)
    colors = [palette[x] if x >= 0 else (0.0, 0.0, 0.0) for x in target]
    plt.scatter(data.T[0], data.T[1], c=colors, **plot_kwds)
    plt.axis('off')

    ## add the labels for each group
    if label is not None:
        for i in target.unique():
            # Position of each label.
            xtext, ytext = np.mean(data[target==i], axis=0)
            if label == 'channel':
                text = channel_labels.get(i)
            elif label == 'show':
                text = i
            plt.annotate(text, (xtext, ytext),
                     horizontalalignment='center',
                     verticalalignment='center',
                     size=22, weight='bold',
                     color='white',
                     backgroundcolor=palette[i])
                     #color=palette[i]
    if title is not None:
        plt.title('Clusters found by {}'.format(title), fontsize=24)
    plt.show()


def plot_archetypes(data, target, arch_df, label=None, title=None):
    # arch_ind = [i[0] for i in archetypes]
    # arch_df = data[arch_ind]
    print(data)
    print(arch_df)

    palette = sns.color_palette('deep', np.unique(target).max() + 1)
    colors = [palette[x] if x >= 0 else (0.0, 0.0, 0.0) for x in target]
    plt.scatter(data[0], data[1], c=colors, **plot_kwds)
    plt.axis('off')
    plt.scatter(arch_df[0], arch_df[1], c='r' ,marker='x')
    ## add the labels for each group
    if label is not None:
        for i in target.unique():
            # Position of each label.
            xtext, ytext = np.mean(data[target==i], axis=0)
            if label == 'channel':
                text = channel_labels.get(i)
                color = 'white'
                backgroundcolor=palette[i]
                fontsize=22
            elif label == 'show':
                text = i
                color=palette[i]
                backgroundcolor=(0, 0, 0, 0) # transparent
                fontsize=18
            plt.annotate(text, (xtext, ytext),
                     horizontalalignment='center',
                     verticalalignment='center',
                     size=fontsize, weight='bold',
                     color=color,
                     backgroundcolor=backgroundcolor)

    if title is not None:
        plt.title('Clusters found by {}'.format(title), fontsize=24)
    plt.show()
