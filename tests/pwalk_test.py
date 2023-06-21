from para_walk import pwalk


for root, dirs, files in pwalk("../", 5):
    print(root, dirs, files)
