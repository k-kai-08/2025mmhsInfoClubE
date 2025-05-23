import streamlit as st

# --- 세션 상태 초기화 ---
if 'current_room' not in st.session_state:
    st.session_state.current_room = "침실"
if 'inventory' not in st.session_state:
    st.session_state.inventory = [] # 획득한 아이템 (힌트 포함)
if 'puzzle_solved_desk' not in st.session_state:
    st.session_state.puzzle_solved_desk = False # 책상 서랍 퍼즐 해결 여부
if 'puzzle_solved_photo' not in st.session_state:
    st.session_state.puzzle_solved_photo = False # 사진 퍼즐 해결 여부

# --- 방 정보 및 가구 상호작용 정의 ---
rooms = {
    "침실": {
        "description": "어두운 침실입니다. 창문으로 희미한 빛이 들어옵니다.",
        "left": None,
        "right": "서재",
        "furniture": {
            "침대": {
                "desc": "정돈되지 않은 침대입니다. 아래에 무언가 있는 것 같습니다.",
                "action": "침대 아래를 들춘다",
                "result": "낡은 쪽지 조각 1",
                "hint": "낡은 쪽지 조각 1을 얻었습니다: '시계.. 12시 30분..' (인벤토리에 추가됨)",
                "found_key": "note_piece_1"
            },
            "옷장": {
                "desc": "육중해 보이는 옷장입니다. 굳게 닫혀 있습니다.",
                "action": "옷장을 연다",
                "result": "옷장 열쇠가 없습니다.",
                "hint": "옷장이 잠겨 있습니다. 열쇠가 필요합니다.",
                "requires": "작은 열쇠",
                "unlock_action": "옷장 안에서 낡은 쪽지 조각 3을 발견했습니다: '..' (인벤토리에 추가됨)",
                "found_key": "note_piece_3_from_closet" # 옷장 열고 얻을 힌트
            },
            "액자": {
                "desc": "벽에 걸린 오래된 액자입니다. 그림이 삐뚤어져 있습니다.",
                "action": "액자를 똑바로 건다",
                "result": "액자 뒤에서 작은 열쇠를 발견했습니다!",
                "hint": "작은 열쇠를 얻었습니다. (인벤토리에 추가됨)",
                "found_key": "작은 열쇠"
            }
        }
    },
    "서재": {
        "description": "수많은 책들로 가득 찬 서재입니다. 고요하고 엄숙한 분위기입니다.",
        "left": "침실",
        "right": "거실",
        "furniture": {
            "책장": {
                "desc": "천장까지 닿는 거대한 책장입니다. 흥미로운 책들이 많습니다.",
                "action": "특정 책을 꺼내본다",
                "result": "책 사이에서 낡은 쪽지 조각 2를 발견했습니다: '..책상 서랍..'",
                "hint": "낡은 쪽지 조각 2를 얻었습니다. (인벤토리에 추가됨)",
                "found_key": "note_piece_2"
            },
            "책상": {
                "desc": "잘 정돈된 책상입니다. 서랍이 하나 있습니다.",
                "action": "서랍을 연다",
                "result": "서랍이 잠겨 있습니다. (암호 필요)",
                "hint": "서랍이 잠겨 있습니다. (힌트: 시계)",
                "requires_puzzle": True,
                "puzzle_hint": "시계의 시간을 맞춰보세요.",
                "puzzle_solution": "1230", # '12시 30분' -> 1230
                "puzzle_solved_msg": "서랍이 '딸깍'하고 열립니다. 안에서 '사진 조각'을 발견했습니다!",
                "found_key": "사진 조각",
                "puzzle_state_key": "puzzle_solved_desk"
            },
            "벽시계": {
                "desc": "오래된 괘종시계입니다. 멈춰있는 것 같습니다.",
                "action": "시계를 확인한다",
                "result": "시계는 12시 30분을 가리키고 있습니다.",
                "hint": "시계는 12시 30분입니다."
            }
        }
    },
    "거실": {
        "description": "아늑해 보이는 거실입니다. 정면에 큰 문이 보입니다.",
        "left": "서재",
        "right": None,
        "furniture": {
            "소파": {
                "desc": "푹신해 보이는 소파입니다. 무언가 떨어져 있는 것 같습니다.",
                "action": "소파 쿠션을 들춰본다",
                "result": "소파 쿠션 아래에서 '낡은 쪽지 조각 4'를 발견했습니다! (인벤토리에 추가됨)",
                "hint": "낡은 쪽지 조각 4를 얻었습니다: '..탈출..' (인벤토리에 추가됨)",
                "found_key": "note_piece_4"
            },
            "테이블": {
                "desc": "가운데 놓인 작은 테이블입니다. 무언가를 놓을 수 있을 것 같습니다.",
                "action": "테이블을 살펴본다",
                "result": "여기에 '사진 조각'을 놓아 퍼즐을 맞춰볼 수 있을 것 같습니다.",
                "requires_item_to_interact": "사진 조각",
                "interaction_prompt": "사진 조각을 맞춰봅니다...",
                "puzzle_solved_msg": "사진 조각이 맞춰지자, 문에 숨겨진 비밀번호가 나타납니다: 'EXIT'",
                "puzzle_state_key": "puzzle_solved_photo"
            },
            "잠긴 문": {
                "desc": "밖으로 통하는 문인 것 같습니다. 굳게 잠겨 있습니다.",
                "action": "문을 연다",
                "result": "문이 잠겨 있습니다. (암호 필요)",
                "hint": "문이 잠겨 있습니다. 암호가 필요합니다.",
                "requires_puzzle": True,
                "puzzle_hint": "모든 힌트를 조합하여 암호를 풀어보세요. ('1230', 'EXIT'를 모두 알아야 함)",
                "puzzle_solution_final": "EXIT", # 최종 탈출 암호
                "puzzle_state_key": "final_door" # 탈출 성공 여부를 위한 상태
            }
        }
    }
}

