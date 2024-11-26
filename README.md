![Stylized laptop side mockup](https://github.com/user-attachments/assets/b64e834b-dae0-43f0-9c2e-b42139c6b804)
# 🐣StudyBuddy AI🐣
노티와 함께 성장하는 공부 파트너, StudyBuddy의 AI입니다!

<br>

## 🔎 Service Introduction
StudyBuddy는 가상의 캐릭터 `노티`가 학습 자세를 관찰하고 피드백을 제공하며, 학습 결과를 시각화하여 목표 달성을 돕는 학습 플랫폼입니다.
이제, 혼자 공부하지 말고, StudyBuddy와 함께하세요!
### 🎥 Demonstration video
[![StudyBuddy 소개 영상](https://github.com/user-attachments/assets/8a6c9c70-004c-4e74-9f5e-1d58c37a0141)
](https://youtu.be/QcWG6GFLRQc)

<br><br>


## 💡Features
> StudyBuddy의 AI는 학습자의 자세를 실시간으로 분석하여 학습 효율을 높이고 올바른 자세를 유지하도록 도움을 제공합니다.
### 1. Object Detection
- YOLOv8 모델을 사용하여 얼굴, 사람, 휴대폰 등 학습 환경을 분석합니다.
- **검출 클래스:**
  + 얼굴: `sleeping face`, `awake face`
  + 사람: `sleeping person`, `awake person`
  + 휴대폰: `phone`
- **모델 성능:**
  + Precision: 0.97696, Recall: 0.93202
  + mAP50: 0.97415, mAP50-95: 0.85769
<table>
  <tbody>
    <tr>
      <td align="center"><img src="https://github.com/user-attachments/assets/83536e1b-2371-45e1-a4fe-8f268c23a4a6"width="200px;" alt="학습 결과"/></td>
      <td align="center"><img src="https://github.com/user-attachments/assets/a7c1f2d3-b4ad-4ab3-8e25-213fd5d989dd"width="100px;" alt="학습 결과"/></td>
      <td align="center"><img src="https://github.com/user-attachments/assets/2b5d537e-5f18-47c8-8a31-81c20b85f9cc"width="220px;" alt="학습결과"/></td>
    </tr>
  </tbody>
</table>

### 2. Pose Estimation
- MediaPipe를 활용하여 학습 자세를 분석합니다.
- **기능:**
  + 어깨 기울기를 바탕으로 올바른 자세와 잘못된 자세를 판별합니다.
  + Hand Pose Detection으로 휴대폰 사용 여부를 감지합니다.
- **기준:**
  + 어깨 기울기 < 0.3일 경우 올바른 자세로 간주합니다.
  + 손 위치와 휴대폰 Bounding Box 간의 거리로 휴대폰 사용을 판별합니다.
<table>
  <tbody>
    <tr>
      <td colspan="2" align="center">estimation 결과</td>
      <td align="center">올바른 자세</td>
      <td align="center">올바르지 않은 자세</td>
    </tr>
    <tr>
      <td align="center"><img src="https://github.com/user-attachments/assets/3a8a92b6-fb0d-4547-8a65-4a44de65496a" height="180" alt="estimation결과"/></td>
      <td align="center"><img src="https://github.com/user-attachments/assets/bc107072-5166-40aa-80c0-e650ea2c3ea9" height="180" alt="estimation결과"/></td>
      <td align="center"><img src="https://github.com/user-attachments/assets/fe2472d6-d814-4961-a96a-60f508003f26" height="160" alt="올바른자세"/></td>
      <td align="center"><img src="https://github.com/user-attachments/assets/059c4c84-a9bf-4805-9878-81d4c7afc8f5" height="160" alt="올바르지않은자세"/></td>
    </tr>
  </tbody>
</table>

### 3. Eye Tracking
- Dlib를 활용하여 눈동자의 움직임과 깜빡임 빈도를 분석합니다.
- **기능:**
  + 눈 깜빡임을 통해 졸음 상태를 판별합니다.
  + 동공 움직임 분석으로 집중도를 측정합니다.
<table>
  <tbody>
    <tr>
      <td align="center">얼굴 랜드마크</td>
    </tr>
    <tr>
      <td align="center"><img src="https://github.com/user-attachments/assets/104e3dde-9d9d-4ff8-b308-3deddd9af4c7"width="240px;" alt="eyetracking"/></td>
    </tr>
  </tbody>
</table>

<br><br>

## 📊 DataSet
- **구축:**
    + 10개의 장소, 3명의 학습자, 3가지의 각도, 다양한 자세를 반영한 990장의 데이터를 수집했습니다.
    + 각도는 정면, 좌측면, 우측면입니다.
    + 자세는 휴대폰을 하는 자세, 누을 감고 있는 상태에서의 각기 다른 자세, 일반적으로 공부하는 자세입니다.
- **라벨링:**
  + 얼굴, 사람, 휴대폰 검출을 위한 클래스별로 데이터를 분리했습니다.
<table>
  <tbody>
    <tr>
      <td align="center">데이터셋 정리</td>
      <td align="center">Pseudo labeling</td>
      <td align="center">Labeling</td>
    </tr>
    <tr>
      <td align="center"><img src="https://github.com/user-attachments/assets/cad0ce0b-ce6a-4a74-a815-343f74ab7b37" height="180" alt="데이터셋정리"/></td>
      <td align="center"><img src="https://github.com/user-attachments/assets/58a0a1f2-4a42-4213-808f-cc7fafff47be" height="180" alt="pseudo labeling"/></td>
      <td align="center"><img src="https://github.com/user-attachments/assets/c0a3a443-4e09-462e-bcae-2192f81d542a" height="180" alt="labeling"/></td></td>
    </tr>
  </tbody>
</table>

 <br><br>

 ## 🎯 Rule-Based Learning State Classification
 1. **잘못된 자세**: 어깨 기울기 0.3 이상
 2. **수면 상태**: `sleeping Face` 또는 `Sleeping Person` 클래스 검출
 3. **휴대폰 사용**: 손 위치와 휴대폰 Bounding Box 간 거리로 판별

<br><br>

## ⚙️ Setup
```
conda create -n env_name python=3.6 
conda update -n base -c defaults conda // you may need this
conda install conda-forge::dlib
conda install conda-forge/label/cf201901::dlib
conda install conda-forge/label/cf202003::dlib
```
```
pip install opencv-python       
pip install scipy
pip install ultralytics
```
<br><br>

## 😁 AI Developer
<table>
  <tbody>
    <tr>
      <td align="center"><img src="https://github.com/user-attachments/assets/e25ad73a-9d66-462c-884a-2eb669b2f4cb"width="100px;" alt="배주현"/></td>
    <tr/>
    <tr>
        <td align="center">배주현</td>
    </tr>
    <tr>
        <td align="center"><a href="https://github.com/qowngus33">qowngus33</a></td>
    </tr>
  </tbody>
</table>
