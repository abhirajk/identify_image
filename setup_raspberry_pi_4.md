
https://singleboardbytes.com/647/install-opencv-raspberry-pi-4.htm

Expand the Filesystem
```commandline
sudo raspi-config
```
Update Raspberry Pi
```commandline
sudo apt update
sudo apt upgrade
```
Install OpenCV dependencies
```commandline
sudo apt-get install libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev
sudo apt install libjpeg-dev libtiff5-dev libjasper-dev libpng-dev
sudo apt install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
sudo apt install libxvidcore-dev libx264-dev
sudo apt install libfontconfig1-dev libcairo2-dev
sudo apt install libgdk-pixbuf2.0-dev libpango1.0-dev
```
Virtual Environment
```commandline
sudo pip3 install virtualenv virtualenvwrapper
vi ~/.bashrc
```
Put location of venv in bashrc
```text
# virtualenv and virtualenvwrapper
export WORKON_HOME=$HOME/.virtualenvs
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
source /usr/local/bin/virtualenvwrapper.sh
```
Switch to virtual env
```commandline
source ~/.bashrc
mkvirtualenv iimg -p python3
pip3 install "picamera[array]"
pip3 install opencv-python
pip3 install RPi.GPIO
```
https://www.tensorflow.org/lite/guide/python#install_tensorflow_lite_for_python

Install Tensorflow Lite runtime
```commandline
python3 -m pip install tflite-runtime
```


