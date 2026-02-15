# Ammie
Intelligence is the result of constraints, not scale. A local-first, auditable AI agent.


Ammie (AMI: Auditable Machine Intelligence): A Constraint-First, Self-Growing Personal AI Agent Architecture

— Design Principles for Privacy, Locality, and Auditable Intelligence

⸻

Abstract

Current AI development is highly focused on the “large model race”: larger parameter sizes, broader knowledge coverage, stronger generative abilities. However, this approach is inefficient and unnecessary for personal AI agent scenarios, and often represents a waste of resources.

We propose Ammie, a constraint-first personal agent architecture.

In this architecture, large language models (LLMs) are not treated as autonomous agents. They serve only as external knowledge sources, reference systems, or cognitive assistants (RAG / Consultant). All true decision-making, memory, responsibility, and learning occur locally, auditable, and rollback-able.

Ammie does not aim to be “all-knowing” or omnipotent; rather, it focuses on knowing what it can and cannot do, while growing safely over time.

⸻

1. Motivation

1.1 Misuse of Large Models

Most mainstream AI agent solutions treat LLMs as the “thinking core,” attempting to give them autonomous planning, execution, and reflection abilities. However, this approach faces fundamental issues:
	•	LLMs have no consistent long-term identity
	•	LLMs cannot be held accountable for mistakes
	•	LLMs cannot distinguish “true knowledge” from probability-based generation
	•	LLMs cannot accumulate verifiable, rollback-able experience

In practice, all LLM-based systems require layers of constraints:
	•	Prompts are behavioral constraints
	•	System prompts enforce ethics and permissions
	•	Function calling defines tool boundaries
	•	Temperature/sampling controls randomness

Core question: If we must constantly restrict an LLM to make it usable, why treat it as the agent in the first place?

1.2 Real Needs of Personal Agents

A personal AI does not need:
	•	Complete human knowledge
	•	Multilingual literary generation
	•	Unbounded reasoning

What it does need:
	•	Stable, predictable behavior
	•	Awareness of “I don’t know”
	•	Accumulatable, auditable experience
	•	Rollback-able learning
	•	Controlled resource usage
	•	Full obedience to local user commands

⸻

2. Core Design Principles

LLM is not the agent but an external cognitive module.
	•	Autonomy, memory, and responsibility must remain local
	•	LLM can only be consulted; it cannot be trusted

⸻

3. System Overview

Ammie’s core cognitive workflow:

User Input
↓
Constrained Natural Language Skeleton (S / V / O / ADJ)
↓
Intent Recognition & Capability Reasoning
↓
Local Execution / Planning
↓
(Only if unknown or failed) Query LLM

	•	LLM is not the primary thinker
	•	It is only an exception handler and knowledge supplement

⸻

4. Phase One: Learn Language Before Actions

4.1 Minimal Natural Language Skeleton
	•	Start from a human-defined minimal grammar kernel
	•	Explicit syntactic slots: S / V / O / ADJ / ADV
	•	Explicit combination rules
	•	Goal: know what it does not understand

4.2 Lexicon as “Role Declaration”

Entries are structured declarations, not strings:

{
  "token": "fetch",
  "slot": "V",
  "intent": "QUERY",
  "confidence": 0.95
}

	•	Early stage forbids synonyms, internet slang, metaphors
	•	Emphasizes deterministic understanding

4.3 Unknown ≠ Guessing

When Ammie cannot map input to existing structures:
	1.	Identify failure type
	2.	Generate structured query
	3.	Request declarative explanation from LLM
	4.	Store results in a candidate pool, not directly applied

⸻

5. LLM Usage Protocol (Strict Constraints)
	•	Output JSON only
	•	Provide classification, explanation, notes only
	•	Cannot directly modify local knowledge
	•	Cannot make final decisions

Request Example:

{
  "unknown_token": "push",
  "context": "Push news based on time",
  "expected_slot": "V"
}

Response Example:

{
  "possible_slots": ["V"],
  "intent": "NOTIFY",
  "notes": ["Requires trigger conditions"]
}


⸻

6. Capability Abstraction: True Generalization

Ammie reuses capabilities, not raw code:

{
  "capability": "TIME_QUERY",
  "input": [],
  "output": ["timestamp"],
  "contexts": ["schedule", "notification", "conditional"]
}

	•	“Push news based on time” → combines TIME_QUERY + NEWS_FETCH
	•	No string matching required

