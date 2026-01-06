import streamlit as st
import random
import time

# 화면 크기 설정
WIDTH = 800
HEIGHT = 600

# 세션 상태 초기화
if "score" not in st.session_state:
    st.session_state.score = 0  # 점수
if "bullets" not in st.session_state:
    st.session_state.bullets = []  # 총알 목록
if "target_position" not in st.session_state:
    st.session_state.target_position = (random.randint(100, 700), random.randint(100, 400))  # 타겟의 랜덤 위치
if "game_started" not in st.session_state:
    st.session_state.game_started = False  # 게임이 시작됐는지 여부

# 타겟 클릭 시 점수 업데이트
def on_target_hit():
    st.session_state.score += 1  # 점수 증가
    st.session_state.target_position = (random.randint(100, 700), random.randint(100, 400))  # 새로운 타겟 위치

# 총알 생성
def create_bullet(start_x, start_y):
    return {"x": start_x, "y": start_y, "active": True}

# 총알을 화면에서 이동시키는 함수
def move_bullets():
    new_bullets = []
    for bullet in st.session_state.bullets:
        if bullet["active"]:
            bullet["y"] -= 10  # 총알의 Y 좌표를 10만큼 이동
            # 타겟과 충돌하면 점수 증가
            if (bullet["x"] > st.session_state.target_position[0] and 
                bullet["x"] < st.session_state.target_position[0] + 50 and 
                bullet["y"] > st.session_state.target_position[1] and 
                bullet["y"] < st.session_state.target_position[1] + 50):
                on_target_hit()
                bullet["active"] = False  # 총알 비활성화
            new_bullets.append(bullet)
    st.session_state.bullets = new_bullets

# 게임 시작 시 초기화
def start_game():
    st.session_state.score = 0
    st.session_state.bullets = []
    st.session_state.target_position = (random.randint(100, 700), random.randint(100, 400))
    st.session_state.game_started = True

# 게임 시작 버튼
if not st.session_state.game_started:
    st.button("게임 시작", on_click=start_game)  # 게임 시작 버튼

# 게임이 시작되었으면
if st.session_state.game_started:
    st.write("게임 시작!")
    
    # 마우스 클릭이나 스페이스바로 총알 발사
    mouse_x = st.slider("총알 발사 위치 X", 0, WIDTH, random.randint(100, 700))
    mouse_y = st.slider("총알 발사 위치 Y", 0, HEIGHT, random.randint(100, 400))

    if st.button("총 쏘기"):
        st.session_state.bullets.append(create_bullet(mouse_x, mouse_y))
    
    # 총알을 이동시키는 함수 호출
    move_bullets()

    # 총알과 타겟을 화면에 표시
    for bullet in st.session_state.bullets:
        if bullet["active"]:
            st.markdown(
                f"""
                <div style="position: absolute; left: {bullet['x']}px; top: {bullet['y']}px; 
                width: 5px; height: 20px; background-color: yellow; border-radius: 2px;"></div>
                """,
                unsafe_allow_html=True,
            )

    # 타겟 표시
    st.markdown(
        f"""
        <div style="position: absolute; left: {st.session_state.target_position[0]}px; top: {st.session_state.target_position[1]}px; 
        width: 50px; height: 50px; background-color: red; border-radius: 50%;"></div>
        """,
        unsafe_allow_html=True,
    )

    # 화면에 점수 표시
    st.write(f"현재 점수: {st.session_state.score}")
