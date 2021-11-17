# Search Tracking Drone

Full Tech [wiki page](https://ruffalolavoisier.github.io/SearchTrackingDrone-Wiki/)  

## 저장소 구조
### [아두이노 PWM 읽기/쓰기](https://github.com/RuffaloLavoisier/SearchTrackingDrone/tree/Dream/ReadWriteArduino)
제어장치인 Arduino를 활용하여 flight controller와 RC receiver의 신호를 자체적으로 생성할 수 있습니다.   
### [물리적인 객체 추적](https://github.com/RuffaloLavoisier/SearchTrackingDrone/tree/Dream/FaceTracking)
pyimagesearch 에서 나온 예제 코드를 기반으로 특정 모듈 없이 아두이노 보드와 연결하여 시리얼 통신 기반으로 코드가 작동할 수 있도록 재구성하였습니다.  
### [비행장치 빌드 환경 구축](https://github.com/RuffaloLavoisier/SearchTrackingDrone/tree/Dream/PixPI)
메인 드론 중앙 코드를 빌드할 환경 및 개발 팁을 기록한 문서입니다.  
### [SBC SERVER](https://github.com/RuffaloLavoisier/Room-CAMERA)
이 프로젝트의 프로토타입 코드입니다.  

## 동작 방식

비행이 시작되면 안면 검출이 시작되어 검출된 위치에 해당되는 위치와 조난자의 상황을 전송 받을 수 있다.
