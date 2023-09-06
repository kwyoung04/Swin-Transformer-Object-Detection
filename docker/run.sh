docker run  -it \
            --gpus all \
            -d \
            -v /home/ubuntu/eric/swint-v2:$HOME/src/swint \
            -v /data/nia/4-2_221221/:$HOME/data \
            --env="DISPLAY" \
            --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
            --name swint-2.0 \
            --ipc=host \
            eric/swint:2.0 \
            /bin/bash