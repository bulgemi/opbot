# 평가지표/튜닝
## 목표
> 장애 상황 발생시 IT 운영자가 장소와 시간에 제약없이 신속하게 장애 원인을 분석 가능하도록 도와주는 플랫폼을 제공한다.
1. 군집화(clustering) 모델
1. 장애 상황 SMS를 유사한 유형별로 군집화한다.
1. 군집별 매핑된 분석 Task를 제공한다.
    * Task는 유사한 유형의 장애 상황 SMS에서 운영자가 많이 사용한 Task 수행 이력을 기반으로 랭킹 리스트 제공
    * Task 수행 이력이 없을 경우 Task 리스트 제공
## 평가 지표
> 장애 상황 SMS는 상황이 진행되면서 더 많은 정보가 추가되고 유사한 장애라도 장애 원인이 동일하지 않을 수 있어 정확한 답을 작성하기 어렵다는 특성이 있다.
> 하지만 기존 작성된 정답지를 이용해 정확도를 평가한다.
### 외부 평가(External Evaluation)
> 군집화 정확도가 높은지 측정하는 방법, 정해놓은 답안을 바탕으로 얼마나 군집화가 잘 되었는지 확인하는 방법
> 클러시터링 개수를 정할수 없어 내부평가(Internal Evaluation)은 사용 안 함.
* 랜덤하게 선택된 검증용 표본을 이용하여 정답지 결과와 비교하여 정확도 측정: 90%
### 모델 정확도(Model Accuracy)
> 장애 상황 SMS 특성상 최초 SMS는 내용이 별로 없어 정확도가 낮을 가능성 높고, 장애 상황이 진행되고 SMS 내용이 구체화되면 정확도가 높아진다.
* Accuracy = (TP+TN) / (TP+TN+FP+FN)
* 전체 장애 상황 SMS 대상: 60%
* 최종 장애 해결 직전 장애 상황 SMS 대상: 90%
#### 오차 행렬(confusion matrix)
> scikit-learn confusion_matrix 사용.

![Fig. 1. 오차 행렬](/doc/confusion_matrix.jpg "confusion matrix")
* sklearn.metrics.confusion_matrix
    * TP(True Positive): 모델이 정답(Positive)을 맞추었을 때
    * TN(True Negative): 모델이 오답(Negative)을 맞추었을 때
    * FP(False Postive): 모델이 오답(Negative)을 정답(Positive)으로 잘못 예측했을 때
    * FN(False Negative): 모델이 정답(Positive)을 오답(Negative)으로 잘못 예측했을 때
### Precision & Recall
> 데이터 특성상 모든 데이터는 장애 상황 SMS이고 전 장애 상황 SMS에 대한 식별이 중요하므로 Recall에 정확도가 중요.
* Precision: 30%
    * Precision = TP / (TP+FP)
* Recall: 60%
    * Recall = TP / (TP+FN)
## 교차 검증
> 일반화 성능을 재기 위해 훈련 세트와 테스트 세트로 한 번 나누는 것보다 더 안정적이고 뛰어난 통계적 평가 방법
### k-겹 교차 검증(k-fold cross-validation)
* sklearn.model_selection.KFold
### 정밀도, 재현율, f-측정
> 정밀도, 재현율, f-측정 모두를 한 번에 계산후 출력.
* sklearn.metrics.classification_report