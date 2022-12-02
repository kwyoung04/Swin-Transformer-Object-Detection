docker run  -it \
            --gpus all \
            --rm \
            -v /home/ubuntu/eric/Swin-Transformer-Object-Detection:$HOME/src/swint \
            -v /data:$HOME/data \
            --env="DISPLAY" \
            --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
            --name $2 \
            --ipc=host \
            $1 \
            /bin/bash