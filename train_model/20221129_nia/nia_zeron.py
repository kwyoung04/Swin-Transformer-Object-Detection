ANNO_FILE0 = '/home/ubuntu/data/train/coco/annotations/instance_train2017.json'
ANNO_FILE = '/home/ubuntu/src/swint/tools/fixed_sample.json'
model = dict(
    type='CascadeRCNN',
    pretrained='work_dirs/nia_zeron/epoch_10.pth',
    backbone=dict(
        type='SwinTransformer',
        embed_dim=128,
        depths=[2, 2, 18, 2],
        num_heads=[4, 8, 16, 32],
        window_size=7,
        mlp_ratio=4.0,
        qkv_bias=True,
        qk_scale=None,
        drop_rate=0.0,
        attn_drop_rate=0.0,
        drop_path_rate=0.3,
        ape=False,
        patch_norm=True,
        out_indices=(0, 1, 2, 3),
        use_checkpoint=False),
    neck=dict(
        type='FPN',
        in_channels=[128, 256, 512, 1024],
        out_channels=256,
        num_outs=5),
    rpn_head=dict(
        type='RPNHead',
        in_channels=256,
        feat_channels=256,
        anchor_generator=dict(
            type='AnchorGenerator',
            scales=[8],
            ratios=[0.5, 1.0, 2.0],
            strides=[4, 8, 16, 32, 64]),
        bbox_coder=dict(
            type='DeltaXYWHBBoxCoder',
            target_means=[0.0, 0.0, 0.0, 0.0],
            target_stds=[1.0, 1.0, 1.0, 1.0]),
        loss_cls=dict(
            type='CrossEntropyLoss', use_sigmoid=True, loss_weight=1.0),
        loss_bbox=dict(
            type='SmoothL1Loss', beta=0.1111111111111111, loss_weight=1.0)),
    roi_head=dict(
        type='CascadeRoIHead',
        num_stages=3,
        stage_loss_weights=[1, 0.5, 0.25],
        bbox_roi_extractor=dict(
            type='SingleRoIExtractor',
            roi_layer=dict(type='RoIAlign', output_size=7, sampling_ratio=0),
            out_channels=256,
            featmap_strides=[4, 8, 16, 32]),
        bbox_head=[
            dict(
                type='ConvFCBBoxHead',
                num_shared_convs=4,
                num_shared_fcs=1,
                in_channels=256,
                conv_out_channels=256,
                fc_out_channels=1024,
                roi_feat_size=7,
                num_classes=161,
                bbox_coder=dict(
                    type='DeltaXYWHBBoxCoder',
                    target_means=[0.0, 0.0, 0.0, 0.0],
                    target_stds=[0.1, 0.1, 0.2, 0.2]),
                reg_class_agnostic=False,
                reg_decoded_bbox=True,
                norm_cfg=dict(type='SyncBN', requires_grad=True),
                loss_cls=dict(
                    type='CrossEntropyLoss',
                    use_sigmoid=False,
                    loss_weight=1.0),
                loss_bbox=dict(type='GIoULoss', loss_weight=10.0)),
            dict(
                type='ConvFCBBoxHead',
                num_shared_convs=4,
                num_shared_fcs=1,
                in_channels=256,
                conv_out_channels=256,
                fc_out_channels=1024,
                roi_feat_size=7,
                num_classes=161,
                bbox_coder=dict(
                    type='DeltaXYWHBBoxCoder',
                    target_means=[0.0, 0.0, 0.0, 0.0],
                    target_stds=[0.05, 0.05, 0.1, 0.1]),
                reg_class_agnostic=False,
                reg_decoded_bbox=True,
                norm_cfg=dict(type='SyncBN', requires_grad=True),
                loss_cls=dict(
                    type='CrossEntropyLoss',
                    use_sigmoid=False,
                    loss_weight=1.0),
                loss_bbox=dict(type='GIoULoss', loss_weight=10.0)),
            dict(
                type='ConvFCBBoxHead',
                num_shared_convs=4,
                num_shared_fcs=1,
                in_channels=256,
                conv_out_channels=256,
                fc_out_channels=1024,
                roi_feat_size=7,
                num_classes=161,
                bbox_coder=dict(
                    type='DeltaXYWHBBoxCoder',
                    target_means=[0.0, 0.0, 0.0, 0.0],
                    target_stds=[0.033, 0.033, 0.067, 0.067]),
                reg_class_agnostic=False,
                reg_decoded_bbox=True,
                norm_cfg=dict(type='SyncBN', requires_grad=True),
                loss_cls=dict(
                    type='CrossEntropyLoss',
                    use_sigmoid=False,
                    loss_weight=1.0),
                loss_bbox=dict(type='GIoULoss', loss_weight=10.0))
        ],
        mask_roi_extractor=dict(
            type='SingleRoIExtractor',
            roi_layer=dict(type='RoIAlign', output_size=14, sampling_ratio=0),
            out_channels=256,
            featmap_strides=[4, 8, 16, 32]),
        mask_head=dict(
            type='FCNMaskHead',
            num_convs=4,
            in_channels=256,
            conv_out_channels=256,
            num_classes=161,
            loss_mask=dict(
                type='CrossEntropyLoss', use_mask=True, loss_weight=1.0))),
    train_cfg=dict(
        rpn=dict(
            assigner=dict(
                type='MaxIoUAssigner',
                pos_iou_thr=0.7,
                neg_iou_thr=0.3,
                min_pos_iou=0.3,
                match_low_quality=True,
                ignore_iof_thr=-1),
            sampler=dict(
                type='RandomSampler',
                num=256,
                pos_fraction=0.5,
                neg_pos_ub=-1,
                add_gt_as_proposals=False),
            allowed_border=0,
            pos_weight=-1,
            debug=False),
        rpn_proposal=dict(
            nms_across_levels=False,
            nms_pre=2000,
            nms_post=2000,
            max_per_img=2000,
            nms=dict(type='nms', iou_threshold=0.7),
            min_bbox_size=0),
        rcnn=[
            dict(
                assigner=dict(
                    type='MaxIoUAssigner',
                    pos_iou_thr=0.5,
                    neg_iou_thr=0.5,
                    min_pos_iou=0.5,
                    match_low_quality=False,
                    ignore_iof_thr=-1),
                sampler=dict(
                    type='RandomSampler',
                    num=512,
                    pos_fraction=0.25,
                    neg_pos_ub=-1,
                    add_gt_as_proposals=True),
                mask_size=28,
                pos_weight=-1,
                debug=False),
            dict(
                assigner=dict(
                    type='MaxIoUAssigner',
                    pos_iou_thr=0.6,
                    neg_iou_thr=0.6,
                    min_pos_iou=0.6,
                    match_low_quality=False,
                    ignore_iof_thr=-1),
                sampler=dict(
                    type='RandomSampler',
                    num=512,
                    pos_fraction=0.25,
                    neg_pos_ub=-1,
                    add_gt_as_proposals=True),
                mask_size=28,
                pos_weight=-1,
                debug=False),
            dict(
                assigner=dict(
                    type='MaxIoUAssigner',
                    pos_iou_thr=0.7,
                    neg_iou_thr=0.7,
                    min_pos_iou=0.7,
                    match_low_quality=False,
                    ignore_iof_thr=-1),
                sampler=dict(
                    type='RandomSampler',
                    num=512,
                    pos_fraction=0.25,
                    neg_pos_ub=-1,
                    add_gt_as_proposals=True),
                mask_size=28,
                pos_weight=-1,
                debug=False)
        ]),
    test_cfg=dict(
        rpn=dict(
            nms_across_levels=False,
            nms_pre=1000,
            nms_post=1000,
            max_per_img=1000,
            nms=dict(type='nms', iou_threshold=0.7),
            min_bbox_size=0),
        rcnn=dict(
            score_thr=0.05,
            nms=dict(type='nms', iou_threshold=0.5),
            max_per_img=100,
            mask_thr_binary=0.5)))
