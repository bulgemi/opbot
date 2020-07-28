# 검증/튜닝
## 교차 검증
> 일반화 성능을 재기 위해 훈련 세트와 테스트 세트로 한 번 나누는 것보다 더 안정적이고 뛰어난 통계적 평가 방법
### k-겹 교차 검증(k-fold cross-validation)
* sklearn.model_selection.KFold
## 그리드 서치(grid search)
> 매개변수 튜닝하여 일반화 성능 개선.
* sklearn.model_selection.GridSearchCV
## 평가 지표
### 목표
* 
### 오차 행렬(confusion matrix)
> scikit-learn confusion_matrix 사용.

![Fig. 1. 오차 행렬](/doc/confusion_matrix.jpg "confusion matrix")
* sklearn.metrics.confusion_matrix
    * TP(진짜 양성)
    * TN(진짜 거짓)
    * FP(거짓 양성)
    * FN(거짓 음성)
### 정밀도, 재현율, f-측정
> 정밀도, 재현율, f-측정 모두를 한 번에 계산후 출력.
* sklearn.metrics.classification_report