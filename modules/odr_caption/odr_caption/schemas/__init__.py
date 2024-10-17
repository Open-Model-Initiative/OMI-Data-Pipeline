from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from odr_caption.schemas.vllm_schemas import (
    VLLMFunction,
    VLLMTool,
    VLLMRequestMessage,
    VLLMRequest,
    ToolCall,
    VLLMMessage,
    VLLMChoice,
    VLLMUsage,
    VLLMResponse,
    Interaction,
)


class TestCase(BaseModel):
    image_path: str
    expected_result: str
    expected_keywords: List[str]


class TestSuite(BaseModel):
    name: str
    output_file: str
    system_message: str
    test_cases: List[TestCase]


class GlobalConfig(BaseModel):

    model: str
    max_tokens: int
    temperature: float
    vllm_server_url: str


class Config(BaseModel):
    global_config: GlobalConfig = Field(..., alias="global")
    test_suites: Dict[str, Dict[str, TestSuite]]


class ResponseAnalysis(BaseModel):
    task_type: str
    response_received: bool
    response_content: str
    total_tokens: int
    expected_result: str
    evaluation: str
    keyword_match_percentage: float
    image_path: str
    test_suite_name: str


class ImageCaptionInputs(BaseModel):
    system_message: str
    image_data: str
    prompt: str | None = None
