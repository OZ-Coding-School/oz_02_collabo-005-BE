## 리포지토리 소개
> `oz_02_collabo-005-BE`는 `OZ 코딩 스쿨`에서 진행되는 협업 프로젝트 과정에 참여중인 5팀의 백엔드 리포지토리 입니다.

---

## 📖 프로젝트 소개
> ### 🛵 Okivery
> 📱 한국에 사는 외국인들이 사용하는 배달음식 어플!!  
> 👌 에피타이저부터 디저트까지 모두 한 번의 주문으로 해결!!  
> 😢 기존의 배달 어플은 언어와 결제라는 큰 벽이 존재하여 외국인들이 사용하기에 많은 어려움이 존재했으며, 한 주문에 한 식당만 선택하는 번거로움도 존재했습니다.  
> 🧐 저희는 이러한 문제점들을 개선하여 외국인들이 사용하기 편한 배달 어플을 만들기로 했습니다!!
>  
> 또한 여기에서 멈추지 않고 출산율 급감으로 초래된 인구절벽의 대한민국이 역동적인 성장을 이어갈 수 있도록 외국인들이 한국에서 음식과 물건 그리고 서비스를 구매하여 당일 배송 받을 수 있는 언어장벽, 온라인결제장벽으로 부터 자유로운 이커머스&컨시어지 플랫폼으로 발전 시키겠습니다.

---
## :link: 링크

> ### [💻 FE Repository](https://github.com/OZ-Coding-School/oz_02_collabo-005-FE)

---
## 🗣️ 프로젝트 발표 영상 & 발표 문서

> ### 🗓️ 2024.04.16 - 2024.05.23
> ### [📺 발표 영상 추후 공개]()

---
## 🧰 사용 스택

<div align=center style="widht:100%"> 
  <img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/django-0B4B33?style=for-the-badge&logo=django&logoColor=white">
  <br>
  <img src="https://img.shields.io/badge/amazonaws-232F3E?style=for-the-badge&logo=amazonaws&logoColor=white">
  <img src="https://img.shields.io/badge/AWS EC2-ff9900?style=for-the-badge&logo=amazonec2&logoColor=white">
  <img src="https://img.shields.io/badge/aws rds-527fff?style=for-the-badge&logo=amazonrds&logoColor=white">
  <br>
  <img src="https://img.shields.io/badge/docker-2496ED?style=for-the-badge&logo=docker&logoColor=white">
  <img src="https://img.shields.io/badge/linux-FCC624?style=for-the-badge&logo=linux&logoColor=black"> 
  <img src="https://img.shields.io/badge/mysql-4479A1?style=for-the-badge&logo=mysql&logoColor=white"> 
  <img src="https://img.shields.io/badge/postman-FF6C37?style=for-the-badge&logo=postman&logoColor=white">
  <img src="https://img.shields.io/badge/nginx-006272?style=for-the-badge&logo=nginx&logoColor=green">
  <br>
</div>


--- 

## :busts_in_silhouette: 팀 동료

### BD
- 장유위
- 천지원

### FE

| <a href=https://github.com/woic-ej><img src="https://avatars.githubusercontent.com/u/77326820?v=4" width=100px/><br/><sub><b>@woic-ej</b></sub></a><br/> | <a href=https://github.com/jjaeho0415><img src="https://avatars.githubusercontent.com/u/91364411?v=4" width=100px/><br/><sub><b>@jjaeho0415</b></sub></a><br/> |
| :------------------------------------------------------------------------------------------------------------------------------------------------------: | :------------------------------------------------------------------------------------------------------------------------------------------------------------: |
|                                                                          최은진                                                                          |                                                                             정재호                                                                             |


### BE

| <a href=https://github.com/sub-blind><img src="https://avatars.githubusercontent.com/u/58137602?v=4" width=100px/><br/><sub><b>@sub-blind</b></sub></a><br/> | <a href=https://github.com/KangJeongHo1><img src="https://avatars.githubusercontent.com/u/155045987?v=4" width=100px/><br/><sub><b>@KangJeongHo1</b></sub></a><br/> | <a href=https://github.com/newbission><img src="https://avatars.githubusercontent.com/u/155050120?v=4" width=100px/><br/><sub><b>@newbission</b></sub></a><br/> |
| :----------------------------------------------------------------------------------------------------------------------------------------------------------: | :-----------------------------------------------------------------------------------------------------------------------------------------------------------------: | :-------------------------------------------------------------------------------------------------------------------------------------------------------------: |
|                                                                            김재섭                                                                            |                                                                               강정호                                                                                |                                                                             윤준명                                                                              |

## 📑 프로젝트 규칙

