import besca as bc
import matplotlib.pyplot as plt
adata = bc.datasets.pbmc3k_raw()
fig, ax = plt.subplots(1)
bc.pl.library_size(adata,ax=ax)