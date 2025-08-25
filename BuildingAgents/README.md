## OpenAi tools and invocation

The official OpenAI Python client does not have a concept of “registering tools” on the OpenAI object itself.
Use the "tools" parameter (newer API) or "functions".

```
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
    tools=[
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "Get the weather forecast",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {"type": "string"}
                    },
                    "required": ["location"],
                }
            }
        }
    ],
    tool_choice="auto"
)
```

```
tools=[{
  "type": "function",
  "function": {
    "name": "get_weather",
    "description": "Get the weather",
    "parameters": {...}
  }
}]
```


LLM doesn't execute the tools on its own, it returns a response like 

```
{
  "role": "assistant",
  "tool_calls": [
    {
      "id": "call_123",
      "type": "function",
      "function": {
        "name": "get_weather",
        "arguments": "{\"location\":\"Vancouver\"}"
      }
    }
  ]
}
```

in response handler we execute the tools
```
tool = tools["get_weather"]
result = tool(location="Vancouver")
```