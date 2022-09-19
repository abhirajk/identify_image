
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
workon iimg
pip3 install "picamera[array]"
pip3 install opencv-python
pip3 install RPi.GPIO
```
https://www.tensorflow.org/lite/guide/python#install_tensorflow_lite_for_python

Install Tensorflow Lite runtime
```commandline
python3 -m pip install tflite-runtime
```
https://www.okdo.com/getting-started/get-started-with-google-coral-and-raspberry-pi/
https://coral.ai/docs/accelerator/get-started/

Coral Google - USB Accelerator
```commandline
echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | sudo tee /etc/apt/sources.list.d/coral-edgetpu.list
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
sudo apt-get update

sudo apt-get install libedgetpu1-std
```

Run a test program
```commandline
mkdir coral && cd coral
git clone https://github.com/google-coral/tflite.git
cd tflite/python/examples/classification/
mkvirtualenv coral

bash install_requirements.sh
python3 classify_image.py \
    --model models/mobilenet_v2_1.0_224_inat_bird_quant_edgetpu.tflite \
    --labels models/inat_bird_labels.txt \
    --input images/parrot.jpg

ERROR: Segmentation Fault
```

Tried

https://coral.ai/docs/accelerator/get-started/#3-run-a-model-on-the-edge-tpu
```commandline
cd ~/coral
git clone https://github.com/google-coral/pycoral.git
cd pycoral
bash examples/install_requirements.sh classify_image.py
python3 examples/classify_image.py \
    --model test_data/mobilenet_v2_1.0_224_inat_bird_quant_edgetpu.tflite \
    --labels test_data/inat_bird_labels.txt \
    --input test_data/parrot.jpg
    
ERROR: No module named 'pycoral'
```
https://discuss.tensorflow.org/t/raspberry-pi-build-process-broken/5470

Fix pycoral
```commandline
python3 -m pip install --extra-index-url https://google-coral.github.io/py-repo/ pycoral~=2.0
python3 examples/classify_image.py \
    --model test_data/mobilenet_v2_1.0_224_inat_bird_quant_edgetpu.tflite \
    --labels test_data/inat_bird_labels.txt \
    --input test_data/parrot.jpg
    
*** EUREKA ****

cd ~/coral/tflite/python/examples/classification/
python3 classify_image.py \
    --model models/mobilenet_v2_1.0_224_inat_bird_quant_edgetpu.tflite \
    --labels models/inat_bird_labels.txt \
    --input images/parrot.jpg
    
*** EUREKA ****
```



