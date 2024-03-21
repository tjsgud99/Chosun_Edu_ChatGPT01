from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain.schema import HumanMessage, AIMessage, SystemMessage
import os
from dotenv import load_dotenv, find_dotenv

# 1.PromptTemplate : 질문:답변 끝!(1회성)
# 2.ChatPromptTemplate: Chat(채팅처럼)

_ = load_dotenv(find_dotenv())

chat = ChatOpenAI(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    # temperature: 0.1~1.0  : 0에 가까울수록 사실기반, 1에가까울수록 창의력
    temperature=0.1
)

# parser: GPT가 생성한 답변을 Parser를 통해서 원하는 형태로 Parsing

from langchain.schema import BaseOutputParser
class CommaOutputParser(BaseOutputParser):

      def parse(self, text):
            items = text.strip().split(",")
            return list(map(str.strip,items))
      
p = CommaOutputParser()
# result = p.parse("Hello, how, are, you")

template = ChatPromptTemplate.from_messages([
      ("system, 너는 리스트 생성 기계다. 모든 답변을 콤마로 구분해서 대답해라."),
      ("human", "{question}")
])

prompt = template.format_messages(
      max_items=10,
      question="색상은 무엇인가?"
)

result = chat.predict_messages(prompt)

print(p.parse(result.content))