dataset_type = 'CocoDataset'
data_root = '/home/ubuntu/data/train/'
classes = (
    'table tennis racket', 'bench', 'toilet bowl', 'toothbrush', 'keyboard',
    'trash bin', 'recorder', 'violin', 'silicon spatula', 'watermelon',
    'scissors', 'handbag', 'tv', 'cutlery', 'pan', 'cake', 'traffic light',
    'garlic', 'couch', 'defibrillator', 'knives', 'squash',
    'blood glucose meter', 'person', 'watch', 'book', 'egg plant', 'toaster',
    'camera', 'cucumber', 'umbrella', 'donut', 'basketball hoop', 'truck',
    'washstand', 'potato', 'drone', 'guitar', 'radish', 'chair', 'golf club',
    'goalpost', 'lettuce', 'hair brush', 'spring onion', 'rice spatula',
    'microwave', 'speaker', 'doll', 'bowl', 'backpack', 'gas stove', 'fan',
    'ball', 'fire extinguisher', 'door', 'Billiards cue', 'table', 'ocarina',
    'treadmill', 'skating shoes', 'cabbage', 'xylophone', 'chicken',
    'pizza', 'car', 'orange', 'sign', 'mirror', 'pear', 'scooter', 'mouse',
    'plate', 'icecream', 'bus', 'muffler', 'pimento', 'Castanets', 'tray',
    'banana', 'hotdog', 'badminton racket', 'cat', 'dish washer', 'laptop',
    'plum', 'plate(skis)', 'dumbbell', 'carabiner', 'sushi', 'poles',
    'rice cooker', 'roof', 'perilla leaf', 'tomato', 'peach', 'window',
    'gimbap', 'tie', 'motorcycle', 'dog', 'bicycle', 'grape', 'purifier',
    'lamp', 'apple', 'mug', 'ladle', 'carrot', 'melon', 'board',
    'chopping boards', 'pot', 'bed', 'hat', 'vegetable peeler', 'cell phone',
    'bird', 'tteokbokki', 'pumpkin', 'sphygmomanometer', 'persimmon', 'kimchi',
    'massage gun', 'tennis racket', 'piano', 'refrigerator', 'clock', 'chili',
    'side dish', 'strawberry', 'flute', 'corn', 'tree', 'building',
    'background_out', 'box grater', 'onion', 'hair drier', 'hamburger',
    'ttoke', 'thermometer', 'white bread', 'Tambourine', 'air conditioner',
    'fire hydrant', 'sandwich', 'pilates equipment', 'gonggibap',
    'espresso machine', 'ceiling', 'floor', 'wall', 'pillar', 'background_in',
    'road', 'pavement', 'sky', 'sweet potato', 'mandu', 'suitcase')
