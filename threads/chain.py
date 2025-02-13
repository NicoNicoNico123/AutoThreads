from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from threads.utils import load_prompt_text
import os

load_dotenv()

class ChainPrompt:
    def __init__(self):
        self.base_url = os.getenv("OPENAI_BASE_URL")
        self.api_key = os.getenv("OPENAI_API_KEY")

    def interact_chain(self,topic: str):


        prompt = ChatPromptTemplate.from_template(load_prompt_text("system_prompt", "system_prompt"))
        model = ChatOpenAI(model="gpt-4o-mini", 
                        base_url=self.base_url,
                        api_key=self.api_key,
                        # max_tokens=00,
                        temperature=0.3
                        )
        chain = prompt | model | StrOutputParser()
        return chain.invoke({"topic": topic})

    def flux_prompt(self):
        prompt = PromptTemplate.from_template(load_prompt_text("image_prompt", "system_prompt"))
        model = ChatOpenAI(model="deepseek-chat", 
                        base_url=self.base_url,
                        api_key=self.api_key,
                        temperature=1.5
                        )
        chain = model | StrOutputParser()
        return chain.invoke(prompt.format())

if __name__ == "__main__":
    chain_prompt = ChainPrompt()
    textprompt = chain_prompt.flux_prompt()
    print(textprompt)