# --- 게임 화면 표시 함수 ---
def display_game_screen():
    current_room_name = st.session_state.current_room
    room_info = rooms[current_room_name]

    st.header(f"현재 위치: {current_room_name}")
    st.write(room_info["description"])
    st.markdown("---")

    # --- 가구 상호작용 ---
    st.subheader("🕵️‍♀️ 주변을 살펴본다...")
    for furniture_name, furniture_data in room_info["furniture"].items():
        if st.button(f"**{furniture_name}**을(를) 살펴본다", key=f"{current_room_name}_{furniture_name}"):
            handle_furniture_interaction(furniture_name, furniture_data)
        st.write(f"- {furniture_data['desc']}")
        st.markdown("---")

    # --- 방 이동 화살표 버튼 ---
    col1, col2, col3 = st.columns([1, 8, 1])

    with col1:
        if room_info["left"]:
            if st.button("⬅️ 이전 방", key="left_arrow"):
                st.session_state.current_room = room_info["left"]
                st.rerun() # 변경된 부분

    with col3:
        if room_info["right"]:
            if st.button("다음 방 ➡️", key="right_arrow"):
                st.session_state.current_room = room_info["right"]
                st.rerun() # 변경된 부분

    st.markdown("---")
    st.subheader("🎒 인벤토리")
    if st.session_state.inventory:
        for item in st.session_state.inventory:
            st.write(f"- {item}")
    else:
        st.write("비어있음")

