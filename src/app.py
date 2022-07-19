import streamlit as st
from bs4 import BeautifulSoup
import requests
from googletrans import Translator

tr = Translator(service_urls=['translate.google.co.jp'])


def get_soup(url):
    response = requests.get(url)
    response.encoding = response.apparent_encoding
    html = response.text
    return BeautifulSoup(html, 'html.parser')


st.set_page_config(page_title="韓国語歌詞翻訳")
st.title("韓国語歌詞翻訳")

q = st.text_input("『曲名 歌手名』")  # 사랑하기 때문에
if st.button("検索"):
    with st.spinner("検索中"):
        url = f"https://music.bugs.co.kr/search/integrated?q={q}"
        soup = get_soup(url)
        try:
            song_url = soup.select("table.list.trackList")[0].tbody.select("tr")[
                0].select(".trackInfo")[0].get("href")
        except:
            st.error("見つかりませんでした")
            st.stop()

        soup = get_soup(song_url)
        basic_info = soup.select(".basicInfo")[0]
        img_url = basic_info.img.get("src")
        artist = basic_info.select("td")[0].text.strip()
        song = soup.h1.text.strip()
        lyrics_rows = soup.xmp.text.split("\r\n")

    st.image(img_url)
    st.subheader(f"{song} / {artist}")
    st.text("歌詞")
    with st.spinner("翻訳中"):
        for word in lyrics_rows:
            if word in [' ', "", '  ']:
                st.write("")
                continue
            st.markdown(f"**{word.strip()}**")
            st.write(tr.translate(word, dest="ja").text)
