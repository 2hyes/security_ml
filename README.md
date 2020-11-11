# security_ml

## 1.개요
- 목표: Detect cyber attack log data(using UNSW-NB15) \
사이버 공격 로그 데이터(UNSW-NB15)로 인공신경망을 학습시켜, 웹 서버를 통해 iOS앱으로 로그 정보에 대한 공격여부 및 공격 정보 예측 결과 시각화한다.

## 2. 예측 모델 소개
- decision tree
- MLP(인공신경망): training accuracy = 0.85, test accuracy = 0.823
- AdaBoost
- SVC
- GaussianNB

activation ='relu’, solver = 'adam’, alpha = 1e-4, H = (70, 58, 77, 95, 57), max_iter=10000
를 파라미터로 갖는 MLP를 최종 모델로 선택한다.

## 3. 개발환경  
1) 개발 환경
* Windows 10. i5-7200U, RAM 8.0GB, 64bit
* macOS Catalina 10.15.5
* conda 4.8.4
* XCode version 11.4.1

2) 개발 언어
* Python 3.8.5 
* Swift 4

3) 라이브러리  
* Data analysis
   * numpy 1.19.1, pandas 1.1.1, scikit-learn 0.23.2, scipy 1.5.2, sklearn 0.0
* Server
   * Flask 1.1.2
   
## 코드 실행 및 재현 방법

1. 트레이닝셋으로 예측 모델 생성
```
python modeling.py
```

2. 생성한 best model로 테스트셋 예측 
```
python test.py
```

3. flask 웹 서버 실행
```
 python app.py
 ```

4. date칸에 1 ~ 4 숫자 중 입력 \
: 테스트셋을 5천개씩 나누어 일일 로그로 가정했다.

5. 웹서버에 입력한 해당 일에 대한 예측 결과 출력됨

6. Xcode에서 'Get'버튼을 누르면, 바로 결과 plot이 생성됨 \
: 시연영상 6:51에서 확인 가능

## 발표 및 시연 영상

[발표 자료](https://github.com/2hyes/security_ml/blob/master/presenstation/%5B%EB%B0%9C%ED%91%9C%5D%EC%9E%A1%EC%95%98%EB%8B%A4%2C%20%EB%96%BD!.pdf)
[발표 영상](https://youtu.be/p4SZcEooRak?t=410)
