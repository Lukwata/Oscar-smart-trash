# Smart recycle-bin

## 1. Research problem
- [x] List all classes of recyclable/non-recyclable.

## 2. Preprocess data
- [x] Split raw dataset to train/val/test.
- [ ] Write make script to transform data.
- [x] Build TFRecords.
- [x] Implement input pipeline with tf.data API.

## 3. Build model
### 3.1. Load pretrained model
- [x] Build Resnet graph with new output layer.
- [x] Implement loss function.
- [x] Implement training logic.
- [x] Implement inference method given a new image.
- [x] Load pre-trained weights.

### 3.2. Improve model
- [x] Wrap model with tf.Estimator API.
- [x] Add metrics (accuracy, recall).
- [x] Evaluate while training.
- [x] Learning rate decay.
- [x] Early stopping.

## 4. Training
- [x] Train with default parameters.

## 5. Experiments
- [x] Search learning rate.
- [x] Data augmentation.
- [ ] No pretrained.
- [x] Confusion matrix.
- [x] Balance classes with example weights.
- [ ] Labels smoothing.
- [x] Custom augmentation: rotate, zoom, color/contrast alteration.

## 6. Serving
- [x] Research serving/bazel.
- [x] Export model for serving.
- [x] Serve model on server.
- [x] Implement client on board to make request.
- [x] Test serving speed with and without batching.

## Note
* ImageNet image Example needs only 1 image (curr), ALOV needs 2 (prev and curr)
    - [ ] Duplicate prev using curr for ImageNet Example, save both for ALOV: easiest to implement
    - [ ] Save 2 types of TFRecord and use a flag to distinguish them: can extend to other types of data
    - [ ] Use SequenceExample to save abitrary number of images and metadata: most versatile, use a single general data reader (no need to implement different data reading schemes for each type of data)
