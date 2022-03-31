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


### code
 - NMS(non-maximum suppression) : 성능 향상에 도움이 된다.
 현재 픽셀을 기준으로 주변 픽셀과 비교했을 때 최대값인 경우 그대로 놔두고 아닌 경우 제거하는 것. - prediction이후 threshold 가 넘는 같은 클래스의 바운딩 박스들이 합쳐 나옴.

 - agnostic_nms : classification없이 바운딩 박스만 찾고 싶을 때 사용

 - EMA(Exponential Moving Average) : 기존의 moving average보다 최근의 데이터에 가중치를 둔 평균값 - 성능을 안정화 하는 역할. (기본적으로는 활용 안하도록 되어 있다.)

 - stride : 필터를 적용하는 간격. 스트라이드를 크게 하면 출력 데이터의 크기가 작아진다.

 - model에 이미지 입력 : pred형태는 바운딩 박스 위치, Confidence, Class확률 정보