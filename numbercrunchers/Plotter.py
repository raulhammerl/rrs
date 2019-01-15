import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import time 

sns.set_context('poster')
sns.set_color_codes()
plot_kwds = {'alpha' : 0.25, 's' : 80, 'linewidths':0}
from matplotlib import rcParams
rcParams['font.family'] = ['sans-serif']
rcParams['font.sans-serif'] = ['PF DinDisplay Pro']
yellow ='#FEDE3D'

channel_labels = {1: 'BR Klassik',
                2: 'Bayern 1',
                3: 'Bayern 3',
                4: 'B5 Aktuell',
                5: 'Puls',
                6: 'WDR2',
                43: 'WDR3',
                44: 'WDR4',
                41235:	"BR_Heimat",
                41236:	"Bayern+",
                41237:	"Bayern_2_Sued",
                41238:	"HR1",
                41239:	"HR2",
                41240:	"HR3",
                41241:	"HR4",
                41242: "You_FM",
                41243:	"MDR_Klassik",
                41244:	"MDR_Jump",
                41245:	"MDR_Sputnik",
                41264:	"NDR_90.3",
                41265:	"NDR2",
                41266:	"NDR_Spez",
                41267:	"NDR_Blue",
                41268:	"NDR1",
                41269:	"B888",
                41270:	"Fritz",
                41271:	"Radio_Eins"
                }

channel_genres = {1: 'Klassik',
                2: 'Folk-Rock',
                3: 'Oldies',
                4: 'Nachrichten',
                5: 'Jungend', # puls
                6: 'Nachrichten',
                43: 'Klassik', # WDR3
                44: 'Oldies', # WDR4
                41235:	"Volksmusik",
                41236:	"Schlager",
                41237:	"Nachrichten",
                41238:	"Oldies",
                41239:	"Klassik",
                41240:	"Oldies",
                41241:	"Schlager",
                41242: "Mainstream",
                41243:	"Klassik",
                41244:	"Mainstream",
                41245:	"Jugend",
                41264:	"Oldies",
                41265:	"Mainstream",
                41266:	"Nachrichten",
                41267:	"Alternativ",
                41268:	"Mainstream",
                41269:	"Mainstream",
                41270:	"Jugend",
                41271:	"Alternativ"
                }

def plot_clusters(data, algorithm, args, kwds):
    start_time = time.time()
    labels = algorithm(*args, **kwds).fit_predict(data)
    end_time = time.time()
    palette = sns.color_palette('deep', np.unique(labels).max() + 1)
    colors = [palette[x] if x >= 0 else (0.0, 0.0, 0.0) for x in labels]
    plt.scatter(data.T[0], data.T[1], c=colors, **plot_kwds)
    frame = plt.gca()
    plt.axis('off')
    plt.title('Clusters found by {}'.format(str(algorithm.__name__)), fontsize=20)
    plt.show()


def plot_real_clusters(data, target, label=None, title=None):
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


def plot_archetypes(data, target, arch_df, label=None, title=None, legend=None):
    # pallets 'deep' 'dark' 'bright'
    palette = sns.color_palette('deep', np.unique(target).max() + 1)
    colors = [palette[x] if x >= 0 else (0.0, 0.0, 0.0) for x in target]
    plt.scatter(data.T[0], data.T[1], c=colors, **plot_kwds)
    plt.axis('off')
    plt.scatter(arch_df[0], arch_df[1], c='r' ,marker='x')
    print(data)
    ## add the labels for each group
    if legend is None and label is not None:
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
    # add patches to graph 
    if legend is not None:
        patches = []
        for i in target.unique():
            patch = mpatches.Patch(color=palette[i], label=i)
            patches.append(patch)
        plt.legend(handles=patches, loc='best', fontsize=12, facecolor='none')

    # add title 
    if title is not None:
        plt.title('{}'.format(title), fontsize=24)
    plt.show()


def plot_genre_clusters(data, target, label=None, title=None):
    # change channel_target to genres 
    for x in range(len(target)):
        target.iloc[x] = channel_genres[target.iloc[x]]
    print(target)
    # 
    palette = sns.color_palette('deep', np.unique(target).max() + 1)
    colors = [palette[x] if x >= 0 else (0.0, 0.0, 0.0) for x in target]
    print(palette)
    plt.scatter(data.T[0], data.T[1], c=colors, **plot_kwds)
    plt.axis('off')
    
    # x = 0 
    for i in target.unique(): 
        # Position of each label.
        # x = x+1 
        xtext, ytext = np.mean(data[target==i], axis=0)
        text = i
        plt.annotate(text, (xtext, ytext),
                    horizontalalignment='center',
                    verticalalignment='center',
                    size=22, weight='bold',
                    color='white',
                    backgroundcolor=palette[x])
                     #color=palette[i]
    if title is not None:
        plt.title('Clusters found by {}'.format(title), fontsize=24)
    plt.show()
