# SPDX-License-Identifier: Apache-2.0
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Union


class VLLMFunction(BaseModel):
    name: str
    description: Optional[str] = None
    parameters: Dict[str, Any]


class VLLMTool(BaseModel):
    type: str
    function: VLLMFunction


class VLLMRequestMessage(BaseModel):
    role: str
    content: Union[str, List[Dict[str, Any]], None]
    name: Optional[str] = None
    function_call: Optional[Dict[str, Any]] = None


class VLLMRequest(BaseModel):
    model: str
    messages: List[VLLMRequestMessage]
    functions: Optional[List[VLLMFunction]] = None
    function_call: Optional[Union[str, Dict[str, Any]]] = None
    tools: Optional[List[VLLMTool]] = None
    tool_choice: Optional[Union[str, Dict[str, Any]]] = None
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    n: Optional[int] = None
    stream: Optional[bool] = None
    stop: Optional[Union[str, List[str]]] = None
    max_tokens: Optional[int] = None
    presence_penalty: Optional[float] = None
    frequency_penalty: Optional[float] = None
    logit_bias: Optional[Dict[str, float]] = None
    user: Optional[str] = None


class ToolCall(BaseModel):
    id: str
    type: str
    function: Dict[str, Any]


class VLLMMessage(BaseModel):
    role: str
    content: Optional[str] = None
    tool_calls: Optional[List[ToolCall]] = None


class VLLMChoice(BaseModel):
    index: int
    message: VLLMMessage
    finish_reason: str


class VLLMUsage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class VLLMResponse(BaseModel):
    id: str
    object: str
    created: int
    model: str
    choices: List[VLLMChoice]
    usage: VLLMUsage
    system_fingerprint: Optional[str] = None

    class Config:
        allow_population_by_field_name = True


class Interaction(BaseModel):
    request: VLLMRequest
    response: VLLMResponse
    timestamp_start: int
    timestamp_end: int
    duration: float

    class Config:
        allow_population_by_field_name = True
