import time
import random
import streamlit as st
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

# ==============================================================================
# 🔒 [보안 설정] 사내 보안 비밀번호 세팅
# ==============================================================================
COMPANY_PASSWORD = "2019"  # <-- 원하는 비밀번호로 자유롭게 변경하세요!

# --- 로그인 체크 로직 (코드 최상단 배치) ---
if "password_correct" not in st.session_state:
    st.session_state.password_correct = False

if not st.session_state.password_correct:
    st.set_page_config(page_title="사내 인증", layout="centered")
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.subheader("🔒 사내 보안 인증")
    st.caption("이 시스템은 사내 관계자 전용 도구입니다. 비밀번호를 입력해 주세요.")
    
    user_password = st.text_input("보안 비밀번호를 입력하세요", type="password")
    if st.button("로그인", use_container_width=True):
        if user_password == COMPANY_PASSWORD:
            st.session_state.password_correct = True
            st.rerun()
        else:
            st.error("❌ 비밀번호가 올바르지 않습니다.")
    st.stop()  # 🚨 비밀번호가 맞기 전까지는 아래 모든 코드를 실행하지 않고 멈춤!

# ==============================================================================
# 🔗 [업데이트 완료] 질문자님의 실제 크몽 상품 고유 ID 매핑 테이블
# ==============================================================================
GIG_ID_MAP = {
    "블로그리뷰(기자단)": "67791",
    "블로그원고 작성": "77157",
    "블로그책 전자책": "85687",
    "블로그 SNS 황금키워드 추출": "105223",
    "기업블로그 브랜드블로그 최적화 월관리": "120068",
    "브랜드 공식 인스타그램 관리": "280072",
    "중/소상공인 회사소개서 제작": "360321",
    "시장조사": "367992",
    "설문지를 통한 여론조사": "403239",
    "인플루언서 만들어 드립니다": "443445",
    "당근마켓 광고": "566030",
    "고객 응대 메뉴얼, CS 전자책": "596292",
    "인스타그램 리그램": "668779",
    "스레드 관리": "697619",
    "KAKA 공식광고 (카카오모먼트 광고)": "704353",
    "인스타그램 감성 피드 (업종별 1:1 디자인)": "756893"
}

