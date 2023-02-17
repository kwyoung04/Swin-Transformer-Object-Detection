sudo /opt/conda/bin/python setup.py develop
pip install -r requirements.txt
## sudo /opt/conda/bin/pip uninstall pycocotools
## pip install mmpycocotools
## MMCV_WITH_OPS=1 FORCE_CUDA=1 pip install mmcv-full==1.4.0

python tools/test.py configs/swin/nia_zeron_origin.py work_dirs/nia_zeron/epoch_10.pth --eval bbox segm




##python mmdet/utils/collect_env.py