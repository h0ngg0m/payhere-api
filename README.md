# payhere-api


## 실행 방법
```
git clone https://github.com/h0ngg0m/payhere-api.git

cd payhere-api

docker-compose up 
```
## 코드 스타일 일관성 유지
- 코드 스타일 일관성 유지를 위해 `black`, `isort`, `flake8`를 사용했습니다.

## 로그인, 로그아웃
- 로그인: `Post /api/v1/auth/login`
  - 로그인 (`인증`) 시, JWT (Access Token) 를 발급합니다. 이후 API 요청 시, JWT 를 `Authorization` 헤더에 담아서 요청하는 것으로 `인가`를 처리합니다. 
  - 로그인 시 회원 (`User 모델`) 의 `logout_flag` 를 False 로 변경합니다. (이유는 아래 `로그아웃` 참고)
- 로그아웃: `Delete /api/v1/auth/logout`
  - 로그인 시 발급되는 JWT 를 서버에서 간단하게 제어할 수 있는 방법은 없다고 판단하였고 따라서 서버에서 로그아웃을 제어하기 위해 `logout_flag` (회원의 로그아웃 여부를 나타내는 필드) 를 사용했습니다.
    - 로그아웃 시, 회원의 `logout_flag` 를 True 로 변경합니다.
  - `logout_flag`가 True인 상태로 권한이 필요한 API 요청 시, `401 Unauthorized` 응답을 반환하고 로그인을 유도합니다.

## 상품 초성 검색
- 상품 리스트 조회 `Get /api/v1/products`
- 상품 이름에 대한 `한글 초성 검색`을 지원하기 위해 상품 `생성`, `수정`시 사용자가 입력한 `name` 필드 값중 한글인 부분에서 초성을 추출하여 `name_chosung` DB 컬럼에 저장했습니다.
  - 이후 상품 리스트 조회 시, `name_chosung` 필드를 사용한 초성 검색, `name` 필드를 사용한 한글 검색을 지원합니다.

## 기타
- API 명세서 위치: 도커 실행 후 http://localhost:8000/docs 에서 확인 가능합니다.
- DB DDL 위치: /payhere-api/sql/ddl.sql