### Branch Strategy
> - main / dev / docs 브랜치 기본 생성 
> - main과 dev로 직접 push 제한
> - README, gitignore 같은 문서파일 docs로 push
> - PR 전 최소 2인 이상 승인 필수

### Progress
#### 1. FOLK & CLONE
> 팀 리포지토리에 직접적인 접근을 제한하기위해 팀 리포지토리를 각자의 리포지토리로 포크
> 
1. [👫 팀 리포지토리]()를 자신의 깃 리포지토리 포크
   1. ❗️주의❗️ `main`브랜치 뿐만 아니라 모든 브랜치를 가져와야함
2. 포크한 리포지토리를 로컬에 `CLONE`
   1. ❗️주의❗️ `dev` 브랜치를 클론해야함
3. 잘 클론 되었는지 확인
```bash
git clone -b dev "자신의 깃 리포지토리 주소"

# remote의 이름이 'origin'인지, branch가 'dev'인지 확인
git remote -v
> origin	https://github.com/newbission/리포지토리이름.git (fetch)
> origin	https://github.com/newbission/리포지토리이름.git (push)
```

#### 2. PULL
> 현재까지 진행된 내용을 원격 저장소에서 로컬로 가져오기
1. 로컬과 팀 리포지토리 연결(최초 한 번)
2. 팀 리포지토리의 `main`브랜치의 내용을 `PULL`
   1. 필요시 `dev`나 `docs`브랜치의 내용을 가져와도 됨
```bash
# 최초 한 번 upstream 연결
git remote add upstream "https://github.com/OZ-Coding-School/oz_02_collabo-005-BE"

# upstream에서 최신 내용 pull
git pull upstream main
```

#### 브랜치 생성
> 개발할 내용에 맞게 브랜치 생성

1. 현재 브랜치가 `dev`인지 확인
2. 새 브랜치 만들기
```bash
# 현재 branch 확인
git branch
> * dev

# 브랜치 생성
git branch feat/sub-blind#이슈번호
git switch feat/sub-blind#이슈번호
```

#### PUSH 및 브랜치 제거
> 작업내용을 `COMMIT`, `PUSH`
> 모든 작업이 완료됐다면 PR을 생성해 머지 요청
> 브랜치를 `dev`로 변경 후 사용한 브랜치 제거
```bash
# push 하기
git add .
git commit -m "커밋메시지"
git push origin feat/sub-blind#이슈번호


# PR 한 뒤 사용한 branch 삭제
git switch dev
git branch -D feat/sub-blind#이슈번호

```

### Git Convention
> 1. 적절한 커밋 접두사 작성
> 2. 커밋 메시지 내용 작성
> 3. 내용 뒤에 이슈 (#이슈 번호)와 같이 작성하여 이슈 연결

> | 접두사     | 설명                           |
> | ---------- | ------------------------------ |
> | Feat :     | 새로운 기능 구현               |
> | Add :      | 에셋 파일 추가                 |
> | Fix :      | 버그 수정                      |
> | Docs :     | 문서 추가 및 수정              |
> | Style :    | 스타일링 작업                  |
> | Refactor : | 코드 리팩토링 (동작 변경 없음) |
> | Test :     | 테스트                         |
> | Deploy :   | 배포                           |
> | Conf :     | 빌드, 환경 설정                |
> | Chore :    | 기타 작업                      |

```bash
git commit -m "Feat: 로그인 API 개발 완료 (#이슈번호)"
```


### Pull Request
> ### Title
> * 제목은 '[Feat] 홈 페이지 구현'과 같이 작성합니다.

> ### PR Type
> > - FEAT: 새로운 기능 구현
> > - ADD : 에셋 파일 추가
> > - FIX: 버그 수정
> > - DOCS: 문서 추가 및 수정
> > - STYLE: 포맷팅 변경
> > - REFACTOR: 코드 리팩토링
> > - TEST: 테스트 관련
> > - DEPLOY: 배포 관련
> > - CONF: 빌드, 환경 설정
> > - CHORE: 기타 작업

> ### Description
> * 구체적인 작업 내용을 작성해주세요.
> * 이미지를 별도로 첨부하면 더 좋습니다 👍

> ### Discussion
> * 추후 논의할 점에 대해 작성해주세요.

### Code Convention
> - 최대한 PEP8 참고
> - 패키지명 전체 소문자
> - 클래스명, 인터페이스명 CamelCase
> - 클래스 이름 명사 사용
> - 상수명 SNAKE_CASE
> - Controller, Service, Dto, Repository, mapper 앞에 접미사로 통일(ex. MemberController)
> - service 계층 메서드명 create, update, find, delete로 CRUD 통일(ex. createMember) 
> - Test 클래스는 접미사로 Test 사용(ex. memberFindTest)

### Communication Rules
> - ZEP, Discord 활용
> - 정기 회의