img_norm_cfg = dict(
    mean=[123.675, 116.28, 103.53], std=[58.395, 57.12, 57.375], to_rgb=True)
train_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(type='LoadAnnotations', with_bbox=True, with_mask=True),
    dict(type='RandomFlip', flip_ratio=0.5),
    dict(
        type='AutoAugment',
        policies=[[{
            'type':
            'Resize',
            'img_scale': [(480, 1333), (512, 1333), (544, 1333), (576, 1333),
                          (608, 1333), (640, 1333), (672, 1333), (704, 1333),
                          (736, 1333), (768, 1333), (800, 1333)],
            'multiscale_mode':
            'value',
            'keep_ratio':
            True
        }],
                  [{
                      'type': 'Resize',
                      'img_scale': [(400, 1333), (500, 1333), (600, 1333)],
                      'multiscale_mode': 'value',
                      'keep_ratio': True
                  }, {
                      'type': 'RandomCrop',
                      'crop_type': 'absolute_range',
                      'crop_size': (768, 1200),
                      'allow_negative_crop': True
                  }, {
                      'type':
                      'Resize',
                      'img_scale': [(480, 1333), (512, 1333), (544, 1333),
                                    (576, 1333), (608, 1333), (640, 1333),
                                    (672, 1333), (704, 1333), (736, 1333),
                                    (768, 1333), (800, 1333)],
                      'multiscale_mode':
                      'value',
                      'override':
                      True,
                      'keep_ratio':
                      True
                  }]]),
    dict(
        type='Normalize',
        mean=[123.675, 116.28, 103.53],
        std=[58.395, 57.12, 57.375],
        to_rgb=True),
    dict(type='Pad', size_divisor=32),
    dict(type='DefaultFormatBundle'),
    dict(type='Collect', keys=['img', 'gt_bboxes', 'gt_labels', 'gt_masks'])
]
test_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(
        type='MultiScaleFlipAug',
        img_scale=(1333, 800),
        flip=False,
        transforms=[
            dict(type='Resize', keep_ratio=True),
            dict(type='RandomFlip'),
            dict(
                type='Normalize',
                mean=[123.675, 116.28, 103.53],
                std=[58.395, 57.12, 57.375],
                to_rgb=True),
            dict(type='Pad', size_divisor=32),
            dict(type='ImageToTensor', keys=['img']),
            dict(type='Collect', keys=['img'])
        ])
]
data = dict(
    samples_per_gpu=8,
    workers_per_gpu=2,
    train=dict(
        type='CocoDataset',
        ann_file='/home/ubuntu/src/swint/tools/fixed_sample.json',
        img_prefix='/home/ubuntu/data/train/fix_test/image/',
        classes=('table tennis racket', 'bench', 'toilet bowl', 'toothbrush',
                 'keyboard', 'trash bin', 'recorder', 'violin',
                 'silicon spatula', 'watermelon', 'scissors', 'handbag', 'tv',
                 'cutlery', 'pan', 'cake', 'traffic light', 'garlic', 'couch',
                 'defibrillator', 'knives', 'squash', 'blood glucose meter',
                 'person', 'watch', 'book', 'egg plant', 'toaster', 'camera',
                 'cucumber', 'umbrella', 'donut', 'basketball hoop', 'truck',
                 'washstand', 'potato', 'drone', 'guitar', 'radish', 'chair',
                 'golf club', 'goalpost', 'lettuce', 'hair brush',
                 'spring onion', 'rice spatula', 'microwave', 'speaker',
                 'doll', 'bowl', 'backpack', 'gas stove', 'fan', 'ball',
                 'fire extinguisher', 'door', 'Billiards cue', 'table',
                 'ocarina', 'treadmill', 'skating shoes', 'cabbage',
                 'xylophone', 'chicken', 'pizza', 'car', 'orange', 'sign',
                 'mirror', 'pear', 'scooter', 'mouse', 'plate', 'icecream',
                 'bus', 'muffler', 'pimento', 'Castanets', 'tray', 'banana',
                 'hotdog', 'badminton racket', 'cat', 'dish washer', 'laptop',
                 'plum', 'plate(skis)', 'dumbbell', 'carabiner', 'sushi',
                 'poles', 'rice cooker', 'roof', 'perilla leaf', 'tomato',
                 'peach', 'window', 'gimbap', 'tie', 'motorcycle', 'dog',
                 'bicycle', 'grape', 'purifier', 'lamp', 'apple', 'mug',
                 'ladle', 'carrot', 'melon', 'board', 'chopping boards', 'pot',
                 'bed', 'hat', 'vegetable peeler', 'cell phone', 'bird',
                 'tteokbokki', 'pumpkin', 'sphygmomanometer', 'persimmon',
                 'kimchi', 'massage gun', 'tennis racket', 'piano',
                 'refrigerator', 'clock', 'chili', 'side dish', 'strawberry',
                 'flute', 'corn', 'tree', 'building', 'background_out',
                 'box grater', 'onion', 'hair drier', 'hamburger', 'ttoke',
                 'thermometer', 'white bread', 'Tambourine', 'air conditioner',
                 'fire hydrant', 'sandwich', 'pilates equipment', 'gonggibap',
                 'espresso machine', 'ceiling', 'floor', 'wall', 'pillar',
                 'background_in', 'road', 'pavement', 'sky', 'sweet potato',
                 'mandu', 'suitcase'),
        pipeline=[
            dict(type='LoadImageFromFile'),
            dict(type='LoadAnnotations', with_bbox=True, with_mask=True),
            dict(type='RandomFlip', flip_ratio=0.5),
            dict(
                type='AutoAugment',
                policies=[[{
                    'type':
                    'Resize',
                    'img_scale': [(480, 1333), (512, 1333), (544, 1333),
                                  (576, 1333), (608, 1333), (640, 1333),
                                  (672, 1333), (704, 1333), (736, 1333),
                                  (768, 1333), (800, 1333)],
                    'multiscale_mode':
                    'value',
                    'keep_ratio':
                    True
                }],
                          [{
                              'type': 'Resize',
                              'img_scale': [(400, 1333), (500, 1333),
                                            (600, 1333)],
                              'multiscale_mode': 'value',
                              'keep_ratio': True
                          }, {
                              'type': 'RandomCrop',
                              'crop_type': 'absolute_range',
                              'crop_size': (768, 1200),
                              'allow_negative_crop': True
                          }, {
                              'type':
                              'Resize',
                              'img_scale': [(480, 1333), (512, 1333),
                                            (544, 1333), (576, 1333),
                                            (608, 1333), (640, 1333),
                                            (672, 1333), (704, 1333),
                                            (736, 1333), (768, 1333),
                                            (800, 1333)],
                              'multiscale_mode':
                              'value',
                              'override':
                              True,
                              'keep_ratio':
                              True
                          }]]),
            dict(
                type='Normalize',
                mean=[123.675, 116.28, 103.53],
                std=[58.395, 57.12, 57.375],
                to_rgb=True),
            dict(type='Pad', size_divisor=32),
            dict(type='DefaultFormatBundle'),
            dict(
                type='Collect',
                keys=['img', 'gt_bboxes', 'gt_labels', 'gt_masks'])
        ]),
    val=dict(
        type='CocoDataset',
        ann_file='/home/ubuntu/src/swint/tools/fixed_sample.json',
        img_prefix='/home/ubuntu/data/train/fix_test/image/',
        classes=('table tennis racket', 'bench', 'toilet bowl', 'toothbrush',
                 'keyboard', 'trash bin', 'recorder', 'violin',
                 'silicon spatula', 'watermelon', 'scissors', 'handbag', 'tv',
                 'cutlery', 'pan', 'cake', 'traffic light', 'garlic', 'couch',
                 'defibrillator', 'knives', 'squash', 'blood glucose meter',
                 'person', 'watch', 'book', 'egg plant', 'toaster', 'camera',
                 'cucumber', 'umbrella', 'donut', 'basketball hoop', 'truck',
                 'washstand', 'potato', 'drone', 'guitar', 'radish', 'chair',
                 'golf club', 'goalpost', 'lettuce', 'hair brush',
                 'spring onion', 'rice spatula', 'microwave', 'speaker',
                 'doll', 'bowl', 'backpack', 'gas stove', 'fan', 'ball',
                 'fire extinguisher', 'door', 'Billiards cue', 'table',
                 'ocarina', 'treadmill', 'skating shoes', 'cabbage',
                 'xylophone', 'chicken', 'pizza', 'car', 'orange', 'sign',
                 'mirror', 'pear', 'scooter', 'mouse', 'plate', 'icecream',
                 'bus', 'muffler', 'pimento', 'Castanets', 'tray', 'banana',
                 'hotdog', 'badminton racket', 'cat', 'dish washer', 'laptop',
                 'plum', 'plate(skis)', 'dumbbell', 'carabiner', 'sushi',
                 'poles', 'rice cooker', 'roof', 'perilla leaf', 'tomato',
                 'peach', 'window', 'gimbap', 'tie', 'motorcycle', 'dog',
                 'bicycle', 'grape', 'purifier', 'lamp', 'apple', 'mug',
                 'ladle', 'carrot', 'melon', 'board', 'chopping boards', 'pot',
                 'bed', 'hat', 'vegetable peeler', 'cell phone', 'bird',
                 'tteokbokki', 'pumpkin', 'sphygmomanometer', 'persimmon',
                 'kimchi', 'massage gun', 'tennis racket', 'piano',
                 'refrigerator', 'clock', 'chili', 'side dish', 'strawberry',
                 'flute', 'corn', 'tree', 'building', 'background_out',
                 'box grater', 'onion', 'hair drier', 'hamburger', 'ttoke',
                 'thermometer', 'white bread', 'Tambourine', 'air conditioner',
                 'fire hydrant', 'sandwich', 'pilates equipment', 'gonggibap',
                 'espresso machine', 'ceiling', 'floor', 'wall', 'pillar',
                 'background_in', 'road', 'pavement', 'sky', 'sweet potato',
                 'mandu', 'suitcase'),
        pipeline=[
            dict(type='LoadImageFromFile'),
            dict(
                type='MultiScaleFlipAug',
                img_scale=(1333, 800),
                flip=False,
                transforms=[
                    dict(type='Resize', keep_ratio=True),
                    dict(type='RandomFlip'),
                    dict(
                        type='Normalize',
                        mean=[123.675, 116.28, 103.53],
                        std=[58.395, 57.12, 57.375],
                        to_rgb=True),
                    dict(type='Pad', size_divisor=32),
                    dict(type='ImageToTensor', keys=['img']),
                    dict(type='Collect', keys=['img'])
                ])
        ]),
    test=dict(
        type='CocoDataset',
        ann_file='/home/ubuntu/src/swint/tools/fixed_sample.json',
        img_prefix='/home/ubuntu/data/train/fix_test/image/',
        classes=('table tennis racket', 'bench', 'toilet bowl', 'toothbrush',
                 'keyboard', 'trash bin', 'recorder', 'violin',
                 'silicon spatula', 'watermelon', 'scissors', 'handbag', 'tv',
                 'cutlery', 'pan', 'cake', 'traffic light', 'garlic', 'couch',
                 'defibrillator', 'knives', 'squash', 'blood glucose meter',
                 'person', 'watch', 'book', 'egg plant', 'toaster', 'camera',
                 'cucumber', 'umbrella', 'donut', 'basketball hoop', 'truck',
                 'washstand', 'potato', 'drone', 'guitar', 'radish', 'chair',
                 'golf club', 'goalpost', 'lettuce', 'hair brush',
                 'spring onion', 'rice spatula', 'microwave', 'speaker',
                 'doll', 'bowl', 'backpack', 'gas stove', 'fan', 'ball',
                 'fire extinguisher', 'door', 'Billiards cue', 'table',
                 'ocarina', 'treadmill', 'skating shoes', 'cabbage',
                 'xylophone', 'chicken', 'pizza', 'car', 'orange', 'sign',
                 'mirror', 'pear', 'scooter', 'mouse', 'plate', 'icecream',
                 'bus', 'muffler', 'pimento', 'Castanets', 'tray', 'banana',
                 'hotdog', 'badminton racket', 'cat', 'dish washer', 'laptop',
                 'plum', 'plate(skis)', 'dumbbell', 'carabiner', 'sushi',
                 'poles', 'rice cooker', 'roof', 'perilla leaf', 'tomato',
                 'peach', 'window', 'gimbap', 'tie', 'motorcycle', 'dog',
                 'bicycle', 'grape', 'purifier', 'lamp', 'apple', 'mug',
                 'ladle', 'carrot', 'melon', 'board', 'chopping boards', 'pot',
                 'bed', 'hat', 'vegetable peeler', 'cell phone', 'bird',
                 'tteokbokki', 'pumpkin', 'sphygmomanometer', 'persimmon',
                 'kimchi', 'massage gun', 'tennis racket', 'piano',
                 'refrigerator', 'clock', 'chili', 'side dish', 'strawberry',
                 'flute', 'corn', 'tree', 'building', 'background_out',
                 'box grater', 'onion', 'hair drier', 'hamburger', 'ttoke',
                 'thermometer', 'white bread', 'Tambourine', 'air conditioner',
                 'fire hydrant', 'sandwich', 'pilates equipment', 'gonggibap',
                 'espresso machine', 'ceiling', 'floor', 'wall', 'pillar',
                 'background_in', 'road', 'pavement', 'sky', 'sweet potato',
                 'mandu', 'suitcase'),
        pipeline=[
            dict(type='LoadImageFromFile'),
            dict(
                type='MultiScaleFlipAug',
                img_scale=(1333, 800),
                flip=False,
                transforms=[
                    dict(type='Resize', keep_ratio=True),
                    dict(type='RandomFlip'),
                    dict(
                        type='Normalize',
                        mean=[123.675, 116.28, 103.53],
                        std=[58.395, 57.12, 57.375],
                        to_rgb=True),
                    dict(type='Pad', size_divisor=32),
                    dict(type='ImageToTensor', keys=['img']),
                    dict(type='Collect', keys=['img'])
                ])
        ]))