# 셀레늄 순위 검색 함수
def check_kmong_rank(keyword, my_gig_id, max_pages=3):
    options = webdriver.ChromeOptions()
    
    # --- 🌐 리눅스/클라우드 서버 배포용 필수 옵션 ---
    options.add_argument("--headless")  # 화면 없는 모드로 실행 (서버 필수)
    options.add_argument("--no-sandbox")  # 권한 보안 제한 해제 (서버 필수)
    options.add_argument("--disable-dev-shm-usage")  # 공유 메모리 오버플로우 방지 (서버 필수)
    options.add_argument("--disable-gpu")  # GPU 가속 해제
    
    # 봇 차단 우회 기본 옵션
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    # 서버 환경에서는 webdriver_manager가 꼬일 수 있으므로 가장 심플하게 선언합니다.
    driver = webdriver.Chrome(options=options)
    current_rank = 0 
    
    try:
        driver.get("https://kmong.com")
        time.sleep(random.uniform(2.0, 3.5))
        
        input_selector = "body > div.min-w-\\[1200px\\] > main > section:nth-child(1) > div > div.w-\\[700px\\] > div.mr-10.mt-8.w-\\[628px\\] > form > div.flex.h-fit.w-full.flex-1.flex-col.gap-1 > div > input"
        search_box = driver.find_element(By.CSS_SELECTOR, input_selector)
        search_box.clear()
        
        for char in keyword:
            search_box.send_keys(char)
            time.sleep(random.uniform(0.05, 0.12))
            
        time.sleep(random.uniform(0.4, 0.9))
        
        button_selector = "body > div.min-w-\\[1200px\\] > main > section:nth-child(1) > div > div.w-\\[700px\\] > div.mr-10.mt-8.w-\\[628px\\] > form > div.flex.h-fit.w-full.flex-1.flex-col.gap-1 > div > div > button"
        search_button = driver.find_element(By.CSS_SELECTOR, button_selector)
        driver.execute_script("arguments[0].click();", search_button)
        
        time.sleep(random.uniform(3.5, 4.8))
        
        if "크몽" not in driver.title and "kmong" not in driver.current_url:
            return "조회 실패(블락)"
            
        for page in range(1, max_pages + 1):
            scroll_pos = random.uniform(0.45, 0.55)
            driver.execute_script(f"window.scrollTo(0, document.body.scrollHeight * {scroll_pos});")
            time.sleep(random.uniform(1.5, 2.2))
            
            container_selector = "main div.mx-auto.my-0.w-\\[1200px\\] section.mb-0.mt-5 div.flex.w-full.flex-wrap"
            try:
                container = driver.find_element(By.CSS_SELECTOR, container_selector)
                children = container.find_elements(By.XPATH, "./*")
            except:
                return "조회 실패"
            
            for child in children:
                tag_name = child.tag_name
                class_attr = child.get_attribute("class") or ""
                
                if tag_name == "div" or (tag_name == "section" and ("bg-black" in class_attr or "bg-gray-200" in class_attr)):
                    continue
                
                if tag_name == "article":
                    current_rank += 1
                    try:
                        a_tag = child.find_element(By.TAG_NAME, "a")
                        href = a_tag.get_attribute("href") or ""
                        
                        if my_gig_id in href:
                            return f"{current_rank}위"
                    except:
                        current_rank -= 1
                        continue
            
            try:
                next_btn_selector = "div.flex.items-center.justify-center.pb-\\[100px\\] ul li button svg"
                next_buttons = driver.find_elements(By.CSS_SELECTOR, next_btn_selector)
                if next_buttons:
                    next_button = next_buttons[-1].find_element(By.XPATH, "..")
                    driver.execute_script("arguments[0].click();", next_button)
                    time.sleep(random.uniform(3.0, 4.0))
                else:
                    break
            except:
                break
                
        return "1page X"
        
    except Exception:
        return "조회 실패"
    finally:
        driver.quit()

# --- Streamlit 세션 상태 초기화 ---
if "rank_results" not in st.session_state:
    st.session_state.rank_results = {}

# --- Streamlit UI ---
st.set_page_config(page_title="크몽 공식광고 순위 체크", layout="wide")
st.title("크몽 공식광고 순위 체크 자동화 시스템")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("카테고리별 키워드 입력")
    max_p = st.slider("최대 검색 페이지 한도", min_value=1, max_value=5, value=2)
    report_title = st.text_input("보고서 상단 문구", value="크몽 공식광고 순위 체크입니다\n @대표님 @박성환 팀장님")
    report_footer = st.text_area("보고서 하단 문구", value="-예산은 차주 중 충전 예정")
    
    st.divider()
    
    # 16개 카테고리 기본 키워드 맵
    default_vals = {
        "블로그리뷰(기자단)": "블로그 작성, 블로그 포스팅, 블로그 글 발행",
        "블로그원고 작성": "블로그 원고, 글쓰기",
        "블로그책 전자책": "전자책 제작, 전자책",
        "블로그 SNS 황금키워드 추출": "구글, 블로드 조회수, 블로그 활성화",
        "기업블로그 브랜드블로그 최적화 월관리": "브랜드 블로그, 기업 블로그, 블로그 관리",
        "브랜드 공식 인스타그램 관리": "인스타그램 관리, 인스타관리, 인스타",
        "중/소상공인 회사소개서 제작": "브랜드소개서, 회사소개서, 제품소개서",
        "시장조사": "리서치, 시장조사, 상권분석",
        "설문지를 통한 여론조사": "리서치, 자료조사, 설문대행",
        "인플루언서 만들어 드립니다": "인스타 인플루언서, 인스타 홍보, 인스타인플루언서",
        "당근마켓 광고": "당근마켓 광고, 당근, 당근 광고",
        "고객 응대 메뉴얼, CS 전자책": "cs, 전자책",
        "인스타그램 리그램": "인스타게시물, 인스타그램 계정, 인스타그램 공유",
        "스레드 관리": "쓰레드, 쓰레드 대행",
        "KAKA 공식광고 (카카오모먼트 광고)": "카카오광고, 카카오모먼트",
        "인스타그램 감성 피드 (업종별 1:1 디자인)": "인스타 피드, 인스타 디자인, 인스타 피드 디자인"
    }
    
    USER_KEYWORDS = {}
    for cat, default_kw in default_vals.items():
        user_input = st.text_input(f"🏷️ {cat}", value=default_kw, key=f"in_{cat}")
        USER_KEYWORDS[cat] = [k.strip() for k in user_input.split(",") if k.strip()]

    st.divider()
    start_btn = st.button("전체 크몽 광고 순위 추적 시작", use_container_width=True, type="primary")

