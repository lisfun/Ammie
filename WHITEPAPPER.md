**Ammie White Paper v0.1**

**f(symbols, scene) → Action + Explain**

**AMI: Auditable Machine Intelligence** – A symbol-first, scene-aware, LLM-assisted personal AI Agent architecture.

**Preamble:**
"Intelligence is the result of constraints, not scale."
We are releasing the Ammie (AMI) Technical White Paper v0.1. This is an attempt to return LLMs to their role as tools and let symbolic systems once again lead decision-making. We do not pursue omniscience; we pursue that every action is auditable and every error is traceable.

**Introduction: Why Symbolic Intelligence Can Succeed in the Age of LLMs**

In the history of artificial intelligence, Symbolic AI was once the earliest mainstream paradigm. It attempted to simulate human intelligence using logical rules, semantic networks, and knowledge bases. Its core belief was: intelligence can be reduced to the manipulation of symbols. However, by the late 1980s, Symbolic AI encountered insurmountable bottlenecks:
*   **Knowledge Acquisition Bottleneck:** All rules and facts required manual coding, which was not only time-consuming and laborious but also difficult to cover the infinite variations of the real world.
*   **Rigidity of Rules:** Symbolic systems lacked the ability to handle ambiguity, fuzziness, and common sense, often "breaking brittlely" when encountering situations not covered by rules.
*   **Lack of Context:** They could not effectively utilize contextual information, leading to understanding natural language only at a literal level.
*   **High Maintenance Costs:** As knowledge bases grew, managing rule conflicts and consistency became extremely difficult.

These flaws made symbolic systems struggle in real-world applications, eventually being overtaken by the wave of connectionism (neural networks). Large Language Models (LLMs), trained on massive data, have demonstrated astonishing language generation and comprehension abilities, seemingly signaling the end of Symbolic AI.

However, LLMs are not omnipotent. They are inherently probabilistic models, lacking stable knowledge representation, explainable reasoning chains, and controllable behavioral boundaries. In practical applications, we must constantly constrain LLMs through prompt engineering, function calling, output structuring, etc., to make them work reliably for specific tasks – precisely exposing the fundamental flaw of LLMs as "agents": they can be consulted, but they are difficult to trust.

The emergence of LLMs did not negate Symbolic AI; instead, it provided the missing piece of the puzzle.
*   **Automated Knowledge Acquisition:** LLMs can extract structured information from natural language, filling the knowledge bases of symbolic systems. Dictionaries, rules, and ontologies that once required manual coding can now be automatically generated through interaction with LLMs.
*   **Handling Ambiguity:** LLMs excel at understanding ambiguity, ellipsis, and colloquial expressions. They can provide candidate interpretations for symbolic parsing, with the symbolic system making the final decision based on context and rules.
*   **Providing Common Sense Background:** The vast world knowledge embedded in LLMs can assist symbolic systems in handling unseen concepts, avoiding brittle failures.

More importantly, symbolic systems retain irreplaceable advantages:
*   **Auditable:** Every decision can be traced back to explicit symbols and rules, not the black-box weights of neural networks.
*   **Evolvable:** Knowledge is stored in a structured format, allowing users to review, correct, and expand it at any time, enabling true personalized growth.
*   **Controllable:** Behavioral boundaries are defined by explicit rules, ensuring outputs are never unexpected.
*   **Local-First:** Symbolic systems are lightweight and efficient, capable of running entirely locally, protecting user privacy.

Therefore, the core philosophy of Ammie emerges naturally:
Let LLMs return to being tools, serving as "external knowledge sources" for the symbolic system; let the symbolic system lead decision-making, becoming the auditable and evolvable core of intelligence.
This is not a rejection of connectionism, but a synthesis of the strengths of both paradigms. Empowered by LLMs, symbolic intelligence can finally transcend its historical bottlenecks and move towards a truly practical, reliable, and personal agent.

**Core Files Overview**
Ammie Core v0.1 consists of the following **6 core files**. Any implementation MUST include equivalent modules.

| Filename | Responsibility |
| :--- | :--- |
| symbols.json | Bridge between symbol ↔ meaning, mapping natural language vocabulary to stable semantic symbols. |
| scenes.json | The "laws of physics" for scenes, defining the meta-model and dynamic rules for the 4Ws (WHO/WHAT/WHEN/WHERE). |
| ontology.json | Ontology tagging system, defining entity existence and executability, acting as the gatekeeper of semantic legality. |
| capabilities.json | Semantic → action mapping, declaring executable minimal action units and their interfaces. |
| llm_bridge.py | Minimalist LLM translator, encapsulating calls to language models with strictly limited output formats and permissions. |
| dialogue.py | Core dialogue engine, responsible for input parsing, scene maintenance, capability dispatching, and response generation. |

