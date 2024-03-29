# 학습 데이터 전처리기
## 학습 데이터
### 목표
신규 상황 문자발생시 기존 발생 문자 중 유사도가 높은 상황의 최종 조치내역을 보여줌.
학습 데이터전처리 설명.

### 개요
> 상황 발생시 SMS를 통해 최초 알림 및 조치가 이루어질 때마다 진행상황 전파.
1. 포맷(format) 설명
1. 정답지 생성
1. 불용어(stopword) 처리
1. BOW(Bag Of Words)
1. LDA
1. TF-IDF(Term Frequency-Inverse Document Frequency)
1. n-gram

### 포맷(format) 설명 
> EXCEL, 총 9306 건('통합품질감시': 3513, '장애의심': 0, '상황': 4209, '장애': 1584)
* 장애 상황 SMS 크기
    * 최장: 948자
    * 평균: 219자
* 상항의 종류는 아래와 같이 4가지가 존재함.
    * 통합품질감시(0)
    * 장애의심(1)
    * 상황관리(2)
    * 장애(3)
<pre>
장애구분
장애
</pre>
<pre>
문자발송일시
202004221629
</pre>
<pre>
[SKT심각도3경과-IT종합상황실]

● 내용 : [Swing 무선] 진위확인시 연동기관 행공센 오류 발생
● 영향 : 주민등록증, 운전면허증 등 진위확인시 연동기관 행공센 오류 발생 (3사 공통)
● 원인 : 대외기관 행공센 측 오류
● 발생 시간 : 15:53
● 점검 현황
- Appl. : 확인 완료
- Network : 관련 없음
- 보안 : 관련 없음
- 서버/스토리지 : 관련 없음
- Middleware : 관련 없음
- DBMS : 관련 없음
● 조치
- 16:00 대외기관 행공센 측 오류확인, 모니터링 진행
- 16:20 현재 정상화 확인, 모니터링 및 ISAC Callback 진행
- 16:29 ISAC Callback 정상확인, 장애종료 (16:20)
● 구분 : 대외기관 장애(행공센)
● 담당 부서 : 고객서비스팀

※ IT종합상황실 상황관리자 이치훈 매니저, 이상일 수석
</pre>

