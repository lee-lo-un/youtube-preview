import streamlit as st
from googleapiclient.discovery import build
from dotenv import load_dotenv
import os

# .env 파일 로드
load_dotenv()

# API 키 가져오기
API_KEY = os.getenv("YOUTUBE_API_KEY")
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# 유튜브 API 클라이언트 생성
def get_youtube_client():
    return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)

# 인기 있는 동영상 가져오기
def get_trending_videos():
    youtube = get_youtube_client()
    request = youtube.videos().list(
        part="snippet",
        chart="mostPopular",
        regionCode="US",
        maxResults=9  # 조회할 영상 개수
    )
    response = request.execute()
    return response["items"]

def main():
    st.title("유튜브 인기 동영상 조회 앱")
    st.write("유튜브에서 현재 인기 있는 영상들의 썸네일과 제목을 3개씩 가로로 보여줍니다.")

    # 인기 영상 조회
    try:
        videos = get_trending_videos()
        
        # 동영상 데이터를 3개씩 나누어 열에 배치
        for i in range(0, len(videos), 3):
            cols = st.columns(3)  # 3개의 열 생성
            for j, video in enumerate(videos[i:i+3]):
                with cols[j]:
                    video_title = video["snippet"]["title"]
                    thumbnail_url = video["snippet"]["thumbnails"]["high"]["url"]

                    st.image(thumbnail_url, use_column_width=True)
                    st.write(f"**{video_title}**")

    except Exception as e:
        st.error("동영상 정보를 불러오는 데 실패했습니다.")
        st.write(e)

if __name__ == "__main__":
    main()
