import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import time 
import pandas as pd

sns.set_context('poster')
sns.set_color_codes()
plot_kwds = {'alpha' : 0.25, 's' : 80, 'linewidths':0}
from matplotlib import rcParams
rcParams['font.family'] = ['sans-serif']
rcParams['font.sans-serif'] = ['PF DinDisplay Pro']
yellow ='#FEDE3D'

import Database

directory = "/Users/Raul/Dropbox/Documents/Uni/Bachelorarbeit/Database/"
database = Database.Database(directory)

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
                41242:  "You_FM",
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

channel_genres = {1: [1, 2, 3], #br klassik: 
                2: [7, 8, 14, 15, 18], #br1: Pop, Folk-Rock, Softrock, 70er, 80er
                3: [18, 19, 17, 16], # br3: Pop, Hits, Charts, Mainstream 
                4: [23, 24], #'B5 Aktuell'
                5: [20, 21, 22], # puls: Zeitgenössisch, alternativ, Jugend
                6: [24, 18, 12], #Wdr Infosender, pop, rock 
                43: [1, 24], # WDR3: Klassik, Inforadio
                44: [19, 8, 9, 7, 18], # WDR4:  Hits, 70er, 80er, “Oldies”, Pop
                41235:	[6, 4, 5], #BR_Heimat: Volksmusik, Blasmusik, Laienmusik
                41236:	[13, 4, 5], #Bayern Plus: Schlager, Blasmusik, Laienmusiksendungen
                41237:	[23, 24], #'Bayern_2': Berichterstattung, Nachrichten,
                41238:	[7,8,9,24], #HR1: “Oldies”, 70er, 80er, Inforadio 
                41239:	[24,1,3], #HR2: Inforadio, Kultur, Klassik, Jazz, 
                41240:	[18, 12, 8, 10], #HR3: Pop, Rock, 70er, 80er, Mainstream 
                41241:	[13, 19, 17, 16], #HR4 Schlager, Hits, Charts, Mainstream
                41242:  [16, 17, 18, 20, 21], #You FM: Mainstream, Charts, Pop, zeitgenössisch, Jugend
                41243:	[1,3], #"MDR_Klassik":
                41244:	[19, 16, 9, 10, 11], #MDR JUMP: Hits, Mainstream, 80er, 90er, 00er 
                41245:	[12, 18, 20], #MDR_Sputnik:
                41264:	[8, 9, 18, 16], #NDR_90.3 70er, 80er, Pop, Mainstream
                41265:	[9, 19, 16, 18, 12], #NDR2	80er, Hits, Mainstream, Pop, Rock
                41266:	[23, 24], #NDR Spez
                41267:	[22, 20, 21], #NDR Blue
                41268:	[9, 10, 18], #NDR1: 80er, 90er, Pop
                41269:	[18, 19, 16], #b888: Pop, Hits, Mainstream 
                41270:	[20, 21, 22], #Fritz: 
                41271:	[22] #Radio Eins
                }

genre_dict = { 
    1: 'Klassik',
    2: 'Opera',
    3: 'Jazz',
    4: 'Blasmusik',
    5: 'Laienmusik',
    6: 'Volksmusik',
    7: 'Oldies',
    8: '70er',
    9: '80er',
    10: '90er',
    11: '00er',
    12: 'Rock',
    13: 'Schlager',
    14: 'Folk-Rock',
    15: 'Softrock',
    16: 'Mainstream',
    17: 'Charts',
    18: 'Pop',
    19: 'Hits',
    20: 'zeitgenoessisch',
    21: 'Jugend',
    22: 'Alternativ',
    23: 'Nachrichten',
    24: 'Inforadio'
}



# Berichterstattung,  Independent, Urban, Electro, Hip-Hop, Kultur,  
# R&B, Rap, Rock, Elektropop,  60er, 
# Wetter, Sport, Politik 

# alternativ 
# Infosender, pop, rock 


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
    genre_target = []
    for x in range(len(target)):
        z = channel_genres[target.iloc[x]]
        genre_target.append(z)   
    main_genres = [item[0] for item in gerne_target[0]]

    palette = sns.color_palette('deep', np.unique(target).max() + 1)
    colors = [palette[x] if x >= 0 else (0.0, 0.0, 0.0) for x in main_genres]
    plt.scatter(data.T[0], data.T[1], c=colors, **plot_kwds)
    plt.axis('off')
    
    for i in target.unique(): 
        # Position of each label.
        xtext, ytext = np.mean(data[target==i], axis=0)
        text = genre_dict[i]
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

