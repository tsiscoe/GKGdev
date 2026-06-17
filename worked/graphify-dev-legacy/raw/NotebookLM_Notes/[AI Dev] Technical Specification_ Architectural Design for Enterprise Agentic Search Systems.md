# [AI Dev] Technical Specification: Architectural Design for Enterprise Agentic Search Systems

# \[AI Dev\] Technical Specification: Architectural Design for Enterprise Agentic Search Systems

## 1. Executive Overview of Agentic RAG Systems

The enterprise landscape is transitioning from traditional Retrieval-Augmented Generation (RAG) toward autonomous agentic architectures. In legacy RAG workflows, retrieval is a linear, pre-defined process where search results are "dumped" into the Large Language Model’s (LLM) context window. Agentic RAG evolves this by delegating tool selection and retrieval strategy to the LLM's reasoning engine. The system does not merely receive data; it autonomously determines the "where and how" of information fetching based on query intent.

The core architectural distinction lies in the shift from passive consumption to transparent multi-hop execution. While standard RAG is often a "black box" to the user, an agentic system allows for visible tool invocation—a critical factor in User Trust and Verification UX. When a bot integrated into Slack or Teams is seen actively "querying internal documentation" or "searching employee handbooks," it provides a psychological anchor for the user, validating the accuracy of the response. This strategic shift requires a transition from static retrieval pipelines to dynamic decision-making frameworks supported by robust infrastructure.

## 2. Infrastructure and Deployment Strategy

Production-grade agentic systems must balance cost-efficiency with rigid latency requirements. Because enterprise search agents are typically event-driven—triggered by Slack webhooks or Teams events—serverless architectures are the preferred deployment model to minimize idle compute costs.

### Serverless Evaluation: Lambda vs. Modal
\*   \*\*AWS Lambda:\*\* The "battle-tested" standard. It offers the highest reliability for production environments, though it requires sophisticated management of "cold starts" through container warmers or provisioned concurrency.
\*   \*\*Modal:\*\* A modern alternative optimized for LLM workloads and long-running ETL processes. While it offers superior developer experience and highly competitive CPU pricing, it is less battle-tested than AWS. On free tiers, it is prone to occasional 500 errors and higher latency during resource allocation.

To mitigate latency, architects should implement background tasks to pre-spin resources when a container starts, ensuring the agent is ready for invocation.

### Economic Considerations for Agentic Systems

