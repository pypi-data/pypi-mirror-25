import os
import respack


# ======== Base Usage ========

respack.set('pic.jpg')

# ...
# you can remove `pic.jpg` after respack.set() run once
# ...

path = respack.get('pic.jpg')

try:
    print('install Pillow to see this image')
    from PIL import Image
    im = Image.open(path)
    im.show()
except ImportError:
    print(path)



# ======== Advance Usage ========

# 1. custom target name
respack.set('./pic.jpg', 'mypic')
path = respack.get('mypic')
print(path)

# 2. custom resources root dir
respack.set('./pic.jpg')
path = respack.get('pic.jpg', resources_dir='./res_root/')
print(path)

# 3. use cache
respack.set('pic.jpg')
path = respack.get('pic.jpg', cached=True)
path = respack.get('pic.jpg', cached=True)  # will not release resource files again
print(path)



