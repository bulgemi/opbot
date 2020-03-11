# 수행모듈(TaskExecutor)
## 설명
> 챗봇(Chatbot)으로부터 요청받은 TASK를 처리하는 모듈이다. 기존 SSH 방식에 OPMATE, K8s, Ansible 연동을 추가한다.
> 연동 대상에 따라 정보보호 요건이 존재함.
## 연동 대상 
### 공통
1. 정보보호
    1. 대상 정보
        1. Infra 정보
            * 서버 IP
            * Hostname
            * User ID
            * 주요 파일(group, password)
        1. 고객정보
            * 이름
            * 전화번호
            * 주민번호
            * email
            * 생년월일
    1. 정보보호 프로세스 
        > 연동 대상에 따라 정보보호 대상이 달라진다. OPBOT에서 K8s의 경우 Cloud 환경에서 컨테이너 애플리케이션의 자동 디플로이,
        > 스케일링 관리같은 기능은 처리하지 않고 컨테이너 모니터링 영역을 기능 대상으로 정의한다.
        > OPMATE의 경우는 정보보호가 필요한 대상으로 아래와 같이 2 단계로 정보보호를 수행한다.
        1. OPMATE
            > OPMATE를 통해 수행되는 TASK는 아래와 같은 절차를 통해 검증된 TASK로 판단
            * TASK 내용 검토(위험명령어 감사)
            * 관리자에 의한 TASK 승인처리
            * 인증된 사용자만 TASK 생성/수행 처리
        1. 마스킹(Masking)
            > 정보보호 대상 데이터의 경우 마스킹(Masking) 처리를 통한 정보보호 처리
            * 문자인식 개인정보 마스킹(Masking)
                * 패턴인식
### OPMATE
1. 주요 정보
    * 연동 계정
    * REST API
1. 연동 방식
    * RESTful
1. 처리 방식
### K8s
1. 주요 정보
    * K8s 시스템 정보
1. 연동 방식
    * SSH
1. 처리 방식
    1. K8s 시스템 접속
    1. TASK 수행
        * TASK에 정의된 K8s 명령어
        * K8s 시스템에 정의된 Script 수행
### Ansible
1. 주요 정보
    * K8s 시스템 정보
1. 연동 방식
    * SSH
1. 처리 방식
    1. Ansible 시스템 접속
    1. TASK 수행
        * TASK에 정의된 Ansible 명령어(Command)
        * Ansible 시스템에 정의된 Script 수행
