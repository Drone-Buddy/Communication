pushd ~
git clone --recursive https://github.com/awslabs/amazon-kinesis-video-streams-producer-sdk-cpp.git
sudo apt-get pkg-config cmake m4
sudo apt-get install libssl-dev libcurl4-openssl-dev liblog4cplus-dev libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev gstreamer1.0-plugins-base-apps gstreamer1.0-plugins-bad gstreamer1.0-plugins-good gstreamer1.0-plugins-ugly gstreamer1.0-tools
mkdir -p amazon-kinesis-video-streams-producer-sdk-cpp/build
cd amazon-kinesis-video-streams-producer-sdk-cpp/build
sudo apt-get install default-jdk
export JAVA_HOME=/usr/bin/java
cmake .. -DBUILD_GSTREAMER_PLUGIN=ON -DBUILD_JNI=TRUE -DBUILD_TEST=TRUE
make
cd ..
export LD_LIBRARY_PATH=`pwd`/open-source/local/lib
export GST_PLUGIN_PATH=`pwd`/build
popd
