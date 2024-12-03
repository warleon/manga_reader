from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import END, START, StateGraph, MessagesState

import image_read 


class ImageReader:
    llm = None
    app = None
    workflow = StateGraph(MessagesState)

    def __init__(self,api_key):
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0,api_key=api_key)
        self.workflow.add_node("agent",self.make_call_model())
        self.workflow.add_edge(START,"agent")
        self.workflow.add_edge("agent",END)
        self.app = self.workflow.compile()

    def make_call_model(self):
        def call(state: MessagesState):
            messages = state['messages']
            response = self.llm.invoke(messages)
            # We return a list, because this will get added to the existing list
            return {"messages": [response]}
        return call


    def run(self,path)->str:
        b64img = image_read.as_base64(path)
        final_state = self.app.invoke(
            {"messages":[
                SystemMessage(
                """
You are an **AMAZING MANGA INTERPRETER** that transcribes manga pannels
These pannels are read FROM TOP TO BOTTOM AND FROM RIGHT TO LEFT
You will only accept images as input
Your job is to DESCRIBE the situation happening in EACH PANNEL of the image and INCLUDE EVERY PART OF THE CONVERSATION OR MONOLOG THAT ANY PRESENT CHARACTER MAY HAVE
To ouput of this job is in a json format as follows:
{
    "text":[
        {
            "type": "sound effect" | "thinking" | "speaking"
            "content": string //the content of the identified text
            "character":string //the character that says or thinks the text, can be the NARRATOR, only when the type is not "sound effect"
        }
    ]
    "narration":string[] // one for each pannel in cronological order according to the reading order, the narrations should include marks like these [0][1]][2] to reference any of the "text"s
}
                """),
                HumanMessage(content=[
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{b64img}"},
                    },
                ])
            ]},
            config={"recursion_limit":3},
            debug=True
        )
        return final_state["messages"][-1].content


