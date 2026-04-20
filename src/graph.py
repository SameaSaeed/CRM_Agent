import os
import json
import asyncio
import nest_asyncio
import re
from pydantic import BaseModel
from typing import Annotated, List, Literal
from langchain_groq import ChatGroq
from langchain_core.messages import (
    BaseMessage,
    SystemMessage,
    AIMessage,
    ToolMessage,
    HumanMessage
)
from langgraph.types import Command, interrupt
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver
from langchain_mcp_adapters.client import MultiServerMCPClient
from ralph.my_mcp.config import mcp_config
from ralph.prompts import ralph_system_prompt

class AgentState(BaseModel):
    """The state of the agent."""
    messages: Annotated[List[BaseMessage], add_messages] = []
    protected_tools: List[str] = ["create_campaign", "send_campaign_email"]
    yolo_mode: bool = False

async def build_graph():
    """
    Build the LangGraph application with environment variable injection.
    """
    for server_name, server_def in mcp_config["mcpServers"].items():
        if server_name == "marketing":
            server_def["args"] = ["ralph/my_mcp/servers/marketing_server.py"]
            server_def["env"] = server_def.get("env", {})
            server_def["env"]["SUPABASE_URI"] = os.getenv("SUPABASE_URI")
        
        if "args" in server_def:
            new_args = []
            for arg in server_def["args"]:
                arg_str = str(arg)
                if "${" in arg_str:
                    new_args.append(os.path.expandvars(arg_str))
                else:
                    new_args.append(arg)
            server_def["args"] = new_args

        if "env" in server_def:
            for key, value in server_def["env"].items():
                if isinstance(value, str) and "${" in value:
                    server_def["env"][key] = os.path.expandvars(value)

    client = MultiServerMCPClient(connections=mcp_config["mcpServers"])
    tools = await client.get_tools()

    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.1).bind_tools(tools)

    def assistant_node(state: AgentState) -> dict:
        messages = [SystemMessage(content=ralph_system_prompt)] + state.messages
        
        try:
            response = llm.invoke(messages)
        except Exception as e:
            error_msg = str(e)
            # Catch the Groq hallucination error with a flexible regex
            # This handles newlines and extra spacing
            match = re.search(r'query\s*(\{.*\})', error_msg, re.DOTALL | re.IGNORECASE)
            if match:
                try:
                    sql_json_str = match.group(1).strip()
                    sql_json = json.loads(sql_json_str)
                    
                    response = AIMessage(
                        content="",
                        tool_calls=[{
                            "name": "query",
                            "args": sql_json,
                            "id": "fix_" + os.urandom(4).hex()
                        }]
                    )
                except:
                    raise e
            else:
                raise e

        return {"messages": [response]}

    def human_tool_review_node(state: AgentState):
        last_message = state.messages[-1]
        tool_call = last_message.tool_calls[-1]
        review = interrupt({"message": "Review required:", "tool_call": tool_call})
        
        action = review.get("action")
        if action == "continue":
            return Command(goto="tools")
        elif action == "update":
            updated_msg = AIMessage(
                content=last_message.content,
                tool_calls=[{
                    "id": tool_call["id"], 
                    "name": tool_call["name"], 
                    "args": json.loads(review["data"])
                }],
                id=last_message.id
            )
            return Command(goto="tools", update={"messages": [updated_msg]})
        
        return Command(
            goto="assistant_node", 
            update={"messages": [ToolMessage(content=str(review.get("data")), tool_call_id=tool_call["id"])]}
        )

    def assistant_router(state: AgentState) -> str:
        last_message = state.messages[-1]
        if not last_message.tool_calls: return END
        if not state.yolo_mode and any(tc["name"] in state.protected_tools for tc in last_message.tool_calls):
            return "human_tool_review_node"
        return "tools"

    builder = StateGraph(AgentState)
    builder.add_node("assistant_node", assistant_node)
    builder.add_node("human_tool_review_node", human_tool_review_node)
    builder.add_node("tools", ToolNode(tools))

    builder.add_edge(START, "assistant_node")
    builder.add_conditional_edges("assistant_node", assistant_router, ["tools", "human_tool_review_node", END])
    builder.add_edge("tools", "assistant_node")
    return builder.compile(checkpointer=MemorySaver())

async def main():
    graph = await build_graph()
    config = {"configurable": {"thread_id": "1"}}
    print("Agent ready. Type 'exit' to quit.")
    
    while True:
        try:
            state = await graph.aget_state(config)
            if state.next and "human_tool_review_node" in state.next:
                user_input = input("\n[REVIEW REQUIRED] Enter action JSON: ")
                if user_input.lower() in ["exit", "quit"]: break
                inp = Command(resume=json.loads(user_input))
            else:
                user_input = input("\nUser: ")
                if user_input.lower() in ["exit", "quit"]: break
                inp = {"messages": [HumanMessage(content=user_input)]}

            async for event in graph.astream(inp, config):
                for node, values in event.items():
                    if values and isinstance(values, dict) and "messages" in values and values["messages"]:
                        msg = values["messages"][-1]
                        if hasattr(msg, 'content') and msg.content:
                            print(f"\n[{node}]: {msg.content}")
                    else:
                        print(f"[{node}]: Step complete.")
                        
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    nest_asyncio.apply()
    asyncio.run(main())