| Category | Cost Driver | Strategic Consideration |
| :--- | :--- | :--- |
| \*\*Engineering\*\* | Development & Prompting | Significant investment in prompt engineering, chunking logic, and output parsing. |
| \*\*Cloud Overhead\*\* | Serverless Functions | AWS Lambda or Modal; costs scale with query volume but remain minimal for event-driven bots. |
| \*\*Storage\*\* | Vector Databases | Free tiers (Zilliz/Qdrant) typically cover 1–5GB. Costs scale rapidly beyond a few thousand chunks. |
| \*\*Embeddings\*\* | OpenAI \`text-embedding-3-small\` | Highly economical; negligible cost even for 1–10 million text segments. |
| \*\*LLM API Calls\*\* | Model Selection | Agentic loops require 2–4 calls per run. This is the primary operational variable. |

Architectural priority is given to low-cost models like GPT-4o-mini or Gemini Flash 2.0. These models maintain monthly operational costs between $10–$50 for typical organizational usage, whereas high-reasoning models (GPT-4o) can increase costs by two orders of magnitude without proportional gains in simple retrieval tasks.

## 3. Data Ingestion and Transformation Pipeline

The quality of the ingestion pipeline sets the performance ceiling for the entire system. Sophisticated LLMs cannot compensate for fragmented or context-poor data chunks.

### Document Processing and Context Expansion
To ensure high-fidelity retrieval, we employ the following processing strategies:
\*   \*\*PDF Extraction:\*\* Use Docling to maintain structural integrity, extracting tables and images while preserving the hierarchy of headings and paragraph relationships.
\*   \*\*Custom Web Crawling:\*\* Crawlers must analyze HTML elements (anchor tags, headers) to determine logical split points rather than relying on arbitrary character counts.
\*   \*\*Context Expansion Patterns:\*\* Implement "Parent-Child" chunking or "Surrounding Chunk Retrieval." By fetching the adjacent blocks of text during the retrieval phase, we provide the LLM with the necessary context that a single similarity-matched chunk might lack.

### Traceability and Summarization
Metadata is the backbone of the "Citation Synthesizer." Every chunk must be tagged with persistent identifiers: URLs, page numbers, block IDs, and permalinks. This ensures the agent can provide verifiable citations.

Furthermore, we utilize LLM-generated summarizations as "high-authority" chunks. These summaries are prioritized during the initial retrieval phase, acting as entry points to scattered datasets. By labeling these as high-authority, the agent can quickly identify the most relevant document before performing a deep-dive search into specific sub-sections.

## 4. Vector Storage and Retrieval Optimization

The vector database must support a hybrid of semantic and keyword-based search to handle the diversity of enterprise queries.

### Vector Database Evaluation
\*   \*\*Qdrant & Milvus:\*\* Recommended for production due to generous cloud free tiers (1–5GB) and robust support for both dense and sparse vectors.
\*   \*\*Weaviate:\*\* A feature-rich alternative, though it carries a higher cost profile for managed cloud instances.
\*   \*\*pgvector/Redis:\*\* Optimal for teams seeking to leverage existing relational or in-memory infrastructure for vector capabilities.

### Hybrid Search and the "Alphanumeric Failure"
A critical architectural requirement is the implementation of Hybrid Search. Semantic (dense) search is excellent for "fuzzy" matching—for example, linking a query about "perks" to a document titled "Employee Benefits." However, dense vectors frequently fail on exact identifiers.

\*\*Technical Requirement:\*\* Developers must configure sparse vectorizers (such as BM25) to handle alphanumeric patterns. Without this, a search for a specific certificate code like \*\*"CAT-00568"\*\* will likely fail, as the semantic embedding may not prioritize the literal string match. Sparse vectors ensure these identifiers are indexed and retrieved with 100% precision.

Following retrieval, the system must apply deduplication and re-ranking to filter irrelevant nodes. This reduces the "noise" sent to the LLM, directly improving citation accuracy and synthesis quality.

## 5. The Agentic Logic Layer: Frameworks and Orchestration

Agent frameworks like LlamaIndex provide necessary abstractions for tool-use and citation management. We utilize the \`FunctionAgent\` to manage tool execution and the \`CitationQueryEngine\` to ensure every output is backed by source nodes.

### The "Double-Call" Architecture
To optimize the user experience and bypass the latency of booting a full agent for trivial queries, we implement a two-stage logic:
1.  \*\*Intent Classification (Logic Call):\*\* A lightweight LLM call determines if the query requires tool-use.
2.  \*\*Agent Invocation:\*\* The full agentic loop is only triggered if the intent classifier confirms that retrieval is necessary.

### Framework Production Risks
While frameworks are ideal for prototyping, they introduce significant risks in production.
\*   \*\*Query Over-Simplification:\*\* LlamaIndex's internal optimization may reduce a user's query too aggressively, stripping away critical context before it reaches the retrieval stage.
\*   \*\*Citation Context Blindness:\*\* A known limitation of the \`CitationQueryEngine\` is that it often lacks access to the full conversation history, leading to poor synthesis in multi-turn dialogues.
\*   \*\*Hidden Latency:\*\* Framework abstractions can mask bottlenecks. We recommend transitioning to direct API calls for the core logic in high-scale environments to regain control over the workflow and reduce overhead.

## 6. Production Performance and System Maintenance

The "Performance Trio" of Latency, Prompting, and Chunking defines the operational success of the agent.

\*   \*\*Latency Targets:\*\* A production agent should respond within \*\*8–13 seconds\*\*. To achieve this, architects should prioritize lower-latency models (GPT-4o-mini), minimize framework overhead, and use background tasks to keep serverless functions warm.
\*   \*\*State and Memory:\*\* To maintain conversational continuity, the architecture must implement a sliding context window by fetching the last \*\*3–6 messages\*\* from the Slack API history. This provides sufficient context for follow-up questions without bloating the context window or confusing the agent's reasoning.
\*   \*\*Dynamic Updates:\*\* For data freshness, while change-detection is ideal, a pragmatic "periodic re-embedding" strategy is often more sustainable. This involves a scheduled refresh of the vector store with updated metadata tags to ensure the agent is not hallucinating based on stale documentation.
\*   \*\*Observability:\*\* Implement \*\*Phoenix (by Arize)\*\* for deep tracing of the agentic chain. This allows engineers to identify exactly where latency occurs—whether in the retrieval, re-ranking, or synthesis stage—providing the visibility required to maintain a reliable enterprise system.