---

**symbols.json – The Bridge Between Symbol and Meaning**

**2.1 Responsibility**
Maps natural language vocabulary (including synonyms, colloquial variants) to stable semantic symbols (canonical symbols) for subsequent intent recognition.

**2.2 Basic Structure**
```json
{
  "version": "1.0.0",
  "symbols": {
    "open": {
      "canonical": "START",
      "pos": ["verb"],
      "aliases": ["begin", "launch", "turn_on"],
      "confidence": 0.92
    },
    "I": {
      "canonical": "SELF",
      "pos": ["pronoun"],
      "resolves_to": "user"
    },
    "music": {
      "canonical": "MUSIC",
      "pos": ["noun"],
      "intent": "PLAY_MUSIC"   // Optional, directly associate intent
    }
  }
}
```

**2.3 Design Principles**
*   ❌ Does NOT store full sentences or raw LLM output.
*   ✅ Stores ONLY stable meanings.
*   ✅ Allows multiple words/phrases to map to the same canonical symbol.
*   ✅ Supports similarity guessing (e.g., typos, dialects, colloquialisms) via `aliases` or confidence adjustments.

---

**scenes.json – The Laws of Physics for Scenes (4W)**

**3.1 Scene Definition**
A Scene is the **physical context** in which language occurs, not the semantics itself. In Ammie, a Scene MUST and can ONLY be constituted by the 4Ws:

| Dimension | Meaning | Example Values |
| :--- | :--- | :--- |
| WHO | Participants | "self", "user", "third_party" |
| WHAT | Event/Intent | "WORK", "ENTERTAINMENT" |
| WHEN | Time | "morning", "2025-03-21", "now" |
| WHERE | Space | "home", "office", "outdoor", "virtual" |

**3.2 Scene Grammar (Meta-model)**
```json
{
  "version": "1.0.0",
  "scene_model": {
    "WHO": {
      "types": ["self", "user", "third_party"],
      "default": "user"
    },
    "WHAT": {
      "types": ["intent", "object"],
      "required": true
    },
    "WHEN": {
      "types": ["now", "relative", "absolute"],
      "default": "now",
      "expiry": "30s"
    },
    "WHERE": {
      "types": ["local", "remote", "virtual"],
      "default": "virtual"
    }
  }
}
```

**3.3 Scene Dynamic Mechanisms (Scene+)**
Scene+ does not add dimensions but consists of the following three implicit mechanisms:
*   **Inheritance:** Fields not declared in the current Scene automatically inherit values from the previous Scene (unless explicitly overridden).
*   **Decay:** Each Scene field can have an expiration (e.g., `expiry`). After expiry, it automatically reverts to the default or null value.
*   **Resolution:** When user input conflicts with the current Scene, the new input takes precedence, and the conflict is recorded for subsequent learning.

**3.4 Scene Rules (Optional Extension)**
`scenes.json` can also contain concrete scene rules to trigger intents or capabilities directly under specific 4W combinations. For example:
```json
{
  "rules": [
    {
      "id": "rule_001",
      "conditions": {
        "WHERE": "home",
        "WHEN": "evening",
        "WHAT": "entertainment"
      },
      "action": {
        "intent": "PLAY_MUSIC",
        "params": { "playlist": "default" }
      },
      "priority": 10
    }
  ]
}
```

---

**ontology.json – Ontology Tagging System**

**4.1 Responsibility**
Ontology is used to determine: "Does this thing exist in Ammie's world, and is it executable?" It acts as the gatekeeper of semantic legality but does NOT perform reasoning or call the LLM.

**4.2 Basic Structure**
```json
{
  "version": "1.0.0",
  "entities": {
    "time": {
      "type": "abstract",
      "actions": ["get", "compare"]
    },
    "news": {
      "type": "information",
      "actions": ["fetch", "notify"]
    },
    "music": {
      "type": "media",
      "actions": ["play", "stop", "search"]
    }
  },
  "intent_to_capability": {
    "PLAY_MUSIC": "play_music",
    "QUERY_TIME": "get_time"
  }
}
```

