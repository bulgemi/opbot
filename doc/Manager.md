# 관리모듈(Manager)
## 설명
> 관리모듈은 Web GUI로 구성된 OPBOT 모듈중 하나이다.<br>
> 작업 채널에 등록된 사용자에 대한 권한검증 및 수행 가능한 TASK들을 관리할 수 있다.
## 주요 기능
### 공통
1. Web Application 모든 처리는 Ajax 적용
1. Web library
    * UI: [INK](http://ink.sapo.pt/)
    * Grid: [jsGrid](http://js-grid.com/)
1. 주요 데이터 암호화
    * 공개키 암호 알고리즘(보안강도: 128bit)
    * 암호 알고리즘 안전성 유지기간: 2030년이후
    * 관련 python package: [pycryptodomex](https://pypi.org/project/pycryptodomex/)
### 사용자(그룹) 관리
1. Database Table
    1. 사용자(user_info)
        > 사용자 정보 테이블
        * user_id: VARCHAR2(64), PK, NotNull, 'u_' + UUID(32자리), 자동생성
        * user_name: VARCHAR2(128), NotNull, 한글/영문, 공백불허
        * email: VARCHAR2(128), PK, NotNull, e-mail(xxx@xxx.xxx), 공백불허
        * passwd: VARCHAR2(512), NotNull, 최소 8자리이상 소문자/대문자/숫자/특수문자 조합, 공백불허
        * status_code: INT, NotNull, 0(inactive)/1(active), default: 0
        * role_code: INT, NotNull, 0(admin)/1(leader)/2(user)
            * 0(admin): 관리자
                > 그룹과 사용자에 대한 생성/수정/삭제 처리.<br>
                > TASK 생성/수정/삭제, 그룹/사용자 연결<br>
                > 사용자 역할(role) 지정
            * 1(leader): 그룹 관리자
                > 그룹내 사용자 생성/수정/삭제.<br>
                > TASK 생성/수정/삭제, 그룹 연결
            * 2(user): 일반 사용자
                > 사용자 본인 생성/수정/삭제.<br>
                > TASK 생성/수정/삭제, 본인 사용자 연결
        * slack_id: VARCHAR(128)
            * email 기준으로 slack 연동 입력, slack 연동 email 없을 경우 Null 처리(Null일 경우 TASK 수행 불가)
            * slack id와 동일한 email 사용
        * create_time: VARCHAR2(16), NotNull, YYYYMMDDhhmmss, 공백불허
        * update_time: VARCHAR2(16), NotNull, YYYYMMDDhhmmss, 공백불허
    1. 그룹(group_info)
        > 그룹 정보 테이블
        * group_id: VARCHAR2(64), PK, NotNull, 'g_' + UUID(32자리), 자동생성
        * group_name: VARCHAR2(256), PK, NotNull, 한글/영문/숫자/'-'/'_', 공백불허
        * owner_id: VARCHAR2(64), NotNull, 'u_' + UUID(32자리)
        * create_time: VARCHAR2(16), NotNull, YYYYMMDDhhmmss, 공백불허
        * update_time: VARCHAR2(16), NotNull, YYYYMMDDhhmmss, 공백불허
        * audit_code: VARCHAR2(64), NotNull, 'u_' + UUID(32자리)
            > 수정하는 user_code update
    1. 그룹관리(group_management)
        > 그룹 관리 테이블
        * user_id: VARCHAR2(64), PK, NotNull, 'u_' + UUID(32자리), 자동생성
        * group_id: VARCHAR2(64), PK, NotNull, 'g_' + UUID(32자리), 자동생성
        * create_time: VARCHAR2(16), NotNull, YYYYMMDDhhmmss, 공백불허
        * update_time: VARCHAR2(16), NotNull, YYYYMMDDhhmmss, 공백불허
        * audit_id: VARCHAR2(64), NotNull, 'u_' + UUID(32자리)
            > 수정하는 user_code update
1. 공통
    * 모든 데이터 처리시 create_time, update_time 갱신
        * 해당 테이블
            * user_info
            * group_info
    * 모든 데이터 처리시 audit_code 갱신
        * 해당 테이블
            * group_info
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
        > login 후 사용, 'admin', 'leader' 권한만 허용 
        * 생성
            1. Groupname 입력(자동 중복체크)
        * 수정
            1. Groupname 수정(자동 중복체크)
        * 삭제
            1. group_management에 해당 group_code row 삭제
        * 사용자 등록관리
            * 추가
                1. 그룹에 등록한 사용자 추가
            * 삭제
                1. 등록된 사용자 삭제
### TASK 관리
1. Database Table
    > 기존 테이블 수정 필수!
    1. TASK(task_info)
        > TASK 정의 테이블
        * task_id: VARCHAR2(64), PK, NotNull, 't_' + UUID(32자리), 자동생성
        * task_name: VARCHAR2(512), PK, NotNull, 한글/영문/숫자/'-'/'_', 공백불허
        * task_type: INT, NotNull, 0(OPMATE)/1(K8s)/2(SSH: Command)/3(SSH: Sell Script)/4(Ansible), 공백불허
        * owner_id: VARCHAR2(64), PK, NotNull, 'u_' or 'g_' + UUID(32자리)
        * action_type: VARCHAR(1), NotNull, 'A'(분석)/'S'(조치), 공백불허
        * status_code: INT, NotNull, 0(abnormal)/1(normal)/2(lock)/3(temporary), default: 0, 공백불허
        * create_time: VARCHAR2(16), NotNull, YYYYMMDDhhmmss, 공백불허
        * update_time: VARCHAR2(16), NotNull, YYYYMMDDhhmmss, 공백불허
        * audit_id: VARCHAR2(64), NotNull, 'u_' + UUID(32자리)
            > 수정하는 user_code update
    1. TASK Playbook(task_playbook)
        > task_type 1/2/3/4일 경우, Script 관리 테이블
        * task_id: VARCHAR2(64), PK, NotNull, 't_' + UUID(32자리)
        * task_seq: INT, PK, NotNull, default: 0, 공백불허
        * contents: TEXT, NotNull, Command/Shell/K8s/Ansible Script
        * cause: VARCHAR(256), Nullable
        * create_time: VARCHAR2(16), NotNull, YYYYMMDDhhmmss, 공백불허
        * update_time: VARCHAR2(16), NotNull, YYYYMMDDhhmmss, 공백불허
        * audit_id: VARCHAR2(64), NotNull, 'u_' + UUID(32자리)
            > 수정하는 user_code update
    1. TASK Management(task_management)
        > 사용자(그룹)별 TASK 관리 테이블 
        * owner_id: VARCHAR2(64), PK, NotNull, 'u_' or 'g_' + UUID(32자리)
        * task_id: VARCHAR2(64), PK, NotNull, 't_' + UUID(32자리)
        * owner_type: INT, NotNull, 0(user)/1(group)
        * create_time: VARCHAR2(16), NotNull, YYYYMMDDhhmmss, 공백불허
        * update_time: VARCHAR2(16), NotNull, YYYYMMDDhhmmss, 공백불허
        * audit_id: VARCHAR2(64), NotNull, 'u_' + UUID(32자리)
            > 수정하는 user_code update
1. 공통
    * 모든 데이터 처리시 create_time, update_time, audit_code 갱신
        * 해당 테이블
            * task_info
            * task_playbook
            * task_management
1. TASK 등록/수정/삭제
    > K8s, SSH, (Ansible) 연동일 경우
    * Web Editor(관련 라이브러리: [CodeMirror](https://codemirror.net/index.html)) 기반 Script 작성 기능 제공
    * 등록
        1. Tasktype 선택(Select Box: OPMATE, K8s, SSH: Command, SSH: Sell Script)
        1. Actiontype 선택(Select Box: 분석, 조치)
        1. Taskname 입력
            * Tasktype OPMATE일 경우, OPMATE Master에서 TASK 리스트 조회하여 Redis 데이터 적재 자동완성 처리
            * Tasktype OPMATE 아닐 경우, 사용자가 Taskname 수동입력(자동 중복체크)
        1. 등록 사유(cause) 입력
        1. Tasktype[K8s, SSH: Command, SSH: Sell Script]일 경우, Web Editor 인터페이스 제공
            * Script 입력
            * Target 입력
    * 수정
        1. Tasktype, Taskname 수정
        1. Script 내용 수정
    * 삭제
        1. Task 삭제
            1. task_management 해당 task_code 삭제
            1. task_playbook 해당 task_code 삭제
            1. task_info 해당 task_code 삭제
1. 사용자별 TASK/그룹별 TASK 관리
    > 사용자가 사용하려는 TASK 정의<br>
    > 그룹이 사용하려는 TASK 정의
    1. 사용자별 TASK 등록/삭제
        > 사용자가 이용하려는 TASK 관리 화면 제공<br>
        > Grid 인터페이스 
        * 등록 
            1. 자신이 등록한 TASK 리스트 조회 후 선택 등록
        * 삭제
            1. Grid 선택 삭제
    1. 그룹별 TASK 등록/수정/삭제
        > login 후 사용, 'admin', 'leader' 권한만 허용<br>
        > 그룹이 이용하려는 TASK 관리 화면 제공<br>
        > Grid 인터페이스 
        * 등록 
            1. 자신이 등록한 TASK 리스트 조회 후 선택 등록
        * 삭제
            1. Grid 선택 삭제
1. 유효성 검증
    > OPMATE 경우 해당
    * daily batch 처리를 통한 OPMATE TASK 유효성 점검
        1. task_info 테이블에 Tasktype이 OPMATE인 TASK의 task_name이 OPMATE Master에서 조회한 TASK 리스트에 존재하는 확인
            * 없을 경우, status_code 0(abnormal) update
            * 있을 경우, status_code 1(normal) update
        2. task_info 테이블에 status_code가 1인 TASK를 수행할 경우 chatbot은 유효하지 않은 TASK라는 내용 사용자에게 통보
1. UI 설계
    1. 로그인(/)
    ![로그인](https://github.com/bulgemi/opbot/blob/master/doc/001login.png)
    1. 사용자 생성(/new)
    ![사용자 생성](https://github.com/bulgemi/opbot/blob/master/doc/101createuser.png)
    1. Task
        1. Task 등록(/task/new)
        ![Task 등록](https://github.com/bulgemi/opbot/blob/master/doc/301tasktaskregist.png)
        1. Task 조회(/task/list)
        ![Task 조회](https://github.com/bulgemi/opbot/blob/master/doc/302tasktaskgrid.png)
    1. Group
        1. Group 등록(/group/new)
        ![Group 등록](https://github.com/bulgemi/opbot/blob/master/doc/401groupgroupregist.png)
        1. Group 조회(/group/list)
        ![Group 조회](https://github.com/bulgemi/opbot/blob/master/doc/402groupgroupgrid.png)
    1. Admin
        1. User 관리(/admin/user)
        ![User 관리](https://github.com/bulgemi/opbot/blob/master/doc/201adminusermanage.png)
        1. Group 관리(/admin/group)
        ![Group 관리](https://github.com/bulgemi/opbot/blob/master/doc/202admingroupmanage.png)
        1. Task 관리(/admin/task)
        ![Task 관리](https://github.com/bulgemi/opbot/blob/master/doc/203admintaskmanage.png)