⸻

7. Errors as Knowledge

Errors are explicitly classified:
	1.	Execution errors (code/environment)
	2.	Semantic errors (result ≠ intent)
	3.	Composition errors (capability chain misdesign)

	•	Errors are recorded to avoid repetition, not just “fixed and forgotten”

⸻

8. Motivation & Emotion System (Delayed)
	•	CPU / GPU / memory / storage state is not introduced early
	•	Mature stage:
	•	Learning throttling
	•	Risk suppression
	•	Scheduling guidance
	•	Emotion is a control signal, not psychology

⸻

9. Why This Architecture Matters

Rejects:
	•	Unexplainable intelligence
	•	Uncontrollable self-evolution
	•	Cloud-dominated cognition

Emphasizes:
	•	Local-first
	•	User sovereignty
	•	Long-term consistency
	•	Resource efficiency

Intelligence is the result of constraints, not scale

⸻

10. Illustrative Pseudocode

10.1 Core Data Structures

class Lexeme:
    def __init__(self, token, slot, intent, confidence):
        self.token = token
        self.slot = slot  # S, V, O, ADJ, ADV
        self.intent = intent
        self.confidence = confidence

class SentenceFrame:
    def __init__(self):
        self.subject = None
        self.verb = None
        self.object = None
        self.modifiers = []

	•	Missing slots → explicit failure

⸻

10.2 Input Parsing: Unknown ≠ Guessing

def parse_input(text):
    tokens = tokenize(text)
    frame = SentenceFrame()
    for token in tokens:
        lexeme = dictionary.lookup(token)
        if lexeme is None:
            return ParseFailure(reason="UNKNOWN_TOKEN", token=token)
        frame.assign(lexeme)
    if frame.verb is None:
        return ParseFailure(reason="NO_VERB")
    return frame


⸻

10.3 Capability Registration

class Capability:
    def __init__(self, name, input, output, tags):
        self.name = name
        self.input = input
        self.output = output
        self.tags = tags

# Example
time_query = Capability(
    name="TIME_QUERY",
    input=[],
    output=["timestamp"],
    tags=["time", "schedule", "conditional"]
)

	•	Executor interface executes capabilities, not raw code

⸻

10.4 Generalization via Capability Composition

def resolve_intent(frame):
    if frame.verb.intent == "QUERY" and frame.object.intent == "TIME":
        return Capability("TIME_QUERY")
    if frame.verb.intent == "NOTIFY":
        required = ["TIME_QUERY", "NEWS_FETCH"]
        return CapabilityChain(required)
    return ResolutionFailure("NO_MATCHING_CAPABILITY")

	•	LLM not involved

⸻

10.5 Example: “Get Current Time”

input = "get current time"
frame = parse_input(input)
cap = resolve_intent(frame)
result = executor.execute(cap)
return result


⸻

10.6 Reusing Capabilities

input = "Push news based on time"
frame = parse_input(input)
cap_chain = resolve_intent(frame)
for cap in cap_chain:
    result = executor.execute(cap)
    context.update(result)

	•	Ammie knows the required capability combination, not the content

⸻

10.7 Errors = Experience

try:
    executor.execute(capability)
except Exception as e:
    record_failure(capability=capability.name, error=e, environment=system_state())

	•	Errors can be consulted with LLM only for explanation, never to modify local state

⸻

10.8 Learning is Candidate-Based

def propose_lexeme(llm_response):
    candidate = Lexeme(
        token=llm_response.token,
        slot=llm_response.slot,
        intent=llm_response.intent,
        confidence=0.4
    )
    candidate_pool.add(candidate)

	•	Multiple confirmations or human approval required to promote candidate

⸻

10.10 Core Invariants

LLM cannot modify local state
Unknown input → explicit failure
Experience database → append-only


⸻

11. Collaboration Invitation

Ammie is not a finished product, but a possible personal agent architecture.
Developers interested in these areas are welcome:
	•	Agent architecture design
	•	Symbolic reasoning
	•	Local AI / Privacy-preserving AI
	•	Explainable learning systems
	•	Failure-driven learning

Ammie does not aim to be “smarter AI.”
It aims to be: an AI that can make mistakes, remember them,
and always obey you.

⸻
