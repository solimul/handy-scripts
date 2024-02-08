import pandas as pd
import sys
import numpy as np

file_path = sys.argv[1]
timeout = int (sys.argv [2])
problemscount = 0


import matplotlib.pyplot as plt

markers = ['o', 's', '^', 'D', 'v', '<', '>', 'p', '*', 'H', '+', 'x', '|', '_', '.']  # Add more markers if needed

def plot_lines(A, title):
    for i, line_data in enumerate(A):
        t_i, a_i, b_i = line_data
        marker = markers[i % len(markers)]
        plt.plot(a_i, b_i, linestyle='-')
        plt.scatter(a_i[::250], b_i[::250], marker=marker, label=f'{t_i}')

    plt.xlabel('time', fontsize=20)
    plt.ylabel('solved instances', fontsize=20)
    plt.legend(fontsize=18, ncols=1)
    plt.title (title, fontsize=18, loc='left')
    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)
    plt.subplots_adjust(top=.7)
    plt.show()

df = pd.read_csv(file_path, sep=',')
grouped_data = df.groupby('configuration')

collection = []
for configuration, group in grouped_data:
    if 'restart' not in configuration:
        filtered_rows = group[group['result'].str.contains('SAT-VERIFIED')]
        problemscount = len (group)
        cputime_values = filtered_rows['cputime'].tolist()
        collection.append ([configuration, len (cputime_values), round ((2*timeout * (problemscount- len(cputime_values)) + np.nansum (cputime_values) / problemscount), 1), cputime_values])

sorted_collection = sorted(collection, key=lambda x: x[1], reverse= True)

cumulative = []


for st in sorted_collection:
    conf = st [0]
    solved = st [1]
    par2 = st [2]
    cputime = st [3]  
    
    c = 0
    t = []
    count = []
    for i in range (0, timeout+100):
        c += len ([n for n in cputime if n>i and n <= i+1])
        t.append (i+1)
        count.append (c)
    cumulative.append ([conf+' (solved: '+str (solved) + ', par2: '+ str (round (par2/10000, 0))+')', t, count])

# title="switch2: probsat gets first turn and interleaves with LiWeT in every 1M flips\n"
# title+="moveavg: probsat uses moving average of clause weights from LiWeT\n"
# title+="mcs: make-weight based clause selection\n"
title = "****************** 5355 benchmarks from 2022 SAT Competition Anniversary Track *******************\n\n"
title += "default: default tassat (TACAS24 submission)\n"
title += "liprob: default liprob\n"
#title += "switchonly\!-\!liprob: switching between ProbSAT and LiWeT in liprob, without performing any cooperation \n"
title += "portfolio: switching between tassat and liprob solvers; at switch always picks the best assignment found so far\n"

title = "****************** 1200 benchmarks from the maintrack of SAT Competition 2021,2022, and 2023 *******************\n\n"
title += "default: default tassat (TACAS24 submission)\n"
title += "liprob: default liprob\n"
# #title += "switchonly\!-\!liprob: switching between ProbSAT and LiWeT in liprob, without performing any cooperation \n"
title += "portfolio: switching between tassat and liprob solvers; at switch always picks the best assignment found so far\n"

formatted_lines = ""
for line in title.split('\n'):
    formatted_line = ' '.join([r"$\bf{" + word.rstrip(':') + ":}$" if ':' in word else word for word in line.split()])
    formatted_lines+=formatted_line+"\n"

plot_lines (cumulative, formatted_lines)
    #print ([conf, t, count])
    
