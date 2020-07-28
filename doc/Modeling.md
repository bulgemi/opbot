# 모델링
## DBSCAN
> 비지도 학습, 유용한 군집 알고리즘, 클러스터 개수 지정할 필요 없다. 밀접지역(데이터가 붐비는 포인트)이 한 클러스터를 구성. 비어 있는 지역이 경계.
* scikit-learn에서 제공하는 DBSCAN 사용.
## ReMixMatch & FixMatch
* [ReMixMatch.pdf](https://github.com/bulgemi/opbot/blob/master/doc/1911.09785.pdf "ReMixMatch")
* [FixMatch.pdf](https://github.com/bulgemi/opbot/blob/master/doc/2001.07685.pdf "FixMatch")
* Semi-Supervised Learning
    * Labeled data 가 많지 않은 상황에서 unlabeled data를 활용
    * Self-Training
        1. Labeled data로 모델 학습
        1. 학습된 모델로 unlabeled data predict
        1. 가장 confident 한 데이터로 labeled data에 추가
        1. batch마다 1~3회 반복
    * Consistency Regularization(일관성 정규화)
        1. 모델 이용해 unlabeled data 분포 예측
        1. unlabeled data noise 추가(Data Augmentation)
        1. 예측한 분포를 Augmented Data의 정답 label로 사용하여 모델 학습
    * Regularization Method
        * Mixup
            * 두개 이미지 mix(5:5)
        * Cutout
            * 특정 pixel 잘라내기
        * CutMix
            * 특정 pixel을 다른 이미지로 대체(6:4)
*  ReMixMatch
    *  distribution alignment
        *  unlabeled data의 예측 분포를 labeled data의 실제 분포에 맞춰 조정
    *  augmentation anchoring
        *  augmentation 할 때 weak augmentation 이 적용된 데이터의 예측 분포를 strong augmentation 적용된 데이터 타겟으로 이용
            *  weak augmentation: 약한 noise 적용
            *  strong augmentation: 강한 noise 적용
    *  RandAugment
        *  proxy task 없이 학습 과정에 바로 적용할 수 있는 augmentation 방법론
    *  CTAugment
        *  RandAugment를 발전시킨것
* FixMatch
    * 초반에는 labeled data로만 모델을 학습시키고 점진적으로 unlabeled data에 포함시킴
    * ablation studies
* Refs.
    * https://arxiv.org/pdf/1911.09785.pdf
    * https://arxiv.org/pdf/2001.07685.pdf
    * https://www.youtube.com/watch?v=mXiPbkyGJ9g
    * https://www.youtube.com/redirect?q=https%3A%2F%2Fdrive.google.com%2Ffile%2Fd%2F1htJtBBWbGtErqXU6hM3MMHhtmLGP0imB%2Fview%3Fusp%3Dsharing&v=mXiPbkyGJ9g&event=video_description&redir_token=QUFFLUhqbUY3RGV6YWlTOWZET0ZqMHhPcGVVMERJaWIzd3xBQ3Jtc0tuelZiZzFTVV9zOWF5Y3FxMnhqR3NqNWk5cjlscUQ4OFlCMGJmRVNTVjBDOWctaGRNRlA2ZWlvVVFSNlhqeXBwNDFaa01SeW82d2pBdHlUOTdWWGRJWDN6MEYwd05EYWt1ZUZfOGFGZjlPOTFNWUVSWQ%3D%3D

## Matching Networks for One Shot Learning
> 2016년 구글 딥마인드팀,
> LSTM,
> One Shot,
> few-shot,
> N-shot,
> N-way, k-shot,
> data augmentation,
> 4stack modules(module: 3 by 3 conv_64 + BN + Relu + 2 by 2 max polling)

* 아주 적은 양의 데이터를 사용하여 모델을 학습 시킬 수 있는 아이디어를 제시
    * 기존 모델은 패턴이 다양하고 많은 학습 데이터가 필요하다. 데이터에 label을 달기 위해서는 domain 지식이 있는 전문인력과 비용이 많이 들고 Label이 적은 데이터는 Overfitting이 발생할 가능성이 높다.
* N-Shot learning(학습에 N개의 Data)
    * zero-shot
    * one-shot
    * few-shot
        * few-shot learning은 one-shot learning의 확장 버전
* 제한된 데이터의 학습 방법
    * 데이터 관점
        * Data augmentation
            * Generative models
            * Self-supervised learning
    * Model 관점
        * unsupervised learning
        * Transfer learning
        * Meta learning
            * Model-based
            * Metric-based
            * Optimization-based
* Matching Networks
    * Training 관점
        * 일반적인 지도학습에서는 Limited data
            * 학습 잘 안됨(overfitting)
            * 성능 안 나옴
        * Episode training(새로운 학습 방법 제시)
            * Training 할 때, Testing과 유사한 episode 구성하여 overfitting 방지
            * Training set
                * Support set(S)
                * Batch set(B)
            * N-way(class 수), k-shot(sample 수)
                * episode에서 발생하는 수: K = kN
    * 해당 논문에서 추천하는 hyper parameter
        * Label: 5~25
        * Label별 sample수: 1~5
* 이미지, Text도 처리 가능
* Refs.
    * https://tensorflow.blog/tag/one-shot-learning/
    * https://www.youtube.com/watch?v=SW0cgNZ9eZ4
    * http://dsba.korea.ac.kr/seminar/?mod=document&uid=63
