## 2022 한국공학대학교 졸업작품
- S3-2팀 한상우

## Backend-server
- Flask
- yolov5

## Description
 - tello 드론을 사용하여 화재 인식 및 인식된 데이터 정보를 Client 에게 전달해주는 서버 역할입니다.
  streaming기능 및 드론을 직접적으로 제어할 수 있는 역할도 가능합니다.
  
## route info
`/start_streaming`  
 - [ ] tello 드론의 카메라와 연동하여 실시간 스트리밍   
 - [ ] 화재 식별시 데이터 Json형태로 제공

## Todo
 - [ ] Dockerize
 - [ ] streamoff 기능
 - [ ] tello api 사용하여 방향 및 속도 제어
 - [ ] aws배포
