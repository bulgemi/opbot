# 챗봇(Chatbot)
## 설명
> 현재 챗봇은 OPBOT에서 이벤트 정보를 이해 관계자에게 알려주고, 분석/조치 가능한 행위를 추천하는 역할을 수행하는 모듈이다.
> 기존 기능에 사용자 기반의 처리가 추가되어 관리모듈(Manager)에서 등록된 TASK들을 권한이 있는 사용자에게 제공하고,
> 리스트 및 수행/결과를 볼수 있도록 기능을 제공한다.
## 주요 기능
### 공통
1. Slack 연동 Package
    * [slackclient](https://slack.dev/python-slackclient/)
    * [slacker](https://github.com/os/slacker/)
1. Splunk 연동 Package
    * [splunk-sdk-python](https://github.com/splunk/splunk-sdk-python)
1. 보고서(Report) 관련 Package
    * [PDF](https://pypi.org/project/pdfkit/)
    * [Matplotlib](https://matplotlib.org/)
1. 주요 데이터 암호화
    * AES-256(보안강도: 256bit)
    * 2011년부터 2025년까지 112bit 이상 보안강도 사용 권고
    * 관련 python package
        * [pycryptodomex](https://pypi.org/project/pycryptodomex/)
### 챗봇(Chatbot)
1. 주요 정보
1. 사용자(User) 검증
    1. 인증
        > 등록된 사용자 여부 확인
        1. Slack 작업 Channel을 통해 TASK 관련 요청 수신
        1. 요청한 사용자 email 확인(작업 channel에 등록되어 있다는 것으로 요청 권한은 있는 것으로 판단)
        1. 사용자 email을 이용하여 Database user_info table에 존재여부 확인
    1. 권한
        > TASK 수행권한 유무, 그룹(Group) 소속 유무 확인
        1. 그룹(Group) 파악
            * Database group_management table 조회(DB 조회)
        1. TASK 파악
            * Database task_management table 조회
                * 사용자(User) TASK 조회
                * 그룹(Group) TASK 조회
1. System 기본 정보 제공
    1. Splunk Macro 연동을 통한 CPU, Memory 사용량 제공
        > !성능 이슈 존재함.
    1. 사용량 정보 Chart 형식의 보고서 제공
1. 구문 분석 
    * '!' 문자를 이용한 OPBOT 명령어 구분
    * OPBOT 명령어 안에 인자 존재 유무는 ','의 존재 유무로 파악
        * ','존재시 0번째 단어는 명령어
        * 1번째 단어부터 인자값
### 명령어(Command)
1. 기능목록 조회
    > !help!<br>
    > !h!<br>
    > !?!
1. TASK 목록 조회
    1. 사용자(User) TASK
        > !my task!<br>
        > !mytask!<br>
        > !mt!
    1. 그룹(Group) TASK
        > !group task!<br>
        > !grouptask!<br>
        > !gt!
1. TASK 수행
    1. 사용자(User) TASK
        > !my task, task_name!<br>
        > !mytask, task_name!<br>
        > !my task, task_index!<br>
        > !mytask, task_index!<br>
        > !mt, task_name!<br>
        > !mt, task_index!
    1. 그룹(Group) TASK
        > !group task, task_name!<br>
        > !grouptask, task_name!<br>
        > !group task, task_index!<br>
        > !grouptask, task_index!<br>
        > !gt, task_name!<br>
        > !gt, task_index!
1. System 상태정보
    1. CPU
        > !cpu, node01, ...!<br>
        > !c, node01, ...!
    1. Memory
        > !mem, node01, ...!<br>
        > !m, node01, ...!
### 보고서(Report) 생성
1. 주요 정보
1. TASK 결과
    1. 표준 출력 결과 PDF 생성
    1. PDF 파일 slack 전달
1. System 기본 정보 결과
    1. Splunk 결과 Matplotlib 이용하여 Chart Image 생성
    1. 생성된 Image PDF append
    1. PDF 생성
    1. PDF 파일 Slack 전달
1. Template 설계
    1. CPU 사용률
    ![CPU 사용률](https://github.com/bulgemi/opbot/blob/master/doc/501reportcpu.png)
    1. MEMORY 사용률
    ![MEMORY 사용률](https://github.com/bulgemi/opbot/blob/master/doc/501reportmemory.png)
