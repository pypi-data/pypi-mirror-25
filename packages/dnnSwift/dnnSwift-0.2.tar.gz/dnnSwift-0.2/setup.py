from distutils.core import setup

setup(
    name='dnnSwift',
    version='0.2',
    packages=['dnnSwift'],
    description="Quick Convolutional Neural Network Implementation",
    url="https://github.com/DragonDuck/DNNSwift",
    license='GNU General Public License Version 3',
    install_requires=["numpy", "tensorflow", "h5py", "pygraphviz"],
    keywords=["Deep Learning", "Convolution", "Neural Network", 
              "DNN", "CNN", "Classification", "Classifier"]
)
