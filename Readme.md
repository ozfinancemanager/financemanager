
<h1>💭 Finance Manager ERD</h1>

![image](https://github.com/user-attachments/assets/8acbeb5d-90fe-4184-b5e8-8c0515ebe8ac)

👀 USERS와 ACCOUNTS 사이의 관계는 각 유저가 여러 개의 계좌를 보유할 수 있음을 나타냅니다.
<br/> 
👀 ACCOUNTS와 TRANSACTION_HISTORY의 관계는 각 계좌별로 여러 거래 기록이 있을 수 있음을 의미합니다.
<br/> 
<br/>
<h1>💫 Finance Manager Flowchart</h1>
<br/> Finance Manager의 회원가입, 로그인, 로그아웃 플로우는 다음을 따릅니다.
<br/> 

![image](https://github.com/user-attachments/assets/f509c2b4-fb80-4dc9-b038-46c47bdd1e98)

<br/> 
👾 회원가입 진행 시 이메일, 비밀번호, 휴대폰 번호의 유효성 등을 serializer를 통해 검증합니다.
<br/> 
👾 로그인 진행 시 해당 이메일과 비밀번호의 유효성을 검증한 후 로그인이 처리됩니다.
<br/> 
👾 로그아웃 시도 시 의사 재확인 후 로그아웃, 이전 사용된 refresh token은 보안 강화를 위해 blacklist에 추가되어 다시 사용할 수 없게 됩니다.
<br/> 
👾 새로운 로그인 시도 시 refresh token이 새롭게 생성됩니다.
