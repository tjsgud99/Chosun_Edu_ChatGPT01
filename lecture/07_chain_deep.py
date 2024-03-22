from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from langchain.callbacks import StreamingStdOutCallbackHandler
import os
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

# 1.Chat모델 생성
chat = ChatOpenAI(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    # temperature: 0.1~1.0  : 0에 가까울수록 사실기반, 1에가까울수록 창의력
    temperature=0.1,
    streaming=True,
    callbacks=[StreamingStdOutCallbackHandler()]
)

chef_prompt = ChatPromptTemplate.from_messages([
        ("system", "당신은 전세계에서 유명한 요리사 입니다. 찾기쉬운 재료를 사용해서 모든 종류의 요리에 대해 쉽게 따라할 수 있는 레시피를 만드세요."),
        ("human", "나는 {cook} 요리를 만들고 싶어요!")

])

# chain 1 생성(=> 음식 종류)
chef_chain = chef_prompt | chat

veg_chef_prompt = ChatPromptTemplate.from_messages([
        ("system" , "당신은 전통적인 요리법을 채식으로 만드는 채식주의 요리사입니다. 대체 재료를 찾고 그 준비과정을 설명하세요. 근본적으로 레시피를 수정하지는 말고, 대체재료가 없는 경우 없다고 하세요."),
        ("human" , "{recipe}")

])

# chain 2 생성(=>recipe)
veg_chain = veg_chef_prompt | chat

# chain 3 생성(연결)
final_chain = {"recipe" : chef_chain} | veg_chain

# chain 실행
final_chain.invoke({
        "cook" : "indian"
})

