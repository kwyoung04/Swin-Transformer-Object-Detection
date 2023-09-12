GPUS=$1
PORT=${PORT:-29500}

#PYTHONPATH="$(dirname $0)/..":$PYTHONPATH \
#python -m torch.distributed.launch --nproc_per_node=$GPUS --master_port=$PORT \
#    $(dirname "$0")/train.py $CONFIG --launcher pytorch ${@:3}


python -m torch.distributed.launch --nproc_per_node=4 --master_port=$PORT tools/train.py configs/swin/nia_zeron.py --launcher pytorch ${@:3}