def plot_genre(data, target, genre, title=None, plot='show'):
    palette = sns.color_palette('deep', np.unique(target).max() + 1)
    grey = (170,170,170,0.1)

    # change channel_target to genres 
    genre_target = []
    for x in range(len(target)):
        z = channel_genres[target.iloc[x]]
        genre_target.append(z)
    # give points of certain genre color
    colors = [palette[genre] if genre in x else 'lightgrey' for x in genre_target]
    # scatter points 
    fig = plt.figure(figsize=(20, 10))
    # plot_kwds = {'alpha' : 0.5, 's' : 50, 'linewidths':0}
    plt.scatter(data.T[0], data.T[1], c=colors, **plot_kwds)
    plt.axis('off')
    
    # add label
    entities_of_genre = [True if genre in x else False for x in genre_target]
    xtext, ytext = np.mean(data[entities_of_genre], axis=0)
    text = genre_dict[genre]
    plt.annotate(text, (xtext, ytext),
                horizontalalignment='center',
                verticalalignment='center',
                size=22, weight='bold',
                color='white',
                backgroundcolor=palette[genre])

    if title is not None:
        plt.title('Clusters found by {}'.format(title), fontsize=24)
    if plot == 'save':
        file_name = "Cluster for genre:" + genre_dict[genre] + ".png"
        plt.savefig(file_name, dpi=230)
        fig.clf()
        print("saving plot to {}".format(file_name))
    else:
       plt.show()


def plot_each_genre(data, target):
    for genre in range(1, len(genre_dict)+1):
        title = "tSNE for genre: {}".format(genre_dict[genre])
        plot_genre(data, target, genre, title=title, plot='save')


def plot_with_annotation(data, target, show_target, label=None, title=None, legend=None):
    palette = sns.color_palette('deep', np.unique(target).max() + 1)
    colors = [palette[x] if x >= 0 else (0.0, 0.0, 0.0) for x in target]

    # names = pd.Series(names).values

    fig, ax = plt.subplots()
    plt.axis('off')
    annot = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
                        fontsize=20,
                        bbox=dict(boxstyle="round", fc="w"),
                        arrowprops=dict(arrowstyle="->"))
    annot.set_visible(False)

    sc = plt.scatter(data.T[0], data.T[1], c=colors, **plot_kwds)
    
    # data = Database.find_show_by_id()

    def update_annot(ind):
        pos = sc.get_offsets()[ind["ind"][0]]
        annot.xy = pos
        # text = "{}, {}".format(" ".join(list(map(str,ind["ind"]))), 
        #                     " ".join([names[n] for n in ind["ind"]]))
        indd = [ind["ind"][0]]
        int_indd = int(indd[0])
        show_id = show_target.iloc[int_indd]
        # recording_tuple = recording_target.iloc[int_indd]
        # path = recording_tuple[6]
        # link_audio_file(path)
        data = database.find_show_by_id(int(show_id))
        text = "{} {} \n channel id: {} \n show id: {} \n index: {}".format(data[2], data[3], str(data[1]), str(data[0]), str(int_indd))
        annot.set_text(text)
        annot.get_bbox_patch().set_facecolor((colors[ind["ind"][0]]))
        annot.get_bbox_patch().set_alpha(1)


    def hover(event):
        vis = annot.get_visible()
        if event.inaxes == ax:
            cont, ind = sc.contains(event)
            if cont:
                update_annot(ind)
                annot.set_visible(True)
                fig.canvas.draw_idle()
            else:
                if vis:
                    annot.set_visible(False)
                    fig.canvas.draw_idle()
    
    fig.canvas.mpl_connect("motion_notify_event", hover)
    plt.show()


def link_audio_file(path):
    """ftp:// username : pw @ server.com / path to file"""
    url = "ftp://raul:tschusch@gh0sthost.ddns.net/"+path 
    subprocess.Popen(['open', url])