evaluation = dict(metric=['bbox', 'segm'])
optimizer = dict(
    type='AdamW',
    lr=0.0001,
    betas=(0.9, 0.999),
    weight_decay=0.05,
    paramwise_cfg=dict(
        custom_keys=dict(
            absolute_pos_embed=dict(decay_mult=0.0),
            relative_position_bias_table=dict(decay_mult=0.0),
            norm=dict(decay_mult=0.0))))
optimizer_config = dict(
    grad_clip=None,
    type='DistOptimizerHook',
    update_interval=1,
    coalesce=True,
    bucket_size_mb=-1,
    use_fp16=True)
lr_config = dict(
    policy='step',
    warmup='linear',
    warmup_iters=500,
    warmup_ratio=0.001,
    step=[27, 33, 60, 80, 100, 140])
runner = dict(type='EpochBasedRunnerAmp', max_epochs=150)
checkpoint_config = dict(interval=1)
log_config = dict(interval=50, hooks=[dict(type='TextLoggerHook')])
custom_hooks = [dict(type='NumClassCheckHook')]
dist_params = dict(backend='nccl')
log_level = 'INFO'
load_from = None
resume_from = '/home/ubuntu/harry/Swin-Transformer-Object-Detection/work_dirs/nia_zeron/epoch_1.pth'
workflow = [('train', 1)]
fp16 = None
work_dir = 'train_model/20221129_nia'
gpu_ids = range(0, 1)
