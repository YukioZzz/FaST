import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
a = [806, 2409, 3913, 4956, 5412]
b = [25.997699, 79.746904, 129.953098, 164.802849, 179.826539]
c = [545.67, 253.29, 150.94, 119.67, 112.47]
d = [0.030, 0.090, 0.141, 0.195, 0.210]
e = [0.011, 0.032, 0.050, 0.070, 0.075]

plt.xlabel('Number of Replicas')
plt.ylabel('Normalized Overhead')
palette = sns.color_palette("mako_r", 5)

idx=[1, 3, 5, 7, 9]
a_normalized = [a[i]/a[0] for i in range(len(a))]
b_normalized = [b[i]/b[0] for i in range(len(b))]
d_normalized = [d[i]/d[0] for i in range(len(d))]
e_normalized = [e[i]/e[0] for i in range(len(e))]
c_normalized = [c[0]/c[i] for i in range(len(c))]

a_normalized_overhead = [a[i]/a[0]/idx[i] for i in range(len(a))]
b_normalized_overhead = [b[i]/b[0]/idx[i] for i in range(len(b))]
d_normalized_overhead = [d[i]/d[0]/idx[i] for i in range(len(d))]
e_normalized_overhead = [e[i]/e[0]/idx[i] for i in range(len(e))]

df = pd.DataFrame({'Throughput': a_normalized_overhead, 'QPS': b_normalized_overhead, 'SM Active': d_normalized_overhead, 'SM Occupancy': e_normalized_overhead}, index=idx)
fig = sns.lineplot(data=df,
     markers=True, dashes=False,
     palette=palette)
fig.figure.savefig('Overhead.pdf')


fig, ax = plt.subplots(figsize=(8, 6))

df = pd.DataFrame({'Throughput': a_normalized, 'QPS': b_normalized, '1/Latency': c_normalized, 'SM Active': d_normalized, 'SM Occupancy': e_normalized}, index=idx)
df.reset_index(inplace=True)
df.rename(columns={'index': 'index'}, inplace=True)
df_melted = pd.melt(df, id_vars=['index'], var_name='Metrics', value_name='Normalized Speed Up')
plt.xlabel('Number of Replicas')
fig = sns.barplot(x="index",y="Normalized Speed Up", hue="Metrics", data=df_melted, palette=palette, ax=ax)
plt.xlabel('Number of Replicas')
fig.figure.savefig('SpeedUp.pdf')

