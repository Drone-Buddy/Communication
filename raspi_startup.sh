apt-get install ./raspberrypi-kernel-headers_1.20200819-1_armhf.deb
apt-get install ./picocom_3.1-2_armhf.deb
apt-get install ./minicom_2.7.1-1_armhf.deb
cp -r /media/pi/LIVE/Quectel_Linux_USB_Driver /home/pi/Desktop
cd /home/pi/Desktop/Quectel_Linux_USB_Driver
make
make install
echo 'Needs to Reboot now.'