""" Image caption generation

## Data Sets

Name, SOA human, SOA machine before S&T (NIC), S&T

- Flickr30k BLEU-1: 56 SOA, 66 S&T
- Pascal BLEU-1: 69 human 
- MS COCO: SOA is BLEU-4 of 27.7

## Measures

- BLEU-1 - BLEU-4 percentage of exact N-gram overlap

- idea: cosine distance of N-gram word-vec

## Models

- ResNet
- VGGNet
- Inception
- Xception

## Competitions

- [ImageNet (ILSVRC) challenge](http://image-net.org/challenges/LSVRC/2014/browse-synsets)
