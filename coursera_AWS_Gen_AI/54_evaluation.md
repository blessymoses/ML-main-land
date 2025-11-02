# Bedrock Evaluations

## Automatic/Programmatic Evaluation
Tests metrics like toxicity, accuracy, and robustness 
Configurable parameters: temperature, top P, response length 
Supports different task types (text generation, summarization, Q&A, classification)

## Judge Model Evaluation
Uses an evaluator model to generate metrics 
Metrics include quality, helpfulness, relevance, coherence, responsible AI 
Can evaluate external inferences via JSONL files

## Human Worker Evaluation 
Uses human evaluators instead of models 
Can compare responses from two models 
Supports rating methods like thumbs up/down or Likert scale

## RAG Evaluation
Evaluates retrieval-augmented generation systems 
Two evaluation types: Retrieval + Response Generation, Retrieval Only 
Metrics vary by evaluation type

## Prompt Caching 
Purpose: Optimize token usage and response time for repeated prompt components 
Implementation:
```python
 cache_point = {"type": "default"}
  prompt = {
    "system_prompt": "...",
    "cache_point": cache_point,
    "user_input": "..."
  }
```
Benefits
Reduces token consumption, Improves response speed, Lower costs
Limitations 
Requires exact match of prefix content, Sensitive to formatting changes

## Intelligent Prompt Routing
Purpose: Automatically direct requests to appropriate models 
Features:
Dynamic model selection based on request complexity 
Cost optimization 
Supports model families (e.g., Meta, Anthropic) 
Implementation Example:
```python
 routing_config = {
    "models": ["<MODEL_ID_1>", "<MODEL_ID_2>"],
    "routing_criteria": {"response_quality_difference": <DIFFERENCE>},
    "fallback_model": "<FALLBACK_MODEL_ID>"
  } 
```

## Cross-Region Inference Profiles
Purpose: Optimize model execution across regions
Benefits:
Improved latency
Better availability
Load balancing
Can be combined with prompt routing for comprehensive optimization