def build_report_text():
    text = f"{report_title}\n\n"
    for category, keywords in USER_KEYWORDS.items():
        text += f"{category}\n"
        for kw in keywords:
            res = st.session_state.rank_results.get((category, kw), "대기 중")
            text += f"- {kw} {res}\n"
        text += "\n"
    text += report_footer
    return text

with col2:
    st.subheader("완성된 카톡 보고서 텍스트")
    report_placeholder = st.empty()
    
    def get_failed_tasks():
        failed = []
        for category, keywords in USER_KEYWORDS.items():
            for kw in keywords:
                current_res = st.session_state.rank_results.get((category, kw), "")
                if "실패" in current_res or not current_res:
                    failed.append((category, kw))
        return failed

    if start_btn:
        st.session_state.rank_results = {}
        total_kws = sum(len(kws) for kws in USER_KEYWORDS.values())
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        current_idx = 0
        for category, keywords in USER_KEYWORDS.items():
            gig_id = GIG_ID_MAP.get(category) # 💥 진짜 매핑된 고유 ID 사용
            for kw in keywords:
                current_idx += 1
                status_text.text(f"⏳ [{category}] -> '{kw}' 조회 중... ({current_idx}/{total_kws})")
                
                rank_result = check_kmong_rank(kw, gig_id, max_pages=max_p)
                st.session_state.rank_results[(category, kw)] = rank_result
                
                progress_bar.progress(current_idx / total_kws)
                report_placeholder.text_area("조회 진행 중...", value=build_report_text(), height=600)
                time.sleep(random.uniform(1.5, 3.0))
                
        status_text.success("✨ 조회가 완료되었습니다!")

    if st.session_state.rank_results:
        current_report = build_report_text()
        report_placeholder.text_area("📢 완료! 복사해서 사용하세요.", value=current_report, height=600)
        
        failed_tasks = get_failed_tasks()
        if failed_tasks:
            st.warning(f"⚠️ 현재 {len(failed_tasks)}개의 키워드가 조회 실패 상태입니다. 잠시 후 재시도 버튼을 누르세요.")
            failed_df = pd.DataFrame(failed_tasks, columns=["카테고리", "실패 키워드"])
            st.dataframe(failed_df, use_container_width=True)
            
            retry_btn = st.button("🔄 ❌ 실패한 키워드만 다시 검색하기", use_container_width=True)
            if retry_btn:
                retry_status = st.empty()
                for r_idx, (cat, kw) in enumerate(failed_tasks):
                    retry_status.text(f"♻️ 재조회 중 ({r_idx+1}/{len(failed_tasks)}): [{cat}] {kw}")
                    gig_id = GIG_ID_MAP.get(cat)
                    
                    rank_result = check_kmong_rank(kw, gig_id, max_pages=max_p)
                    st.session_state.rank_results[(cat, kw)] = rank_result
                    
                    report_placeholder.text_area("재조회 반영 중...", value=build_report_text(), height=600)
                    time.sleep(random.uniform(2.5, 4.0))
                    
                retry_status.success("♻️ 실패 키워드 재조회가 끝났습니다!")
                st.rerun()
        else:
            st.success("🎉 모든 키워드가 실패 없이 완벽하게 조회되었습니다!")
            st.balloons()
    else:
        report_placeholder.info("왼쪽에서 설정을 마친 뒤 '전체 광고 순위 추적 시작' 버튼을 눌러주세요.")

        # --- kmong.py 상단 UI 구역에 추가하면 좋은 로그인 기능 ---
