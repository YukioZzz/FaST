import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def draw_plot(fileName, ax):
    df = pd.read_csv(fileName+'.csv')
    df = df[df['metric_name']=='checks']
    df.index = pd.to_datetime(df['timestamp'], unit='s')
    df = df.loc[:, ['extra_tags']]
    counts = df.groupby('extra_tags').resample('S').size()
    counts = counts.rename('Throughput(req/s)')
    counts = counts.reset_index()
    counts['timestamp'] = (counts['timestamp'] - counts['timestamp'].min()).dt.total_seconds()
    #pd.set_option('display.max_rows', None)
    #counts
    # Plot the resulting DataFrame using Seaborn's lineplot with 'timestamp' on the x-axis, 'rps' on the y-axis, and 'type' as the hue
    
    def sliding_average(seq, window_size): #, start, last):
        #seq = fullseq[start:last]
        size = len(seq)
        seq = pd.concat([seq, seq[size-window_size:size]]) # append last window_size values
        averages = []
        for i in range(size):
            window = seq[i:i+window_size]
            averages.append(sum(window) / window_size)
        return averages
        #return pd.concat([fullseq[:start], pd.Series(averages), fullseq[last:]])
    
    def replace_with_average(seq, r):
        #seq = fullseq[start:end+1]
        for i in range(0, len(seq), r):
            end = min(i+r, len(seq))
            avg = sum(seq[i:end])/r
            for j in range(i, end):
                seq[j] = avg
        return seq #pd.concat([fullseq[0:start], seq, fullseq[end, len(fullseq)]])
    
    throughput = counts['Throughput(req/s)']
    timestamp = counts['timestamp']
    resnet_idx = counts['extra_tags'] == 'test_type=resnet'
    rnnt_idx = counts['extra_tags'] == 'test_type=rnnt'
    
    #throughput[resnet_idx] = range_filter(throughput[resnet_idx], 20, 0, 150, 450, 600)
    #throughput[resnet_idx] = range_filter(throughput[resnet_idx], 40, 0, 150, 450, 600)
    #throughput[rnnt_idx] = range_filter(throughput[rnnt_idx], 20, 0, 150, 450, 600)
    #throughput[rnnt_idx] = range_filter(throughput[rnnt_idx], 40, 0, 150, 450, 600)
    
    throughput[resnet_idx] = sliding_average(throughput[resnet_idx], 10)
    throughput[resnet_idx] = sliding_average(throughput[resnet_idx], 20)
    throughput[rnnt_idx] = sliding_average(throughput[rnnt_idx], 10)
    throughput[rnnt_idx] = sliding_average(throughput[rnnt_idx], 20)
    
    
    def get_range_averages(seq, r):
        range_averages = []
        for i in range(0, len(seq), r):
            end = min(i+r, len(seq))
            avg = sum(seq[i:end])/r
            range_averages.append(avg)
        return range_averages
    
    # replace values in the extra_tags column
    counts['extra_tags'].replace({'test_type=resnet': 'ResNet', 'test_type=rnnt': 'RNNT'}, inplace=True)
    # rename the extra_tags column to types
    counts.rename(columns={'extra_tags': 'types'}, inplace=True)
    counts.rename(columns={'timestamp': 'Time(s)'}, inplace=True)

    #range_averages = get_range_averages(counts['throughput(req/s)'], 20)
    
    #plt.plot(range(0, len(counts['throughput(req/s)']), 20), range_averages)
    #plt.show()
    sns.lineplot(data=counts, x='Time(s)', y='Throughput(req/s)', hue='types', ax=ax, legend=False)
    #plt.suptitle('Effective Spatial Sharing', fontsize=15)
    ax.legend(fontsize=13, title=None) 
    ax.set_ylabel('Throughput(req/s)', fontsize=15)
    plt.yticks(fontsize=14)
    plt.xticks(fontsize=14)
    ax.set_xlabel('Time(s)', fontsize=15)
    plt.savefig(fileName+".pdf", format="pdf", bbox_inches='tight')

#fig, axes = plt.subplots(1, 2, figsize=(8, 3))
#axes = axes.flatten()
fig, ax = plt.subplots(figsize=(4, 3))
fig.subplots_adjust(hspace=0.35, wspace=0.2)
draw_plot('time-fixed', ax)

fig, ax = plt.subplots(figsize=(4, 3))
fig.subplots_adjust(hspace=0.35, wspace=0.2)
draw_plot('space-fixed', ax)
## Show the plot
#fig = plt.gcf()
#fig.set_size_inches(8, 3)
#plt.savefig("vct.png", format="png", bbox_inches='tight')
