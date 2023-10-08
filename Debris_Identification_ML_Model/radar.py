from matplotlib import pyplot as plt
import numpy as np

statsLabel = ['HP', 'Attack', 'Defense', 'Sp. Attack', 'Sp. Defense', 'Speed']
stats = [77, 83, 77, 74, 77, 66]

angles = np.linspace(0, 2*np.pi, len(statsLabel), endpoint=False)
angles = np.concatenate((angles, [angles[0]]))
fig = plt.figure()
ax = fig.add_subplot(111, polar=True)

stats = np.concatenate((stats, [stats[0]]))
ax.plot(angles, stats, linewidth=1, linestyle='solid', label="First Set")
ax.fill(angles, stats, alpha=0.1)
ax.set_thetagrids(angles[:-1] * 180/np.pi, statsLabel)
for angle, value in zip(angles, stats):
    ax.text(angle, value+10, str(value))

# create inset axis (origin at 0, 0 and with height and width of 1
# and use zorder to set behind current axes)
axins = ax.inset_axes([0, 0, 1, 1], polar=False, zorder=-10)

img = plt.imread("/Users/priyanshukumarsaw/Downloads/WhatsApp Image 2023-10-08 at 3.04.54 PM.jpeg")

# Reduce the transparency by changing the alpha value
axins.imshow(img, alpha=0.6)  # Adjust alpha here

# remove axes spines
axins.spines[["right", "left", "bottom", "top"]].set_visible(False)
axins.xaxis.set_tick_params(labelbottom=False)
axins.yaxis.set_tick_params(labelleft=False)
axins.set_xticks([])
axins.set_yticks([])

plt.show()
