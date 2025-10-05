import streamlit as st
import requests
import re
from bs4 import BeautifulSoup

# 페이지 설정
st.set_page_config(
    page_title="금칙어 검사기",
    page_icon="🔍",
    layout="centered"
)

# 금칙어 리스트
word_listf = [
    '쌍검', '총칼', '참사', '박도', '진검', '독인', '질싸', '염탐', '도청', '사찰', '책동',
    '암표', '섹파', '무단', '영사', '누드', '연초', '궐련', '담배', '구초', '관연', '영초', '마약', '대마', '야바',
    '참사', '경마', '나가요', '폭약', '야사', '영면', '작고', '익사', '피폐', '임명', '졸사', '병폐', '적보', '마땅',
    '참시', '누두', '애널', '에널', '야동', '마다', '병신', '초짜', '음독', '그자', '씹질', '애무', '오랄',
    '체위', '슴가', '폭약', '폭탄', '폰섹', '폰쎅', '호빠', '후장', '섹시', '씨빨', '야덩', '야시', '오럴', '유흥', '잠지',
    '존나', '노모', '도촬', '띠발', '몰래', '몰카', '미친', '벌기', '벌려', '변녀', '빨아', '빨어', '성방',
    '변태', '색스', '동거', '불륜', '애로', '원조', '최근', '장물', '카섹', '폰팅', '섹골', '섹녀', '쌕스', '펨돔', '펨섭',
    '빠굴', '뻐킹', '난교', '색쓰', '섹쓰', '폰쎅', '문섹', '용색', '웬만', '대략', '날이', '실제', '조금',
    '지속', '여럿', '찐', '대부분', '질사', '야설', '빙신', '발기', '귀두', '페팅', '폰색', '섹마', '야겜', '야껨', '야똥',
    '야섹', '음욕', '자쥐', '재랄', '전라', '좀물', '짬지', '찌찌', '체모', '꼬추', '떡걸', '떡촌', '망까', '보짓', '봉알',
    '뵤지', '불알', '색골', '세엑', '육봉', '싸죠', '쌩쑈', '컴섹', '음란', '색폰', '셀걸', '멜섭', '섹할',
    '잡년', '재랄', '저년', '뻘노', '뽀지', '뽈노', '섹쑤', '컴색', '화간', '음경', '음핵', '비엘', '보지', '자지', '성기',
    '야캠', '나체', '음모', '옥문', '고환', '정액', '색마', '망가', '노콘', '콘돔', '음탕', '거유', '창녀', "야한", "야해",
    "할때", "다른", '에로', '시신', '가장', '년', '다양', '부족', '핸플', '세워', '인분', '실천', '블로그마케팅',
    '않', '이반', '텐가', '대딸', '인마', '참수', '정사', '음부', '도추', '성교', '강간', '수간', '간사', "보내죠",
    '뒤져', '자살', '자위', '지발', '가오', '아다', '빠가', '씹', '한거', '살생', '살육', '테러', '난자', '너무',
    '당연', '가질', '여근', '비추', '식인', '옥루', '학살', '음서', '수음', '사의', '상간', '유살', '섹수', '자진',
    '섹수', '요절', '절사', '요함', '국부', '게이', '남색', '파정', '게네', '밤일', '자결', '딜도', '갈보', '살육',
    '척살', '압살', '시역', '역살', '활살', '유살', '불구', '색녀', '대범', '도범', '전범', '혼음', '윤간', '능욕', '야바',
    '아편', '애액', '퀴어', '살인', '창기', '춘부', '포주', '침노', '취한', '야양', '겨웅', '회신',
    '고2', '고1', '고3', '계모', '처자', '과비', '떨', '각하', '계부', '팸', '가결', '가득한', '가어',
    '감정이', '강을', '같네', '것도', '것은', '게으른', '격하', '결여', '곁들인', '관련', '그만큼', '그분', '그에', '꼬물',
    '끊고', '나라는말', '낫다', '내릴', '내블로그', '내에서', '내용은', '네이버에', '높다', '느끼는', '느릿', '다네이버',
    '닫는', '담을', '더위', '돼기', '돼야', '되는것', '되지', '듣고', '들인', '로추', '류요', '많다', '머물', '멍한', '며미',
    '목하', '바로키', '방금', '배워', '병을', '보내세요', '분문', '사는', '사람이', '삶에', '상위노출', '슬픔에', '습득', '시서',
    '시청', '신중', '안에다', '어다', '어떤경우', '어려워', '어르', '에대한', '에들', '에유', '여뉴', '여이', '예민하게', '와함께',
    '완료', '완벽', '욱하는', '울하', '워우', '원래', '위해서', '유난', '의외로', '이것', '이내에', '이상을', '이어짐', '읽었다',
    '있는지', '재방', '재의', '저하', '정신적', '제잘', '줄고', '지닌', '챙겨', '충분히', '친구가', '침에', '커뮤', '판박', '포함',
    '숙한', '제부', '엄청', '무료', '최고', '최초', '무척', '강추', '추천', '되게', '발기', '콘돔', '야싸', '만냥',
    '콘돔', '부분', '초점', '체팅방', '썰툰', '핑두', '옥링', '표적', '내돈내산', '최저가', '좋아요', '비싸다', '싫어요',
    '효과', '예쁜', '멋진', '기준', '성인용', '성기구', '성생활', '성도구', '성용품', '권장',
    '창피해', '야오이', '학생', '좋습니다', '주세요', '하세요', '갈수', '걸림', '결핍', '됩니다', '겁니다', '습니다',
    '그럼', '기에', '나때', '내는', '넘어', '놓치', '따라', '가능', '들어', '들었', '들을', '같습니다', '드릴게요',
    '천거', '드립니다', '발라', '넣어', '후퇴', '활발', '혹은', '구건', '과전', '특정', '추진', '쳐줘', '게모', '실물',
    '처하', '주중', '나이', '해새', '함이', '한변', '개씩', '각지', '가편', '필요', '펼쳐', '주게',
    '전적', '저희', '있어', '인근', '이처', '이죠', '무슨', '맞이', '려고', '떠나', '원인', '외롭', '될때',
    '동을', '데에', '다녀', '오랜', '얻어', '어나', '야추', '않게', '심한', '성으', '빠른', '빠르', '분한', '부터',
    '보입', '변화', '때는', '과에', '고쳐', '늦은', '는지', '느슨', '뇌가', '높이', '내용', '장례'
]