## 데이터 처리 단계
### 정답지 생성
1. 1단계: result 추출
    1. EXCEL 로딩([pandas](https://pandas.pydata.org/))
    1. DB 초기화
    1. 장애구분, 문자발송일시, 발송메시지 정보 추출
    <!--
    1. 장애구분 별 데이터 분류하여 csv 포맷으로 저장
    1. 문자발송일시로 정렬
    -->
    1. 발생메시지 분석
        1. '\n'(new line)으로 row 파싱
        1. row 분석
            1. "내용:" 정보 추출 
            1. "조치" 카워드 아래 내용중 "상황종료" 존재여부 확인.
            1. "상황종료" 존재시 File 저장
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
    1. EXCEL 로딩
    1. 장애구분, 문자발송일시, 발송메시지 정보 추출
    1. 문자발송일시로 정렬
    1. 발생메시지 분석
        1. '\n'(new line)으로 row 파싱
            1. "내용:" 정보 추출 
    1. 전처리(space/특수문자 제거)된 "내용:" 정보와 장애구분 값을 key로 File 조회.
    1. File 데이터 존재시 result column에 데이터 추가.

### 불용어(stopword) 처리
> 의미없는 단어이거나 너무 빈번하여 유용하지 않은 단어 제거
1. 의미없는 단어 제거
    * 직급, 담당자 정보
    * 날자, 시간, 숫자
1. 유용하지 않은 단어 제거
    * 특수 문자([,./<>?~!@#$%^&*()-_=+\|[]{}●]`)
1. 처리 결과
    * Before
    <pre>
    [SKT상황]● 내용 : [MOVIOS-MVNO] KSNET 가상계좌 입금 결과 수신 큐 적체 점검되어 전일 배포 원복 RTA 진행● 영향 : KSNET 가상계좌 입금 결과 수신 큐 적체로 MOVIOS를 통한 입금 이력 및 입금가능여부 조회 불가● 원인 : 전일 배포 영향● 영향 확인- 10:08 전일 배포 원복 진행- 10:17 배포 원복 완료- 10:18 해당 인스턴스 재기동 완료, 서비스 점검 진행- 10:19 큐적체 해소 확인- 10:20 추가 모니터링 결과 특이사항 없음, 상황종료.※ IT종합상황실 상황관리자 이상일 수석
    </pre>
    * After
    <pre>
    SKT상황 내용  MOVIOSMVNO KSNET 가상계좌 입금 결과 수신 큐 적체 점검되어 전일 배포 원복 RTA 진행 영향  KSNET 가상계좌 입금 결과 수신 큐 적체로 MOVIOS를 통한 입금 이력 및 입금가능여부 조회 불가 원인  전일 배포 영향 조치  인스턴  해당 인스턴스 재기동 완료 서비스 점검 진행  큐적체 해소 확인  추가 모니터링 결과 특이사항 없음 상황종료
    </pre>
1. 대소문자 변환
    * Before
    <pre>
    SKT상황 내용  SMSMMS GW Swing포탈 게시글 작성 시 문자 오발송 수신대상 안내 MMS 발송 중 영향  Swing 사용자 건임직원 제외 대상 분산 발송 건으로 모니터링 대응 원인  Swing포탈 게시글 작성 시 문자 오발송 후속 대응 조치  건 대상 MMS 발송 진행 중
    </pre>
    * After
    <pre>
    skt상황 내용  smsmms gw swing포탈 게시글 작성 시 문자 오발송 수신대상 안내 mms 발송 중 영향  swing 사용자 건임직원 제외 대상 분산 발송 건으로 모니터링 대응 원인  swing포탈 게시글 작성 시 문자 오발송 후속 대응 조치  건 대상 mms 발송 진행 중
    </pre>

### BOW(Bag Of Words)
> soynlp(https://github.com/lovit/soynlp):
> 학습데이터를 이용하지 않으면서 데이터에 존재하는 단어를 찾거나, 문장을 단어열로 분해, 혹은 품사 판별을 할 수 있는 비지도학습 접근법을 지향.
> 말뭉치를 기반으로 학습된 품사 판별기/형태소 분석기는 학습하지 못한 단어를(새로운 단어) 제대로 인식하지 못하는 미등록단어 문제 (out of vocabulry, OOV)가 발생
1. Why
    * 장애 문자를 단어로 분해하고 특징을 추출하여 클러스터링을 위한 코드워드 생성
1. 토큰화(tokenization)
    > 형태소 최대 갯수: 173, 평균 갯수: 57
    * 명사 추출
        > soynlp는 Noun Extractor v1과 Noun Extractor v2 모두 제공되나 v2가 성능이 더 좋다.
        > (정확성과 합성명사 인식 능력, 출력되는 정보의 오류를 수정한 버전)
        > 통계를 이용하여 단어의 경계 점수를 학습, 명사의 오른쪽에는 -은, -는, -라는, -하는 처럼 특정 글자들이 자주 등장합니다. 문서의 어절 (띄어쓰기 기준 유닛)에서 왼쪽에 위치한 substring 의 오른쪽에 어떤 글자들이 등장하는지 분포를 살펴보면 명사인지 아닌지 판단.
        * Noun Extractor v2 사용
        <pre>
        [('법인정보조회화면', ('법인', '정보', '조회', '화면')), ('법인정보조회장애현상', ('법인', '정보', '조회', '장애', '현상')), ('네트워크장안고객센터', ('네트워크', '장안', '고객센터')), ('스위치Standby', ('스위치', 'Standby')),', '화면')), ('KAIT진위확인처리', ('KAIT', '진위확인', '처리')), ('2호기Standby', ('2호기', 'Standby')), ('주민등록증운전면허증', ('주민등록증', '운전면허증')), ('없음Failover', ('없음', 'Failover'))]
        </pre>
    * 단어 추출(Cohesion score, Branching Entropy, Accessor Variety)
        > [Cohesion score](https://lovit.github.io/nlp/2018/04/09/cohesion_ltokenizer/), 
        > [Branching Entropy&Accessor Variety](https://lovit.github.io/nlp/2018/04/09/branching_entropy_accessor_variety/)
        * Cohesion score: 단어를 구성하는 글자들이 얼마나 함께 자주 등장하는지의 정보로도 단어의 경계를 판단
        * Branching Entropy: 말뭉치에서 단어를 추출하는 기법, 단어 내부에서는 불확실성(uncertainty), 엔트로피(entropy)가 줄어들고, 경계에서는 증가하는 현상을 모델링한 것
        * Accessor Variety: 단어 경계에서의 불확실성을 단어 경계 다음에 등장한 글자의 종류로 정의
        * 어휘 사전 구축
        ![Fig. 1. 명사 빈도수](/doc/noun_frequency.png "명사 빈도수")
    * Tokenizer(LTokenizer)
        > 단어의 경계를 따라 문장을 단어열로 분해, 한국어 어절의 구조를 "명사 + 조사" 처럼 "L + [R]" 로 생각.
        > L parts 에는 명사/동사/형용사/부사가 위치. 어절에서 L 만 잘 인식한다면 나머지 부분이 R parts.
        * LTokenizer 사용
        <pre>
        ['skt', '상황', '내용', 'sms', 'mms', 'gw', 'swing', '포탈', '게시글', '작성', '시', '문자', '오발송', '수신', '대상', '안내', 'mms', '발송', '중', '영향', 'swing', '사용', '자', '건임직원', '제외', '대상', '분산', '발송', '건으로', '모니터링', '대응', '원인 '대응', '조치', '건', '대상', 'mms', '발송', '진행', '중']
        </pre>
    * Normalizer 
        *  반복되는 이모티콘의 정리 및 한글, 혹은 텍스트만 남기기 위한 함수를 제공
            * repeat_normalize 사용
    * Before
        <pre>
        skt상황 내용  smsmms gw swing포탈 게시글 작성 시 문자 오발송 수신대상 안내 mms 발송 중 영향  swing 사용자 건임직원 제외 대상 분산 발송 건으로 모니터링 대응 원인  swing포탈 게시글 작성 시 문자 오발송 후속 대응 조치  건 대상 mms 발송 진행 중
        </pre>
    * After
        <pre>
        skt 상황 내용 sms mms gw swing 포탈 게시글 작성 시 문자 오발송 수신 대상 안내 mms 발송 중 영향 swing 사용 자 건임직원 제외 대상 분산 발송 건으로 모니터링 대응 원인 swing 포탈 게시글 작성 시 문자 오발송 후속 대응 조치 건 대상 mms 발송 진행 중
        </pre>
    * Vectorizer
        * 학습된 토크나이저를 이용하여 문서를 sparse matrix 생성
        * original
        <pre>
        skt 상황 내용 sms mms gw swing 포탈 게시글 작성 시 문자 오발송 수신 대상 안내 mms 발송 중 영향 swing 사용 자 건임직원 제외 대상 분산 발송 건으로 모니터링 대응 원인 swing 포탈 게시글 작성 시 문자 오발송 후속 대응 조치 건 대상 mms 발송 진행 중
        </pre>
        * 인코딩(encoding)
        <pre>
        [0, 15, 8, 365, 470, 347, 33, 543, 4870, 794, 43, 708, 1957, 319, 155, 263, 470, 359, 7, 1, 33, 38, 24, 8504, 461, 155, 1600, 359, 409, 44, 16, 2, 33, 543, 4870, 794, 43, 708, 1957, 182, 16, 3, 123, 155, 470, 359, 11, 7]
        </pre>
        * 디코딩(decoding)
        <pre>
        ['skt', '상황', '내용', 'sms', 'mms', 'gw', 'swing', '포탈', '게시글', '작성', '시', '문자', '오발송', '수신', '대상', '안내', 'mms', '발송', '중', '영향', 'swing', '사용', '자', '건임직원', '제외', '대상', '분산', '발송', '건으로', '모니터링', '대응', '원인 '대응', '조치', '건', '대상', 'mms', '발송', '진행', '중']
        </pre>

### LDA(Latent Dirichlet Allocation)
> 자주 나타나는 단어의 토픽을 찾는 것, 아래 표는 도출한 토픽의 가중치 정보

![Fig. 2. LDA](/doc/lda.png "LDA")

### TF-IDF(Term Frequency-Inverse Document Frequency)
> 장애 상황 SMS내 단어의 중요도를 구하기 위해 사용.
> 해당 기법을 선정한 이유는 TF-IDF의 서에서 자주 등장하는 단어는 중요도가 낮다고 판단하며,
> 특정 문서에서만 자주 등장하는 단어는 중요도가 높다고 판단하는 특성 때문이다.
> DTM(Document-Term Matrix, scikit-learn: CountVectorizer)을 사용할 경우 단순 단어 빈도 수 기번 접근이어서 장애 상황 SMS 특성상 자주 사용되나 중요도가 떨어지는 
> 단어가 불용어 처리에서 누락될 경우 모델 정확도가 떨어질 위험이 있다.
* TfidfVectorizer 사용
    * scikit-learn
    * tfidf matrix 추출
<pre>
...
'부가': 6.704427427919447
'부가상품변경': 7.0473721790462776
'부가상품변경화면에서': 6.77111880241812
'부가서비스': 5.964027362508957
'부분': 7.573465274943057
'부산': 7.3052012883483775
'부서': 3.0961284604648505
...
</pre>
* 데이터(pickle) 저장 
* cosine similarity 측정
<pre>
...
similarity:  0.8447320746327309
skt 심각도3경과it종합상황실 내용 운전면허증 kait 진위확인 시 불가 영향 운전면허증 kait 진위확인 시 간헐적 불가 주민등록증 정상 3사 공통 원인 대외기관 경찰청 측 시스템 장애 발생 시간 점검 현황 ap pl 확인 중 network 관련 없음 보안 관련 없음 서버스토리지 관련 없 구분 대외기관 장애 kait 경찰청 담당 부서 고객 상품unit
sdate09skt심각도3경과it종합상황실 내용 운전면허증 진위확인 시 연동 기관 행공센 오류 영향 운전면허증 진위확인 불가 주민등록증 은 정상 3사 공통 장애 69 call 원인 대외기관 경찰청 장애 발생 시간 점검 현황 ap pl 확인 중 network 관련 없음 보안 관련 없음 서버스토리트 적용 구분 대외기관 장애 kait 경찰청 담당 부서 고객 상품unit
similarity:  0.9000015548210456
skt 심각도3경과it종합상황실 내용 운전면허증 kait 진위확인 시 불가 영향 운전면허증 kait 진위확인 시 간헐적 불가 주민등록증 정상 3사 공통 원인 대외기관 경찰청 측 시스템 장애 발생 시간 점검 현황 ap pl 확인 중 network 관련 없음 보안 관련 없음 서버스토리지 관련 없 구분 대외기관 장애 kait 경찰청 담당 부서 고객 상품unit
sdate09skt심각도3경과it종합상황실 내용 운전면허증 진위확인 시 연동 기관 행공센 오류 영향 운전면허증 진위확인 불가 주민등록증 은 정상 3사 공통 장애 원인 대외기관 경찰청 장애 발생 시간 점검 현황 ap pl 확인 중 network 관련 없음 보안 관련 없음 서버스토리지 관련 품unit
similarity:  1.0000000000000002
skt 심각도3경과it종합상황실 내용 운전면허증 kait 진위확인 시 불가 영향 운전면허증 kait 진위확인 시 간헐적 불가 주민등록증 정상 3사 공통 원인 대외기관 경찰청 측 시스템 장애 발생 시간 점검 현황 ap pl 확인 중 network 관련 없음 보안 관련 없음 서버스토리지 관련 없 구분 대외기관 장애 kait 경찰청 담당 부서 고객 상품unit
skt 심각도3경과it종합상황실 내용 운전면허증 kait 진위확인 시 불가 영향 운전면허증 kait 진위확인 시 간헐적 불가 주민등록증 정상 3사 공통 원인 대외기관 경찰청 측 시스템 장애 발생 시간 점검 현황 ap pl 확인 중 network 관련 없음 보안 관련 없음 서버스토리지 관련 없 구분 대외기관 장애 kait 경찰청 담당 부서 고객 상품unit
similarity:  0.977147335339306
skt 심각도3경과it종합상황실 내용 운전면허증 kait 진위확인 시 불가 영향 운전면허증 kait 진위확인 시 간헐적 불가 주민등록증 정상 3사 공통 원인 대외기관 경찰청 측 시스템 장애 발생 시간 점검 현황 ap pl 확인 중 network 관련 없음 보안 관련 없음 서버스토리지 관련 없 구분 대외기관 장애 kait 경찰청 담당 부서 고객 상품unit
skt 심각도3경과it종합상황실 내용 운전면허증 kait 진위확인 시 불가 영향 운전면허증 kait 진위확인 시 간헐적 불가 주민등록증 정상 3사 공통 원인 대외기관 경찰청 측 시스템 장애 발생 시간 점검 현황 ap pl 확인 중 network 관련 없음 보안 관련 없음 서버스토리지 관련 없담당 부서 고객 상품unit
...
</pre>

### n-gram
<pre>
... '후속 조치 야간에', '후속 조치 영향', '후속 조치 예정', '후속 조치 온프라미스', '후속 조치 위하여', '후속 조치 작업', '후속 조치 장애', '후속 조치 조치', '후속 조치 진행', '후속 조치 필요', '후속 조치 확인', '후속 조치gbic', '후속 조치gbic 교체', '후속 조'후속 처리 작업', '후속배치', '후속배치 지연', '후속배치 지연 발생', '후에도', '후에도 cpu', '후에도 cpu 부하', '후에도 동일', '후에도 동일 증상', '후에도 동일 현상', '후에도 오류', '후에도 오류 해소', '후에도 재기동', '후에도 재기동 안됨', '후에도 현상', '후', '후첨부 첨부된', '후첨부 첨부된 문서', '후청구', '후청구 대상', '후청구 대상 원인', '후행', '후행 배치', '후행 배치 미수행', '후행 배치 수행', '훼손', '훼손 발생', '훼손 발생 시간', '훼손 조치', '훼손 조치 담당', '휴가', '휴가 조회', '휴가 조회 기능', '휴, '휴일 기준 정보', '휴일 상담', '휴일 상담 영향', '휴일 상담 이중화', '휴일예약', '휴일예약 접수', '휴일예약 접수 불가', '휴일예약 처리', '휴일예약 처리 오류', '휴일예약 처리 저장', '히어로', '히어로 심야휴일', '히어로 심야휴일 데이터']
어휘 사전 크기: 125118

</pre>

## 아키텍처 
![Fig. 3. 데이터전처리기 구조](/doc/DataPreprocessor.png "데이터전처리기 구조")

## 결론
> 입력 데이터셋 생성
* 장애 상황 SMS에서 단어 추출 후 IF-IDF로 도출된 단어 중요도를 기반으로 정렬 후 벡터화 후 173개의 특성에 0번째부터 순차적으로 입력.
    * shape: (n, 173)