# --- 가구 상호작용 처리 함수 ---
def handle_furniture_interaction(furniture_name, furniture_data):
    current_room_name = st.session_state.current_room

    # 아이템이 필요한 상호작용 처리 (옷장)
    if "requires" in furniture_data and furniture_data["requires"] not in st.session_state.inventory:
        st.warning(furniture_data["hint"])
        return

    # 아이템을 놓아야 하는 상호작용 처리 (테이블)
    if "requires_item_to_interact" in furniture_data:
        required_item = furniture_data["requires_item_to_interact"]
        if required_item in st.session_state.inventory and not st.session_state[furniture_data["puzzle_state_key"]]:
            st.info(furniture_data["interaction_prompt"])
            st.success(furniture_data["puzzle_solved_msg"])
            st.session_state[furniture_data["puzzle_state_key"]] = True
            st.session_state.inventory.remove(required_item) # 사용한 아이템 제거
        elif st.session_state[furniture_data["puzzle_state_key"]]:
            st.info("이미 이 퍼즐은 해결했습니다.")
        else:
            st.warning(f"{required_item}이(가) 필요합니다.")
        return

    # 퍼즐이 필요한 상호작용 처리 (책상, 잠긴 문)
    if "requires_puzzle" in furniture_data:
        st.info(furniture_data["puzzle_hint"])
        user_input = st.text_input("정답을 입력하세요:", key=f"puzzle_input_{current_room_name}_{furniture_name}")
        if user_input:
            if furniture_name == "책상":
                if user_input == furniture_data["puzzle_solution"] and not st.session_state[furniture_data["puzzle_state_key"]]:
                    st.success(furniture_data["puzzle_solved_msg"])
                    st.session_state[furniture_data["puzzle_state_key"]] = True
                    if "found_key" in furniture_data and furniture_data["found_key"] not in st.session_state.inventory:
                        st.session_state.inventory.append(furniture_data["found_key"])
                        st.info(f"인벤토리에 '{furniture_data['found_key']}'이(가) 추가되었습니다.")
                elif st.session_state[furniture_data["puzzle_state_key"]]:
                    st.info("이미 이 퍼즐은 해결했습니다.")
                else:
                    st.error("틀렸습니다. 다시 시도해 보세요.")
            elif furniture_name == "잠긴 문": # 최종 탈출 퍼즐
                if st.session_state.puzzle_solved_desk and st.session_state.puzzle_solved_photo: # 모든 힌트가 준비되었는지 확인
                    if user_input.upper() == furniture_data["puzzle_solution_final"]:
                        st.balloons()
                        st.success("🎉 축하합니다! 문이 열렸습니다. 당신은 탈출에 성공했습니다!")
                        st.session_state.current_room = "탈출 성공" # 게임 종료 상태
                    else:
                        st.error("틀렸습니다. 모든 힌트를 조합하여 다시 시도해 보세요.")
                else:
                    st.warning("아직 모든 퍼즐을 풀지 못했습니다. 다른 힌트를 찾아보세요!")
        return

    # 일반적인 상호작용 (아이템 획득 또는 단순 정보 제공)
    st.info(furniture_data["result"])
    if "found_key" in furniture_data and furniture_data["found_key"] not in st.session_state.inventory:
        st.session_state.inventory.append(furniture_data["found_key"])
        st.info(furniture_data["hint"])
        # 옷장 열쇠로 옷장을 열었을 때 특별한 힌트 제공
        if furniture_name == "옷장" and "작은 열쇠" in st.session_state.inventory:
            st.session_state.inventory.remove("작은 열쇠") # 열쇠 사용
            st.session_state.inventory.append("낡은 쪽지 조각 3")
            st.info("낡은 쪽지 조각 3을 얻었습니다: '..' (인벤토리에 추가됨)")
            st.warning("옷장 열쇠를 사용했습니다.")


# --- 메인 게임 루프 ---
st.title("🏚️ 미스터리 방탈출 게임")

if st.session_state.current_room == "탈출 성공":
    st.balloons()
    st.success("🌟 당신은 방을 탈출하는 데 성공했습니다! 🌟")
    st.write("게임이 종료되었습니다. 다시 플레이하려면 앱을 새로고침하세요.")
else:
    display_game_screen()