**4.3 Design Principles**
*   ❌ Does NOT perform reasoning (e.g., does not automatically derive subclass relationships). (Allows single-level parent association, prohibits multi-level recursion to ensure audit trail clarity.)
*   ❌ Does NOT store instance data (e.g., "Beethoven's 5th Symphony"). (Ontology stores only the schema. Instance data is managed by a separate Memory module or RAG, with storage boundaries defined by the user.)
*   ✅ Only answers: Given an entity and an action, is it legal?
*   ✅ Intent-to-capability mapping can be placed here or in `capabilities.json`, depending on project scale.

---

**capabilities.json – Capability Mapping**

**5.1 Definition**
Capability = The smallest executable action unit, including input/output interfaces, potentially corresponding to a script or function.
```json
{
  "version": "1.0.0",
  "capabilities": [
    {
      "name": "play_music",
      "intent": "PLAY_MUSIC",
      "description": "Play music",
      "input_schema": {
        "song": { "type": "string", "optional": true },
        "playlist": { "type": "string", "optional": true }
      },
      "output_schema": {
        "status": { "type": "string", "enum": ["playing", "error"] }
      },
      "tags": ["entertainment", "media"],
      "executor": "music_player"   // Points to concrete implementation module
    },
    {
      "name": "get_time",
      "intent": "QUERY_TIME",
      "description": "Get current time",
      "input_schema": {},
      "output_schema": {
        "time": { "type": "string" }
      },
      "tags": ["tool"],
      "executor": "system_time"
    }
  ]
}
```

**5.2 Capability Discovery Mechanism (Advanced Feature)**
When a user request cannot be matched with existing capabilities, the system can:
1.  Submit the user input and current scene to the LLM.
2.  The LLM returns a JSON description of candidate capabilities (must conform to `capabilities.json` schema).
3.  Store the candidate in a "pending review" area. It can be added to the formal capability library after user confirmation or several successful automatic uses.

---

**llm_bridge.py – Minimalist Translator**

**6.1 Positioning**
The LLM is **not** an agent, but merely an unreliable yet powerful external interpreter. All calls must adhere to strict constraints.

**6.2 Interface Design**
```python
class LLMBridge:
    def __init__(self, config):
        self.backend = config.get("backend", "openai")  # or "ollama"
        self.model = config.get("model", "gpt-3.5-turbo")
        self.cache = {}

    def ask(self, prompt: str, expected_schema: dict = None) -> dict:
        """Sends a request, returns JSON. Retries or returns None if it doesn't match the schema."""
        # Implementation includes caching, retries, timeout, format validation
```

**6.3 Strict Limitations**
*   ✅ **Allowed ONLY for:**
    *   Word sense induction (explaining unknown words)
    *   Similarity suggestions (providing candidate intents or capabilities)
    *   Outputting JSON format
*   ❌ **Forbidden from:**
    *   Directly writing to core files (During the initial symbol and ontology construction phase, we trust LLM output by default, allowing direct writing. Humans act as post-hoc correctors, not pre-hoc censors.)
    *   Making execution decisions
    *   Controlling the process flow
    *   Generating free-text responses (unless used for human-readable explanations)

---

**dialogue.py – Core Dialogue Engine**

**7.1 Input Processing Flow**
```
User Input
    ↓
Tokenization & Symbol Matching (symbols.json)
    ↓
Parse Basic Frame (verb, object, modifiers)
    ↓
Scene Completion (Use current Scene to fill missing slots, disambiguate)
    ↓
Ontology Legality Check (ontology.json)
    ↓
Capability Matching (capabilities.json)
    ↓
Execution (or trigger disambiguation/learning)
    ↓
Generate Output Response
```

**7.2 Core Data Structures**
*   **Scene Class:** Maintains the 4W information for the current session, including an objective layer (e.g., system time) and a mentioned layer (e.g., location mentioned by user).
*   **DialogState Class:** Records pending clarification questions, retry counts, etc.

**7.3 Key Methods (Conceptual)**
```python
def process_input(user_input: str) -> str:
    # Full processing logic
    pass

def _parse(text: str) -> ParsedFrame:
    # Simple parsing based on symbols.json
    pass

def _resolve_capabilities(parsed: ParsedFrame, scene: Scene) -> List[Capability]:
    # Returns a list of candidate capabilities based on intent and scene
    pass

def _execute_capability(cap: Capability, params: dict) -> str:
    # Simulate or actually execute, returning a user-readable result
    pass

def _ask_clarification(candidates: List[Capability]) -> str:
    # Generates a clarification question and records the state
    pass
```

