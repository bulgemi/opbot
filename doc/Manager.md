# 관리모듈(Manager)
## 설명
> 관리모듈은 Web GUI로 구성된 OPBOT 모듈중 하나이다.
> 작업 채널에 등록된 사용자에 대한 권한검증 및 수행 가능한 TASK들을 관리할 수 있다.
> 
## 주요 기능
### 공통
1. 주요 데이터 암호화
    * AES-256(보안강도: 256bit)
    * 2011년부터 2025년까지 112bit 이상 보안강도 사용 권고
    * 관련 python package: pycryptodomex
### 사용자(그룹) 관리
1. 주요 정보
    1. 사용자 정보
        * user_name: VARCHAR2(128), NotNull, 한글/영문, 공백불허
        * email: VARCHAR2(128), PK, NotNull, e-mail(xxx@xxx.xxx), 공백불허
        * password: VARCHAR2(512), NotNull, 최소 8자리이상 소문자/대문자/숫자/특수문자 조합, 공백불허
        * group_code: VARCHAR2(64), NotNull, default: 'None', 'g_' + UUID(32자리)
        * status_code: INT, NotNull, 0(inactive)/1(active), default: 0
        * role_code: INT, NotNull, 0(admin)/1(leader)/2(user)
            * 0(admin): 관리자
                > 그룹과 사용자에 대한 생성/수정/삭제 처리. TASK 생성/수정/삭제, 그룹/사용자 연결. 사용자 역할(role) 지정
            * 1(leader): 그룹 관리자
                > 그룹내 사용자 생성/수정/삭제. TASK 생성/수정/삭제, 그룹 연결
            * 2(user): 일반 사용자
                > 사용자 본인 생성/수정/삭제. TASK 생성/수정/삭제, 본인 사용자 연결
        * slack_id: VARCHAR(128)
            * email 기준으로 slack 연동 입력, slack 연동 email이 없을 경우 Null 처리(Null일 경우 TASK 수행 불가)
            * slack과 동일한 email 사용
    1. 그룹 정보
        * group_code: VARCHAR2(64), PK, NotNull, 'g_' + UUID(32자리), 자동생성
        * group_name: VARCHAR2(256), PK, NotNull, 한글/영문/숫자/'-'/'_', 공백불허
1. 권한검증
    * slack 사용자 ID와 관리모듈에 등록된 사용자 정보를 기반으로 권한 및 수행가능 TASK 검증
1. 사용자/그룹 등록/수정/삭제
    1. 사용자
        * 생성(가입)
            1. Username 입력
            1. Email address 입력(자동 중복체크)
            1. Password 입력
            1. email 인증(사용자 email로 인증 URL 전송)시 활성화(status_code 변경 0 -> 1)
        * 수정
            1. Username 수정만 가능
        * 삭제
            1. 탈퇴시 삭제
    1. 그룹
        > login 후 사용가능, 'admin', 'leader' 권한만 생성/수정/삭제/등록 가능
        * 생성
            1. Groupname 입력(자동 중복체크)
        * 수정
            1. Groupname 수정(자동 중복체크)
        * 삭제
            1. 삭제시 사용자 정보에 해당 group_code 정보 'None' update
        * 사용자 등록관리
            * 추가
                1. 그룹에 등록한 사용자 추가
            * 삭제
                1. 등록된 사용자 삭제
### TASK 관리
1. 신규 정의
    > K8s or 연동일 경우
1. 관리
1. 사용자/그룹 관리
1. 유효성 검증