import streamlit as st
import random
from openai import AzureOpenAI

# API 키 입력 받기
if "api_key" not in st.session_state:
    st.session_state["api_key"] = ""

api_key = st.text_input("API key를 넣어주세요", type="password", value=st.session_state["api_key"])

# API 키 저장
if api_key:
    st.session_state["api_key"] = api_key

# API 키 확인
if not st.session_state["api_key"]:
    st.warning("API key를 입력해주세요.")
    st.stop()

# Azure OpenAI 클라이언트 생성
try:
    client = AzureOpenAI(
        azure_endpoint="https://zion-aoai.openai.azure.com/",
        api_key=st.session_state["api_key"],
        api_version="2024-02-15-preview",
    )
    st.success("Azure OpenAI 클라이언트가 성공적으로 생성되었습니다! 🚀")

except Exception as e:
    st.error(f"클라이언트 생성 중 오류 발생: {e}")
    st.stop()

st.title("배정")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
# st.write("")
# st.write("")
# st.write("")
# st.write("")
# st.write("")
st.write("")    

col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    st.write("")
    # 저장된 데이터를 보여주는 기능
    if st.button("저장된 데이터 보기"):
        try:
            with open("grade1.txt", "r") as f:
                data = f.read()
            st.text_area("저장된 학년/학생 리스트", data)
        except FileNotFoundError:
            st.warning("아직 저장된 데이터가 없습니다.")
with col2:
    # 학년과 학생 이름을 입력받기
    grade = st.text_input("학년을 입력하세요")
    student_name = st.text_input("학생 이름을 입력하세요")

    # 입력 버튼을 클릭하면 데이터를 파일에 저장
    if st.button("저장"):
        if grade and student_name:
            with open("grade1.txt", "a") as f:
                f.write(f"{grade}학년 - {student_name}\n")
            st.success(f"{grade}학년 {student_name}이(가) 저장되었습니다!")
        else:
            st.warning("학년과 학생 이름을 모두 입력해주세요.")


    # 배정 버튼 클릭 시 순서 지정
    if st.button("배정", use_container_width=True, icon=":material/cruelty_free:"):
        st.write(grade, "학년", student_name, "학생의 순서")
        numbers = ['빙하가 이븐하게 얼었어요', '퀴즈', '책갈피','너펭귄']
        
        # Remove '윤여완을 이겨라' and shuffle the rest
        other_numbers = numbers[1:]
        random.shuffle(other_numbers)
        
        # Add '윤여완을 이겨라' back at index 0
        final_list = ['빙하가 이븐하게 얼었어요'] + other_numbers
        st.table(final_list)

with col3:
    st.write("")
    st.markdown("#### 이름 삼행시")
    
    if student_name:
        deployment_name = "gpt-4o"  # ⚠️ 실제 Azure 배포된 모델 이름으로 변경해야 함

        try:
            response = client.chat.completions.create(
                model=deployment_name,  # ✅ Azure는 'gpt-4o'가 아니라 배포된 모델 이름을 사용해야 함
                messages=[
                    {"role": "system", "content": """너는 student 이름으로 우리 모두가 빵터질만한 삼행시 만들어줘. 
                    웃음폭탄 기대할게. 아재개그 버전으로. 아래는 샘플이야. 학생이름 허시온. 
                    - 허 : 허시온
                    - 시 : 시끄러 못살곘네..
                    - 온 : 온 동네방네 방구 끼고 다니지 마라... """},
                    {"role": "user", "content": f"학생이름은 {student_name}"}
                ],
            stream=True  # ✅ 스트리밍 응답 활성화
            )
            st.write_stream(response)
        except Exception as e:
            st.write("이름삼행시를 지을 수 없습니다. azure openai client 를 확인해주세요.")

    else:
        st.warning("학생 이름을 입력해주세요.")

    