**7.4 Reverse Sentence Construction (Autonomous Explanation Mechanism)**
Ammie MUST use **only its already learned vocabulary** to explain its actions.
If the system refuses an action, the explanation MUST be constructed autonomously based on the S-V-O (Subject-Verb-Object) structure of its symbols, **NOT** generated directly by the LLM.

**Workflow Example:**
1.  **Input:** "Can you play basketball?"
2.  **Recognition:** The system finds "basketball" as an unknown word.
3.  **LLM Inquiry:** Queries the LLM to get the canonical symbol and ontology attributes for "basketball".
4.  **Update:** Automatically supplements `symbols.json` and `ontology.json`.
5.  **Autonomous Construction:**
    *   **Logic:** ammie (S) + NEG_POTENTIAL (V_mod) + ACTION_PLAY (V) + OBJ_BASKETBALL (O).
6.  **Output:** "I (S) + cannot (V_mod) + play (V) + basketball (O)."

---

**Core Abstraction**

**Behavior Function:**
`f(symbols, scene) → Action + Explain`

Where:
*   `symbols`: The user's natural language input, processed into symbols.
*   `scene`: The 4W context of the current session.
*   `action`: The action executed by the system (can be a capability call, a question, a learning request, etc.).
*   `explain`: An explanation of the action constructed from symbols.

This function is NOT an end-to-end model, but a decomposable causal chain where each step is auditable.

---

**Key Mechanism Extensions (Optional, but Recommended)**

**9.1 Disambiguation System**
When the confidence for multiple candidate capabilities is below a threshold, the system proactively asks questions to clarify intent.
*   **Trigger Condition:** Candidate list length > 1, and highest confidence < threshold (e.g., 0.7).
*   **Question Generation:** Generate a natural language question based on candidate capability names or parameters (e.g., "Do you want to play music or video?").
*   **Answer Parsing:** Determine the user's choice through keyword matching or simple semantic understanding.
*   **State Management:** The clarification context is stored in `DialogState` and cleared after processing the user's answer.

**9.2 User Rules Library**
Allows users to explicitly teach the system to perform specific actions in specific scenes.
*   **Rule Format:** Similar to scene rules, but with higher priority than general rules.
*   **Storage Location:** Can be independent as `user_rules.json` or merged into `scenes.json` with a source marker.
*   **Management Interface:** Provide commands or a UI to view, add, and delete rules.

**9.3 Behavior Pattern Detection & Proactive Suggestions**
The system can record users' historical choices in different scenes. When a repetitive pattern is detected, it can proactively ask if the user wants to create a rule.
*   **Recorded Data:** `(scene_fingerprint, input_pattern, selected_action, timestamp)`
*   **Detection Algorithm:** Statistics on the distribution of user choices under the same pattern. If consistency exceeds a threshold (e.g., 3 consecutive times), a suggestion is triggered.
*   **Interaction:** "I noticed you often play music when you're at home in the evening. Should I do this automatically in the future?" The user can choose "Yes" to create a rule, "No" to ignore, or "Don't ask again" to disable this feature.

**9.4 Memory Module**
Long-term storage of user preferences, common entities, interaction history summaries, etc., used for initializing scenes and optimizing rules.
*   **Storage:** Local JSON file or lightweight database (e.g., SQLite).
*   **Content:** Does NOT store raw conversations, only statistical information and explicitly taught user data.
*   **Privacy:** All data is stored locally, and users can view and clear it at any time.

---

**Non-Goals**
*   ❌ Emotion simulation
*   ❌ Persona扮演
*   ❌ End-to-end large model
*   ❌ Unexplainable reasoning
*   ❌ Cloud dependency
*   ❌ Multi-modal perception (initial phase)

**Conclusion**
Ammie is not a replacement for LLMs, but an attempt to return LLMs to their role as tools. Without LLMs, this system would be difficult to scale; if LLMs were to dominate, this system would inevitably spiral out of control.
Through a symbol-first, scene-aware, locally-run design, Ammie aims to become a truly auditable, evolvable personal agent that is loyal to its user.
Community participation in discussion and contribution is welcome.

**Version History**
*   v0.1 (2026-02-17): Initial core specification release.
