# install on windows

1. choose python 2.7.13 and pls use the X86 not the X86-X64 installer package.
2. install scipy by the 32bit installer package of exe.
3. change backend from tensorflow to theano
    search your file system and find the keras.json file. change the contends from tensorflow to theano.
4. download and install ffmpeg from ffmpeg.org
5. use pip install baseZhang

# install_requires

['numpy==1.12.1', 'pandas==0.19.2', 'matplotlib==2.0.0', 'h5py==2.7.0', 'tqdm==4.11.2',
                      'PyAudio==0.2.11', 'pydub==0.18.0', 'pyPdf==1.13', 'PyYAML==3.12', 'six==1.10.0',
                      'SoundFile==0.9.0.post1', 'Theano==0.9.0', 'scikit-learn==0.18.1', 'Keras==1.2.2'],
 