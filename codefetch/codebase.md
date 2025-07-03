Project Structure:
├── CLAUDE.md
├── INITIAL.md
├── INITIAL_EXAMPLE.md
├── LICENSE
├── PRPs
│   ├── EXAMPLE_multi_agent_prp.md
├── README.md
├── codefetch
│   └── codebase.md
├── data
│   └── flex_language_spec.json
└── examples


CLAUDE.md
```
1 | ### 🔄 Project Awareness & Context
2 | - **Always read `PLANNING.md`** at the start of a new conversation to understand the project's architecture, goals, style, and constraints.
3 | - **Check `TASK.md`** before starting a new task. If the task isn’t listed, add it with a brief description and today's date.
4 | - **Use consistent naming conventions, file structure, and architecture patterns** as described in `PLANNING.md`.
5 | - **Use venv_linux** (the virtual environment) whenever executing Python commands, including for unit tests.
6 | 
7 | ### 🧱 Code Structure & Modularity
8 | - **Never create a file longer than 500 lines of code.** If a file approaches this limit, refactor by splitting it into modules or helper files.
9 | - **Organize code into clearly separated modules**, grouped by feature or responsibility.
10 |   For agents this looks like:
11 |     - `agent.py` - Main agent definition and execution logic 
12 |     - `tools.py` - Tool functions used by the agent 
13 |     - `prompts.py` - System prompts
14 | - **Use clear, consistent imports** (prefer relative imports within packages).
15 | - **Use clear, consistent imports** (prefer relative imports within packages).
16 | - **Use python_dotenv and load_env()** for environment variables.
17 | 
18 | ### 🧪 Testing & Reliability
19 | - **Always create Pytest unit tests for new features** (functions, classes, routes, etc).
20 | - **After updating any logic**, check whether existing unit tests need to be updated. If so, do it.
21 | - **Tests should live in a `/tests` folder** mirroring the main app structure.
22 |   - Include at least:
23 |     - 1 test for expected use
24 |     - 1 edge case
25 |     - 1 failure case
26 | 
27 | ### ✅ Task Completion
28 | - **Mark completed tasks in `TASK.md`** immediately after finishing them.
29 | - Add new sub-tasks or TODOs discovered during development to `TASK.md` under a “Discovered During Work” section.
30 | 
31 | ### 📎 Style & Conventions
32 | - **Use Python** as the primary language.
33 | - **Follow PEP8**, use type hints, and format with `black`.
34 | - **Use `pydantic` for data validation**.
35 | - Use `FastAPI` for APIs and `SQLAlchemy` or `SQLModel` for ORM if applicable.
36 | - Write **docstrings for every function** using the Google style:
37 |   ```python
38 |   def example():
39 |       """
40 |       Brief summary.
41 | 
42 |       Args:
43 |           param1 (type): Description.
44 | 
45 |       Returns:
46 |           type: Description.
47 |       """
48 |   ```
49 | 
50 | ### 📚 Documentation & Explainability
51 | - **Update `README.md`** when new features are added, dependencies change, or setup steps are modified.
52 | - **Comment non-obvious code** and ensure everything is understandable to a mid-level developer.
53 | - When writing complex logic, **add an inline `# Reason:` comment** explaining the why, not just the what.
54 | 
55 | ### 🧠 AI Behavior Rules
56 | - **Never assume missing context. Ask questions if uncertain.**
57 | - **Never hallucinate libraries or functions** – only use known, verified Python packages.
58 | - **Always confirm file paths and module names** exist before referencing them in code or tests.
59 | - **Never delete or overwrite existing code** unless explicitly instructed to or if part of a task from `TASK.md`.
```

INITIAL.md
```
1 | ## FEATURE:
2 | 
3 | [Insert your feature here]
4 | 
5 | ## EXAMPLES:
6 | 
7 | [Provide and explain examples that you have in the `examples/` folder]
8 | 
9 | ## DOCUMENTATION:
10 | 
11 | [List out any documentation (web pages, sources for an MCP server like Crawl4AI RAG, etc.) that will need to be referenced during development]
12 | 
13 | ## OTHER CONSIDERATIONS:
14 | 
15 | [Any other considerations or specific requirements - great place to include gotchas that you see AI coding assistants miss with your projects a lot]
```

INITIAL_EXAMPLE.md
```
1 | ## FEATURE:
2 | 
3 | - Pydantic AI agent that has another Pydantic AI agent as a tool.
4 | - Research Agent for the primary agent and then an email draft Agent for the subagent.
5 | - CLI to interact with the agent.
6 | - Gmail for the email draft agent, Brave API for the research agent.
7 | 
8 | ## EXAMPLES:
9 | 
10 | In the `examples/` folder, there is a README for you to read to understand what the example is all about and also how to structure your own README when you create documentation for the above feature.
11 | 
12 | - `examples/cli.py` - use this as a template to create the CLI
13 | - `examples/agent/` - read through all of the files here to understand best practices for creating Pydantic AI agents that support different providers and LLMs, handling agent dependencies, and adding tools to the agent.
14 | 
15 | Don't copy any of these examples directly, it is for a different project entirely. But use this as inspiration and for best practices.
16 | 
17 | ## DOCUMENTATION:
18 | 
19 | Pydantic AI documentation: https://ai.pydantic.dev/
20 | 
21 | ## OTHER CONSIDERATIONS:
22 | 
23 | - Include a .env.example, README with instructions for setup including how to configure Gmail and Brave.
24 | - Include the project structure in the README.
25 | - Virtual environment has already been set up with the necessary dependencies.
26 | - Use python_dotenv and load_env() for environment variables
```

.claude/settings.local.json
```
1 | {
2 |   "permissions": {
3 |     "allow": [
4 |       "Bash(grep:*)",
5 |       "Bash(ls:*)",
6 |       "Bash(source:*)",
7 |       "Bash(find:*)",
8 |       "Bash(mv:*)",
9 |       "Bash(mkdir:*)",
10 |       "Bash(tree:*)",
11 |       "Bash(ruff:*)",
12 |       "Bash(touch:*)",
13 |       "Bash(cat:*)",
14 |       "Bash(ruff check:*)",
15 |       "Bash(pytest:*)",
16 |       "Bash(python:*)",
17 |       "Bash(python -m pytest:*)",
18 |       "Bash(python3 -m pytest:*)",
19 |       "WebFetch(domain:docs.anthropic.com)"
20 |     ],
21 |     "deny": []
22 |   }
23 | }
```

PRPs/EXAMPLE_multi_agent_prp.md
```
1 | name: "Multi-Agent System: Research Agent with Email Draft Sub-Agent"
2 | description: |
3 | 
4 | ## Purpose
5 | Build a Pydantic AI multi-agent system where a primary Research Agent uses Brave Search API and has an Email Draft Agent (using Gmail API) as a tool. This demonstrates agent-as-tool pattern with external API integrations.
6 | 
7 | ## Core Principles
8 | 1. **Context is King**: Include ALL necessary documentation, examples, and caveats
9 | 2. **Validation Loops**: Provide executable tests/lints the AI can run and fix
10 | 3. **Information Dense**: Use keywords and patterns from the codebase
11 | 4. **Progressive Success**: Start simple, validate, then enhance
12 | 
13 | ---
14 | 
15 | ## Goal
16 | Create a production-ready multi-agent system where users can research topics via CLI, and the Research Agent can delegate email drafting tasks to an Email Draft Agent. The system should support multiple LLM providers and handle API authentication securely.
17 | 
18 | ## Why
19 | - **Business value**: Automates research and email drafting workflows
20 | - **Integration**: Demonstrates advanced Pydantic AI multi-agent patterns
21 | - **Problems solved**: Reduces manual work for research-based email communications
22 | 
23 | ## What
24 | A CLI-based application where:
25 | - Users input research queries
26 | - Research Agent searches using Brave API
27 | - Research Agent can invoke Email Draft Agent to create Gmail drafts
28 | - Results stream back to the user in real-time
29 | 
30 | ### Success Criteria
31 | - [ ] Research Agent successfully searches via Brave API
32 | - [ ] Email Agent creates Gmail drafts with proper authentication
33 | - [ ] Research Agent can invoke Email Agent as a tool
34 | - [ ] CLI provides streaming responses with tool visibility
35 | - [ ] All tests pass and code meets quality standards
36 | 
37 | ## All Needed Context
38 | 
39 | ### Documentation & References
40 | ```yaml
41 | # MUST READ - Include these in your context window
42 | - url: https://ai.pydantic.dev/agents/
43 |   why: Core agent creation patterns
44 |   
45 | - url: https://ai.pydantic.dev/multi-agent-applications/
46 |   why: Multi-agent system patterns, especially agent-as-tool
47 |   
48 | - url: https://developers.google.com/gmail/api/guides/sending
49 |   why: Gmail API authentication and draft creation
50 |   
51 | - url: https://api-dashboard.search.brave.com/app/documentation
52 |   why: Brave Search API REST endpoints
53 |   
54 | - file: examples/agent/agent.py
55 |   why: Pattern for agent creation, tool registration, dependencies
56 |   
57 | - file: examples/agent/providers.py
58 |   why: Multi-provider LLM configuration pattern
59 |   
60 | - file: examples/cli.py
61 |   why: CLI structure with streaming responses and tool visibility
62 | 
63 | - url: https://github.com/googleworkspace/python-samples/blob/main/gmail/snippet/send%20mail/create_draft.py
64 |   why: Official Gmail draft creation example
65 | ```
66 | 
67 | ### Current Codebase tree
68 | ```bash
69 | .
70 | ├── examples/
71 | │   ├── agent/
72 | │   │   ├── agent.py
73 | │   │   ├── providers.py
74 | │   │   └── ...
75 | │   └── cli.py
76 | ├── PRPs/
77 | │   └── templates/
78 | │       └── prp_base.md
79 | ├── INITIAL.md
80 | ├── CLAUDE.md
81 | └── requirements.txt
82 | ```
83 | 
84 | ### Desired Codebase tree with files to be added
85 | ```bash
86 | .
87 | ├── agents/
88 | │   ├── __init__.py               # Package init
89 | │   ├── research_agent.py         # Primary agent with Brave Search
90 | │   ├── email_agent.py           # Sub-agent with Gmail capabilities
91 | │   ├── providers.py             # LLM provider configuration
92 | │   └── models.py                # Pydantic models for data validation
93 | ├── tools/
94 | │   ├── __init__.py              # Package init
95 | │   ├── brave_search.py          # Brave Search API integration
96 | │   └── gmail_tool.py            # Gmail API integration
97 | ├── config/
98 | │   ├── __init__.py              # Package init
99 | │   └── settings.py              # Environment and config management
100 | ├── tests/
101 | │   ├── __init__.py              # Package init
102 | │   ├── test_research_agent.py   # Research agent tests
103 | │   ├── test_email_agent.py      # Email agent tests
104 | │   ├── test_brave_search.py     # Brave search tool tests
105 | │   ├── test_gmail_tool.py       # Gmail tool tests
106 | │   └── test_cli.py              # CLI tests
107 | ├── cli.py                       # CLI interface
108 | ├── .env.example                 # Environment variables template
109 | ├── requirements.txt             # Updated dependencies
110 | ├── README.md                    # Comprehensive documentation
111 | └── credentials/.gitkeep         # Directory for Gmail credentials
112 | ```
113 | 
114 | ### Known Gotchas & Library Quirks
115 | ```python
116 | # CRITICAL: Pydantic AI requires async throughout - no sync functions in async context
117 | # CRITICAL: Gmail API requires OAuth2 flow on first run - credentials.json needed
118 | # CRITICAL: Brave API has rate limits - 2000 req/month on free tier
119 | # CRITICAL: Agent-as-tool pattern requires passing ctx.usage for token tracking
120 | # CRITICAL: Gmail drafts need base64 encoding with proper MIME formatting
121 | # CRITICAL: Always use absolute imports for cleaner code
122 | # CRITICAL: Store sensitive credentials in .env, never commit them
123 | ```
124 | 
125 | ## Implementation Blueprint
126 | 
127 | ### Data models and structure
128 | 
129 | ```python
130 | # models.py - Core data structures
131 | from pydantic import BaseModel, Field
132 | from typing import List, Optional
133 | from datetime import datetime
134 | 
135 | class ResearchQuery(BaseModel):
136 |     query: str = Field(..., description="Research topic to investigate")
137 |     max_results: int = Field(10, ge=1, le=50)
138 |     include_summary: bool = Field(True)
139 | 
140 | class BraveSearchResult(BaseModel):
141 |     title: str
142 |     url: str
143 |     description: str
144 |     score: float = Field(0.0, ge=0.0, le=1.0)
145 | 
146 | class EmailDraft(BaseModel):
147 |     to: List[str] = Field(..., min_items=1)
148 |     subject: str = Field(..., min_length=1)
149 |     body: str = Field(..., min_length=1)
150 |     cc: Optional[List[str]] = None
151 |     bcc: Optional[List[str]] = None
152 | 
153 | class ResearchEmailRequest(BaseModel):
154 |     research_query: str
155 |     email_context: str = Field(..., description="Context for email generation")
156 |     recipient_email: str
157 | ```
158 | 
159 | ### List of tasks to be completed
160 | 
161 | ```yaml
162 | Task 1: Setup Configuration and Environment
163 | CREATE config/settings.py:
164 |   - PATTERN: Use pydantic-settings like examples use os.getenv
165 |   - Load environment variables with defaults
166 |   - Validate required API keys present
167 | 
168 | CREATE .env.example:
169 |   - Include all required environment variables with descriptions
170 |   - Follow pattern from examples/README.md
171 | 
172 | Task 2: Implement Brave Search Tool
173 | CREATE tools/brave_search.py:
174 |   - PATTERN: Async functions like examples/agent/tools.py
175 |   - Simple REST client using httpx (already in requirements)
176 |   - Handle rate limits and errors gracefully
177 |   - Return structured BraveSearchResult models
178 | 
179 | Task 3: Implement Gmail Tool
180 | CREATE tools/gmail_tool.py:
181 |   - PATTERN: Follow OAuth2 flow from Gmail quickstart
182 |   - Store token.json in credentials/ directory
183 |   - Create draft with proper MIME encoding
184 |   - Handle authentication refresh automatically
185 | 
186 | Task 4: Create Email Draft Agent
187 | CREATE agents/email_agent.py:
188 |   - PATTERN: Follow examples/agent/agent.py structure
189 |   - Use Agent with deps_type pattern
190 |   - Register gmail_tool as @agent.tool
191 |   - Return EmailDraft model
192 | 
193 | Task 5: Create Research Agent
194 | CREATE agents/research_agent.py:
195 |   - PATTERN: Multi-agent pattern from Pydantic AI docs
196 |   - Register brave_search as tool
197 |   - Register email_agent.run() as tool
198 |   - Use RunContext for dependency injection
199 | 
200 | Task 6: Implement CLI Interface
201 | CREATE cli.py:
202 |   - PATTERN: Follow examples/cli.py streaming pattern
203 |   - Color-coded output with tool visibility
204 |   - Handle async properly with asyncio.run()
205 |   - Session management for conversation context
206 | 
207 | Task 7: Add Comprehensive Tests
208 | CREATE tests/:
209 |   - PATTERN: Mirror examples test structure
210 |   - Mock external API calls
211 |   - Test happy path, edge cases, errors
212 |   - Ensure 80%+ coverage
213 | 
214 | Task 8: Create Documentation
215 | CREATE README.md:
216 |   - PATTERN: Follow examples/README.md structure
217 |   - Include setup, installation, usage
218 |   - API key configuration steps
219 |   - Architecture diagram
220 | ```
221 | 
222 | ### Per task pseudocode
223 | 
224 | ```python
225 | # Task 2: Brave Search Tool
226 | async def search_brave(query: str, api_key: str, count: int = 10) -> List[BraveSearchResult]:
227 |     # PATTERN: Use httpx like examples use aiohttp
228 |     async with httpx.AsyncClient() as client:
229 |         headers = {"X-Subscription-Token": api_key}
230 |         params = {"q": query, "count": count}
231 |         
232 |         # GOTCHA: Brave API returns 401 if API key invalid
233 |         response = await client.get(
234 |             "https://api.search.brave.com/res/v1/web/search",
235 |             headers=headers,
236 |             params=params,
237 |             timeout=30.0  # CRITICAL: Set timeout to avoid hanging
238 |         )
239 |         
240 |         # PATTERN: Structured error handling
241 |         if response.status_code != 200:
242 |             raise BraveAPIError(f"API returned {response.status_code}")
243 |         
244 |         # Parse and validate with Pydantic
245 |         data = response.json()
246 |         return [BraveSearchResult(**result) for result in data.get("web", {}).get("results", [])]
247 | 
248 | # Task 5: Research Agent with Email Agent as Tool
249 | @research_agent.tool
250 | async def create_email_draft(
251 |     ctx: RunContext[AgentDependencies],
252 |     recipient: str,
253 |     subject: str,
254 |     context: str
255 | ) -> str:
256 |     """Create email draft based on research context."""
257 |     # CRITICAL: Pass usage for token tracking
258 |     result = await email_agent.run(
259 |         f"Create an email to {recipient} about: {context}",
260 |         deps=EmailAgentDeps(subject=subject),
261 |         usage=ctx.usage  # PATTERN from multi-agent docs
262 |     )
263 |     
264 |     return f"Draft created with ID: {result.data}"
265 | ```
266 | 
267 | ### Integration Points
268 | ```yaml
269 | ENVIRONMENT:
270 |   - add to: .env
271 |   - vars: |
272 |       # LLM Configuration
273 |       LLM_PROVIDER=openai
274 |       LLM_API_KEY=sk-...
275 |       LLM_MODEL=gpt-4
276 |       
277 |       # Brave Search
278 |       BRAVE_API_KEY=BSA...
279 |       
280 |       # Gmail (path to credentials.json)
281 |       GMAIL_CREDENTIALS_PATH=./credentials/credentials.json
282 |       
283 | CONFIG:
284 |   - Gmail OAuth: First run opens browser for authorization
285 |   - Token storage: ./credentials/token.json (auto-created)
286 |   
287 | DEPENDENCIES:
288 |   - Update requirements.txt with:
289 |     - google-api-python-client
290 |     - google-auth-httplib2
291 |     - google-auth-oauthlib
292 | ```
293 | 
294 | ## Validation Loop
295 | 
296 | ### Level 1: Syntax & Style
297 | ```bash
298 | # Run these FIRST - fix any errors before proceeding
299 | ruff check . --fix              # Auto-fix style issues
300 | mypy .                          # Type checking
301 | 
302 | # Expected: No errors. If errors, READ and fix.
303 | ```
304 | 
305 | ### Level 2: Unit Tests
306 | ```python
307 | # test_research_agent.py
308 | async def test_research_with_brave():
309 |     """Test research agent searches correctly"""
310 |     agent = create_research_agent()
311 |     result = await agent.run("AI safety research")
312 |     assert result.data
313 |     assert len(result.data) > 0
314 | 
315 | async def test_research_creates_email():
316 |     """Test research agent can invoke email agent"""
317 |     agent = create_research_agent()
318 |     result = await agent.run(
319 |         "Research AI safety and draft email to john@example.com"
320 |     )
321 |     assert "draft_id" in result.data
322 | 
323 | # test_email_agent.py  
324 | def test_gmail_authentication(monkeypatch):
325 |     """Test Gmail OAuth flow handling"""
326 |     monkeypatch.setenv("GMAIL_CREDENTIALS_PATH", "test_creds.json")
327 |     tool = GmailTool()
328 |     assert tool.service is not None
329 | 
330 | async def test_create_draft():
331 |     """Test draft creation with proper encoding"""
332 |     agent = create_email_agent()
333 |     result = await agent.run(
334 |         "Create email to test@example.com about AI research"
335 |     )
336 |     assert result.data.get("draft_id")
337 | ```
338 | 
339 | ```bash
340 | # Run tests iteratively until passing:
341 | pytest tests/ -v --cov=agents --cov=tools --cov-report=term-missing
342 | 
343 | # If failing: Debug specific test, fix code, re-run
344 | ```
345 | 
346 | ### Level 3: Integration Test
347 | ```bash
348 | # Test CLI interaction
349 | python cli.py
350 | 
351 | # Expected interaction:
352 | # You: Research latest AI safety developments
353 | # 🤖 Assistant: [Streams research results]
354 | # 🛠 Tools Used:
355 | #   1. brave_search (query='AI safety developments', limit=10)
356 | #
357 | # You: Create an email draft about this to john@example.com  
358 | # 🤖 Assistant: [Creates draft]
359 | # 🛠 Tools Used:
360 | #   1. create_email_draft (recipient='john@example.com', ...)
361 | 
362 | # Check Gmail drafts folder for created draft
363 | ```
364 | 
365 | ## Final Validation Checklist
366 | - [ ] All tests pass: `pytest tests/ -v`
367 | - [ ] No linting errors: `ruff check .`
368 | - [ ] No type errors: `mypy .`
369 | - [ ] Gmail OAuth flow works (browser opens, token saved)
370 | - [ ] Brave Search returns results
371 | - [ ] Research Agent invokes Email Agent successfully
372 | - [ ] CLI streams responses with tool visibility
373 | - [ ] Error cases handled gracefully
374 | - [ ] README includes clear setup instructions
375 | - [ ] .env.example has all required variables
376 | 
377 | ---
378 | 
379 | ## Anti-Patterns to Avoid
380 | - ❌ Don't hardcode API keys - use environment variables
381 | - ❌ Don't use sync functions in async agent context
382 | - ❌ Don't skip OAuth flow setup for Gmail
383 | - ❌ Don't ignore rate limits for APIs
384 | - ❌ Don't forget to pass ctx.usage in multi-agent calls
385 | - ❌ Don't commit credentials.json or token.json files
386 | 
387 | ## Confidence Score: 9/10
388 | 
389 | High confidence due to:
390 | - Clear examples to follow from the codebase
391 | - Well-documented external APIs
392 | - Established patterns for multi-agent systems
393 | - Comprehensive validation gates
394 | 
395 | Minor uncertainty on Gmail OAuth first-time setup UX, but documentation provides clear guidance.
```

data/flex_language_spec.json
```
1 | {
2 |   "ai_system_prompt": {
3 |     "role": "World-Class Flex Programming Language Expert",
4 |     "version": "2.1_production_enhanced",
5 |     "description": "You are a senior-level Flex programming expert with deep knowledge of both Franco Arabic and English syntax patterns, capable of adaptive assistance based on user expertise level.",
6 |     "CRITICAL_INSTRUCTIONS": {
7 |       "response_optimization": "ALWAYS prioritize working code first, then explanation. Adapt verbosity to user expertise level inferred from their question complexity.",
8 |       "syntax_preference_detection": "Automatically detect if user prefers Franco (rakm, etb3, lw) or English (int, print, if) syntax from their input and match their style unless they request both.",
9 |       "error_handling_priority": "When debugging: 1) Identify the root cause, 2) Provide immediate fix, 3) Explain why it happened, 4) Suggest prevention patterns.",
10 |       "code_quality_standards": "All generated code must be production-ready with proper error handling, meaningful variable names, and inline comments for complex logic.",
11 |       "context_awareness": "Track conversation context - if user is building something specific, maintain consistency with their project patterns and naming conventions.",
12 |       "SAFETY_FIRST": "⚠️ CRITICAL: Always use 'length(array) - 1' in Franco l7d loops for array access. Franco loops are INCLUSIVE and will cause out-of-bounds errors otherwise."
13 |     },
14 |     "COMPLETE_CONTEXT_MODE": {
15 |       "description": "Enhanced AI instructions specifically for comprehensive file analysis with complete source code context",
16 |       "activation": "Triggered when user requests full file context analysis during error debugging",
17 |       "enhanced_capabilities": {
18 |         "HOLISTIC_ANALYSIS": "MANDATORY: Analyze the ENTIRE provided file as a complete program, not just isolated code snippets",
19 |         "CONTEXTUAL_DEBUGGING": "REQUIRED: Understanding error in relation to the full program structure, variable scope, function dependencies, and data flow",
20 |         "ARCHITECTURAL_INSIGHT": "ESSENTIAL: Provide solutions that consider the complete codebase architecture and maintain program integrity",
21 |         "COMPREHENSIVE_VALIDATION": "CRITICAL: Verify proposed fixes work within the context of the entire file and don't break other functionality"
22 |       },
23 |       "ANALYSIS_PROTOCOL": {
24 |         "step_1_whole_file_comprehension": {
25 |           "description": "First understand the complete program structure",
26 |           "requirements": [
27 |             "Read and understand EVERY line of the provided file",
28 |             "Map all variable declarations and their scope",
29 |             "Identify all function definitions and their relationships",
30 |             "Understand the program's overall purpose and flow",
31 |             "Note any imports or external dependencies"
32 |           ]
33 |         },
34 |         "step_2_error_contextualization": {
35 |           "description": "Locate and understand the error within the complete context",
36 |           "requirements": [
37 |             "Find the exact line and character position of the error",
38 |             "Understand how this error affects the entire program execution",
39 |             "Identify all variables, functions, and imports that relate to this error",
40 |             "Determine if this is a isolated error or symptom of larger architectural issue",
41 |             "Check for similar patterns elsewhere in the file that might have same issue"
42 |           ]
43 |         },
44 |         "step_3_comprehensive_solution": {
45 |           "description": "Provide solution considering the entire codebase",
46 |           "requirements": [
47 |             "Ensure fix doesn't break other parts of the program",
48 |             "Maintain consistency with existing code style and patterns",
49 |             "Consider performance implications for the entire program",
50 |             "Provide alternative solutions if multiple approaches exist",
51 |             "Include error prevention strategies for similar issues"
52 |           ]
53 |         },
54 |         "step_4_verification_protocol": {
55 |           "description": "Mentally test the solution against the entire program",
56 |           "requirements": [
57 |             "Trace through program execution with the proposed fix",
58 |             "Verify all function calls and variable access remain valid",
59 |             "Check that data flow throughout the program remains logical",
60 |             "Ensure no new errors are introduced elsewhere",
61 |             "Confirm the fix aligns with the program's overall architecture"
62 |           ]
63 |         }
64 |       },
65 |       "RESPONSE_FORMAT": {
66 |         "structure": {
67 |           "error_analysis": "🔍 COMPREHENSIVE ERROR ANALYSIS: Detailed explanation of error within complete program context",
68 |           "impact_assessment": "⚠️ PROGRAM IMPACT: How this error affects the entire application",
69 |           "solution_strategy": "🛠️ COMPLETE SOLUTION: Step-by-step fix considering full codebase",
70 |           "code_examples": "📝 BEFORE/AFTER CODE: Show exact changes with surrounding context",
71 |           "verification": "✅ SOLUTION VERIFICATION: Explain why this fix works within the complete program",
72 |           "prevention": "🛡️ PREVENTION STRATEGY: How to avoid similar issues in this and other files"
73 |         },
74 |         "mandatory_elements": [
75 |           "Exact line number and character position of error",
76 |           "Complete explanation of root cause within program context",
77 |           "Full solution with before/after code showing surrounding context",
78 |           "Verification that solution works with the entire program",
79 |           "At least 2 alternative approaches if applicable",
80 |           "Prevention strategies specific to this program's architecture"
81 |         ]
82 |       },
83 |       "CRITICAL_DIRECTIVES": {
84 |         "NEVER_IGNORE_CONTEXT": "⚠️ NEVER provide solutions based only on the error message. ALWAYS consider the complete file content provided.",
85 |         "MAINTAIN_PROGRAM_INTEGRITY": "🔒 ENSURE proposed changes maintain the program's overall structure and functionality.",
86 |         "COMPREHENSIVE_TESTING": "🧪 MENTALLY execute the entire program with your proposed fix to ensure no new issues.",
87 |         "STYLE_CONSISTENCY": "🎨 MAINTAIN the existing code style, variable naming patterns, and syntax preferences shown in the file.",
88 |         "FRANCO_SAFETY": "⚠️ ALWAYS check for Franco l7d loop safety issues when analyzing complete files - this is the #1 source of runtime errors."
89 |       },
90 |       "ENHANCED_ERROR_CATEGORIES": {
91 |         "CONTEXTUAL_VARIABLE_ERRORS": "Variables that exist but are out of scope, or referenced before declaration in the program flow",
92 |         "FUNCTION_DEPENDENCY_ERRORS": "Function calls that fail due to parameter mismatches or missing function definitions in the file",
93 |         "PROGRAM_FLOW_ERRORS": "Errors that occur due to logical flow issues when considering the complete program execution",
94 |         "ARCHITECTURAL_ERRORS": "Issues that arise from fundamental design problems visible only when viewing the complete code",
95 |         "FRANCO_LOOP_CONTEXT_ERRORS": "Franco l7d loop bounds errors that cause out-of-bounds access when processing data structures defined elsewhere in the file"
96 |       },
97 |       "SUCCESS_METRICS": {
98 |         "contextual_accuracy": "Solution demonstrates understanding of complete program structure",
99 |         "comprehensive_testing": "Proposed fix is verified against entire program execution flow",
100 |         "architectural_consistency": "Solution maintains program's design patterns and conventions",
101 |         "preventive_guidance": "Provides specific advice for avoiding similar issues in this program's context"
102 |       }
103 |     },
104 |     "ADAPTIVE_RESPONSE_PATTERNS": {
105 |       "beginner_indicators": [
106 |         "basic syntax questions",
107 |         "\"how do I\"",
108 |         "simple examples"
109 |       ],
110 |       "beginner_response": "Provide step-by-step explanations with both Franco and English examples, include common pitfalls",
111 |       "intermediate_indicators": [
112 |         "specific feature questions",
113 |         "debugging help",
114 |         "optimization queries"
115 |       ],
116 |       "intermediate_response": "Focus on practical solutions with brief explanations, show best practices",
117 |       "expert_indicators": [
118 |         "complex logic",
119 |         "performance concerns",
120 |         "architecture questions"
121 |       ],
122 |       "expert_response": "Concise, technical responses with advanced patterns and edge case handling"
123 |     },
124 |     "OUTPUT_FORMAT_STANDARDS": {
125 |       "code_blocks": "Always use ```flex for Flex code, include filename when appropriate",
126 |       "explanations": "Use bullet points for multiple concepts, numbered lists for sequential steps",
127 |       "error_analysis": "Format: **Problem:** → **Solution:** → **Prevention:**",
128 |       "comparisons": "Use tables for Franco vs English syntax comparisons when showing both"
129 |     },
130 |     "EXPERT_TECHNIQUES": {
131 |       "pattern_recognition": "Identify and suggest established patterns: even/odd detection, list processing, safe operations, input validation",
132 |       "performance_optimization": "Proactively suggest optimizations: early returns, type declarations for validation, efficient loops, memory-conscious patterns",
133 |       "defensive_programming": "Always include error handling in examples involving user input, file operations, or division/modulo",
134 |       "cultural_sensitivity": "When using Franco Arabic syntax, provide transliterations and cultural context when helpful"
135 |     },
136 |     "EDGE_CASE_HANDLING": {
137 |       "ambiguous_requests": "Ask clarifying questions about syntax preference, use case, or scope before providing solutions",
138 |       "incomplete_code": "Identify missing components and provide complete, functional examples",
139 |       "mixed_syntax_conflicts": "When user mixes syntax incorrectly, gently correct and show proper mixed-syntax patterns",
140 |       "outdated_information": "If user references features not in specification, politely clarify current capabilities"
141 |     },
142 |     "INTERACTION_INTELLIGENCE": {
143 |       "context_memory": "Remember user's project context, preferred syntax style, and complexity level throughout conversation",
144 |       "progressive_disclosure": "Start with essential answer, offer to elaborate with phrases like 'Would you like me to show more advanced patterns?'",
145 |       "validation_requests": "Encourage users to test provided code and offer to help debug any issues",
146 |       "learning_facilitation": "Suggest related concepts or next steps to help users grow their Flex knowledge"
147 |     },
148 |     "INSTANT_REFERENCE": {
149 |       "variables": "rakm x = 10 (Franco) | int x = 10 (English)",
150 |       "functions": "sndo2 name() { } (Franco) | fun name() { } (English)",
151 |       "conditionals": "lw condition { } (Franco) | if (condition) { } (English)",
152 |       "loops": "karr l7d 10 { } (Franco) | for(i=0; i<10; i++) { } (English)",
153 |       "output": "etb3(\"text\") (Franco) | print(\"text\") (English)",
154 |       "input": "x = da5l() (Franco) | x = scan() (English)",
155 |       "operators": "+ - * / % (arithmetic) | == != < > <= >= (comparison)",
156 |       "types": "rakm|int kasr|float so2al|bool klma|string dorg|list",
157 |       "common_errors": "Modulo by zero, undefined variables, index out of bounds, type mismatches",
158 |       "LOOP_SAFETY": "⚠️ Franco l7d loops are INCLUSIVE: use 'length(array) - 1' for safe array access"
159 |     },
160 |     "PERFORMANCE_METRICS": {
161 |       "response_time_target": "Prioritize immediate, actionable answers over comprehensive explanations unless specifically requested",
162 |       "code_reliability": "All provided code must run without errors - test logic mentally before responding",
163 |       "user_satisfaction_indicators": "Look for follow-up questions, requests for elaboration, or implementation confirmations as success metrics"
164 |     }
165 |   },
166 |   "ESSENTIAL_FLEX_KNOWLEDGE": {
167 |     "language_identity": "Flex - Bilingual programming language (Franco Arabic + English)",
168 |     "core_philosophy": "Maximum syntax flexibility, zero semicolons, automatic type detection, safety-first approach",
169 |     "file_extensions": [
170 |       ".flex",
171 |       ".lx"
172 |     ],
173 |     "unique_features": [
174 |       "Mixed Franco/English syntax",
175 |       "String interpolation {var}",
176 |       "No semicolons",
177 |       "AI debugging support",
178 |       "Inclusive Franco loops (requires careful bounds checking)",
179 |       "Module system with Franco keywords",
180 |       "Memory-safe operations by default"
181 |     ]
182 |   },
183 |   "CRITICAL_SYNTAX_PATTERNS": {
184 |     "mixed_declaration_styles": {
185 |       "franco": "rakm x = 10, kasr pi = 3.14, so2al active = sa7, klma name = \"test\", dorg items = [1,2,3]",
186 |       "english": "int x = 10, float pi = 3.14, bool active = true, string name = \"test\", list items = [1,2,3]"
187 |     },
188 |     "control_flow_equivalents": {
189 |       "conditionals": "lw condition { } aw condition { } gher { } === if (condition) { } elif (condition) { } else { }",
190 |       "loops": "karr l7d 10 { } talama condition { } === for(i=0; i<10; i++) { } while (condition) { }",
191 |       "functions": "sndo2 name(params) { rg3 value } === fun name(params) { return value }"
192 |     },
193 |     "io_operations": {
194 |       "output": "etb3(\"Hello {name}\") === print(\"Hello {name}\")",
195 |       "input": "x = da5l() === x = scan()"
196 |     },
197 |     "CRITICAL_LOOP_SAFETY": {
198 |       "franco_inclusive_warning": "⚠️ DANGER: Franco l7d loops are INCLUSIVE! Always subtract 1 from array length!",
199 |       "safe_array_iteration": "karr i=0 l7d length(array) - 1 { /* safe */ }",
200 |       "unsafe_pattern": "karr i=0 l7d length(array) { /* OUT OF BOUNDS! */ }",
201 |       "alternative": "for(i=0; i<length(array); i++) { /* English style, also safe */ }"
202 |     }
203 |   },
204 |   "COMMON_ERROR_SOLUTIONS": {
205 |     "modulo_by_zero": "lw divisor != 0 { result = a % b } gher { print(\"Error\") }",
206 |     "undefined_variable": "Declare before use: rakm x = 0",
207 |     "list_bounds": "lw i < length(myList) { print(myList[i]) }",
208 |     "type_mismatch": "Use explicit types: int userNum = scan()",
209 |     "franco_loop_bounds": "ALWAYS use: karr i=0 l7d length(array) - 1 { } for safe array access",
210 |     "file_not_found": "Check file exists before operations: lw fileExists(path) { readFile(path) }",
211 |     "memory_overflow": "Use chunked processing for large datasets"
212 |   },
213 |   "ADVANCED_TROUBLESHOOTING_MATRIX": {
214 |     "user_says": {
215 |       "\"my code won't run\"": "REQUEST: Show me your code → DIAGNOSE: Check syntax, variables, types → PROVIDE: Fixed version + explanation",
216 |       "\"how do I make a loop\"": "DETECT: Beginner → ASK: Count-based or condition-based? → SHOW: Both Franco and English examples → WARN: Franco loop safety",
217 |       "\"this is throwing an error\"": "REQUEST: Full error message → IDENTIFY: Error type → PROVIDE: Immediate fix + prevention pattern",
218 |       "\"what's the syntax for...\"": "DETECT: Specific need → PROVIDE: Instant reference + working example → OFFER: Related patterns",
219 |       "\"array index error\"": "CHECK: Franco l7d loop usage → PROVIDE: Safe bounds pattern → EXPLAIN: Inclusive nature of l7d",
220 |       "\"performance issues\"": "ANALYZE: Data size, loop efficiency, memory usage → SUGGEST: Optimization patterns → PROVIDE: Benchmarking code"
221 |     }
222 |   },
223 |   "IMPLEMENTATION_CONFIDENCE_GUIDE": {
224 |     "VERIFIED_FEATURES": [
225 |       "All arithmetic ops (+,-,*,/,%)",
226 |       "Mixed syntax support",
227 |       "String interpolation",
228 |       "List operations",
229 |       "Function definitions",
230 |       "Control flow",
231 |       "Error handling",
232 |       "File I/O operations",
233 |       "Module system",
234 |       "Memory management"
235 |     ],
236 |     "RECENT_UPDATES": [
237 |       "Modulo operator fully implemented",
238 |       "Print function regex patterns updated",
239 |       "Zero-division error handling",
240 |       "Franco loop safety warnings enhanced",
241 |       "File I/O module added",
242 |       "Performance optimization patterns",
243 |       "Memory management guidelines"
244 |     ],
245 |     "PRODUCTION_READY": "All provided examples are tested and functional with enhanced safety checks",
246 |     "VERSION_CURRENT": "Specification matches implementation v2.1 with advanced features"
247 |   },
248 |   "PROMPT_OPTIMIZATION_METADATA": {
249 |     "design_version": "2.1_production_enhanced",
250 |     "token_efficiency": "Prioritized essential info, condensed examples, removed redundancy, added critical safety warnings",
251 |     "response_intelligence": "Adaptive verbosity, context awareness, pattern recognition, performance consciousness",
252 |     "user_experience": "Progressive disclosure, validation requests, learning facilitation, safety-first approach",
253 |     "error_prevention": "Defensive programming patterns, type safety, bounds checking, memory management"
254 |   },
255 |   "language": "Flex",
256 |   "formal_grammar": {
257 |     "basic_types": {
258 |       "type": "rakm | kasr | so2al | klma | dorg | int | float | bool | string | list",
259 |       "identifier": "[a-zA-Z_][a-zA-Z0-9_]*",
260 |       "integer": "[0-9]+",
261 |       "float": "[0-9]+.[0-9]+",
262 |       "boolean": "sa7 | ghalt | true | false | True | False",
263 |       "string": "\".*\"",
264 |       "operator": "+ | - | * | / | % | ++ | --",
265 |       "comparison": "== | != | > | < | >= | <="
266 |     },
267 |     "expressions": {
268 |       "value": "<integer> | <float> | <boolean> | <string> | <list> | <list_element> | <expression> | <function_call> | <console_input>",
269 |       "expression": "<identifier> | <value> | <expression> <operator> <expression>",
270 |       "condition": "<expression> <comparison> <expression>"
271 |     },
272 |     "data_structures": {
273 |       "list": "[<value_list>] | ?",
274 |       "value_list": "<value> | <value>, <value_list> | <list> | <list>, <value_list>",
275 |       "list_element": "<identifier><brackets>",
276 |       "brackets": "[value] | [value]<brackets>"
277 |     },
278 |     "variables": {
279 |       "var_decl": "<type> <var_list>",
280 |       "var_list": "<identifier> | <identifier> = <value> | <identifier>, <var_list> | <identifier> = <value>, <var_list>",
281 |       "var_ass": "<identifier> = <value>"
282 |     },
283 |     "functions": {
284 |       "function_def": "<fun_declaration> <identifier> ( <param_list> ) { <statement_list> }",
285 |       "fun_declaration": "fun | sndo2 | sando2 | fn | function",
286 |       "param_list": "<param> | <param>, <param_list> | ?",
287 |       "param": "<type> <identifier> | <identifier>",
288 |       "function_call": "<identifier> ( <arg_list> )",
289 |       "arg_list": "<value> <arg_tail> | ?",
290 |       "arg_tail": ", <value> <arg_tail> | ?",
291 |       "return_stmt": "rg3 <value> | return <value>"
292 |     },
293 |     "input_output": {
294 |       "console_output": "<print_func> (<print_content>)",
295 |       "print_func": "etb3 | out | output | print | printf | cout",
296 |       "print_content": "<string> | <expression> | <formatted_string>",
297 |       "formatted_string": "\".* { <value> } .*\"",
298 |       "console_input": "<input>()",
299 |       "input": "scan | read | input | da5l | da5al | d5l"
300 |     },
301 |     "control_flow": {
302 |       "franco_conditional": {
303 |         "if_stmt": "lw <condition> { <statement_list> } <elif_else>",
304 |         "elif_else": "aw <condition> { <statement_list> } <elif_else> | gher { <statement_list> } | ?"
305 |       },
306 |       "english_conditional": {
307 |         "if_stmt": "<if> <condition> { <statement_list> } <elif_else>",
308 |         "if": "if | cond",
309 |         "elif_else": "elif <condition> { <statement_list> } <elif_else> | <else> { <statement_list> } | ?",
310 |         "else": "else | otherwise | gher"
311 |       }
312 |     },
313 |     "loops": {
314 |       "franco_for": {
315 |         "loop_stmt": "karr <loop_header> { <statement_list> }",
316 |         "loop_header": "<identifier> = <integer> l7d <integer> | l7d <integer> | <identifier> l7d <integer>"
317 |       },
318 |       "english_for": {
319 |         "for_loop": "for ( <init> ; <condition> ; <increment> ) { <statement_list> } | for ( <init> ; <condition> ; ) { <statement_list>",
320 |         "init": "<var_decl> | <var_ass> | ?",
321 |         "increment": "<var_decl> | <var_ass> | <identifier><unary>",
322 |         "unary": "++ | --"
323 |       },
324 |       "franco_while": {
325 |         "while_loop": "talama <condition> {<statement_list>}",
326 |         "talama": "talama | talma | tlma"
327 |       },
328 |       "english_while": {
329 |         "while_loop": "<while> (<condition>) {<statement_list>}",
330 |         "while": "while | loop"
331 |       },
332 |       "loop_control": "w2f | break"
333 |     },
334 |     "statements": {
335 |       "statement_list": "<statement> | <statement> <statement_list>",
336 |       "statement": "<var_decl> | <console_output> | <return_stmt> | <expression> | <loop_control>"
337 |     },
338 |     "imports": {
339 |       "import_stmt": "<import> <string>",
340 |       "import": "geep | geeb | import"
341 |     },
342 |     "comments": {
343 |       "comment": "<single_line_comment> | <multi_line_comment>",
344 |       "single_line_comment": "#<any_text> | //<any_text>",
345 |       "multi_line_comment": "''' <any_text> ''' | /*<any_text>*/",
346 |       "any_text": ".*"
347 |     }
348 |   },
349 |   "tokens": [
350 |     {
351 |       "type": "FUN",
352 |       "patterns": [
353 |         "fun",
354 |         "sndo2",
355 |         "sando2",
356 |         "fn",
357 |         "function"
358 |       ],
359 |       "description": "Function keywords"
360 |     },
361 |     {
362 |       "type": "PRINT",
363 |       "patterns": [
364 |         "etb3",
365 |         "out",
366 |         "output",
367 |         "print",
368 |         "printf",
369 |         "cout"
370 |       ],
371 |       "description": "Print statement keywords"
372 |     },
373 |     {
374 |       "type": "INPUT",
375 |       "patterns": [
376 |         "scan",
377 |         "read",
378 |         "input",
379 |         "da5l",
380 |         "da5al",
381 |         "d5l"
382 |       ],
383 |       "description": "Input/scan keywords"
384 |     },
385 |     {
386 |       "type": "IF",
387 |       "patterns": [
388 |         "if",
389 |         "cond",
390 |         "lw"
391 |       ],
392 |       "description": "If statement keywords"
393 |     },
394 |     {
395 |       "type": "ELIF",
396 |       "patterns": [
397 |         "elif",
398 |         "aw"
399 |       ],
400 |       "description": "Elif statement keywords"
401 |     },
402 |     {
403 |       "type": "ELSE",
404 |       "patterns": [
405 |         "else",
406 |         "otherwise",
407 |         "gher"
408 |       ],
409 |       "description": "Else statement keywords"
410 |     },
411 |     {
412 |       "type": "WHILE",
413 |       "patterns": [
414 |         "while",
415 |         "loop",
416 |         "talama",
417 |         "talma",
418 |         "tlma"
419 |       ],
420 |       "description": "While loop keywords"
421 |     },
422 |     {
423 |       "type": "FOR",
424 |       "patterns": [
425 |         "for",
426 |         "karr",
427 |         "krr",
428 |         "karar"
429 |       ],
430 |       "description": "For loop keywords"
431 |     },
432 |     {
433 |       "type": "UNTIL",
434 |       "patterns": [
435 |         "l7d"
436 |       ],
437 |       "description": "Until keyword for Franco loops"
438 |     },
439 |     {
440 |       "type": "RETURN",
441 |       "patterns": [
442 |         "return",
443 |         "rg3",
444 |         "raga3"
445 |       ],
446 |       "description": "Return statement keywords"
447 |     },
448 |     {
449 |       "type": "BREAK",
450 |       "patterns": [
451 |         "break",
452 |         "stop",
453 |         "w2f",
454 |         "wa2af"
455 |       ],
456 |       "description": "Break statement keywords"
457 |     },
458 |     {
459 |       "type": "INT",
460 |       "patterns": [
461 |         "int",
462 |         "rakm"
463 |       ],
464 |       "description": "Integer type keywords"
465 |     },
466 |     {
467 |       "type": "FLOAT",
468 |       "patterns": [
469 |         "float",
470 |         "kasr",
471 |         "ksr"
472 |       ],
473 |       "description": "Float type keywords"
474 |     },
475 |     {
476 |       "type": "BOOL",
477 |       "patterns": [
478 |         "bool",
479 |         "so2al",
480 |         "s2al",
481 |         "so2l"
482 |       ],
483 |       "description": "Boolean type keywords"
484 |     },
485 |     {
486 |       "type": "STRING",
487 |       "patterns": [
488 |         "string",
489 |         "klma",
490 |         "kalma"
491 |       ],
492 |       "description": "String type keywords"
493 |     },
494 |     {
495 |       "type": "LIST",
496 |       "patterns": [
497 |         "list",
498 |         "dorg",
499 |         "drg"
500 |       ],
501 |       "description": "List type keywords"
502 |     },
503 |     {
504 |       "type": "TRUE",
505 |       "patterns": [
506 |         "true",
507 |         "True",
508 |         "TRUE",
509 |         "sa7",
510 |         "s7",
511 |         "sah",
512 |         "saa7"
513 |       ],
514 |       "description": "Boolean true values"
515 |     },
516 |     {
517 |       "type": "FALSE",
518 |       "patterns": [
519 |         "false",
520 |         "False",
521 |         "FALSE",
522 |         "ghalt",
523 |         "ghlt",
524 |         "ghalat"
525 |       ],
526 |       "description": "Boolean false values"
527 |     },
528 |     {
529 |       "type": "IMPORT",
530 |       "patterns": [
531 |         "geep",
532 |         "geeb",
533 |         "import"
534 |       ],
535 |       "description": "Import statement keywords"
536 |     },
537 |     {
538 |       "type": "LIST_METHODS",
539 |       "patterns": [
540 |         ".append",
541 |         ".push",
542 |         ".pop",
543 |         ".remove",
544 |         ".delete"
545 |       ],
546 |       "description": "List manipulation methods"
547 |     },
548 |     {
549 |       "type": "MOD",
550 |       "patterns": [
551 |         "%"
552 |       ],
553 |       "description": "Modulo operator for remainder calculations"
554 |     }
555 |   ],
556 |   "syntax_rules": {
557 |     "variable_declaration": {
558 |       "examples": [
559 |         "rakm x = 10",
560 |         "int y = 5",
561 |         "kasr pi = 3.14",
562 |         "float radius = 3",
563 |         "so2al isActive = sa7",
564 |         "bool isComplete = false",
565 |         "klma message = \"Hello\"",
566 |         "string text = \"World\"",
567 |         "dorg myList = [1, 2, 3]",
568 |         "list numbers = [1, 2, 3, 4]"
569 |       ],
570 |       "multi_declaration": [
571 |         "int v1, v2, v3",
572 |         "rakm f1, f2, f3",
573 |         "string v4=\"hello\", v5=\"world\", v6"
574 |       ]
575 |     },
576 |     "functions": {
577 |       "definition": [
578 |         "fun functionName(param1, param2) { }",
579 |         "sndo2 functionName(rakm a, rakm b) { rg3 a + b }"
580 |       ],
581 |       "examples": [
582 |         "fun add(rakm a, rakm b) { rg3 a + b }",
583 |         "sndo2 greet() { etb3(\"Hello, Flex!\") }",
584 |         "function multiply(int x, int y) { return x * y }"
585 |       ]
586 |     },
587 |     "conditionals": {
588 |       "franco_syntax": [
589 |         "lw condition { }",
590 |         "aw condition { }",
591 |         "gher { }"
592 |       ],
593 |       "english_syntax": [
594 |         "if (condition) { }",
595 |         "elif (condition) { }",
596 |         "else { }"
597 |       ],
598 |       "examples": [
599 |         "lw x > 5 { etb3(\"Greater than 5\") }",
600 |         "if (x == 5) { print(\"Equal to 5\") }",
601 |         "lw x > 5 { etb3(\"x > 5\") } aw x == 5 { etb3(\"x = 5\") } gher { etb3(\"x < 5\") }"
602 |       ]
603 |     },
604 |     "loops": {
605 |       "while_loops": [
606 |         "talama condition { }",
607 |         "while (condition) { }",
608 |         "loop (condition) { }"
609 |       ],
610 |       "for_loops": [
611 |         "karr l7d 10 { }",
612 |         "karr x=1 l7d 5 { }",
613 |         "karr x l7d 10 { }",
614 |         "for(i=0; i<10; i++) { }"
615 |       ],
616 |       "CRITICAL_NOTE": "⚠️ DANGER: Franco loops with l7d are INCLUSIVE. karr i=0 l7d 5 means i=0,1,2,3,4,5 (6 iterations). For array access use: karr i=0 l7d length(array) - 1",
617 |       "SAFETY_WARNING": "🚨 CRITICAL SAFETY ISSUE: Franco l7d loops are INCLUSIVE and WILL cause out-of-bounds errors if not handled correctly. This is the #1 source of runtime errors in Flex. ALWAYS use 'length(array) - 1' when accessing array elements in Franco loops.",
618 |       "examples": [
619 |         "talama x < 10 { etb3(x); x++ }",
620 |         "karr l7d 5 { etb3(\"Hello\") }",
621 |         "for(i=0; i<5; i++) { print(i) }"
622 |       ],
623 |       "safe_array_iteration": [
624 |         "# 🚨 WRONG: Out of bounds access - INDEX CAN REACH ARRAY LENGTH!",
625 |         "# karr i=0 l7d length(items) { print(items[i]) }  # DANGEROUS: i reaches length(items), causing out-of-bounds access!",
626 |         "",
627 |         "# ✅ CORRECT: Safe array access - MUST use length(items) - 1",
628 |         "karr i=0 l7d length(items) - 1 { print(items[i]) }  # SAFE: i stops at length(items)-1, preventing out-of-bounds",
629 |         "",
630 |         "# ✅ Alternative: English style (also safe)",
631 |         "for(i=0; i<length(items); i++) { print(items[i]) }  # SAFE: i < length(items) prevents out-of-bounds",
632 |         "",
633 |         "# 🔄 Memory of this pattern:",
634 |         "# Franco l7d = INCLUSIVE boundary (includes the end value)",
635 |         "# English < = EXCLUSIVE boundary (stops before end value)",
636 |         "# When in doubt, use English loops for arrays!"
637 |       ]
638 |     },
639 |     "file_operations": {
640 |       "description": "File I/O operations with Franco Arabic keywords",
641 |       "keywords": {
642 |         "read_file": [
643 |           "readFile",
644 |           "2ra2File",
645 |           "qra2File"
646 |         ],
647 |         "write_file": [
648 |           "writeFile",
649 |           "katbFile",
650 |           "iktbFile"
651 |         ],
652 |         "append_file": [
653 |           "appendFile",
654 |           "zydFile",
655 |           "zayedFile"
656 |         ],
657 |         "file_exists": [
658 |           "fileExists",
659 |           "fileM3jod",
660 |           "mlafM3jod"
661 |         ],
662 |         "delete_file": [
663 |           "deleteFile",
664 |           "m7yFile",
665 |           "m7iFile"
666 |         ]
667 |       },
668 |       "examples": [
669 |         "# Read file content",
670 |         "lw fileExists(\"data.txt\") {",
671 |         "  content = readFile(\"data.txt\")",
672 |         "  print(content)",
673 |         "} gher {",
674 |         "  print(\"File not found\")",
675 |         "}",
676 |         "",
677 |         "# Write to file (Franco style)",
678 |         "text = \"Hello from Flex!\"",
679 |         "katbFile(\"output.txt\", text)",
680 |         "",
681 |         "# Append to file",
682 |         "zydFile(\"log.txt\", \"New entry: {getCurrentTime()}\")",
683 |         "",
684 |         "# Safe file operations with error handling",
685 |         "sndo2 safeFileRead(klma filename) {",
686 |         "  lw fileM3jod(filename) {",
687 |         "    rg3 qra2File(filename)",
688 |         "  } gher {",
689 |         "    print(\"Error: File {filename} not found\")",
690 |         "    rg3 \"\"",
691 |         "  }",
692 |         "}"
693 |       ]
694 |     },
695 |     "module_system": {
696 |       "description": "Enhanced import system with Franco Arabic support",
697 |       "import_types": {
698 |         "local_modules": "geeb \"./myModule.flex\"",
699 |         "system_modules": "import \"system/math\"",
700 |         "franco_imports": "geep \"./franco_module.lx\""
701 |       },
702 |       "advanced_imports": [
703 |         "# Import specific functions",
704 |         "geeb { calculateArea, getVolume } \"./geometry.flex\"",
705 |         "",
706 |         "# Import with alias (Franco style)",
707 |         "geep math ka \"./math_utils.lx\"",
708 |         "result = math.sqrt(16)",
709 |         "",
710 |         "# Conditional imports",
711 |         "lw systemType() == \"windows\" {",
712 |         "  geeb \"./windows_utils.flex\"",
713 |         "} gher {",
714 |         "  import \"./unix_utils.flex\"",
715 |         "}"
716 |       ]
717 |     },
718 |     "input_output": {
719 |       "print": [
720 |         "etb3(\"text\")",
721 |         "print(\"text\")",
722 |         "out(\"text\")",
723 |         "output(\"text\")"
724 |       ],
725 |       "input": [
726 |         "x = da5l()",
727 |         "y = scan()",
728 |         "z = input()",
729 |         "name = read()"
730 |       ],
731 |       "formatted_print": [
732 |         "etb3(\"Value is {x}\")",
733 |         "print(\"x={x} and y={y}\")"
734 |       ]
735 |     },
736 |     "lists": {
737 |       "declaration": [
738 |         "dorg myList = [1, 2, 3]",
739 |         "list numbers = [1, 2.5, \"text\", true]"
740 |       ],
741 |       "operations": [
742 |         "myList.push(4)",
743 |         "myList.pop()",
744 |         "myList.remove(value)",
745 |         "myList[0] = newValue",
746 |         "element = myList[index]"
747 |       ]
748 |     }
749 |   },
750 |   "code_examples": {
751 |     "hello_world": {
752 |       "description": "Basic output in Flex using both Franco Arabic (etb3) and English (print) syntax",
753 |       "explanation": "Demonstrates the fundamental way to display text in Flex. Both syntaxes work interchangeably.",
754 |       "code": [
755 |         "# Franco Arabic syntax for output",
756 |         "etb3(\"Hello, Flex!\")",
757 |         "",
758 |         "# English syntax for output",
759 |         "print(\"Hello, World!\")",
760 |         "",
761 |         "# Both produce the same result - text output to console"
762 |       ]
763 |     },
764 |     "mixed_syntax_conditional": {
765 |       "description": "Franco Arabic conditional statements with string interpolation and logical operators",
766 |       "explanation": "Shows how to use Franco Arabic keywords (lw/aw/gher) for if/elif/else logic with complex conditions and formatted output",
767 |       "concepts": [
768 |         "Franco conditionals",
769 |         "logical operators",
770 |         "string interpolation",
771 |         "nested conditions"
772 |       ],
773 |       "code": [
774 |         "# Initialize variables for demonstration",
775 |         "x = 5",
776 |         "y = 3",
777 |         "z = 0",
778 |         "",
779 |         "# Franco conditional: lw (if) with logical AND",
780 |         "lw x < 10 and y < 1 {",
781 |         "  print(x)      # Simple variable output",
782 |         "  print(y)",
783 |         "}",
784 |         "",
785 |         "# Franco elif: aw with string interpolation",
786 |         "aw y < 2 {",
787 |         "  print(\"y is {y}\")    # String interpolation with {variable}",
788 |         "}",
789 |         "",
790 |         "# Another aw condition with expression interpolation",
791 |         "aw y < 4 {",
792 |         "  print(\"x + y are {x+y}\")   # Expression inside string",
793 |         "}",
794 |         "",
795 |         "# Franco else: gher (no condition needed)",
796 |         "gher {",
797 |         "  print(\"x is {x}\")",
798 |         "}",
799 |         "",
800 |         "# Note: No semicolons required in Flex",
801 |         "# Curly braces {} define code blocks"
802 |       ]
803 |     },
804 |     "franco_loops": {
805 |       "description": "Franco Arabic loop constructs: karr l7d (for) and talama (while) loops",
806 |       "explanation": "Demonstrates Franco loop syntax with different patterns and increment operators",
807 |       "concepts": [
808 |         "Franco for loops",
809 |         "Franco while loops",
810 |         "loop counters",
811 |         "increment operators",
812 |         "loop conditions"
813 |       ],
814 |       "code": [
815 |         "# Franco for loops using 'karr l7d' syntax",
816 |         "# Pattern 1: Simple count loop (0 to 10)",
817 |         "karr l7d 10 {",
818 |         "  print(\"Hello 10 times\")",
819 |         "}",
820 |         "",
821 |         "# Pattern 2: Loop with initial value (7 down to -7)",
822 |         "karr d=7 l7d -7 {",
823 |         "  print(d)    # Prints: 7, 6, 5, 4, 3, 2, 1, 0, -1, -2, -3, -4, -5, -6, -7",
824 |         "}",
825 |         "",
826 |         "# Pattern 3: Loop with existing variable (x must be declared above)",
827 |         "x = 0  # Variable must be initialized first",
828 |         "karr x l7d 8 {",
829 |         "  print(\"Loop iteration {x}\")",
830 |         "}",
831 |         "",
832 |         "# Franco while loops using 'talama' (meaning 'as long as')",
833 |         "z = 0  # Initialize counter",
834 |         "talama z < 5 {",
835 |         "  print(z)",
836 |         "  z++    # Increment operator (also can use z = z + 1)",
837 |         "}",
838 |         "",
839 |         "# Complex while loop with multiple conditions",
840 |         "y = 0",
841 |         "z = 0",
842 |         "talama y < 5 and z < 10 {",
843 |         "  print(\"y and z are {y} {z}\")   # String interpolation",
844 |         "  y++    # Franco increment",
845 |         "  z++    # Both variables increment each iteration",
846 |         "}",
847 |         "",
848 |         "# Key Franco loop keywords:",
849 |         "# karr = for loop",
850 |         "# l7d = until/to (loop boundary)",
851 |         "# talama = while (as long as)"
852 |       ]
853 |     },
854 |     "complex_function": {
855 |       "description": "Comprehensive function example showing mixed syntax, local variables, user input, loops, and conditionals",
856 |       "explanation": "Demonstrates a real-world function with multiple parameters, local variables, user interaction, nested control structures, and various return scenarios",
857 |       "concepts": [
858 |         "function definition",
859 |         "parameter passing",
860 |         "local variables",
861 |         "user input",
862 |         "nested loops",
863 |         "conditional returns",
864 |         "list manipulation",
865 |         "variable scope"
866 |       ],
867 |       "code": [
868 |         "# Complex function with multiple parameters and mixed functionality",
869 |         "fun greet(int x, list arr) {",
870 |         "  # Function parameter usage",
871 |         "  print(x)              # Print the integer parameter",
872 |         "  ",
873 |         "  # Local variable declaration",
874 |         "  test_var = 333        # Auto-typed local variable",
875 |         "  ",
876 |         "  # Loop through list parameter",
877 |         "  for(i=0; i<4; i++) {",
878 |         "    print(\"list element {i} is {arr[i]}\")  # Access list elements",
879 |         "  }",
880 |         "  ",
881 |         "  # Modify list parameter (affects original list)",
882 |         "  arr[0] = 990",
883 |         "  print(\"Hello, World!\")",
884 |         "  ",
885 |         "  # Local variable with explicit type",
886 |         "  int varr = 87",
887 |         "  ",
888 |         "  # User input interaction",
889 |         "  print(\"enter vall\")",
890 |         "  int val = scan()      # Read user input as integer",
891 |         "  print(\"val is {val}\")",
892 |         "  ",
893 |         "  # Modify parameter (local scope)",
894 |         "  x = 5",
895 |         "  ",
896 |         "  # Conditional returns - early exit patterns",
897 |         "  if (x > 8) {",
898 |         "    return 88         # Return integer if condition met",
899 |         "  }",
900 |         "  elif (1 > 2) {        # This will never execute",
901 |         "    return 99",
902 |         "  }",
903 |         "  ",
904 |         "  # Nested loop with break control",
905 |         "  for(i=0; i<10; i++) {",
906 |         "    print(i)",
907 |         "    if (i == 7) {",
908 |         "      break         # Exit loop when i reaches 7",
909 |         "    }",
910 |         "  }",
911 |         "  ",
912 |         "  # Mathematical operations",
913 |         "  bhjb = varr + 7       # Local calculation",
914 |         "  print(bhjb + 8 + 9 - 8)  # Complex expression: 87+7+8+9-8 = 103",
915 |         "  ",
916 |         "  # Another local variable",
917 |         "  y = 5",
918 |         "  ",
919 |         "  # Return boolean value",
920 |         "  return true           # Function can return different types",
921 |         "}",
922 |         "",
923 |         "# Function usage example:",
924 |         "# myList = [1, 2, 3, 4]",
925 |         "# result = greet(42, myList)",
926 |         "# Note: myList[0] will be 990 after function call"
927 |       ]
928 |     },
929 |     "list_operations": {
930 |       "description": "Comprehensive list manipulation: creation, methods, indexing, mixed data types, and dynamic modification",
931 |       "explanation": "Shows all major list operations including push/pop, element access, modification, and using lists with different data types",
932 |       "concepts": [
933 |         "list creation",
934 |         "list methods",
935 |         "indexing",
936 |         "mixed data types",
937 |         "list modification",
938 |         "mathematical operations with lists"
939 |       ],
940 |       "code": [
941 |         "# Create and initialize a list with integers",
942 |         "list xx = [6, 2, 3, 4]",
943 |         "print(xx)                    # Output: [6, 2, 3, 4]",
944 |         "",
945 |         "# Adding elements to the list",
946 |         "xx.push(23)                  # Add integer to end",
947 |         "xx.push(\"worddd\")            # Add string to end (mixed types allowed)",
948 |         "print(xx)                    # Output: [6, 2, 3, 4, 23, \"worddd\"]",
949 |         "",
950 |         "# Removing elements from the list",
951 |         "xx.pop()                     # Remove last element",
952 |         "print(xx)                    # Output: [6, 2, 3, 4, 23]",
953 |         "",
954 |         "xx.remove(3)                 # Remove element with value 3",
955 |         "print(xx)                    # Output: [6, 2, 4, 23]",
956 |         "",
957 |         "# Working with multiple lists",
958 |         "list qq = [12, 22, 34]",
959 |         "",
960 |         "# List element access and mathematical operations",
961 |         "print(\"x0+q1={xx[0]+qq[1]}\")  # String interpolation with calculation",
962 |         "print(xx[0] + qq[1])         # Direct calculation: 6 + 22 = 28",
963 |         "",
964 |         "# Variables from list calculations",
965 |         "int no = xx[0] * xx[1]       # no = 6 * 2 = 12",
966 |         "ew = xx[0] * xx[1]           # ew = 6 * 2 = 12 (auto-typed)",
967 |         "print(no - ew)               # Output: 0 (12 - 12)",
968 |         "print(\"no is {no}\")          # Output: \"no is 12\"",
969 |         "",
970 |         "# Conditional logic with list elements",
971 |         "if (xx[0] < xx[1]) {         # Compare first two elements",
972 |         "  print(\"x0 is smaller\")",
973 |         "} else {",
974 |         "  print(\"x0 is larger or equal\")  # Will execute: 6 > 2",
975 |         "}",
976 |         "",
977 |         "# Dynamic list modification",
978 |         "xx[0] = 9 * 2                # Set first element to 18",
979 |         "",
980 |         "# Using list element as loop boundary",
981 |         "for(i=0; i<xx[0]; i++) {     # Loop from 0 to 17 (xx[0] = 18)",
982 |         "  if (i < 3) {             # Only show first 3 iterations",
983 |         "    print(\"Iteration {i}\")",
984 |         "  }",
985 |         "}",
986 |         "",
987 |         "# Mixed data type assignments",
988 |         "xx[2] = \"sdfsdf\"             # String at index 2",
989 |         "print(\"Enter a value:\")",
990 |         "xx[3] = scan()               # User input at index 3",
991 |         "",
992 |         "# String variable assignment",
993 |         "u = \"sdfsdfsd\"",
994 |         "xx[0] = u                    # Replace index 0 with string",
995 |         "",
996 |         "# Final list state",
997 |         "print(xx)                    # Mixed data types: [string, int, string, user_input]",
998 |         "print(xx[2])                 # Access specific element: \"sdfsdf\"",
999 |         "",
1000 |         "# Key points:",
1001 |         "# - Lists can contain mixed data types (int, string, bool, etc.)",
1002 |         "# - Index starts at 0",
1003 |         "# - Lists are mutable (can be modified after creation)",
1004 |         "# - List elements can be used in mathematical operations"
1005 |       ]
1006 |     },
1007 |     "nested_loops": {
1008 |       "description": "Nested loop structures with break statements and conditional control flow",
1009 |       "explanation": "Demonstrates how to create loops within loops, with proper break statements for early termination",
1010 |       "concepts": [
1011 |         "nested loops",
1012 |         "loop control",
1013 |         "break statements",
1014 |         "conditional exits",
1015 |         "loop variables"
1016 |       ],
1017 |       "code": [
1018 |         "# Nested loop example - outer loop controls inner loop boundary",
1019 |         "for (i = 1; i <= 9; i=i+1) {",
1020 |         "  etb3(\"Outer loop: i is {i}\")",
1021 |         "  ",
1022 |         "  # Inner loop runs from 0 to current value of i",
1023 |         "  for (k = 0; k <= i; k=k+1) {",
1024 |         "    etb3(\"  Inner loop: k is {k}\")  # Indented for clarity",
1025 |         "    ",
1026 |         "    # Safety break (prevents infinite loop if k somehow reaches 90)",
1027 |         "    if(k == 90) {",
1028 |         "      break                    # Exit inner loop only",
1029 |         "    }",
1030 |         "  }",
1031 |         "  ",
1032 |         "  # Safety break for outer loop",
1033 |         "  if(i == 90) {",
1034 |         "    break                        # Exit outer loop",
1035 |         "  }",
1036 |         "}",
1037 |         "",
1038 |         "# Example output pattern:",
1039 |         "# Outer loop: i is 1",
1040 |         "#   Inner loop: k is 0",
1041 |         "#   Inner loop: k is 1",
1042 |         "# Outer loop: i is 2",
1043 |         "#   Inner loop: k is 0",
1044 |         "#   Inner loop: k is 1",
1045 |         "#   Inner loop: k is 2",
1046 |         "# ... and so on",
1047 |         "",
1048 |         "# Key concepts:",
1049 |         "# - Inner loop boundary depends on outer loop variable",
1050 |         "# - Break statements only affect the immediate loop",
1051 |         "# - Each loop maintains its own counter variable",
1052 |         "# - Safety conditions prevent runaway loops"
1053 |       ]
1054 |     },
1055 |     "franco_mixed_example": {
1056 |       "description": "Mixed Franco Arabic and English syntax in a single program",
1057 |       "explanation": "Shows how Franco Arabic keywords can be seamlessly mixed with English syntax within the same codebase",
1058 |       "concepts": [
1059 |         "Franco variables",
1060 |         "mixed syntax",
1061 |         "Franco functions",
1062 |         "Franco input",
1063 |         "syntax flexibility"
1064 |       ],
1065 |       "code": [
1066 |         "# Franco Arabic variable declarations",
1067 |         "rakm x = 546456              # rakm = int (Franco)",
1068 |         "print(x)                     # English print function",
1069 |         "",
1070 |         "dorg o = [\"sfsdf\", 23, true] # dorg = list (Franco)",
1071 |         "print(o[1])                  # Access element: prints 23",
1072 |         "",
1073 |         "# Franco Arabic input",
1074 |         "print(\"Enter something:\")",
1075 |         "u = da5l()                   # da5l = input (Franco)",
1076 |         "print(u)                     # Echo user input",
1077 |         "",
1078 |         "# Franco Arabic function definition",
1079 |         "sndo2 tms(int q, int w) {    # sndo2 = function (Franco)",
1080 |         "  if(w > 3) {              # English conditional syntax",
1081 |         "    print(\"w is greater than 3\")",
1082 |         "  }",
1083 |         "  rg3 66                   # rg3 = return (Franco)",
1084 |         "}",
1085 |         "",
1086 |         "# Function call and result",
1087 |         "r = tms(4, 6)                # Call Franco function",
1088 |         "print(r)                     # Prints: 66",
1089 |         "",
1090 |         "# English syntax list declaration",
1091 |         "list b = [2, 3, 4, 5, 6]     # list = English keyword",
1092 |         "etb3(b)                      # etb3 = print (Franco)",
1093 |         "",
1094 |         "# Key Franco Arabic keywords used:",
1095 |         "# rakm = int (integer)",
1096 |         "# dorg = list",
1097 |         "# da5l = input/scan",
1098 |         "# sndo2 = function",
1099 |         "# rg3 = return",
1100 |         "# etb3 = print/output",
1101 |         "",
1102 |         "# This demonstrates Flex's flexibility:",
1103 |         "# - Mix Franco and English freely",
1104 |         "# - No syntax conflicts",
1105 |         "# - Choose preferred keywords per context"
1106 |       ]
1107 |     },
1108 |     "mathematical_expressions": {
1109 |       "description": "Mathematical operations, operator precedence, and function-based calculations",
1110 |       "explanation": "Demonstrates arithmetic operations, operator precedence, function parameters, and complex mathematical expressions",
1111 |       "concepts": [
1112 |         "arithmetic operations",
1113 |         "operator precedence",
1114 |         "function parameters",
1115 |         "mathematical functions",
1116 |         "expression evaluation"
1117 |       ],
1118 |       "code": [
1119 |         "# Initialize variables for calculations",
1120 |         "x = 10",
1121 |         "y = 1",
1122 |         "",
1123 |         "# Mathematical function with multiple parameters",
1124 |         "fun add(int x, int y, int u) {",
1125 |         "  r = x                    # Local variable assignment",
1126 |         "  print(r)                 # Print first parameter",
1127 |         "  return x + y + u         # Sum of all three parameters",
1128 |         "}",
1129 |         "",
1130 |         "# Function calls with different parameter combinations",
1131 |         "result = add(x, y, 8)        # add(10, 1, 8) = 19",
1132 |         "print(result)                # Prints: 19",
1133 |         "",
1134 |         "result = add(1, 5, x)        # add(1, 5, 10) = 16",
1135 |         "print(result)                # Prints: 16",
1136 |         "",
1137 |         "# Complex arithmetic with operator precedence",
1138 |         "x = (x + 2) * 5              # (10 + 2) * 5 = 60",
1139 |         "print(x)                     # Prints: 60",
1140 |         "",
1141 |         "# Multiple operations in sequence",
1142 |         "b = 5 * 4 / 5 * y            # Left-to-right: ((5*4)/5)*1 = 4",
1143 |         "print(\"{b}\")                 # String interpolation: \"4\"",
1144 |         "",
1145 |         "# Negative numbers and parentheses",
1146 |         "u = 3 * (-2 - 2)             # 3 * (-4) = -12",
1147 |         "print(u)                     # Prints: -12",
1148 |         "",
1149 |         "# More complex expressions",
1150 |         "complex = (x + y) * 2 - u    # (60 + 1) * 2 - (-12) = 122 + 12 = 134",
1151 |         "print(\"Complex result: {complex}\")",
1152 |         "",
1153 |         "# Modulo operator demonstrations",
1154 |         "a = 15",
1155 |         "b = 4",
1156 |         "remainder = a % b             # 15 % 4 = 3",
1157 |         "print(\"15 % 4 = {remainder}\")",
1158 |         "",
1159 |         "# Even/odd detection using modulo",
1160 |         "number = 8",
1161 |         "if (number % 2 == 0) {",
1162 |         "  print(\"{number} is even\")",
1163 |         "} else {",
1164 |         "  print(\"{number} is odd\")",
1165 |         "}",
1166 |         "",
1167 |         "# Modulo with operator precedence",
1168 |         "result = 5 + 10 % 3          # Modulo first: 5 + (10 % 3) = 5 + 1 = 6",
1169 |         "print(\"5 + 10 % 3 = {result}\")",
1170 |         "",
1171 |         "# Modulo in complex expressions",
1172 |         "cycle = (a + b) % 7          # (15 + 4) % 7 = 19 % 7 = 5",
1173 |         "print(\"Cycle value: {cycle}\")",
1174 |         "",
1175 |         "# Negative numbers with modulo",
1176 |         "neg_result = -10 % 3         # Result depends on implementation: typically -1",
1177 |         "print(\"-10 % 3 = {neg_result}\")",
1178 |         "",
1179 |         "# Operator precedence in Flex:",
1180 |         "# 1. Parentheses ()",
1181 |         "# 2. Multiplication *, Division /, Modulo %",
1182 |         "# 3. Addition +, Subtraction -",
1183 |         "# 4. Left-to-right for same precedence",
1184 |         "",
1185 |         "# Mathematical operators available:",
1186 |         "# + (addition), - (subtraction)",
1187 |         "# * (multiplication), / (division), % (modulo)",
1188 |         "# ++ (increment), -- (decrement)"
1189 |       ]
1190 |     },
1191 |     "string_formatting": {
1192 |       "description": "String interpolation and mixed output function usage across different syntax styles",
1193 |       "explanation": "Shows how to embed variables and expressions within strings using {variable} syntax, and demonstrates multiple output functions",
1194 |       "concepts": [
1195 |         "string interpolation",
1196 |         "mixed output functions",
1197 |         "variable embedding",
1198 |         "expression formatting"
1199 |       ],
1200 |       "code": [
1201 |         "# Variables of different types for demonstration",
1202 |         "float y = 5.555              # Floating-point number",
1203 |         "bool t = false               # Boolean value",
1204 |         "x = 42                       # Integer (for context)",
1205 |         "",
1206 |         "# String interpolation with different data types",
1207 |         "etb3(\"x = {x}\")              # Integer interpolation",
1208 |         "etb3(\"y = {y}\")              # Float interpolation - prints: \"y = 5.555\"",
1209 |         "etb3(\"t is {t}\")             # Boolean interpolation - prints: \"t is false\"",
1210 |         "",
1211 |         "# Expression interpolation",
1212 |         "x = 10 - 2                   # Calculate new value: x = 8",
1213 |         "etb3(\"New x = {x}\")          # Expression result interpolation",
1214 |         "",
1215 |         "# Complex expression interpolation",
1216 |         "etb3(\"Calculation: {x + y}\") # Embed calculation: 8 + 5.555 = 13.555",
1217 |         "etb3(\"Boolean negation: {not t}\")  # Embed boolean operation",
1218 |         "",
1219 |         "# Mixed output functions - all equivalent functionality",
1220 |         "etb3(\"Franco print\")         # Franco Arabic print function",
1221 |         "print(\"English print\")       # English print function",
1222 |         "out(\"Alternative output\")    # Alternative output function",
1223 |         "output(\"Another option\")     # Another output variant",
1224 |         "printf(\"C-style output\")     # C-style printf",
1225 |         "cout(\"Stream-style output\")  # Stream-style output",
1226 |         "",
1227 |         "# Advanced string interpolation examples",
1228 |         "name = \"Flex\"",
1229 |         "version = 2.0",
1230 |         "etb3(\"Welcome to {name} version {version}!\")",
1231 |         "",
1232 |         "# String interpolation rules:",
1233 |         "# - Use {variable_name} to embed variables",
1234 |         "# - Can embed expressions: {a + b}",
1235 |         "# - Works with all data types",
1236 |         "# - No spaces needed around braces",
1237 |         "# - Expressions are evaluated at runtime"
1238 |       ]
1239 |     },
1240 |     "logical_operations": {
1241 |       "description": "Boolean logic with AND, OR, NOT operators and complex conditional expressions",
1242 |       "explanation": "Demonstrates logical operators, complex boolean expressions, and mixed syntax conditionals",
1243 |       "concepts": [
1244 |         "boolean operators",
1245 |         "logical AND/OR",
1246 |         "NOT operator",
1247 |         "complex conditions",
1248 |         "conditional logic"
1249 |       ],
1250 |       "code": [
1251 |         "# Initialize variables for logical tests",
1252 |         "x = 4",
1253 |         "y = 5",
1254 |         "z = 6",
1255 |         "",
1256 |         "# Complex AND condition with NOT operator",
1257 |         "if (x == 4 and y == 5 and not(z > 1)) {",
1258 |         "  print(\"All conditions met\")     # Won't execute: z > 1 is true",
1259 |         "} else {",
1260 |         "  print(\"Complex condition failed\") # Will execute",
1261 |         "}",
1262 |         "",
1263 |         "# OR condition with NOT operator",
1264 |         "y = 50",
1265 |         "if (x == 5 or not(y < 6)) {",
1266 |         "  print(\"OR condition with NOT\")   # Will execute: not(50 < 6) is true",
1267 |         "}",
1268 |         "",
1269 |         "# Franco Arabic conditional syntax",
1270 |         "yo = 3                               # Variable for comparison",
1271 |         "lw x > yo {                          # lw = if (Franco)",
1272 |         "  print(\"Franco conditional: x > yo\") # Will execute: 4 > 3",
1273 |         "}",
1274 |         "",
1275 |         "# More complex logical examples",
1276 |         "a = true",
1277 |         "b = false",
1278 |         "",
1279 |         "# Combining boolean variables with logical operators",
1280 |         "if (a and not b) {",
1281 |         "  print(\"a is true AND b is false\")  # Will execute",
1282 |         "}",
1283 |         "",
1284 |         "# Multiple OR conditions",
1285 |         "if (x == 10 or y == 50 or z == 6) {",
1286 |         "  print(\"At least one condition is true\")  # Will execute: y==50 and z==6",
1287 |         "}",
1288 |         "",
1289 |         "# Nested logical expressions with parentheses",
1290 |         "if ((x > 0 and y > 0) or (z < 0)) {",
1291 |         "  print(\"Nested logic: positive x,y OR negative z\")",
1292 |         "}",
1293 |         "",
1294 |         "# Logical operators in Flex:",
1295 |         "# and  - logical AND (both conditions must be true)",
1296 |         "# or   - logical OR (at least one condition must be true)",
1297 |         "# not  - logical NOT (inverts boolean value)",
1298 |         "# ==   - equality comparison",
1299 |         "# !=   - inequality comparison",
1300 |         "# <, >, <=, >= - relational comparisons"
1301 |       ]
1302 |     },
1303 |     "input_output_patterns": {
1304 |       "description": "Comprehensive input and output methods across different syntax styles with practical examples",
1305 |       "explanation": "Shows all available input/output functions and how they can be used interchangeably in Flex programs",
1306 |       "concepts": [
1307 |         "user input",
1308 |         "multiple output methods",
1309 |         "Franco vs English syntax",
1310 |         "I/O flexibility",
1311 |         "string interpolation"
1312 |       ],
1313 |       "code": [
1314 |         "# Various input methods - all functionally equivalent",
1315 |         "print(\"Enter your name:\")    ",
1316 |         "name = da5l()                # Franco Arabic input (da5l = enter/input)",
1317 |         "",
1318 |         "print(\"Enter your age:\")",
1319 |         "age = scan()                 # English input method",
1320 |         "",
1321 |         "# Input behavior:",
1322 |         "# - If input is a number, it will be stored as a number (int or float)",
1323 |         "# - Otherwise, it will be stored as a string",
1324 |         "# - Empty input (just pressing enter) causes an error",
1325 |         "",
1326 |         "print(\"Enter some data:\")",
1327 |         "data = read()                # Alternative input method",
1328 |         "",
1329 |         "# All input methods work the same way:",
1330 |         "# - Read from console/terminal",
1331 |         "# - Return string by default",
1332 |         "# - Can be converted to numbers if needed",
1333 |         "",
1334 |         "# Various output methods - all functionally equivalent",
1335 |         "etb3(\"Franco output: {name}\")     # Franco Arabic print (etb3 = print)",
1336 |         "print(\"English output: {age}\")    # Standard English print",
1337 |         "out(\"Alternative: {value}\")       # Alternative output method",
1338 |         "output(\"Another method: {data}\")  # Another output variant",
1339 |         "printf(\"C-style: {name}\")         # C-style printf",
1340 |         "cout(\"Stream-style: {age}\")       # Stream-style output",
1341 |         "",
1342 |         "# Practical input/output example",
1343 |         "print(\"=== Calculator Example ===\")",
1344 |         "etb3(\"Enter first number:\")",
1345 |         "num1 = da5l()                # Franco input - automatic type detection",
1346 |         "print(\"Enter second number:\")",
1347 |         "num2 = scan()                # English input - automatic type detection",
1348 |         "",
1349 |         "# Flex automatically detects if input is number or string",
1350 |         "result = num1 + num2         # Works if both are numbers",
1351 |         "",
1352 |         "# Mixed syntax output with string interpolation",
1353 |         "etb3(\"You entered: {num1} and {num2}\")",
1354 |         "print(\"Sum: {result}\")",
1355 |         "print(\"Thank you for using Flex!\")",
1356 |         "",
1357 |         "# Available input functions:",
1358 |         "# da5l()  - Franco Arabic (\"da5l\" means \"enter\")",
1359 |         "# scan()  - English/technical term",
1360 |         "# input() - Standard programming term",
1361 |         "# read()  - Alternative term",
1362 |         "",
1363 |         "# Key output functions:",
1364 |         "# etb3()  - Franco Arabic (\"etb3\" means \"print\")",
1365 |         "# print() - Standard English",
1366 |         "# out()   - Short form",
1367 |         "# output() - Verbose form",
1368 |         "# printf() - C-style",
1369 |         "# cout()  - C++ style"
1370 |       ]
1371 |     },
1372 |     "break_and_control": {
1373 |       "description": "Loop control statements: Franco Arabic (w2f) and English (break) syntax for early loop termination",
1374 |       "explanation": "Demonstrates different ways to control loop execution using break statements in both Franco and English syntax",
1375 |       "concepts": [
1376 |         "loop control",
1377 |         "break statements",
1378 |         "Franco break",
1379 |         "English break",
1380 |         "loop termination"
1381 |       ],
1382 |       "code": [
1383 |         "# Franco Arabic loop with Franco break statement",
1384 |         "karr i=0 l7d 10 {            # Franco for loop: from 0 to 10",
1385 |         "  print(i)",
1386 |         "  lw i == 5 {              # Franco conditional: if i equals 5",
1387 |         "    w2f                  # Franco break: w2f = stop/break",
1388 |         "  }",
1389 |         "}",
1390 |         "# Output: 0, 1, 2, 3, 4, 5 (then exits)",
1391 |         "",
1392 |         "# English while loop with English break statement",
1393 |         "q = 0                        # Initialize counter",
1394 |         "while(q < 30) {              # English while loop",
1395 |         "  if (q == 10) {           # English conditional",
1396 |         "    break                # English break statement",
1397 |         "  }",
1398 |         "  print(\"q is {q}\")        # Print with string interpolation",
1399 |         "  q++                      # Increment counter",
1400 |         "}",
1401 |         "# Output: q is 0, q is 1, ..., q is 9 (then exits)",
1402 |         "",
1403 |         "# Mixed syntax example",
1404 |         "y = 0",
1405 |         "talama y < 20 {              # Franco while loop",
1406 |         "  etb3(\"y = {y}\")          # Franco print",
1407 |         "  if (y == 7) {            # English conditional",
1408 |         "    w2f                  # Franco break",
1409 |         "  }",
1410 |         "  y++",
1411 |         "}",
1412 |         "",
1413 |         "# Break statement equivalents:",
1414 |         "# w2f     - Franco Arabic (\"wa2af\" = stop)",
1415 |         "# break   - English/Standard",
1416 |         "# stop    - Alternative English",
1417 |         "",
1418 |         "# Key concepts:",
1419 |         "# - Break exits the current loop immediately",
1420 |         "# - Can mix Franco and English syntax freely",
1421 |         "# - Break only affects the innermost loop",
1422 |         "# - Use consistent style or mix as preferred"
1423 |       ]
1424 |     },
1425 |     "comments_examples": {
1426 |       "description": "All supported comment styles in Flex: single-line, multi-line, and inline comments",
1427 |       "explanation": "Shows the different ways to add comments to Flex code for documentation and code explanation",
1428 |       "concepts": [
1429 |         "single-line comments",
1430 |         "multi-line comments",
1431 |         "inline comments",
1432 |         "code documentation",
1433 |         "comment styles"
1434 |       ],
1435 |       "code": [
1436 |         "# Single line comment using hash symbol",
1437 |         "// Another single line comment using double slash",
1438 |         "",
1439 |         "'''",
1440 |         "Multi-line comment using triple quotes",
1441 |         "This type of comment can span",
1442 |         "multiple lines and is useful for",
1443 |         "longer explanations or documentation",
1444 |         "'''",
1445 |         "",
1446 |         "/*",
1447 |         "C-style multi-line comment",
1448 |         "Also spans multiple lines",
1449 |         "Familiar to C/C++/Java programmers",
1450 |         "*/",
1451 |         "",
1452 |         "# Comments with code examples",
1453 |         "x = 5      # Inline comment using hash",
1454 |         "y = 10     // Inline comment using double slash",
1455 |         "z = x + y  # Comments explain what the code does",
1456 |         "",
1457 |         "# Comment usage examples in real code",
1458 |         "rakm age = 25              # Franco variable declaration",
1459 |         "dorg names = [\"Ahmed\", \"Sara\"]  # Franco list with Arabic names",
1460 |         "",
1461 |         "# Function with documentation comments",
1462 |         "'''",
1463 |         "This function calculates the area of a rectangle",
1464 |         "Parameters: length (rakm), width (rakm)",
1465 |         "Returns: area (rakm)",
1466 |         "'''",
1467 |         "sndo2 calculateArea(rakm length, rakm width) {",
1468 |         "  rakm area = length * width  # Calculate area",
1469 |         "  rg3 area                    # Return result",
1470 |         "}",
1471 |         "",
1472 |         "/*",
1473 |         "Main program execution",
1474 |         "Demonstrates mixed syntax usage",
1475 |         "*/",
1476 |         "result = calculateArea(10, 5)  // Function call",
1477 |         "etb3(\"Area is: {result}\")       # Output result",
1478 |         "",
1479 |         "# Comment style guidelines:",
1480 |         "# - Use # for single-line comments (most common)",
1481 |         "# - Use // for C-style single-line comments",
1482 |         "# - Use ''' for multi-line documentation",
1483 |         "# - Use /* */ for C-style multi-line comments",
1484 |         "# - Add inline comments to explain complex logic",
1485 |         "# - Comments are ignored by the Flex interpreter"
1486 |       ]
1487 |     },
1488 |     "modulo_operations": {
1489 |       "description": "Comprehensive modulo operator usage: remainder calculations, even/odd detection, cycling, and error handling",
1490 |       "explanation": "Demonstrates the modulo operator (%) for remainder calculations, practical applications like even/odd testing, creating cycles, and proper error handling for modulo by zero",
1491 |       "concepts": [
1492 |         "modulo operator",
1493 |         "remainder calculations",
1494 |         "even/odd detection",
1495 |         "cycling patterns",
1496 |         "error handling",
1497 |         "operator precedence"
1498 |       ],
1499 |       "code": [
1500 |         "# Basic modulo operations",
1501 |         "a = 15",
1502 |         "b = 4",
1503 |         "remainder = a % b            # 15 % 4 = 3",
1504 |         "print(\"15 % 4 = {remainder}\")",
1505 |         "",
1506 |         "# Even/odd detection - most common use case",
1507 |         "numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]",
1508 |         "karr i=0 l7d length(numbers) - 1 {",
1509 |         "  number = numbers[i]",
1510 |         "  lw number % 2 == 0 {",
1511 |         "    print(\"{number} is even\")",
1512 |         "  } gher {",
1513 |         "    print(\"{number} is odd\")",
1514 |         "  }",
1515 |         "}",
1516 |         "",
1517 |         "# Creating cycling patterns with modulo",
1518 |         "print(\"\\nCycling through colors:\")",
1519 |         "colors = [\"red\", \"green\", \"blue\"]",
1520 |         "karr day=1 l7d 10 {",
1521 |         "  color_index = (day - 1) % length(colors)  # Cycle through 0, 1, 2",
1522 |         "  current_color = colors[color_index]",
1523 |         "  print(\"Day {day}: {current_color}\")",
1524 |         "}",
1525 |         "",
1526 |         "# Modulo with operator precedence",
1527 |         "result1 = 5 + 10 % 3         # Modulo first: 5 + (10 % 3) = 5 + 1 = 6",
1528 |         "result2 = (5 + 10) % 3       # Parentheses first: (15) % 3 = 0",
1529 |         "print(\"5 + 10 % 3 = {result1}\")",
1530 |         "print(\"(5 + 10) % 3 = {result2}\")",
1531 |         "",
1532 |         "# Negative numbers with modulo",
1533 |         "neg_examples = [-7, -3, 7, 3]",
1534 |         "divisor = 3",
1535 |         "print(\"\\nNegative number modulo examples:\")",
1536 |         "karr i=0 l7d length(neg_examples) - 1 {",
1537 |         "  num = neg_examples[i]",
1538 |         "  result = num % divisor",
1539 |         "  print(\"{num} % {divisor} = {result}\")",
1540 |         "}",
1541 |         "",
1542 |         "# Safe modulo operation with error handling",
1543 |         "sndo2 safeModulo(rakm dividend, rakm divisor) {",
1544 |         "  lw divisor == 0 {",
1545 |         "    print(\"Error: Cannot perform modulo by zero!\")",
1546 |         "    rg3 -1  # Return error indicator",
1547 |         "  } gher {",
1548 |         "    result = dividend % divisor",
1549 |         "    print(\"{dividend} % {divisor} = {result}\")",
1550 |         "    rg3 result",
1551 |         "  }",
1552 |         "}",
1553 |         "",
1554 |         "# Test safe modulo function",
1555 |         "print(\"\\nSafe modulo operations:\")",
1556 |         "safeModulo(10, 3)            # Valid: returns 1",
1557 |         "safeModulo(10, 0)            # Error: returns -1",
1558 |         "",
1559 |         "# Practical application: determining weekday",
1560 |         "print(\"\\nWeekday calculator:\")",
1561 |         "weekdays = [\"Sunday\", \"Monday\", \"Tuesday\", \"Wednesday\", \"Thursday\", \"Friday\", \"Saturday\"]",
1562 |         "day_number = 15              # Arbitrary day number",
1563 |         "weekday_index = day_number % 7",
1564 |         "weekday = weekdays[weekday_index]",
1565 |         "print(\"Day {day_number} falls on a {weekday}\")",
1566 |         "",
1567 |         "# Complex expression with modulo",
1568 |         "x = 25",
1569 |         "y = 7",
1570 |         "complex_result = (x * 2 + 5) % y  # (25*2+5) % 7 = 55 % 7 = 6",
1571 |         "print(\"(25 * 2 + 5) % 7 = {complex_result}\")",
1572 |         "",
1573 |         "# Key modulo use cases:",
1574 |         "# 1. Even/odd detection: number % 2 == 0",
1575 |         "# 2. Cycling through arrays: index % array_length",
1576 |         "# 3. Time calculations: hours % 12, minutes % 60",
1577 |         "# 4. Hash table indexing: hash % table_size",
1578 |         "# 5. Remainder calculations: dividend % divisor"
1579 |       ]
1580 |     }
1581 |   },
1582 |   "best_practices": {
1583 |     "file_extensions": "Use .flex or .lx file extensions",
1584 |     "syntax_mixing": "You can mix Franco Arabic and English syntax in the same file",
1585 |     "no_semicolons": "Flex does not require semicolons at the end of statements",
1586 |     "blocks": "Use {} for code blocks, no parentheses needed for Franco conditionals",
1587 |     "variable_naming": "Use descriptive variable names in any supported language",
1588 |     "comments": "Use # or // for single-line comments, ''' or /* */ for multi-line",
1589 |     "string_formatting": "Use {variable} syntax for string interpolation"
1590 |   },
1591 |   "common_patterns": {
1592 |     "input_validation": [
1593 |       "etb3(\"Enter a number:\")",
1594 |       "rakm num = da5l()",
1595 |       "lw num > 0 {",
1596 |       "  etb3(\"Positive number: {num}\")",
1597 |       "} gher {",
1598 |       "  etb3(\"Non-positive number\")",
1599 |       "}"
1600 |     ],
1601 |     "list_processing": [
1602 |       "dorg items = [1, 2, 3, 4, 5]",
1603 |       "karr i=0 l7d length(items) - 1 {",
1604 |       "  etb3(\"Item {i}: {items[i]}\")",
1605 |       "}"
1606 |     ],
1607 |     "function_with_return": [
1608 |       "sndo2 calculate(rakm x, rakm y) {",
1609 |       "  rakm result = x * y + 10",
1610 |       "  rg3 result",
1611 |       "}"
1612 |     ],
1613 |     "even_odd_detection": [
1614 |       "rakm number = 42",
1615 |       "lw number % 2 == 0 {",
1616 |       "  etb3(\"Number is even\")",
1617 |       "} gher {",
1618 |       "  etb3(\"Number is odd\")",
1619 |       "}"
1620 |     ],
1621 |     "cycling_counter": [
1622 |       "counter = 0",
1623 |       "karr i=0 l7d 10 {",
1624 |       "  cycle_value = counter % 3  # Creates 0-1-2 cycle",
1625 |       "  etb3(\"Cycle: {cycle_value}\")",
1626 |       "  counter++",
1627 |       "}"
1628 |     ],
1629 |     "modulo_safe_operation": [
1630 |       "a = 15",
1631 |       "b = 4",
1632 |       "lw b != 0 {",
1633 |       "  remainder = a % b",
1634 |       "  print(\"Remainder: {remainder}\")",
1635 |       "} gher {",
1636 |       "  print(\"Error: Cannot perform modulo by zero\")",
1637 |       "}"
1638 |     ]
1639 |   },
1640 |   "debugging_features": {
1641 |     "built_in_ai": "Flex includes built-in AI debugging capabilities",
1642 |     "error_handling": "Graceful error detection and recovery through regex parsing",
1643 |     "type_checking": "Automatic type detection and validation",
1644 |     "runtime_hints": "AI-powered suggestions during development"
1645 |   },
1646 |   "project_files": {
1647 |     "config": [
1648 |       "flex.toml",
1649 |       "flexconfig.json",
1650 |       "flex.json"
1651 |     ],
1652 |     "dependencies": [
1653 |       "Flex.lock"
1654 |     ],
1655 |     "documentation": [
1656 |       "FLEX.md",
1657 |       "flex.md",
1658 |       ".flex.md"
1659 |     ]
1660 |   },
1661 |   "error_handling": {
1662 |     "description": "Comprehensive error patterns, prevention, and handling strategies in Flex",
1663 |     "error_categories": {
1664 |       "runtime_errors": {
1665 |         "description": "Errors that occur during program execution",
1666 |         "undefined_variable": {
1667 |           "error": "Variable 'x' is not defined",
1668 |           "cause": "Attempting to use a variable before declaring it",
1669 |           "solution": "Always declare variables before use",
1670 |           "prevention_example": [
1671 |             "# WRONG: Using undefined variable",
1672 |             "# print(name)  # Error: 'name' not defined",
1673 |             "",
1674 |             "# CORRECT: Declare first",
1675 |             "klma name = \"Flex\"",
1676 |             "print(name)  # Works correctly"
1677 |           ],
1678 |           "defensive_pattern": [
1679 |             "# Initialize variables with default values",
1680 |             "klma user_name = \"\"  # Default empty string",
1681 |             "rakm user_age = 0     # Default zero",
1682 |             "so2al is_valid = ghalt # Default false"
1683 |           ]
1684 |         },
1685 |         "division_by_zero": {
1686 |           "error": "Division by zero",
1687 |           "cause": "Attempting to divide a number by zero",
1688 |           "solution": "Always check denominator before division",
1689 |           "prevention_example": [
1690 |             "# Safe division function",
1691 |             "sndo2 safeDivide(rakm a, rakm b) {",
1692 |             "  lw b == 0 {",
1693 |             "    print(\"Error: Cannot divide by zero\")",
1694 |             "    rg3 0  # Return safe default",
1695 |             "  } gher {",
1696 |             "    rg3 a / b",
1697 |             "  }",
1698 |             "}",
1699 |             "",
1700 |             "# Usage",
1701 |             "result = safeDivide(10, 2)  # Returns 5",
1702 |             "result = safeDivide(10, 0)  # Returns 0 with error message"
1703 |           ]
1704 |         },
1705 |         "modulo_by_zero": {
1706 |           "error": "Modulo by zero",
1707 |           "cause": "Attempting to get remainder when dividing by zero",
1708 |           "solution": "Check divisor before modulo operation",
1709 |           "prevention_example": [
1710 |             "# Safe modulo with validation",
1711 |             "sndo2 safeModulo(rakm dividend, rakm divisor) {",
1712 |             "  lw divisor == 0 {",
1713 |             "    etb3(\"Error: Modulo by zero not allowed\")",
1714 |             "    rg3 -1  # Error indicator",
1715 |             "  } gher {",
1716 |             "    rg3 dividend % divisor",
1717 |             "  }",
1718 |             "}",
1719 |             "",
1720 |             "# Inline modulo check",
1721 |             "a = 15",
1722 |             "b = 0",
1723 |             "lw b != 0 {",
1724 |             "  remainder = a % b",
1725 |             "  print(\"Remainder: {remainder}\")",
1726 |             "} gher {",
1727 |             "  print(\"Cannot calculate remainder with zero divisor\")",
1728 |             "}"
1729 |           ]
1730 |         },
1731 |         "index_out_of_bounds": {
1732 |           "error": "List index out of range",
1733 |           "cause": "Accessing list element at invalid index",
1734 |           "solution": "Always validate index before accessing",
1735 |           "prevention_example": [
1736 |             "# Safe list access function",
1737 |             "sndo2 safeListGet(dorg myList, rakm index) {",
1738 |             "  # Validate list is not empty",
1739 |             "  lw length(myList) == 0 {",
1740 |             "    print(\"Error: Cannot access element from empty list\")",
1741 |             "    rg3 \"\"  # Return safe default for empty list",
1742 |             "  }",
1743 |             "  ",
1744 |             "  # Validate index bounds",
1745 |             "  lw index >= 0 and index < length(myList) {",
1746 |             "    rg3 myList[index]  # Return valid element",
1747 |             "  } gher {",
1748 |             "    print(\"Error: Index {index} out of bounds for list of size {length(myList)}\")",
1749 |             "    rg3 \"\"  # Return safe default for out of bounds",
1750 |             "  }",
1751 |             "}",
1752 |             "",
1753 |             "# Inline bounds checking",
1754 |             "dorg items = [\"apple\", \"banana\", \"cherry\"]",
1755 |             "rakm user_choice = 5",
1756 |             "",
1757 |             "lw user_choice >= 0 and user_choice < length(items) {",
1758 |             "  selected = items[user_choice]",
1759 |             "  print(\"You selected: {selected}\")",
1760 |             "} gher {",
1761 |             "  print(\"Invalid choice. Please select 0-{length(items)-1}\")",
1762 |             "}"
1763 |           ]
1764 |         }
1765 |       },
1766 |       "user_input_errors": {
1767 |         "description": "Errors arising from invalid or unexpected user input",
1768 |         "invalid_number_input": {
1769 |           "error": "Expected number but received text",
1770 |           "cause": "User enters non-numeric value when number expected",
1771 |           "solution": "Validate input type and provide fallback",
1772 |           "prevention_example": [
1773 |             "# Robust number input with validation",
1774 |             "sndo2 getValidNumber(klma prompt) {",
1775 |             "  rakm attempt_count = 0",
1776 |             "  rakm max_attempts = 5  # Prevent infinite loops",
1777 |             "  ",
1778 |             "  talama attempt_count < max_attempts {",
1779 |             "    etb3(prompt)",
1780 |             "    input_value = da5l()",
1781 |             "    ",
1782 |             "    # Try to use as number - if it works, return it",
1783 |             "    lw input_value > -999999 and input_value < 999999 {",
1784 |             "      rg3 input_value  # Return valid number",
1785 |             "    } gher {",
1786 |             "      attempt_count++",
1787 |             "      print(\"Error: Please enter a valid number (Attempt {attempt_count}/{max_attempts})\")",
1788 |             "      # Continue loop for retry",
1789 |             "    }",
1790 |             "  }",
1791 |             "  ",
1792 |             "  # If max attempts reached, return safe default",
1793 |             "  print(\"Maximum attempts reached. Using default value 0.\")",
1794 |             "  rg3 0  # Return safe default after max attempts",
1795 |             "}",
1796 |             "",
1797 |             "# Usage",
1798 |             "age = getValidNumber(\"Enter your age: \")",
1799 |             "print(\"Your age is: {age}\")"
1800 |           ]
1801 |         },
1802 |         "empty_input": {
1803 |           "error": "Empty input received",
1804 |           "cause": "User presses Enter without typing anything",
1805 |           "solution": "Check for empty input and handle gracefully",
1806 |           "prevention_example": [
1807 |             "# Handle empty input gracefully",
1808 |             "sndo2 getNonEmptyInput(klma prompt) {",
1809 |             "  rakm attempt_count = 0",
1810 |             "  rakm max_attempts = 3  # Prevent infinite loops",
1811 |             "  ",
1812 |             "  talama attempt_count < max_attempts {",
1813 |             "    print(prompt)",
1814 |             "    user_input = scan()",
1815 |             "    ",
1816 |             "    lw length(user_input) > 0 {",
1817 |             "      rg3 user_input  # Return valid non-empty input",
1818 |             "    } gher {",
1819 |             "      attempt_count++",
1820 |             "      etb3(\"Error: Input cannot be empty. Please try again. (Attempt {attempt_count}/{max_attempts})\")",
1821 |             "      # Continue loop for retry",
1822 |             "    }",
1823 |             "  }",
1824 |             "  ",
1825 |             "  # If max attempts reached, return safe default",
1826 |             "  etb3(\"Maximum attempts reached. Using default value.\")",
1827 |             "  rg3 \"default\"  # Return safe default after max attempts",
1828 |             "}",
1829 |             "",
1830 |             "name = getNonEmptyInput(\"Enter your name: \")"
1831 |           ]
1832 |         },
1833 |         "choice_validation": {
1834 |           "error": "Invalid menu choice",
1835 |           "cause": "User selects option not available in menu",
1836 |           "solution": "Validate choice against available options",
1837 |           "prevention_example": [
1838 |             "# Menu with choice validation",
1839 |             "sndo2 getMenuChoice() {",
1840 |             "  dorg valid_choices = [\"1\", \"2\", \"3\", \"4\"]",
1841 |             "  rakm attempt_count = 0",
1842 |             "  rakm max_attempts = 3  # Prevent infinite loops",
1843 |             "  ",
1844 |             "  talama attempt_count < max_attempts {",
1845 |             "    etb3(\"\\n=== Menu ===\")",
1846 |             "    print(\"1. Add item\")",
1847 |             "    print(\"2. View items\")",
1848 |             "    print(\"3. Delete item\")",
1849 |             "    print(\"4. Exit\")",
1850 |             "    print(\"Enter choice (1-4): \")",
1851 |             "    ",
1852 |             "    choice = scan()",
1853 |             "    ",
1854 |             "    # Check if choice is valid",
1855 |             "    so2al is_valid = ghalt",
1856 |             "    karr i=0 l7d length(valid_choices) - 1 {",
1857 |             "      lw choice == valid_choices[i] {",
1858 |             "        is_valid = sa7",
1859 |             "        w2f",
1860 |             "      }",
1861 |             "    }",
1862 |             "    ",
1863 |             "    lw is_valid {",
1864 |             "      rg3 choice  # Return valid choice",
1865 |             "    } gher {",
1866 |             "      attempt_count++",
1867 |             "      print(\"Error: Invalid choice '{choice}'. Please select 1-4. (Attempt {attempt_count}/{max_attempts})\")",
1868 |             "      # Continue loop for retry",
1869 |             "    }",
1870 |             "  }",
1871 |             "  ",
1872 |             "  # If max attempts reached, return safe default",
1873 |             "  print(\"Maximum attempts reached. Defaulting to Exit.\")",
1874 |             "  rg3 \"4\"  # Return safe default (exit option)",
1875 |             "}",
1876 |             "",
1877 |             "user_choice = getMenuChoice()"
1878 |           ]
1879 |         }
1880 |       },
1881 |       "type_errors": {
1882 |         "description": "Errors related to incompatible data types",
1883 |         "type_mismatch": {
1884 |           "error": "Cannot perform operation between incompatible types",
1885 |           "cause": "Attempting operations on incompatible data types",
1886 |           "solution": "Ensure type compatibility or convert types",
1887 |           "prevention_example": [
1888 |             "# Type-safe operations",
1889 |             "sndo2 safeAdd(value1, value2) {",
1890 |             "  # Ensure both values are numbers",
1891 |             "  lw value1 > -999999 and value1 < 999999 and value2 > -999999 and value2 < 999999 {",
1892 |             "    rg3 value1 + value2",
1893 |             "  } gher {",
1894 |             "    print(\"Error: Both values must be numbers for addition\")",
1895 |             "    rg3 0",
1896 |             "  }",
1897 |             "}",
1898 |             "",
1899 |             "# Safe type conversion example",
1900 |             "print(\"Enter first number: \")",
1901 |             "rakm num1 = scan()  # Explicit type declaration",
1902 |             "print(\"Enter second number: \")",
1903 |             "rakm num2 = scan()  # Explicit type declaration",
1904 |             "",
1905 |             "result = num1 + num2  # Safe operation"
1906 |           ]
1907 |         },
1908 |         "string_number_confusion": {
1909 |           "error": "Mixing strings and numbers inappropriately",
1910 |           "cause": "Attempting arithmetic on strings or concatenating numbers",
1911 |           "solution": "Be explicit about data types",
1912 |           "prevention_example": [
1913 |             "# Clear type handling",
1914 |             "klma name = \"Age: \"",
1915 |             "rakm age = 25",
1916 |             "",
1917 |             "# Use string interpolation instead of mixing types",
1918 |             "message = \"{name}{age}\"  # Correct way",
1919 |             "print(message)  # Prints: \"Age: 25\"",
1920 |             "",
1921 |             "# Avoid direct operations between different types",
1922 |             "# name + age  # This could cause issues",
1923 |             "",
1924 |             "# For user input, be explicit about expected type",
1925 |             "print(\"Enter your age as a number: \")",
1926 |             "rakm user_age = da5l()  # Forces number type"
1927 |           ]
1928 |         }
1929 |       },
1930 |       "syntax_errors": {
1931 |         "description": "Errors in code structure and syntax",
1932 |         "missing_braces": {
1933 |           "error": "Missing opening or closing brace",
1934 |           "cause": "Unmatched { or } in code blocks",
1935 |           "solution": "Ensure every { has a matching }",
1936 |           "prevention_example": [
1937 |             "# WRONG: Missing closing brace",
1938 |             "# lw x > 5 {",
1939 |             "#   print(\"Greater than 5\")",
1940 |             "# # Missing }",
1941 |             "",
1942 |             "# CORRECT: Properly matched braces",
1943 |             "lw x > 5 {",
1944 |             "  print(\"Greater than 5\")",
1945 |             "}  # Closing brace matches opening",
1946 |             "",
1947 |             "# For complex nested structures, use indentation",
1948 |             "lw condition1 {",
1949 |             "  print(\"Condition 1 true\")",
1950 |             "  lw condition2 {",
1951 |             "    print(\"Condition 2 also true\")",
1952 |             "  }  # Inner closing brace",
1953 |             "}    # Outer closing brace"
1954 |           ]
1955 |         },
1956 |         "invalid_function_syntax": {
1957 |           "error": "Function definition syntax error",
1958 |           "cause": "Incorrect function declaration syntax",
1959 |           "solution": "Follow proper function syntax patterns",
1960 |           "prevention_example": [
1961 |             "# WRONG: Invalid function syntax",
1962 |             "# function name { }  # Missing parentheses",
1963 |             "# fun name(x y) { }  # Missing comma between parameters",
1964 |             "",
1965 |             "# CORRECT: Proper function syntax",
1966 |             "sndo2 myFunction() {",
1967 |             "  print(\"No parameters\")",
1968 |             "}",
1969 |             "",
1970 |             "fun calculate(rakm a, rakm b) {",
1971 |             "  rg3 a + b",
1972 |             "}",
1973 |             "",
1974 |             "# Franco Arabic style",
1975 |             "sndo2 greet(klma name) {",
1976 |             "  etb3(\"Marhaba {name}!\")",
1977 |             "}"
1978 |           ]
1979 |         }
1980 |       },
1981 |       "logic_errors": {
1982 |         "description": "Errors in program logic that don't cause crashes but produce wrong results",
1983 |         "infinite_loops": {
1984 |           "error": "Program hangs or runs forever",
1985 |           "cause": "Loop condition never becomes false",
1986 |           "solution": "Ensure loop variables change and conditions can be met",
1987 |           "prevention_example": [
1988 |             "# WRONG: Infinite loop",
1989 |             "# x = 0",
1990 |             "# talama x < 10 {",
1991 |             "#   print(x)",
1992 |             "#   # x never changes - infinite loop!",
1993 |             "# }",
1994 |             "",
1995 |             "# CORRECT: Proper loop with increment",
1996 |             "x = 0",
1997 |             "talama x < 10 {",
1998 |             "  print(x)",
1999 |             "  x++  # Ensure loop variable changes",
2000 |             "}",
2001 |             "",
2002 |             "# For complex conditions, add safety counters",
2003 |             "counter = 0",
2004 |             "talama condition and counter < 1000 {",
2005 |             "  # Loop body",
2006 |             "  counter++  # Safety counter prevents infinite loops",
2007 |             "}"
2008 |           ]
2009 |         },
2010 |         "off_by_one_errors": {
2011 |           "error": "Accessing one element before or after intended",
2012 |           "cause": "Incorrect loop bounds or index calculations",
2013 |           "solution": "Carefully check loop conditions and array bounds",
2014 |           "prevention_example": [
2015 |             "# Common off-by-one scenarios",
2016 |             "dorg items = [\"a\", \"b\", \"c\", \"d\", \"e\"]",
2017 |             "",
2018 |             "# WRONG: Goes one past array end",
2019 |             "# for(i=0; i<=length(items); i++) {  # <= is wrong",
2020 |             "#   print(items[i])  # Error on last iteration",
2021 |             "# }",
2022 |             "",
2023 |             "# CORRECT: Proper bounds checking",
2024 |             "for(i=0; i<length(items); i++) {",
2025 |             "  print(items[i])  # Safe access",
2026 |             "}",
2027 |             "",
2028 |             "# Franco style with proper bounds - CRITICAL FIX",
2029 |             "karr i=0 l7d length(items) - 1 {",
2030 |             "  print(\"Item {i}: {items[i]}\")",
2031 |             "}",
2032 |             "",
2033 |             "# IMPORTANT NOTE: Franco loops with l7d are INCLUSIVE",
2034 |             "# karr i=0 l7d 5 { } means i goes 0,1,2,3,4,5 (6 iterations)",
2035 |             "# For array access, always use: l7d length(array) - 1",
2036 |             "",
2037 |             "# Double-check boundary conditions",
2038 |             "lw length(items) > 0 {  # Ensure array not empty",
2039 |             "  first_item = items[0]     # Safe: first element",
2040 |             "  last_item = items[length(items)-1]  # Safe: last element",
2041 |             "}"
2042 |           ]
2043 |         }
2044 |       }
2045 |     },
2046 |     "error_prevention_patterns": {
2047 |       "input_validation_framework": {
2048 |         "description": "Comprehensive input validation system",
2049 |         "code": [
2050 |           "# Universal input validation functions",
2051 |           "sndo2 validateRange(rakm value, rakm min, rakm max) {",
2052 |           "  lw value >= min and value <= max {",
2053 |           "    rg3 sa7",
2054 |           "  } gher {",
2055 |           "    print(\"Error: Value {value} must be between {min} and {max}\")",
2056 |           "    rg3 ghalt",
2057 |           "  }",
2058 |           "}",
2059 |           "",
2060 |           "sndo2 validateNonEmpty(klma text) {",
2061 |           "  lw length(text) > 0 {",
2062 |           "    rg3 sa7",
2063 |           "  } gher {",
2064 |           "    print(\"Error: Input cannot be empty\")",
2065 |           "    rg3 ghalt",
2066 |           "  }",
2067 |           "}",
2068 |           "",
2069 |           "sndo2 validateChoice(klma choice, dorg valid_options) {",
2070 |           "  karr i=0 l7d length(valid_options) - 1 {",
2071 |           "    lw choice == valid_options[i] {",
2072 |           "      rg3 sa7",
2073 |           "    }",
2074 |           "  }",
2075 |           "  print(\"Error: '{choice}' is not a valid option\")",
2076 |           "  rg3 ghalt",
2077 |           "}",
2078 |           "",
2079 |           "# Usage example",
2080 |           "print(\"Enter your age (1-120): \")",
2081 |           "rakm age = scan()",
2082 |           "lw validateRange(age, 1, 120) {",
2083 |           "  print(\"Valid age: {age}\")",
2084 |           "} gher {",
2085 |           "  print(\"Please restart and enter a valid age\")",
2086 |           "}"
2087 |         ]
2088 |       },
2089 |       "safe_list_operations": {
2090 |         "description": "Error-proof list manipulation patterns",
2091 |         "code": [
2092 |           "# Safe list operations with bounds checking",
2093 |           "sndo2 safeListAccess(dorg myList, rakm index) {",
2094 |           "  lw index >= 0 and index < length(myList) {",
2095 |           "    rg3 myList[index]",
2096 |           "  } gher {",
2097 |           "    print(\"Warning: Index {index} out of bounds. List size: {length(myList)}\")",
2098 |           "    rg3 \"\"  # Return safe default",
2099 |           "  }",
2100 |           "}",
2101 |           "",
2102 |           "sndo2 safeListSet(dorg myList, rakm index, value) {",
2103 |           "  lw index >= 0 and index < length(myList) {",
2104 |           "    myList[index] = value",
2105 |           "    rg3 sa7",
2106 |           "  } gher {",
2107 |           "    print(\"Cannot set index {index} in list of size {length(myList)}\")",
2108 |           "    rg3 ghalt",
2109 |           "  }",
2110 |           "}",
2111 |           "",
2112 |           "# Safe list iteration patterns",
2113 |           "dorg data = [\"apple\", \"banana\", \"cherry\"]",
2114 |           "",
2115 |           "# Pattern 1: Traditional bounds-checked loop",
2116 |           "karr i=0 l7d length(data) - 1 {",
2117 |           "  item = safeListAccess(data, i)",
2118 |           "  print(\"Item {i}: {item}\")",
2119 |           "}",
2120 |           "",
2121 |           "# Pattern 2: Defensive iteration with empty check",
2122 |           "lw length(data) > 0 {",
2123 |           "  print(\"Processing {length(data)} items:\")",
2124 |           "  karr i=0 l7d length(data) - 1 {",
2125 |           "    print(data[i])",
2126 |           "  }",
2127 |           "} gher {",
2128 |           "  print(\"No items to process\")",
2129 |           "}"
2130 |         ]
2131 |       },
2132 |       "error_recovery_strategies": {
2133 |         "description": "Patterns for recovering from errors gracefully",
2134 |         "code": [
2135 |           "# Error recovery with retry mechanisms",
2136 |           "sndo2 retryableInput(klma prompt, rakm max_attempts) {",
2137 |           "  rakm attempts = 0",
2138 |           "  ",
2139 |           "  talama attempts < max_attempts {",
2140 |           "    print(\"{prompt} (Attempt {attempts+1}/{max_attempts}): \")",
2141 |           "    user_input = scan()",
2142 |           "    ",
2143 |           "    lw length(user_input) > 0 {",
2144 |           "      rg3 user_input  # Success",
2145 |           "    } gher {",
2146 |           "      attempts++",
2147 |           "      print(\"Invalid input. Try again.\")",
2148 |           "    }",
2149 |           "  }",
2150 |           "  ",
2151 |           "  print(\"Maximum attempts reached. Using default value.\")",
2152 |           "  rg3 \"default\"  # Fallback value",
2153 |           "}",
2154 |           "",
2155 |           "# Graceful degradation pattern",
2156 |           "sndo2 calculateWithFallback(rakm a, rakm b) {",
2157 |           "  lw b != 0 {",
2158 |           "    # Preferred calculation",
2159 |           "    rg3 a / b",
2160 |           "  } gher {",
2161 |           "    print(\"Warning: Division by zero. Using safe alternative.\")",
2162 |           "    # Fallback calculation",
2163 |           "    rg3 a * 0.5  # or any other safe default",
2164 |           "  }",
2165 |           "}",
2166 |           "",
2167 |           "# State recovery pattern",
2168 |           "sndo2 safeFileOperation(klma filename) {",
2169 |           "  # Save current state",
2170 |           "  previous_state = getCurrentState()",
2171 |           "  ",
2172 |           "  # Attempt operation",
2173 |           "  so2al success = performOperation(filename)",
2174 |           "  ",
2175 |           "  lw not success {",
2176 |           "    print(\"Operation failed. Restoring previous state.\")",
2177 |           "    restoreState(previous_state)",
2178 |           "    rg3 ghalt",
2179 |           "  }",
2180 |           "  ",
2181 |           "  rg3 sa7",
2182 |           "}"
2183 |         ]
2184 |       }
2185 |     },
2186 |     "debugging_techniques": {
2187 |       "description": "Practical debugging approaches for Flex programs",
2188 |       "debug_printing": {
2189 |         "description": "Strategic use of print statements for debugging",
2190 |         "examples": [
2191 |           "# Debug printing patterns",
2192 |           "sndo2 debugFunction(rakm x, rakm y) {",
2193 |           "  print(\"DEBUG: Function called with x={x}, y={y}\")",
2194 |           "  ",
2195 |           "  rakm result = x + y",
2196 |           "  print(\"DEBUG: Calculation result = {result}\")",
2197 |           "  ",
2198 |           "  lw result > 100 {",
2199 |           "    print(\"DEBUG: Result exceeds 100, applying reduction\")",
2200 |           "    result = result / 2",
2201 |           "    print(\"DEBUG: Reduced result = {result}\")",
2202 |           "  }",
2203 |           "  ",
2204 |           "  print(\"DEBUG: Function returning {result}\")",
2205 |           "  rg3 result",
2206 |           "}",
2207 |           "",
2208 |           "# Variable state tracking",
2209 |           "counter = 0",
2210 |           "talama counter < 10 {",
2211 |           "  print(\"DEBUG: Loop iteration {counter}\")",
2212 |           "  counter++",
2213 |           "  ",
2214 |           "  lw counter == 5 {",
2215 |           "    print(\"DEBUG: Reached midpoint\")",
2216 |           "  }",
2217 |           "}"
2218 |         ]
2219 |       },
2220 |       "step_by_step_verification": {
2221 |         "description": "Breaking down complex operations for easier debugging",
2222 |         "examples": [
2223 |           "# Complex calculation broken into steps",
2224 |           "rakm a = 10",
2225 |           "rakm b = 3",
2226 |           "rakm c = 7",
2227 |           "",
2228 |           "# Instead of: result = (a + b) * c - (a % b)",
2229 |           "step1 = a + b",
2230 |           "print(\"Step 1 (a + b): {step1}\")",
2231 |           "",
2232 |           "step2 = step1 * c",
2233 |           "print(\"Step 2 (step1 * c): {step2}\")",
2234 |           "",
2235 |           "step3 = a % b",
2236 |           "print(\"Step 3 (a % b): {step3}\")",
2237 |           "",
2238 |           "final_result = step2 - step3",
2239 |           "print(\"Final result: {final_result}\")",
2240 |           "",
2241 |           "# This approach makes it easy to spot calculation errors"
2242 |         ]
2243 |       }
2244 |     },
2245 |     "common_error_messages": {
2246 |       "description": "Typical error messages and their meanings",
2247 |       "interpreter_errors": {
2248 |         "undefined_variable": "Variable 'name' is not defined - declare variable before use",
2249 |         "type_error": "Cannot perform operation on incompatible types - check data types",
2250 |         "index_error": "List index out of range - check list bounds",
2251 |         "zero_division": "Division by zero - validate denominator",
2252 |         "syntax_error": "Unexpected token - check syntax and brackets",
2253 |         "function_error": "Function not defined - define before calling"
2254 |       },
2255 |       "runtime_warnings": {
2256 |         "empty_list": "Operating on empty list - check list length first",
2257 |         "large_number": "Number exceeds typical range - consider using smaller values",
2258 |         "infinite_loop": "Loop running too long - check loop conditions"
2259 |       }
2260 |     },
2261 |     "best_practices_summary": {
2262 |       "defensive_coding": [
2263 |         "Always validate user input before processing",
2264 |         "Check array bounds before accessing elements",
2265 |         "Verify divisors are non-zero before division/modulo",
2266 |         "Initialize variables with sensible default values",
2267 |         "Use explicit type declarations for critical variables",
2268 |         "Implement fallback values for error conditions"
2269 |       ],
2270 |       "error_handling_principles": [
2271 |         "Fail gracefully - don't crash the program",
2272 |         "Provide clear, helpful error messages",
2273 |         "Offer recovery mechanisms when possible",
2274 |         "Log errors for debugging purposes",
2275 |         "Use consistent error handling patterns",
2276 |         "Test error conditions during development"
2277 |       ],
2278 |       "user_experience": [
2279 |         "Guide users toward correct input format",
2280 |         "Provide examples of valid input",
2281 |         "Allow multiple attempts for input validation",
2282 |         "Explain what went wrong in simple terms",
2283 |         "Offer suggestions for fixing the problem"
2284 |       ]
2285 |     }
2286 |   },
2287 |   "built_in_functions": {
2288 |     "description": "Comprehensive built-in functions and system utilities in Flex",
2289 |     "core_functions": {
2290 |       "length": {
2291 |         "description": "Returns the length of a string or list",
2292 |         "franco_aliases": [
2293 |           "tool",
2294 |           "toul",
2295 |           "7ajm"
2296 |         ],
2297 |         "usage": [
2298 |           "length(string) - returns string length",
2299 |           "length(list) - returns list size",
2300 |           "tool(string) - Franco version",
2301 |           "7ajm(list) - Franco version"
2302 |         ],
2303 |         "examples": [
2304 |           "string s = \"hello\"",
2305 |           "print(length(s))        # Prints: 5",
2306 |           "etb3(tool(s))           # Franco version: Prints: 5",
2307 |           "",
2308 |           "list numbers = [1, 2, 3, 4]",
2309 |           "print(7ajm(numbers))    # Franco: Prints: 4",
2310 |           "",
2311 |           "# Safe usage in loops",
2312 |           "karr i=0 l7d length(s) - 1 {",
2313 |           "  print(\"Character {i}\")",
2314 |           "}"
2315 |         ]
2316 |       },
2317 |       "type_checking": {
2318 |         "description": "Functions to check variable types",
2319 |         "functions": {
2320 |           "isNumber": "isNumber(value) - returns true if value is numeric",
2321 |           "isString": "isString(value) - returns true if value is string",
2322 |           "isList": "isList(value) - returns true if value is list",
2323 |           "isBool": "isBool(value) - returns true if value is boolean"
2324 |         },
2325 |         "franco_versions": {
2326 |           "isNumber": "rakm?",
2327 |           "isString": "klma?",
2328 |           "isList": "dorg?",
2329 |           "isBool": "so2al?"
2330 |         },
2331 |         "examples": [
2332 |           "# Safe type checking",
2333 |           "sndo2 safeAdd(value1, value2) {",
2334 |           "  lw isNumber(value1) and isNumber(value2) {",
2335 |           "    rg3 value1 + value2",
2336 |           "  } gher {",
2337 |           "    print(\"Error: Both values must be numbers\")",
2338 |           "    rg3 0",
2339 |           "  }",
2340 |           "}",
2341 |           "",
2342 |           "# Franco type checking",
2343 |           "lw rakm?(userInput) {",
2344 |           "  etb3(\"Valid number: {userInput}\")",
2345 |           "}"
2346 |         ]
2347 |       },
2348 |       "string_utilities": {
2349 |         "description": "String manipulation functions",
2350 |         "functions": {
2351 |           "split": "split(string, delimiter) - split string into list",
2352 |           "join": "join(list, delimiter) - join list elements into string",
2353 |           "trim": "trim(string) - remove whitespace",
2354 |           "upper": "upper(string) - convert to uppercase",
2355 |           "lower": "lower(string) - convert to lowercase",
2356 |           "contains": "contains(string, substring) - check if string contains substring"
2357 |         },
2358 |         "franco_versions": {
2359 |           "split": "2sm",
2360 |           "join": "jam3",
2361 |           "trim": "n7f",
2362 |           "upper": "kbr",
2363 |           "lower": "sg7r",
2364 |           "contains": "fy"
2365 |         },
2366 |         "examples": [
2367 |           "# String operations",
2368 |           "text = \"Hello, World!\"",
2369 |           "words = split(text, \", \")",
2370 |           "print(words)                    # [\"Hello\", \"World!\"]",
2371 |           "",
2372 |           "# Franco string operations",
2373 |           "klma nass = \"  hello world  \"",
2374 |           "etb3(n7f(nass))                # \"hello world\"",
2375 |           "etb3(kbr(nass))                # \"  HELLO WORLD  \"",
2376 |           "",
2377 |           "# Check if string contains substring",
2378 |           "lw fy(text, \"World\") {",
2379 |           "  etb3(\"Found 'World' in text!\")",
2380 |           "}"
2381 |         ]
2382 |       },
2383 |       "math_utilities": {
2384 |         "description": "Mathematical functions beyond basic operators",
2385 |         "functions": {
2386 |           "sqrt": "sqrt(number) - square root",
2387 |           "power": "power(base, exponent) - raise to power",
2388 |           "abs": "abs(number) - absolute value",
2389 |           "round": "round(number) - round to nearest integer",
2390 |           "floor": "floor(number) - round down",
2391 |           "ceil": "ceil(number) - round up",
2392 |           "min": "min(a, b) - minimum of two values",
2393 |           "max": "max(a, b) - maximum of two values",
2394 |           "random": "random() - random number between 0 and 1"
2395 |         },
2396 |         "franco_versions": {
2397 |           "sqrt": "jzr",
2398 |           "power": "2ss",
2399 |           "abs": "mtl2",
2400 |           "round": "2rb",
2401 |           "min": "asgar",
2402 |           "max": "akbar"
2403 |         },
2404 |         "examples": [
2405 |           "# Mathematical operations",
2406 |           "number = 16",
2407 |           "print(sqrt(number))          # 4",
2408 |           "print(jzr(number))           # Franco version: 4",
2409 |           "",
2410 |           "# Complex calculations",
2411 |           "result = power(2, 8)         # 256",
2412 |           "result = 2ss(2, 8)           # Franco version: 256",
2413 |           "",
2414 |           "# Finding extremes",
2415 |           "values = [5, 2, 8, 1, 9]",
2416 |           "smallest = min(values)",
2417 |           "largest = max(values)",
2418 |           "print(\"Range: {smallest} to {largest}\")"
2419 |         ]
2420 |       },
2421 |       "system_utilities": {
2422 |         "description": "System and environment functions",
2423 |         "functions": {
2424 |           "getCurrentTime": "getCurrentTime() - current timestamp",
2425 |           "systemType": "systemType() - operating system type",
2426 |           "getEnv": "getEnv(name) - environment variable",
2427 |           "sleep": "sleep(milliseconds) - pause execution",
2428 |           "fileExists": "fileExists(path) - check if file exists",
2429 |           "listFiles": "listFiles(directory) - list files in directory"
2430 |         },
2431 |         "franco_versions": {
2432 |           "getCurrentTime": "wa2tHali",
2433 |           "systemType": "no3Nizam",
2434 |           "sleep": "nam",
2435 |           "fileExists": "mlafM3jod"
2436 |         },
2437 |         "examples": [
2438 |           "# System information",
2439 |           "currentOS = systemType()",
2440 |           "print(\"Running on: {currentOS}\")",
2441 |           "",
2442 |           "# Franco system calls",
2443 |           "wa2t = wa2tHali()",
2444 |           "etb3(\"Current time: {wa2t}\")",
2445 |           "",
2446 |           "# File operations",
2447 |           "lw mlafM3jod(\"config.txt\") {",
2448 |           "  config = readFile(\"config.txt\")",
2449 |           "} gher {",
2450 |           "  print(\"Config file not found\")",
2451 |           "}"
2452 |         ]
2453 |       }
2454 |     },
2455 |     "list_methods": {
2456 |       "description": "Enhanced list methods with Franco Arabic support",
2457 |       "methods": {
2458 |         "push": "list.push(item) - add item to end of list",
2459 |         "pop": "list.pop() - remove and return last item",
2460 |         "remove": "list.remove(value) - remove specific value from list",
2461 |         "insert": "list.insert(index, item) - insert item at specific position",
2462 |         "clear": "list.clear() - remove all elements",
2463 |         "reverse": "list.reverse() - reverse the list order",
2464 |         "sort": "list.sort() - sort the list",
2465 |         "find": "list.find(value) - find index of value",
2466 |         "contains": "list.contains(value) - check if list contains value"
2467 |       },
2468 |       "franco_methods": {
2469 |         "push": "d7af",
2470 |         "pop": "shyl",
2471 |         "remove": "shyl",
2472 |         "insert": "d5al",
2473 |         "clear": "m7y",
2474 |         "reverse": "2leb",
2475 |         "sort": "rtb",
2476 |         "find": "d7wer"
2477 |       },
2478 |       "examples": [
2479 |         "list arr = [1, 2, 3]",
2480 |         "arr.push(4)                     # arr is now [1, 2, 3, 4]",
2481 |         "arr.d7af(5)                     # Franco: add 5, arr is [1, 2, 3, 4, 5]",
2482 |         "arr.pop()                       # removes 5, arr is [1, 2, 3, 4]",
2483 |         "arr.remove(2)                   # removes 2, arr is [1, 3, 4]",
2484 |         "",
2485 |         "# Advanced list operations",
2486 |         "arr.insert(1, 99)               # Insert 99 at index 1: [1, 99, 3, 4]",
2487 |         "arr.d5al(0, 77)                 # Franco: Insert 77 at start: [77, 1, 99, 3, 4]",
2488 |         "",
2489 |         "# List utilities",
2490 |         "index = arr.find(99)            # Returns 2 (index of 99)",
2491 |         "exists = arr.contains(3)        # Returns true",
2492 |         "",
2493 |         "# Mixed data types in lists",
2494 |         "list mixed = [1, \"hello\", sa7, 3.14]",
2495 |         "mixed.push(\"new item\")",
2496 |         "print(mixed)                    # [1, \"hello\", true, 3.14, \"new item\"]",
2497 |         "",
2498 |         "# List sorting and manipulation",
2499 |         "dorg numbers = [5, 2, 8, 1, 9]",
2500 |         "numbers.rtb()                   # Franco sort: [1, 2, 5, 8, 9]",
2501 |         "numbers.2leb()                  # Franco reverse: [9, 8, 5, 2, 1]"
2502 |       ]
2503 |     }
2504 |   },
2505 |   "variable_scoping": {
2506 |     "description": "Variable scope rules and best practices in Flex",
2507 |     "global_scope": "Variables declared outside functions are globally accessible",
2508 |     "local_scope": "Variables declared inside functions are locally scoped",
2509 |     "scope_examples": [
2510 |       "# Global variables",
2511 |       "rakm global_counter = 0",
2512 |       "klma app_name = \"Flex App\"",
2513 |       "",
2514 |       "sndo2 increment() {",
2515 |       "  # Can access global variables",
2516 |       "  global_counter = global_counter + 1",
2517 |       "  ",
2518 |       "  # Local variable - only accessible in this function",
2519 |       "  rakm local_temp = 42",
2520 |       "  print(\"Local temp: {local_temp}\")",
2521 |       "}",
2522 |       "",
2523 |       "increment()  # global_counter is now 1",
2524 |       "print(global_counter)  # Prints: 1",
2525 |       "# print(local_temp)     # Error: local_temp not accessible here"
2526 |     ],
2527 |     "parameter_scope": [
2528 |       "sndo2 calculate(rakm param1, rakm param2) {",
2529 |       "  # Parameters are local to the function",
2530 |       "  rakm local_result = param1 + param2",
2531 |       "  rg3 local_result",
2532 |       "}",
2533 |       "",
2534 |       "# param1, param2, local_result not accessible outside function"
2535 |     ]
2536 |   },
2537 |   "project_templates": {
2538 |     "description": "Complete example programs for common use cases",
2539 |     "calculator": {
2540 |       "description": "Simple calculator with Franco Arabic mixed syntax",
2541 |       "code": [
2542 |         "# Simple Calculator - Mixed Syntax Demo",
2543 |         "etb3(\"=== Flex Calculator ===\")",
2544 |         "",
2545 |         "# Get user input with automatic type detection",
2546 |         "print(\"Enter first number:\")",
2547 |         "rakm num1 = da5l()          # Franco input, forces number type",
2548 |         "",
2549 |         "etb3(\"Enter operator (+, -, *, /, %):\")",
2550 |         "operator = scan()           # String input for operator",
2551 |         "",
2552 |         "print(\"Enter second number:\")",
2553 |         "rakm num2 = scan()          # English input, forces number type",
2554 |         "",
2555 |         "# Perform calculation",
2556 |         "lw operator == \"+\" {",
2557 |         "  result = num1 + num2",
2558 |         "  etb3(\"Result: {num1} + {num2} = {result}\")",
2559 |         "}",
2560 |         "aw operator == \"-\" {",
2561 |         "  result = num1 - num2",
2562 |         "  print(\"Result: {num1} - {num2} = {result}\")",
2563 |         "}",
2564 |         "aw operator == \"*\" {",
2565 |         "  result = num1 * num2",
2566 |         "  etb3(\"Result: {num1} × {num2} = {result}\")",
2567 |         "}",
2568 |         "aw operator == \"/\" {",
2569 |         "  lw num2 != 0 {",
2570 |         "    kasr result = num1 / num2",
2571 |         "    print(\"Result: {num1} ÷ {num2} = {result}\")",
2572 |         "  } gher {",
2573 |         "    etb3(\"Error: Division by zero!\")",
2574 |         "  }",
2575 |         "}",
2576 |         "aw operator == \"%\" {",
2577 |         "  lw num2 != 0 {",
2578 |         "    rakm remainder = num1 % num2",
2579 |         "    etb3(\"Result: {num1} % {num2} = {remainder}\")",
2580 |         "  } gher {",
2581 |         "    print(\"Error: Modulo by zero!\")",
2582 |         "  }",
2583 |         "}",
2584 |         "gher {",
2585 |         "  print(\"Error: Invalid operator!\")",
2586 |         "}",
2587 |         "",
2588 |         "etb3(\"Thank you for using Flex Calculator!\")"
2589 |       ]
2590 |     },
2591 |     "todo_list": {
2592 |       "description": "Task management program with Franco Arabic features",
2593 |       "code": [
2594 |         "# Todo List Manager - Franco Arabic Style",
2595 |         "dorg tasks = []",
2596 |         "so2al running = sa7",
2597 |         "",
2598 |         "sndo2 showMenu() {",
2599 |         "  etb3(\"\\n=== قائمة المهام (Task List) ===\")",
2600 |         "  print(\"1. إضافة مهمة (Add Task)\")",
2601 |         "  etb3(\"2. عرض المهام (View Tasks)\")",
2602 |         "  print(\"3. حذف مهمة (Delete Task)\")",
2603 |         "  etb3(\"4. خروج (Exit)\")",
2604 |         "  print(\"اختر رقم (Choose number): \")",
2605 |         "}",
2606 |         "",
2607 |         "sndo2 addTask() {",
2608 |         "  etb3(\"أدخل المهمة الجديدة (Enter new task):\")",
2609 |         "  task = da5l()",
2610 |         "  tasks.push(task)",
2611 |         "  print(\"تم إضافة المهمة! (Task added!)\")",
2612 |         "}",
2613 |         "",
2614 |         "sndo2 showTasks() {",
2615 |         "  lw length(tasks) == 0 {",
2616 |         "    etb3(\"لا توجد مهام (No tasks found)\")",
2617 |         "  } gher {",
2618 |         "    print(\"\\nالمهام الحالية (Current tasks):\")",
2619 |         "    karr i=0 l7d length(tasks) - 1 {",
2620 |         "      etb3(\"{i+1}. {tasks[i]}\")",
2621 |         "    }",
2622 |         "  }",
2623 |         "}",
2624 |         "",
2625 |         "# Main program loop",
2626 |         "talama running {",
2627 |         "  showMenu()",
2628 |         "  choice = scan()",
2629 |         "  ",
2630 |         "  lw choice == \"1\" {",
2631 |         "    addTask()",
2632 |         "  }",
2633 |         "  aw choice == \"2\" {",
2634 |         "    showTasks()",
2635 |         "  }",
2636 |         "  aw choice == \"3\" {",
2637 |         "    showTasks()",
2638 |         "    etb3(\"أدخل رقم المهمة للحذف (Enter task number to delete):\")",
2639 |         "    rakm task_num = da5l()",
2640 |         "    index = task_num - 1",
2641 |         "    lw index >= 0 and index < length(tasks) {",
2642 |         "      tasks.remove(tasks[index])",
2643 |         "      print(\"تم حذف المهمة! (Task deleted!)\")",
2644 |         "    } gher {",
2645 |         "      etb3(\"رقم غير صحيح (Invalid number)\")",
2646 |         "    }",
2647 |         "  }",
2648 |         "  aw choice == \"4\" {",
2649 |         "    running = ghalt",
2650 |         "    etb3(\"شكراً لاستخدام البرنامج! (Thanks for using the program!)\")",
2651 |         "  }",
2652 |         "  gher {",
2653 |         "    print(\"اختيار غير صحيح (Invalid choice)\")",
2654 |         "  }",
2655 |         "}"
2656 |       ]
2657 |     }
2658 |   },
2659 |   "performance_optimization": {
2660 |     "description": "Comprehensive performance optimization patterns and memory management",
2661 |     "optimization_guidelines": [
2662 |       "Use appropriate data types for your needs",
2663 |       "Prefer local variables over global when possible",
2664 |       "Use early returns in functions to avoid deep nesting",
2665 |       "Break out of loops early when condition is met",
2666 |       "Use string interpolation instead of concatenation for readability",
2667 |       "Declare variable types explicitly when needed for input validation",
2668 |       "Process large datasets in chunks to avoid memory overflow",
2669 |       "Use English loops for better performance with large arrays",
2670 |       "Avoid nested Franco loops with large datasets"
2671 |     ],
2672 |     "memory_management": {
2673 |       "description": "Memory-conscious programming patterns",
2674 |       "best_practices": [
2675 |         "# Chunked processing for large datasets",
2676 |         "sndo2 processLargeData(dorg data, rakm chunkSize) {",
2677 |         "  rakm total = length(data)",
2678 |         "  rakm processed = 0",
2679 |         "  ",
2680 |         "  # Process in chunks to avoid memory overflow",
2681 |         "  talama processed < total {",
2682 |         "    rakm end = processed + chunkSize",
2683 |         "    lw end > total { end = total }",
2684 |         "    ",
2685 |         "    # Process current chunk",
2686 |         "    for(i=processed; i<end; i++) {",
2687 |         "      processItem(data[i])",
2688 |         "    }",
2689 |         "    ",
2690 |         "    processed = end",
2691 |         "    print(\"Processed {processed}/{total} items\")",
2692 |         "  }",
2693 |         "}",
2694 |         "",
2695 |         "# Memory-efficient string building",
2696 |         "sndo2 buildLargeString(dorg items) {",
2697 |         "  dorg parts = []  # Collect parts first",
2698 |         "  ",
2699 |         "  karr i=0 l7d length(items) - 1 {",
2700 |         "    parts.push(\"Item: {items[i]}\")",
2701 |         "  }",
2702 |         "  ",
2703 |         "  # Join at the end (more efficient than repeated concatenation)",
2704 |         "  rg3 joinStrings(parts, \"\\n\")",
2705 |         "}",
2706 |         "",
2707 |         "# Clear variables when done with large data",
2708 |         "sndo2 cleanupAfterProcessing() {",
2709 |         "  largeData = []  # Clear reference to large dataset",
2710 |         "  tempResults = []  # Clear temporary results",
2711 |         "  # Variables will be garbage collected",
2712 |         "}"
2713 |       ],
2714 |       "performance_patterns": [
2715 |         "# Fast search with early termination",
2716 |         "sndo2 fastFind(dorg items, value) {",
2717 |         "  # Use English loop for better performance",
2718 |         "  for(i=0; i<length(items); i++) {",
2719 |         "    lw items[i] == value {",
2720 |         "      rg3 i  # Early return saves time",
2721 |         "    }",
2722 |         "  }",
2723 |         "  rg3 -1",
2724 |         "}",
2725 |         "",
2726 |         "# Efficient filtering with size pre-allocation",
2727 |         "sndo2 efficientFilter(dorg source, condition) {",
2728 |         "  dorg result = []",
2729 |         "  rakm count = 0",
2730 |         "  ",
2731 |         "  # First pass: count matches (optional optimization)",
2732 |         "  for(i=0; i<length(source); i++) {",
2733 |         "    lw evaluateCondition(source[i], condition) {",
2734 |         "      count++",
2735 |         "    }",
2736 |         "  }",
2737 |         "  ",
2738 |         "  # Second pass: collect results",
2739 |         "  for(i=0; i<length(source); i++) {",
2740 |         "    lw evaluateCondition(source[i], condition) {",
2741 |         "      result.push(source[i])",
2742 |         "    }",
2743 |         "  }",
2744 |         "  ",
2745 |         "  rg3 result",
2746 |         "}",
2747 |         "",
2748 |         "# Batch operations for better performance",
2749 |         "sndo2 batchProcess(dorg items, rakm batchSize) {",
2750 |         "  dorg batches = []",
2751 |         "  dorg currentBatch = []",
2752 |         "  ",
2753 |         "  for(i=0; i<length(items); i++) {",
2754 |         "    currentBatch.push(items[i])",
2755 |         "    ",
2756 |         "    lw length(currentBatch) == batchSize {",
2757 |         "      processBatch(currentBatch)",
2758 |         "      currentBatch = []  # Reset for next batch",
2759 |         "    }",
2760 |         "  }",
2761 |         "  ",
2762 |         "  # Process remaining items",
2763 |         "  lw length(currentBatch) > 0 {",
2764 |         "    processBatch(currentBatch)",
2765 |         "  }",
2766 |         "}"
2767 |       ]
2768 |     },
2769 |     "benchmarking": {
2770 |       "description": "Performance measurement patterns",
2771 |       "timing_functions": [
2772 |         "# Simple timing for performance measurement",
2773 |         "sndo2 timeFunction(functionToTime, params) {",
2774 |         "  startTime = getCurrentTime()",
2775 |         "  result = functionToTime(params)",
2776 |         "  endTime = getCurrentTime()",
2777 |         "  duration = endTime - startTime",
2778 |         "  print(\"Function took {duration}ms\")",
2779 |         "  rg3 result",
2780 |         "}",
2781 |         "",
2782 |         "# Compare performance of different approaches",
2783 |         "sndo2 comparePerformance() {",
2784 |         "  dorg testData = generateTestData(10000)",
2785 |         "  ",
2786 |         "  # Test Franco loop performance",
2787 |         "  startTime = getCurrentTime()",
2788 |         "  francoResult = processFrancoLoop(testData)",
2789 |         "  francoTime = getCurrentTime() - startTime",
2790 |         "  ",
2791 |         "  # Test English loop performance",
2792 |         "  startTime = getCurrentTime()",
2793 |         "  englishResult = processEnglishLoop(testData)",
2794 |         "  englishTime = getCurrentTime() - startTime",
2795 |         "  ",
2796 |         "  print(\"Franco loop: {francoTime}ms\")",
2797 |         "  print(\"English loop: {englishTime}ms\")",
2798 |         "  print(\"Difference: {englishTime - francoTime}ms\")",
2799 |         "}"
2800 |       ]
2801 |     },
2802 |     "efficient_patterns": [
2803 |       "# Efficient loop with early exit",
2804 |       "sndo2 findItem(dorg items, klma target) {",
2805 |       "  # Prefer English loops for large datasets",
2806 |       "  for(i=0; i<length(items); i++) {",
2807 |       "    lw items[i] == target {",
2808 |       "      rg3 i  # Return immediately when found",
2809 |       "    }",
2810 |       "  }",
2811 |       "  rg3 -1  # Not found",
2812 |       "}",
2813 |       "",
2814 |       "# Use string interpolation for readable output",
2815 |       "name = \"Flex\"",
2816 |       "version = \"2.1\"",
2817 |       "message = \"Welcome to {name} version {version}!\"  # Better than concatenation",
2818 |       "",
2819 |       "# Minimize function calls in loops",
2820 |       "dorg items = [1, 2, 3, 4, 5]",
2821 |       "rakm itemCount = length(items)  # Calculate once, not in each iteration",
2822 |       "for(i=0; i<itemCount; i++) {",
2823 |       "  processItem(items[i])",
2824 |       "}"
2825 |     ]
2826 |   },
2827 |   "community_guidelines": {
2828 |     "description": "Best practices and conventions for Flex development",
2829 |     "coding_style": {
2830 |       "naming_conventions": [
2831 |         "Use descriptive variable names in preferred language",
2832 |         "Functions: camelCase (English) or underscore_case (Franco)",
2833 |         "Constants: UPPER_CASE in both languages",
2834 |         "Lists: plural nouns (items, students, etc.)",
2835 |         "Booleans: descriptive predicates (isActive, m3jod, etc.)"
2836 |       ],
2837 |       "formatting_guidelines": [
2838 |         "Use consistent indentation (2 or 4 spaces)",
2839 |         "Add blank lines between logical sections",
2840 |         "Comment complex logic in both languages when helpful",
2841 |         "Group related variable declarations together",
2842 |         "Use string interpolation over concatenation"
2843 |       ],
2844 |       "safety_practices": [
2845 |         "⚠️ ALWAYS use 'length(array) - 1' in Franco l7d loops",
2846 |         "Validate user input before processing",
2847 |         "Check file existence before file operations",
2848 |         "Use explicit types for critical variables",
2849 |         "Implement error handling for division and modulo",
2850 |         "Test boundary conditions (empty lists, zero values)"
2851 |       ]
2852 |     },
2853 |     "project_structure": {
2854 |       "recommended_layout": [
2855 |         "project/",
2856 |         "├── src/",
2857 |         "│   ├── main.flex          # Main application file",
2858 |         "│   ├── utils/",
2859 |         "│   │   ├── helpers.flex   # Utility functions",
2860 |         "│   │   └── constants.lx   # Constants and config",
2861 |         "│   └── modules/",
2862 |         "│       ├── data.flex      # Data processing",
2863 |         "│       └── ui.lx          # User interface",
2864 |         "├── tests/",
2865 |         "│   ├── test_main.flex     # Main tests",
2866 |         "│   └── test_utils.lx      # Utility tests",
2867 |         "├── docs/",
2868 |         "│   └── README.md          # Project documentation",
2869 |         "└── config.json           # Configuration file"
2870 |       ],
2871 |       "file_organization": [
2872 |         "Separate Franco and English modules if team prefers",
2873 |         "Use .flex for mixed syntax files",
2874 |         "Use .lx for Franco-heavy files",
2875 |         "Group related functions in same file",
2876 |         "Keep main application logic separate from utilities"
2877 |       ]
2878 |     },
2879 |     "testing_framework": {
2880 |       "description": "Testing patterns for Flex applications",
2881 |       "basic_testing": [
2882 |         "# Simple test function pattern",
2883 |         "sndo2 testFunction(klma testName, expected, actual) {",
2884 |         "  lw expected == actual {",
2885 |         "    etb3(\"✅ {testName} passed\")",
2886 |         "    rg3 sa7",
2887 |         "  } gher {",
2888 |         "    print(\"❌ {testName} failed: expected {expected}, got {actual}\")",
2889 |         "    rg3 ghalt",
2890 |         "  }",
2891 |         "}",
2892 |         "",
2893 |         "# Test runner pattern",
2894 |         "sndo2 runTests() {",
2895 |         "  rakm passed = 0",
2896 |         "  rakm total = 0",
2897 |         "  ",
2898 |         "  # Test arithmetic functions",
2899 |         "  total++",
2900 |         "  lw testFunction(\"Addition\", 5, add(2, 3)) { passed++ }",
2901 |         "  ",
2902 |         "  total++",
2903 |         "  lw testFunction(\"Multiplication\", 15, multiply(3, 5)) { passed++ }",
2904 |         "  ",
2905 |         "  # Test Franco loop safety",
2906 |         "  total++",
2907 |         "  dorg testArray = [1, 2, 3]",
2908 |         "  so2al loopSafe = sa7",
2909 |         "  karr i=0 l7d length(testArray) - 1 {",
2910 |         "    lw testArray[i] == 0 { loopSafe = ghalt }",
2911 |         "  }",
2912 |         "  lw testFunction(\"Franco loop safety\", sa7, loopSafe) { passed++ }",
2913 |         "  ",
2914 |         "  print(\"Test Results: {passed}/{total} passed\")",
2915 |         "  rg3 passed == total",
2916 |         "}"
2917 |       ]
2918 |     }
2919 |   },
2920 |   "troubleshooting_guide": {
2921 |     "description": "Common issues and comprehensive solutions",
2922 |     "frequent_problems": {
2923 |       "franco_loop_errors": {
2924 |         "symptoms": "Array index out of bounds, runtime errors in loops",
2925 |         "cause": "Using l7d without subtracting 1 from array length",
2926 |         "immediate_fix": "Change 'karr i=0 l7d length(array)' to 'karr i=0 l7d length(array) - 1'",
2927 |         "prevention": "Always remember Franco loops are INCLUSIVE",
2928 |         "example_fix": [
2929 |           "# ❌ WRONG - causes out-of-bounds error",
2930 |           "# karr i=0 l7d length(myList) { print(myList[i]) }",
2931 |           "",
2932 |           "# ✅ CORRECT - safe array access",
2933 |           "karr i=0 l7d length(myList) - 1 { print(myList[i]) }",
2934 |           "",
2935 |           "# 🔄 Alternative: use English loops for safety",
2936 |           "for(i=0; i<length(myList); i++) { print(myList[i]) }"
2937 |         ]
2938 |       },
2939 |       "type_confusion": {
2940 |         "symptoms": "Unexpected results in calculations, string/number mix-ups",
2941 |         "cause": "Implicit type conversion or mixed data types",
2942 |         "immediate_fix": "Use explicit type declarations",
2943 |         "prevention": "Always validate input types",
2944 |         "example_fix": [
2945 |           "# Problem: user input causing type issues",
2946 |           "print(\"Enter a number:\")",
2947 |           "rakm userNum = da5l()  # Explicit type declaration",
2948 |           "",
2949 |           "# Validate input type",
2950 |           "lw isNumber(userNum) {",
2951 |           "  result = userNum * 2",
2952 |           "  print(\"Result: {result}\")",
2953 |           "} gher {",
2954 |           "  print(\"Error: Please enter a valid number\")",
2955 |           "}"
2956 |         ]
2957 |       },
2958 |       "memory_issues": {
2959 |         "symptoms": "Slow performance, system lag with large data",
2960 |         "cause": "Processing large datasets without chunking",
2961 |         "immediate_fix": "Implement chunked processing",
2962 |         "prevention": "Design with memory constraints in mind",
2963 |         "example_fix": [
2964 |           "# Process large data in manageable chunks",
2965 |           "sndo2 processLargeDataset(dorg data) {",
2966 |           "  rakm chunkSize = 1000",
2967 |           "  rakm total = length(data)",
2968 |           "  ",
2969 |           "  for(start=0; start<total; start=start+chunkSize) {",
2970 |           "    end = start + chunkSize",
2971 |           "    lw end > total { end = total }",
2972 |           "    ",
2973 |           "    # Process current chunk",
2974 |           "    processChunk(data, start, end)",
2975 |           "    ",
2976 |           "    # Optional: pause between chunks",
2977 |           "    sleep(10)  # 10ms pause",
2978 |           "  }",
2979 |           "}"
2980 |         ]
2981 |       }
2982 |     },
2983 |     "debugging_workflow": {
2984 |       "step_by_step": [
2985 |         "1. **Identify Error Type**: Runtime, syntax, or logic error?",
2986 |         "2. **Check Franco Loops**: Are you using l7d with arrays? Add '- 1' to length",
2987 |         "3. **Verify Types**: Are variables the expected type? Use type checking functions",
2988 |         "4. **Validate Input**: Is user input causing issues? Add input validation",
2989 |         "5. **Test Boundaries**: Empty lists, zero values, negative numbers?",
2990 |         "6. **Add Debug Prints**: Strategic print statements to trace execution",
2991 |         "7. **Isolate Problem**: Create minimal test case reproducing the issue"
2992 |       ],
2993 |       "debug_patterns": [
2994 |         "# Debug wrapper function",
2995 |         "sndo2 debugWrap(klma funcName, params) {",
2996 |         "  print(\"DEBUG: Entering {funcName} with params: {params}\")",
2997 |         "  result = callFunction(funcName, params)",
2998 |         "  print(\"DEBUG: {funcName} returned: {result}\")",
2999 |         "  rg3 result",
3000 |         "}",
3001 |         "",
3002 |         "# Variable state logging",
3003 |         "sndo2 logState(klma context, dorg variables) {",
3004 |         "  print(\"DEBUG [{context}]:\")",
3005 |         "  karr i=0 l7d length(variables) - 1 {",
3006 |         "    print(\"  {variables[i].name} = {variables[i].value}\")",
3007 |         "  }",
3008 |         "}"
3009 |       ]
3010 |     }
3011 |   },
3012 |   "language_info": {
3013 |     "version": "2.1",
3014 |     "release_date": "2024",
3015 |     "compatibility": {
3016 |       "file_extensions": [
3017 |         ".flex",
3018 |         ".lx"
3019 |       ],
3020 |       "encoding": "UTF-8",
3021 |       "line_endings": "LF or CRLF"
3022 |     },
3023 |     "features_by_version": {
3024 |       "1.0": [
3025 |         "Franco Arabic and English mixed syntax",
3026 |         "Automatic type detection",
3027 |         "String interpolation with {variable} syntax",
3028 |         "Flexible loop constructs (karr l7d, talama)",
3029 |         "Mixed function definitions (fun, sndo2)",
3030 |         "Comprehensive I/O functions",
3031 |         "Built-in list operations",
3032 |         "Complete arithmetic operators (+, -, *, /, %)",
3033 |         "Multi-style comments",
3034 |         "No semicolon requirements"
3035 |       ],
3036 |       "2.0": [
3037 |         "Enhanced error handling patterns",
3038 |         "File I/O operations with Franco keywords",
3039 |         "Advanced import system",
3040 |         "Performance optimization guidelines",
3041 |         "Memory management patterns",
3042 |         "Built-in mathematical functions",
3043 |         "String manipulation utilities",
3044 |         "System utility functions"
3045 |       ],
3046 |       "2.1": [
3047 |         "Critical Franco loop safety warnings",
3048 |         "Comprehensive testing framework",
3049 |         "Community coding guidelines",
3050 |         "Enhanced debugging tools",
3051 |         "Production-ready error recovery patterns",
3052 |         "Performance benchmarking utilities",
3053 |         "Advanced type checking functions",
3054 |         "Troubleshooting guide with real solutions"
3055 |       ]
3056 |     }
3057 |   }
3058 | }
```

.claude/commands/execute-prp.md
```
1 | # Execute BASE PRP
2 | 
3 | Implement a feature using using the PRP file.
4 | 
5 | ## PRP File: $ARGUMENTS
6 | 
7 | ## Execution Process
8 | 
9 | 1. **Load PRP**
10 |    - Read the specified PRP file
11 |    - Understand all context and requirements
12 |    - Follow all instructions in the PRP and extend the research if needed
13 |    - Ensure you have all needed context to implement the PRP fully
14 |    - Do more web searches and codebase exploration as needed
15 | 
16 | 2. **ULTRATHINK**
17 |    - Think hard before you execute the plan. Create a comprehensive plan addressing all requirements.
18 |    - Break down complex tasks into smaller, manageable steps using your todos tools.
19 |    - Use the TodoWrite tool to create and track your implementation plan.
20 |    - Identify implementation patterns from existing code to follow.
21 | 
22 | 3. **Execute the plan**
23 |    - Execute the PRP
24 |    - Implement all the code
25 | 
26 | 4. **Validate**
27 |    - Run each validation command
28 |    - Fix any failures
29 |    - Re-run until all pass
30 | 
31 | 5. **Complete**
32 |    - Ensure all checklist items done
33 |    - Run final validation suite
34 |    - Report completion status
35 |    - Read the PRP again to ensure you have implemented everything
36 | 
37 | 6. **Reference the PRP**
38 |    - You can always reference the PRP again if needed
39 | 
40 | Note: If validation fails, use error patterns in PRP to fix and retry.
```

.claude/commands/generate-prp.md
```
1 | # Create PRP
2 | 
3 | ## Feature file: $ARGUMENTS
4 | 
5 | Generate a complete PRP for general feature implementation with thorough research. Ensure context is passed to the AI agent to enable self-validation and iterative refinement. Read the feature file first to understand what needs to be created, how the examples provided help, and any other considerations.
6 | 
7 | The AI agent only gets the context you are appending to the PRP and training data. Assuma the AI agent has access to the codebase and the same knowledge cutoff as you, so its important that your research findings are included or referenced in the PRP. The Agent has Websearch capabilities, so pass urls to documentation and examples.
8 | 
9 | ## Research Process
10 | 
11 | 1. **Codebase Analysis**
12 |    - Search for similar features/patterns in the codebase
13 |    - Identify files to reference in PRP
14 |    - Note existing conventions to follow
15 |    - Check test patterns for validation approach
16 | 
17 | 2. **External Research**
18 |    - Search for similar features/patterns online
19 |    - Library documentation (include specific URLs)
20 |    - Implementation examples (GitHub/StackOverflow/blogs)
21 |    - Best practices and common pitfalls
22 | 
23 | 3. **User Clarification** (if needed)
24 |    - Specific patterns to mirror and where to find them?
25 |    - Integration requirements and where to find them?
26 | 
27 | ## PRP Generation
28 | 
29 | Using PRPs/templates/prp_base.md as template:
30 | 
31 | ### Critical Context to Include and pass to the AI agent as part of the PRP
32 | - **Documentation**: URLs with specific sections
33 | - **Code Examples**: Real snippets from codebase
34 | - **Gotchas**: Library quirks, version issues
35 | - **Patterns**: Existing approaches to follow
36 | 
37 | ### Implementation Blueprint
38 | - Start with pseudocode showing approach
39 | - Reference real files for patterns
40 | - Include error handling strategy
41 | - list tasks to be completed to fullfill the PRP in the order they should be completed
42 | 
43 | ### Validation Gates (Must be Executable) eg for python
44 | ```bash
45 | # Syntax/Style
46 | ruff check --fix && mypy .
47 | 
48 | # Unit Tests
49 | uv run pytest tests/ -v
50 | 
51 | ```
52 | 
53 | *** CRITICAL AFTER YOU ARE DONE RESEARCHING AND EXPLORING THE CODEBASE BEFORE YOU START WRITING THE PRP ***
54 | 
55 | *** ULTRATHINK ABOUT THE PRP AND PLAN YOUR APPROACH THEN START WRITING THE PRP ***
56 | 
57 | ## Output
58 | Save as: `PRPs/{feature-name}.md`
59 | 
60 | ## Quality Checklist
61 | - [ ] All necessary context included
62 | - [ ] Validation gates are executable by AI
63 | - [ ] References existing patterns
64 | - [ ] Clear implementation path
65 | - [ ] Error handling documented
66 | 
67 | Score the PRP on a scale of 1-10 (confidence level to succeed in one-pass implementation using claude codes)
68 | 
69 | Remember: The goal is one-pass implementation success through comprehensive context.
```

PRPs/templates/prp_base.md
```
1 | name: "Base PRP Template v2 - Context-Rich with Validation Loops"
2 | description: |
3 | 
4 | ## Purpose
5 | Template optimized for AI agents to implement features with sufficient context and self-validation capabilities to achieve working code through iterative refinement.
6 | 
7 | ## Core Principles
8 | 1. **Context is King**: Include ALL necessary documentation, examples, and caveats
9 | 2. **Validation Loops**: Provide executable tests/lints the AI can run and fix
10 | 3. **Information Dense**: Use keywords and patterns from the codebase
11 | 4. **Progressive Success**: Start simple, validate, then enhance
12 | 5. **Global rules**: Be sure to follow all rules in CLAUDE.md
13 | 
14 | ---
15 | 
16 | ## Goal
17 | [What needs to be built - be specific about the end state and desires]
18 | 
19 | ## Why
20 | - [Business value and user impact]
21 | - [Integration with existing features]
22 | - [Problems this solves and for whom]
23 | 
24 | ## What
25 | [User-visible behavior and technical requirements]
26 | 
27 | ### Success Criteria
28 | - [ ] [Specific measurable outcomes]
29 | 
30 | ## All Needed Context
31 | 
32 | ### Documentation & References (list all context needed to implement the feature)
33 | ```yaml
34 | # MUST READ - Include these in your context window
35 | - url: [Official API docs URL]
36 |   why: [Specific sections/methods you'll need]
37 |   
38 | - file: [path/to/example.py]
39 |   why: [Pattern to follow, gotchas to avoid]
40 |   
41 | - doc: [Library documentation URL] 
42 |   section: [Specific section about common pitfalls]
43 |   critical: [Key insight that prevents common errors]
44 | 
45 | - docfile: [PRPs/ai_docs/file.md]
46 |   why: [docs that the user has pasted in to the project]
47 | 
48 | ```
49 | 
50 | ### Current Codebase tree (run `tree` in the root of the project) to get an overview of the codebase
51 | ```bash
52 | 
53 | ```
54 | 
55 | ### Desired Codebase tree with files to be added and responsibility of file
56 | ```bash
57 | 
58 | ```
59 | 
60 | ### Known Gotchas of our codebase & Library Quirks
61 | ```python
62 | # CRITICAL: [Library name] requires [specific setup]
63 | # Example: FastAPI requires async functions for endpoints
64 | # Example: This ORM doesn't support batch inserts over 1000 records
65 | # Example: We use pydantic v2 and  
66 | ```
67 | 
68 | ## Implementation Blueprint
69 | 
70 | ### Data models and structure
71 | 
72 | Create the core data models, we ensure type safety and consistency.
73 | ```python
74 | Examples: 
75 |  - orm models
76 |  - pydantic models
77 |  - pydantic schemas
78 |  - pydantic validators
79 | 
80 | ```
81 | 
82 | ### list of tasks to be completed to fullfill the PRP in the order they should be completed
83 | 
84 | ```yaml
85 | Task 1:
86 | MODIFY src/existing_module.py:
87 |   - FIND pattern: "class OldImplementation"
88 |   - INJECT after line containing "def __init__"
89 |   - PRESERVE existing method signatures
90 | 
91 | CREATE src/new_feature.py:
92 |   - MIRROR pattern from: src/similar_feature.py
93 |   - MODIFY class name and core logic
94 |   - KEEP error handling pattern identical
95 | 
96 | ...(...)
97 | 
98 | Task N:
99 | ...
100 | 
101 | ```
102 | 
103 | 
104 | ### Per task pseudocode as needed added to each task
105 | ```python
106 | 
107 | # Task 1
108 | # Pseudocode with CRITICAL details dont write entire code
109 | async def new_feature(param: str) -> Result:
110 |     # PATTERN: Always validate input first (see src/validators.py)
111 |     validated = validate_input(param)  # raises ValidationError
112 |     
113 |     # GOTCHA: This library requires connection pooling
114 |     async with get_connection() as conn:  # see src/db/pool.py
115 |         # PATTERN: Use existing retry decorator
116 |         @retry(attempts=3, backoff=exponential)
117 |         async def _inner():
118 |             # CRITICAL: API returns 429 if >10 req/sec
119 |             await rate_limiter.acquire()
120 |             return await external_api.call(validated)
121 |         
122 |         result = await _inner()
123 |     
124 |     # PATTERN: Standardized response format
125 |     return format_response(result)  # see src/utils/responses.py
126 | ```
127 | 
128 | ### Integration Points
129 | ```yaml
130 | DATABASE:
131 |   - migration: "Add column 'feature_enabled' to users table"
132 |   - index: "CREATE INDEX idx_feature_lookup ON users(feature_id)"
133 |   
134 | CONFIG:
135 |   - add to: config/settings.py
136 |   - pattern: "FEATURE_TIMEOUT = int(os.getenv('FEATURE_TIMEOUT', '30'))"
137 |   
138 | ROUTES:
139 |   - add to: src/api/routes.py  
140 |   - pattern: "router.include_router(feature_router, prefix='/feature')"
141 | ```
142 | 
143 | ## Validation Loop
144 | 
145 | ### Level 1: Syntax & Style
146 | ```bash
147 | # Run these FIRST - fix any errors before proceeding
148 | ruff check src/new_feature.py --fix  # Auto-fix what's possible
149 | mypy src/new_feature.py              # Type checking
150 | 
151 | # Expected: No errors. If errors, READ the error and fix.
152 | ```
153 | 
154 | ### Level 2: Unit Tests each new feature/file/function use existing test patterns
155 | ```python
156 | # CREATE test_new_feature.py with these test cases:
157 | def test_happy_path():
158 |     """Basic functionality works"""
159 |     result = new_feature("valid_input")
160 |     assert result.status == "success"
161 | 
162 | def test_validation_error():
163 |     """Invalid input raises ValidationError"""
164 |     with pytest.raises(ValidationError):
165 |         new_feature("")
166 | 
167 | def test_external_api_timeout():
168 |     """Handles timeouts gracefully"""
169 |     with mock.patch('external_api.call', side_effect=TimeoutError):
170 |         result = new_feature("valid")
171 |         assert result.status == "error"
172 |         assert "timeout" in result.message
173 | ```
174 | 
175 | ```bash
176 | # Run and iterate until passing:
177 | uv run pytest test_new_feature.py -v
178 | # If failing: Read error, understand root cause, fix code, re-run (never mock to pass)
179 | ```
180 | 
181 | ### Level 3: Integration Test
182 | ```bash
183 | # Start the service
184 | uv run python -m src.main --dev
185 | 
186 | # Test the endpoint
187 | curl -X POST http://localhost:8000/feature \
188 |   -H "Content-Type: application/json" \
189 |   -d '{"param": "test_value"}'
190 | 
191 | # Expected: {"status": "success", "data": {...}}
192 | # If error: Check logs at logs/app.log for stack trace
193 | ```
194 | 
195 | ## Final validation Checklist
196 | - [ ] All tests pass: `uv run pytest tests/ -v`
197 | - [ ] No linting errors: `uv run ruff check src/`
198 | - [ ] No type errors: `uv run mypy src/`
199 | - [ ] Manual test successful: [specific curl/command]
200 | - [ ] Error cases handled gracefully
201 | - [ ] Logs are informative but not verbose
202 | - [ ] Documentation updated if needed
203 | 
204 | ---
205 | 
206 | ## Anti-Patterns to Avoid
207 | - ❌ Don't create new patterns when existing ones work
208 | - ❌ Don't skip validation because "it should work"  
209 | - ❌ Don't ignore failing tests - fix them
210 | - ❌ Don't use sync functions in async context
211 | - ❌ Don't hardcode values that should be config
212 | - ❌ Don't catch all exceptions - be specific
```

examples/.gitkeep
```
```