def clean_text(input_string):
    """특수문자 제거"""
    text_rmv = re.sub(r'[-=+,#/\?:^.@*\"※~ㆍ!』' |\(\)\[\]$`\'…%&><》\"\"\'·.~_;]', ' ', input_string)
    return text_rmv


def process_blog_text(text):
    """블로그 텍스트 분석"""
    # 텍스트 전처리
    linea1 = text.replace("\n", "").replace("출처 입력", "").replace("사진 설명을 입력하세요", "")
    linea2 = str(linea1)
    line1 = clean_text(linea2)
    line2 = line1.replace(" ", "")

    # 금칙어 검사
    penlistf = []
    for word in sorted(word_listf):
        count = line2.count(word)
        if count > 0:
            penlistf.append({"word": word, "count": count})

    # 총 글자수
    total_chars = len(line2)

    return {
        "cleaned_text": line2,
        "total_chars": total_chars,
        "penlistf": penlistf
    }


def process_blog_url(url):
    """블로그 URL에서 텍스트 추출"""
    # 모바일 URL로 변경
    if 'm.blog' not in url:
        url = url.replace('blog', 'm.blog')

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except Exception as e:
        return {"error": f"URL 요청 실패: {e}"}

    soup = BeautifulSoup(response.text, "html.parser")
    container = soup.select_one("div.se-main-container")

    if container is None:
        return {"error": "블로그 본문을 찾을 수 없습니다. URL을 확인해주세요."}

    text = container.get_text().replace("\n", "")
    return process_blog_text(text)


# ==================== 메인 앱 ====================
st.title("🔍 금칙어 검사기")

# 메인 키워드 입력
main_keyword = st.text_input("메인 키워드 (선택)", placeholder="예: 다이어트")

# 입력 방식 선택
input_mode = st.radio("입력 방식", ("블로그 URL", "직접 입력"), horizontal=True)

st.markdown("---")

# URL 입력 모드
if input_mode == "블로그 URL":
    blog_url = st.text_input("블로그 URL", placeholder="https://blog.naver.com/...")

    if st.button("분석 시작", type="primary"):
        if blog_url:
            with st.spinner("분석 중..."):
                result = process_blog_url(blog_url)

            if "error" in result:
                st.error(result["error"])
            else:
                # 기본 정보
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("총 글자수", f"{result['total_chars']:,}자")
                with col2:
                    if main_keyword:
                        keyword_clean = main_keyword.replace(" ", "")
                        keyword_count = result["cleaned_text"].count(keyword_clean)
                        st.metric("메인키워드", f"{keyword_count}회")
                with col3:
                    st.metric("금칙어 종류", f"{len(result['penlistf'])}개")

                st.markdown("---")

                # 금칙어 검사 결과
                st.subheader("금칙어 검사 결과")
                if result["penlistf"]:
                    st.warning(f"{len(result['penlistf'])}개의 금칙어 발견!")
                    for item in result["penlistf"]:
                        st.write(f"• **{item['word']}**: {item['count']}회")
                else:
                    st.success("✅ 금칙어 없음")

                # 원본 텍스트
                with st.expander("처리된 텍스트 보기"):
                    st.text_area("", result["cleaned_text"], height=200)
        else:
            st.warning("URL을 입력해주세요")

# 텍스트 직접 입력 모드
else:
    blog_text = st.text_area("텍스트 입력", height=300, placeholder="블로그 글을 붙여넣으세요...")

    if st.button("분석 시작", type="primary"):
        if blog_text:
            with st.spinner("분석 중..."):
                result = process_blog_text(blog_text)

            # 기본 정보
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("총 글자수", f"{result['total_chars']:,}자")
            with col2:
                if main_keyword:
                    keyword_clean = main_keyword.replace(" ", "")
                    keyword_count = result["cleaned_text"].count(keyword_clean)
                    st.metric("메인키워드", f"{keyword_count}회")
            with col3:
                st.metric("금칙어 종류", f"{len(result['penlistf'])}개")

            st.markdown("---")

            # 금칙어 검사 결과
            st.subheader("금칙어 검사 결과")
            if result["penlistf"]:
                st.warning(f"{len(result['penlistf'])}개의 금칙어 발견!")
                for item in result["penlistf"]:
                    st.write(f"• **{item['word']}**: {item['count']}회")
            else:
                st.success("✅ 금칙어 없음")

            # 원본 텍스트
            with st.expander("처리된 텍스트 보기"):
                st.text_area("", result["cleaned_text"], height=200)
        else:
            st.warning("텍스트를 입력해주세요")