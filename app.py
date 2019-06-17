from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import json
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d, Axes3D
import mpld3
import numpy as np

with open('vecs.json', 'r') as f:
    data = json.loads(f.read())

req_outside_labels = []
req_outside_lib = []
all_labels = list(data.keys())
all_vecs = list(data.values())


for vec in data:
    if data[vec][0] == 1:
        req_outside_lib.append(data[vec])
        req_outside_labels.append(vec)

req_norm = StandardScaler().fit_transform(req_outside_lib)
all_norm = StandardScaler().fit_transform(all_vecs)

pca = PCA(n_components=2)

req_principle = np.asarray(pca.fit_transform(req_norm))
all_principle = np.asarray(pca.fit_transform(all_norm))

# principle_req_df = pd.DataFrame(data = req_principle, columns = ['principle 1', 'principle 2', 'principle 3'])
principle_req_df = pd.DataFrame(data = req_principle, columns = ['principle 1', 'principle 2'])
# principle_all_df = pd.DataFrame(data = all_principle, columns = ['principal 1', 'principal 2', 'principal 3'])
# principle_all_df = pd.DataFrame(data = all_principle, columns = ['principle 1', 'principle 2'])

fig = plt.figure()
# ax = Axes3D(fig)
ax = fig.add_subplot()

# scatter = ax.scatter(principle_req_df['principle 1'], principle_req_df['principle 2'], principle_req_df['principle 3'])
scatter = ax.scatter(principle_req_df['principle 1'], principle_req_df['principle 2'])
# scatter = ax.scatter(principle_all_df['principle 1'], principle_all_df['principle 2'])

tooltip = mpld3.plugins.PointLabelTooltip(scatter, labels=req_outside_labels)
mpld3.plugins.connect(fig, tooltip)
mpld3.show()

fig2 = plt.figure()
ax2 = fig2.add_subplot()
boxes = ax2.bar(['Dependent','Independent'], [len(req_principle), len(all_principle) - len(req_principle)])
mpld3.plugins.connect(fig2)
# plt.show()
mpld3.show()
