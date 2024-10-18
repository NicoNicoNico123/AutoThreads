from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from .utils import load_prompt_text
import os

load_dotenv()

def interact_chain(topic: str):
    base_url = os.getenv("OPENAI_BASE_URL")
    api_key = os.getenv("OPENAI_API_KEY")

    prompt = ChatPromptTemplate.from_template(load_prompt_text("system_prompt", "system_prompt"))
    model = ChatOpenAI(model="gpt-4o-mini", 
                    base_url=base_url,
                    api_key=api_key,
                    # max_tokens=00,
                    temperature=1
                    )
    chain = prompt | model | StrOutputParser()
    return chain.invoke({"topic": topic})

if __name__ == "__main__":
    text= """
    ['熱門報導',
    '巨星殞落丨One Direction前成員Liam Payne 酒店墮樓亡終年31歲',
    '前One Direction成員Liam Payne阿根廷墮樓亡 終年31歲',
    'One Direction成員Liam Payne逝世！樂壇星星殞落，Charlie Puth發文悼念：「我真的很傷心」',
    '前One Direction 成員Liam Payne 逝世 終年 31 歲',
    '英國天團 One Direction 前成員 Liam Payne 墜樓過世，享年 31 歲',
    'One Direction前成員 Liam Payne 陽台墜樓身亡 享年31歲',
    '前 One Direction 成員 Liam Payne 過世享年31歲！',
    '英國前One Direction成員Liam Payne阿根廷墮樓身亡 終年 31歲',
    'Liam Payne離世終年31歲，震驚1D樂迷：還是等不到他們合體的一天']
    """
    text2 = """
        '劉德華巡迴演唱會2024香港站丨《今天…is the Day》劉德華巡迴演唱會香港站門票10.17公開發售即睇Urbtix搶飛攻略、票價、座位表',
        '劉德華演唱會2024香港站｜20場紅館演唱會門票10.17公開發售（附Urbtix連結/票價）',
        '劉德華香港演唱會2024公售｜Urbtix 城網搶票攻略｜座位表+連結',
        '演唱會搶飛技巧Urbtix/快達票/Cityline！8大事前準備改DNS設定步驟助成功',
        '第四屆「粵港澳大灣區文化藝術節」反應熱烈 兩個亮點節目安排加推門票或加開演出（附圖）',
        '劉德華香港演唱會｜20場門票個多小時售罄 歌迷呻：排了個寂寞',
        '國家隊訪港門票今發售 這些特別安排你要知（附連結）',
        '劉德華演唱會2024香港站｜75分鐘完售20場紅館演唱會門票 14萬人齊搶飛歌迷求加場',
        '粵港澳大灣區文化藝術節反應熱烈 《聲音河流》《詠春》加票加場演出',
        '國家隊訪港｜5300張門票周四公售 城市電腦售票網5招購票攻略'  
    """
    text3 = """
    ['熱門報導',
    '易建聯傳嫖妓變性人丨重溫精彩情史！曾傳戀劉亦菲豪花六位數冧女 娶女模育有兩子',
    '易建聯被曝「嫖娼」 多代言品牌疑割席 東莞市政協：等官方通報',
    '易建聯傳嫖妓變性人丨重溫精彩情史！曾傳戀劉亦菲豪花六位數冧女 娶女模育有兩子',
    '籃球巨星易建聯花1500美元嫖變性人？ 「證據」曝光、本人未回應',
    '易建聯疑似嫖妓 被影裸照及身份證放上網',
    '中國籃球巨星｜前NBA球星易建聯疑嫖娼 事件疑點不斷網民化身金田一尋證據',
    '易建聯捲桃色風波｜疑似嫖妓被影裸照及放身份證上網 多家代言品牌刪名撇清關係',
    '易建聯疑嫖妓｜30年偶像係香港頂流 被邀做演唱會嘉賓看來夢碎',
    '易建聯傳嫖妓變性人身份曝光？瘋傳「女角」撞樣宋慧喬竟是易服男兼曾被刑拘']
    """
    print(interact_chain(text3))

