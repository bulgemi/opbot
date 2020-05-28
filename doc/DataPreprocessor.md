# 학습 데이터 전처리기
## 학습 데이터
### 목표
신규 상황 문자발생시 기존 발생 문자 중 유사도가 높은 상황의 최종 조치내역을 보여줌.

### 개요
상황 발생시 SMS를 통해 최초 알림 및 조치가 이루어질 때마다 진행상황 전파.
상항의 종류는 아래와 같이 4가지가 존재함.
* 통합품질감시(0)
* 장애의심(1)
* 상황관리(2)
* 장애(3)

### 포맷 
EXCEL

## 데이터 처리 단계
1. 1단계: result 추출
    1. EXCEL 로딩([pandas](https://pandas.pydata.org/))
    1. 장애구분, 문자발송일시, 발송메시지 정보 추출
    <!--
    1. 장애구분 별 데이터 분류하여 csv 포맷으로 저장
    -->
    1. 문자발송일시로 정렬
    1. 발생메시지 분석
        1. '\n'(new line)으로 row 파싱
        1. row 분석
            1. "내용:" 정보 추출 
            1. "내용:" 정보 space/특수문자(,./<>?~!@#$%^&*()-_=+\|[]{}`) 제거
            1. "조치" 카워드 아래 내용중 "상황종료" 존재여부 확인.
            1. "상황종료" 존재시 DB 저장
                * key: 전처리(space/특수문자 제거)된 "내용:" 정보
                * type: 장애구분
                * contents: "상황종료" 존재하는 발송메시지
            <!--
            1. 한글 띄어쓰기 재처리([soyspacing](https://github.com/lovit/soyspacing))
            1. space 제거된 "내용:" 정보 2글자 단위로 split
            1. split 된 데이터를 기반으로 sub directory 생성
            1. 발송메시지내 불필요한 항목 제거
                * [SKT상황], 내용:, 원인:, 조치:, IT종합상황실 상황관리자 김희만 수석
            1. '내용:' 키워드 다음에 나온 내용 추출
            1. 마지막으로 생성된 디렉토리에 문자발송일시 정보를 파일명으로 발송메시지 저장
            -->
1. 2단계: result 추가
    1. EXCEL 로딩([pandas](https://pandas.pydata.org/))
    1. 장애구분, 문자발송일시, 발송메시지 정보 추출
    1. 문자발송일시로 정렬
    1. 발생메시지 분석
        1. '\n'(new line)으로 row 파싱
            1. "내용:" 정보 추출 
            1. "내용:" 정보 space/특수문자(,./<>?~!@#$%^&*()-_=+\|[]{}`) 제거
    1. 전처리(space/특수문자 제거)된 "내용:" 정보와 장애구분 값을 key로 DB 조회.
    1. DB 데이터 존재시 result column에 데이터 추가.
    
## 아키텍처 
## 결론