# TASK 수행 기능
## 요약
> 사용자가 수행하려는 스크립트를 등록하고 챗봇을 이용하여 수행하는 위한 방법을 제안하고 아키텍처 구조와 기능에 대해 설명한다. 
## 서론
> 현재 챗봇은 3가지의 연구 트랜드를 보이고 있다.
> 첫번째로 챗봇 알고리즘에 대한 연구이다. 최근에는 딥러닝을 통해 자연어를 처리하는 방법이 많이 연구되고 있다.
> 두번째는 경영이나 사회과학적인 측면에서의 챗봇 적용에 관현 연구이다.
> 챗봇이라는 기술적인 서비스를 어떠한 방식으로 사람한테 적용할 것인지 혹은 어떻게 하면 사람들이 효과적으로 챗봇을 받아들일 수 있을지에 대한 연구를 의미한다.
> 마지막으로, 다양한 도메인 특성에 맞는 챗봇 개발 연구이다.
> OPBOT은 IT 도메인 특성에 맞게 구현된 챗봇으로 주요 목적은 특정 이벤트에 대한 TASK 추천 및 수행, 사용자(그룹)를 위한 TASK 등록 및 수행을 지원한다.
## 관련 연구
### 분석
> 현재 개발된 OPBOT은 IT 인프라 자원에서(서버, 미들웨어, 어플리케이션) 발생한 특정 이벤트를 대응하는 것을 목적으로 구현되어 있어 이벤트가 발생한 경우에만 사용할 수 있다.
> 하지만 IT 인프라 자원을 운영하는 담당자의 경우 이벤트가 발생한 상황이 아니더라도 모니터링 같은 작업을 수행할 필요가 있다.
> 이를 위해서는 이벤트 기반의 처리에 사용자 기반의 처리가 추가되어야 한다.
### 요건
1. [사용자(그룹) 관리](https://github.com/bulgemi/opbot/blob/master/doc/Manager.md) __[관리모듈(Manager), GUI]__
    * 권한검증
    * 암호화
    * 사용자/그룹 생성/수정/삭제
        * Slack에 등록된 사용자 중 TASK 수행 가능한 사용자/그룹 관리
1. [TASK 관리](https://github.com/bulgemi/opbot/blob/master/doc/Manager.md) __[관리모듈(Manager), GUI]__
    * TASK 신규 정의 (K8s or SSH 연동일 경우)
        * 운영자가 사용하려는 TASK 정의(TASK 명, 설명)
        * Web Editor
        * Code Inspection
    * TASK 관리
        * 유형별(OPMATE[1], K8s[2], Ansible[3], SSH) 등록된 TASK 조회
        * TASK 등록/변경/삭제
    * TASK별 사용자/그룹 관리
        * TASK와 사용자/그룹 연결
    * TASK 유효성 검증
        * 사용가능 TASK 여부
1. [챗봇](https://github.com/bulgemi/opbot/blob/master/doc/Chatbot.md) __[챗봇(Chatbot)]__
    * 사용자 검증(인증, 권한)
        * Slack을 통해 요청한 사용자에 대한 유효성 검증 및 소속 그룹 확인
        * 사용자(그룹) 사용 가능한 TASK 검증 
1. [명령어](https://github.com/bulgemi/opbot/blob/master/doc/Chatbot.md) __[챗봇(Chatbot)]__
    * 사용자(그룹) TASK 리스트
    * TASK 수행
1. [TASK 수행](https://github.com/bulgemi/opbot/blob/master/doc/TaskExecutor.md) __[수행모듈(TaskExecutor)]__
    * 다양한 연동 방식 제공(OPMATE[1], K8s[2], Ansible[3], SSH)
    * 결과 출력 포맷(PDF)
    * System 기본 정보(CPU, Memory) Chart 제공(파라메터 설정)
        > !cpu, node01!<br>
        > !mem, node01!
## 구현 및 적용
## 결론
## References 
* [챗봇 기반의 지능형 시각화 프레임워크.pdf](https://github.com/bulgemi/opbot/blob/master/doc/%EC%B1%97%EB%B4%87%20%EA%B8%B0%EB%B0%98%EC%9D%98%20%EC%A7%80%EB%8A%A5%ED%98%95%20%EC%8B%9C%EA%B0%81%ED%99%94%20%ED%94%84%EB%A0%88%EC%9E%84%EC%9B%8C%ED%81%AC.pdf "챗봇 기반의 지능형 시각화 프레임워크")
* [사용자 니즈 기반의 챗봇 개발 프로세스 디자인 사고방법론을 중심으로.pdf](https://github.com/bulgemi/opbot/blob/master/doc/%EC%82%AC%EC%9A%A9%EC%9E%90%20%EB%8B%88%EC%A6%88%20%EA%B8%B0%EB%B0%98%EC%9D%98%20%EC%B1%97%EB%B4%87%20%EA%B0%9C%EB%B0%9C%20%ED%94%84%EB%A1%9C%EC%84%B8%EC%8A%A4%20%EB%94%94%EC%9E%90%EC%9D%B8%20%EC%82%AC%EA%B3%A0%EB%B0%A9%EB%B2%95%EB%A1%A0%EC%9D%84%20%EC%A4%91%EC%8B%AC%EC%9C%BC%EB%A1%9C.pdf "사용자 니즈 기반의 챗봇 개발 프로세스 디자인 사고방법론을 중심으로")
* [빈칸 되묻기 방식 기반 다중 키워드 처리가 가능한 주문용 챗봇 개발.pdf](https://github.com/bulgemi/opbot/blob/master/doc/%EB%B9%88%EC%B9%B8%20%EB%90%98%EB%AC%BB%EA%B8%B0%20%EB%B0%A9%EC%8B%9D%20%EA%B8%B0%EB%B0%98%20%EB%8B%A4%EC%A4%91%20%ED%82%A4%EC%9B%8C%EB%93%9C%20%EC%B2%98%EB%A6%AC%EA%B0%80%20%EA%B0%80%EB%8A%A5%ED%95%9C%20%EC%A3%BC%EB%AC%B8%EC%9A%A9%20%EC%B1%97%EB%B4%87%20%EA%B0%9C%EB%B0%9C.pdf "빈칸 되묻기 방식 기반 다중 키워드 처리가 가능한 주문용 챗봇 개발")
* [BERT 모델과 지식 그래프를 활용한 지능형 챗봇.pdf](https://github.com/bulgemi/opbot/blob/master/doc/BERT%20%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EC%A7%80%EC%8B%9D%20%EA%B7%B8%EB%9E%98%ED%94%84%EB%A5%BC%20%ED%99%9C%EC%9A%A9%ED%95%9C%20%EC%A7%80%EB%8A%A5%ED%98%95%20%EC%B1%97%EB%B4%87.pdf "BERT 모델과 지식 그래프를 활용한 지능형 챗봇")
