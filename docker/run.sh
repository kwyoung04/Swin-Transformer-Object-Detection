docker run  -it \
            --gpus all \
            -d \
            -v /home/ubuntu/eric/Swin-Transformer-Object-Detection:$HOME/src/swint \
            -v /data/nia/4-2_221221/:$HOME/data \
            --env="DISPLAY" \
            --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
            --name $2 \
            --ipc=host \
            $1 \
            /bin/bash