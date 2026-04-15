# Product Requirements Document (PRD)

## AI/Human Interaction Layer for Intent Modeling, Explanation, and Mockup Generation

**Document status:** Draft for implementation handoff
**Audience:** Product Manager, Designer, Developer, AI Agent / Implementation Agent
**Primary stack constraints:** vue-flow, Tailwind, Nuxt.js
**Explicit exclusions:** No code-level implementation details, no version pinning, no framework lock beyond the technologies listed above

---

## 1. Executive Summary

This product is an **AI/Human interaction layer** that helps a human express intent to an AI and helps the AI explain, clarify, and visualize that understanding back to the human.

The core idea is simple:

- A human should be able to express an idea visually, quickly, and without needing to write a full technical specification.
- An AI should be able to interpret that visual intent in a structured way.
- The AI should be able to respond not only with text, but with visual explanations, flow diagrams, mockups, and structured documentation.
- The system should support round-tripping between **canvas interaction**, **structured semantic intent**, **markdown artifacts**, and **tool-driven AI actions**.

The product is not just a whiteboard and not just a chat interface. It is a **shared reasoning surface** where humans and AI collaborate on understanding, refining, and documenting intent.

This PRD is written to be understandable without any prior knowledge of earlier discussions, internal projects, or source conversations.

---

## 2. Problem Statement

Existing human/AI interfaces are weak in three areas:

1. **Humans struggle to express intent precisely** in plain chat alone.
   - Users often think spatially, visually, and relationally.
   - They may know what they want but not how to phrase it in a complete prompt.

2. **AI struggles when user intent is underspecified or scattered**.
   - Long text prompts are often ambiguous.
   - Important constraints, flows, dependencies, and assumptions are easy to miss.

3. **AI responses are often not easy for humans to validate**.
   - A block of text may not clearly show how a system works.
   - A user may need diagrams, mockups, highlighted uncertainties, and explanation overlays.

The result is a repeated translation problem:

- Human idea → vague text
- AI interpretation → uncertain output
- Human correction → more text
- AI revision → more drift

The product must reduce this friction by giving both parties a **shared visual-semantic medium**.

---

## 3. Vision

Create a system where:

- the **human can model intent visually and incrementally**,
- the **AI can convert that into structured semantic understanding**,
- the **AI can illustrate its understanding back to the human**,
- and the resulting work can be persisted into **markdown artifacts** and **tool-driven workflows**.

In practical terms, the product should feel like:

- a visual intent board,
- an AI-assisted explainer canvas,
- a mockup generation surface,
- and a documentation bridge.

---

## 4. Product Goals

### 4.1 Primary Goals

1. **Make user intent easy to express**
   - Support visual composition rather than forcing prompt-only interaction.
   - Reduce the need for the user to be precise in purely textual form.

2. **Make AI input easy to understand**
   - Convert human interactions into a structured intent model.
   - Preserve meaning beyond freeform drawing or layout.

3. **Make AI output easy to validate**
   - Allow the AI to explain visually.
   - Let the AI annotate, question, propose alternatives, and render mockups.

4. **Support durable artifacts**
   - Allow the system to generate markdown files suitable for review, version control, collaboration, and downstream workflows.

5. **Support round-trip collaboration**
   - Changes on canvas, in chat, in tool calls, or in markdown should flow through a consistent semantic layer instead of becoming disconnected sources of truth.

### 4.2 Secondary Goals

- Reduce ambiguity in AI collaboration.
- Improve trust in AI-generated understanding.
- Enable handoff to human developers, designers, or future AI agents.
- Provide a foundation for later automation, planning, implementation, and validation workflows.

---

## 5. Non-Goals

This project does **not** aim to be:

- a generic freeform whiteboard,
- a pure chat assistant,
- a code editor,
- a final visual design tool competing with high-fidelity design suites,
- a workflow execution engine,
- or a markdown-only documentation system.

This project may later connect to such systems, but its focus is the **interaction layer between human intent and AI understanding**.

---

## 6. Intended Users

### 6.1 Primary User Types

**1. Business / product user**

- Has goals, constraints, examples, and workflows in mind.
- Needs to express intent without formal system design language.

**2. PM / designer / analyst**

- Needs to refine scope, flows, edge cases, and user journeys.
- Needs visual explanation and structured outputs.

**3. Developer / technical architect**

- Needs semantic clarity, durable artifacts, and implementation-ready structure.

**4. AI agent**

- Needs a compact, structured, unambiguous representation of what the human means.
- Needs access to tool-driven actions and markdown projections.

### 6.2 Core User Need

All user types need a shared surface where intent can be:

- created,
- clarified,
- transformed,
- explained,
- and persisted.

---

## 7. Product Principles

1. **Visual first, but semantically grounded**
   A canvas alone is not enough. Visual objects must map to meaning.

2. **Structure over pixel-dependence**
   The AI should reason primarily over semantic objects and relations, not over raw coordinates or screenshots.

3. **Constrained freedom**
   The interface should feel flexible to the human, but the system should encourage a controlled visual language that stays machine-readable.

4. **Round-trip without drift**
   Canvas, markdown, chat, and tool-driven actions must not diverge into competing truths.

5. **Explainability is a first-class feature**
   The AI must be able to show its reasoning in human-friendly ways, not only produce final outputs.

6. **Documentation should be a projection, not a burden**
   Markdown should be generated and maintained from the semantic model rather than requiring the user to manually duplicate work.

7. **Human override is always allowed**
   The human must be able to correct the AI at any point through chat, canvas edits, or markdown edits.

---

## 8. Conceptual Model

The product is built around **three representations** of the same underlying work.

### 8.1 Representation A: Visual Canvas

The canvas is the human-friendly interaction surface.

It is used for:

- intent sketching,
- flow modeling,
- grouping,
- annotation,
- explanation,
- and mockup illustration.

This is the primary direct manipulation layer and will be implemented with **vue-flow**.

### 8.2 Representation B: Semantic Intent Model

The semantic intent model is the canonical structured meaning layer.

It represents:

- what objects exist,
- what kind of things they are,
- how they relate,
- what the user wants,
- what is known,
- what is uncertain,
- and what the AI believes the current understanding is.

This representation should be the system’s **operational source of truth**.

### 8.3 Representation C: Markdown Artifacts

Markdown files are durable, readable, diff-friendly, and portable projections of the semantic model.

They are used for:

- reviews,
- handoffs,
- repository storage,
- planning artifacts,
- and future implementation workflows.

Markdown is important, but it is **not** the highest-fidelity representation.

---

## 9. Core Product Modes

### 9.1 Intent Mode

The human expresses intent.

Typical activities:

- placing semantic shapes,
- connecting concepts,
- attaching constraints,
- identifying user goals,
- outlining workflows,
- highlighting uncertainty,
- and sketching rough structure.

The system should encourage the user to express meaning using known object types rather than arbitrary drawing.

### 9.2 Explain Mode

The AI explains back to the human.

Typical activities:

- annotating flows,
- highlighting missing information,
- showing cause/effect relationships,
- presenting alternative interpretations,
- calling out assumptions,
- and visually summarizing the current understanding.

### 9.3 Mockup Mode

The AI generates human-readable interface or process mockups from the semantic model.

Typical activities:

- low-fidelity UI layouts,
- screen grouping,
- interaction state sketches,
- flow previews,
- and visual examples of how a system could work.

### 9.4 Documentation Mode

The system generates or updates markdown artifacts.

Typical outputs:

- intent summaries,
- flows,
- decisions,
- risks,
- open questions,
- screen descriptions,
- and handoff material.

---

## 10. Functional Requirements

### 10.1 Canvas and Visual Authoring

The system must:

- provide a canvas-based interaction layer using vue-flow,
- support a constrained set of semantic object types,
- allow drag-and-drop placement,
- allow visual connections between related objects,
- support grouping and layout organization,
- support object inspection and editing,
- support annotations and callouts,
- support selection-based AI actions,
- and support zoom, pan, and multi-object editing behavior expected from a modern canvas.

The system should:

- discourage raw unstructured drawing as the primary authoring method,
- provide templates and starter patterns,
- and keep authoring understandable for non-technical users.

### 10.2 Semantic Object Types

The product must support a defined, extensible visual language. At minimum, the conceptual system should support categories such as:

- Goal
- Constraint
- Question
- Actor
- Screen
- Component
- Data
- Flow Step
- Decision
- Example
- Risk
- Note

The exact final taxonomy may evolve, but the system must begin with a manageable set of types that are meaningful both to humans and AI.

### 10.3 Relations / Links

The system must support explicit typed relations between objects. Examples include:

- depends on,
- causes,
- uses,
- outputs,
- blocks,
- asks,
- answers,
- displays,
- transitions to,
- and contains.

Relations are not merely lines; they must carry meaning.

### 10.4 AI Understanding and Normalization

The system must allow AI to:

- interpret canvas content,
- normalize rough or incomplete user input into structured semantic objects,
- infer likely relationships when appropriate,
- identify ambiguity,
- ask for clarification,
- and mark confidence or uncertainty where necessary.

AI normalization must be traceable enough that a human can see what changed and why.

### 10.5 AI Explanation Back to the User

The system must allow AI to:

- place visual explanations on the canvas,
- add grouped interpretations,
- annotate selections,
- produce alternative flows,
- highlight incomplete areas,
- and explain complex behavior in simpler visual terms.

AI explanation must prioritize user clarity over raw technical completeness.

### 10.6 Mockup Generation

The system must allow AI to generate visual mockups based on the semantic model.

Mockups may include:

- screens,
- components,
- transitions,
- states,
- and sample interactions.

The product should favor low-to-medium fidelity mockups that aid reasoning and communication rather than polished final design.

### 10.7 Chat Integration

The system must allow text-based interaction alongside the canvas.

The user must be able to:

- ask the AI to explain the canvas,
- request transformation of selected items,
- ask questions about relationships or gaps,
- request mockups,
- and request documentation generation.

The AI must be able to reference canvas objects in its responses.

### 10.8 Markdown Projection

The system must support generation of markdown artifacts from the semantic model.

Markdown outputs should be:

- readable by humans,
- useful for AI agents,
- suitable for repository storage,
- and stable enough to support version diffs.

The product must support at least:

- project-level summary markdown,
- object-level markdown,
- flow-level markdown,
- and decision/risk/open-question markdown.

### 10.9 Markdown Reconciliation

The system should support markdown-to-model updates.

If markdown is edited externally or manually:

- the system should parse the changes,
- convert them into semantic patches where possible,
- and update the canonical model and canvas without destructive full resets.

### 10.10 Tool-Driven AI Actions

The product must expose domain-level tool actions to the AI.

These actions should be meaningful in product terms, for example:

- create object,
- update object,
- connect objects,
- generate explanation,
- generate mockup,
- export markdown,
- import markdown patch,
- mark uncertainty,
- group related items,
- and propose alternative flows.

The AI should not depend primarily on low-level canvas-manipulation primitives.

---

## 11. User Experience Requirements

### 11.1 UX Objectives

The experience should feel:

- approachable,
- visually legible,
- conversational,
- structured but not rigid,
- and collaborative rather than command-line-like.

### 11.2 UX Rules

1. The user should not need to understand formal notation to use the system.
2. The user should not need to write a giant prompt before seeing value.
3. The user should be able to start small and refine progressively.
4. The AI should visibly distinguish between facts, assumptions, and questions.
5. The AI should be able to show what it inferred rather than hiding that work.
6. The user should always be able to correct the system from the nearest interaction surface.

### 11.3 UI Zones (Conceptual)

A likely product layout should include:

- **Canvas area** for visual interaction
- **Side panel** for object details, metadata, and AI explanations
- **Chat / command panel** for language-driven requests
- **Action toolbar** for creating semantic object types and invoking AI actions
- **Artifact panel or export surface** for generated markdown views

Tailwind should be used to support a clean, responsive UI shell around the vue-flow canvas and surrounding interaction components.

---

## 12. Canonical Data Strategy

### 12.1 Source of Truth

The source of truth should be the **semantic intent model**, not raw markdown and not raw visual layout.

Rationale:

- Visual layout is too presentation-specific.
- Markdown is too lossy for full round-trip behavior.
- The semantic layer allows structured reasoning, stable identifiers, meaningful relations, and clean transformations.

### 12.2 Stable IDs

Every semantic object must have a stable identifier.

Stable IDs are required for:

- reconciliation,
- tool actions,
- markdown references,
- AI conversation grounding,
- and round-trip updates.

### 12.3 Metadata

Each object should support a baseline metadata envelope, conceptually including:

- id,
- type,
- title,
- summary,
- details,
- status,
- tags,
- relations,
- evidence/examples,
- uncertainty markers,
- provenance,
- and links to canvas representation(s).

---

## 13. Canvas-to-Model Translation

When the user manipulates the canvas, the system must convert that interaction into semantic meaning.

### 13.1 Required Behavior

The system should:

- recognize the semantic type of created objects,
- map visual connections into typed relations,
- preserve object metadata,
- capture grouping intent where meaningful,
- and treat layout as supporting context rather than primary truth.

### 13.2 AI Assistance in Translation

The AI may assist by:

- converting rough notes into structured summaries,
- proposing object types for untyped content,
- inferring relation semantics when the user leaves them implicit,
- and flagging ambiguity rather than silently overfitting.

### 13.3 Human Control

The human must be able to accept, reject, or edit AI-normalized interpretations.

---

## 14. Model-to-Canvas Translation

The semantic model must be renderable back into a usable visual interface.

### 14.1 Required Behavior

The system must be able to:

- create visual shapes from semantic objects,
- render relations meaningfully,
- display uncertainty,
- display grouped interpretations,
- place explanatory overlays,
- and generate mockup-oriented visual structures.

### 14.2 Layout Strategy

Layout may be:

- user-driven,
- template-driven,
- or AI-assisted.

However, layout should remain secondary to semantic content.

---

## 15. Markdown Projection Strategy

### 15.1 Purpose of Markdown

Markdown exists to make the system’s current understanding portable, reviewable, and storable.

### 15.2 Characteristics of Good Markdown Output

Markdown output should be:

- concise enough to scan,
- structured enough to parse,
- explicit enough for future AI use,
- and diff-friendly for repository workflows.

### 15.3 Suggested Markdown Categories

The product should support markdown documents such as:

- project intent summary,
- flow descriptions,
- screen summaries,
- object-level records,
- open questions,
- risks,
- assumptions,
- and implementation handoff notes.

### 15.4 Projection Rules

Markdown should be generated from the semantic model.

Edits to markdown should, where feasible, produce semantic patches rather than trigger full destructive re-import.

---

## 16. Tool Call Strategy

### 16.1 Principle

AI tools should operate in terms of **semantic intent**, not raw canvas primitives.

### 16.2 Domain Tool Categories

The system should conceptually support tool categories such as:

- Object creation
- Object update
- Relation creation / removal
- Grouping / classification
- Explanation generation
- Mockup generation
- Markdown export
- Markdown import / patch
- Ambiguity detection
- Alternative interpretation generation

### 16.3 Tool Call Requirements

Tool calls should:

- reference stable semantic identifiers,
- operate on meaningful objects,
- produce traceable changes,
- and avoid tight coupling to layout-specific implementation details.

### 16.4 Why This Matters

If the AI acts on low-level drawing commands directly, the system becomes brittle and harder to validate. Domain-level tools preserve meaning and make the system easier to reason about for both humans and future AI agents.

---

## 17. AI Behavior Requirements

The AI in this system is not only a generator. It plays several roles.

### 17.1 AI Roles

**Interpreter**
Transforms rough user input into structured meaning.

**Clarifier**
Finds ambiguity, missing information, and conflicting assumptions.

**Explainer**
Shows how things work in plain language and visually.

**Mockup Assistant**
Creates rough visual proposals.

**Documentarian**
Generates markdown artifacts.

**Transformation Agent**
Applies changes via tool calls in a traceable way.

### 17.2 AI Output Expectations

The AI should:

- identify what is certain vs inferred,
- expose important assumptions,
- avoid pretending ambiguity does not exist,
- prefer structured updates when changing shared state,
- and keep human understanding central.

### 17.3 AI Failure Modes to Avoid

The AI must avoid:

- silently inventing structure,
- overfitting to layout,
- conflating notes with requirements,
- treating every drawn connection as equally meaningful,
- and rewriting user intent too aggressively without traceability.

---

## 18. System Workflow

### 18.1 Core Collaboration Loop

1. Human creates or edits content on the canvas.
2. The system converts this into semantic updates.
3. The AI interprets and normalizes the content.
4. The AI explains its interpretation back on the canvas and/or in chat.
5. The human refines or corrects that interpretation.
6. The system updates the semantic model.
7. Markdown artifacts are generated or updated from the semantic model.
8. Future humans or AI agents can continue from the saved model and markdown artifacts.

### 18.2 Alternate Entry Points

The system should also allow work to begin from:

- chat input,
- imported markdown,
- a blank template,
- or an AI-generated initial structure.

All entry paths should converge into the same semantic model.

---

## 19. Example Semantic Flow (Illustrative)

This section is conceptual and not code-binding.

### 19.1 Example User Action

A user places:

- a Goal called “User signs up quickly”
- a Screen called “Signup page”
- a Constraint called “Email only at first”
- a Flow Step called “Verify email”

The user visually connects them.

### 19.2 Example System Interpretation

The system interprets:

- Goal: desired business/user outcome
- Screen: interface artifact
- Constraint: requirement boundary
- Flow Step: sequential action
- Relations: screen supports goal; flow step belongs to signup flow; constraint restricts signup method

### 19.3 Example AI Response

The AI may:

- add an explanatory note about what is missing,
- propose a branch for “resend verification email,”
- generate a low-fidelity mockup of the signup flow,
- and export a markdown summary for review.

---

## 20. Pseudocode-Level Guidance (Conceptual Only)

This section exists only to clarify the architecture at a high level.

### 20.1 High-Level Representation Flow

```text
User Interaction -> Canvas Update -> Semantic Patch -> Canonical Model
Canonical Model -> AI Interpretation / Tool Actions -> Model Update
Canonical Model -> Canvas Projection
Canonical Model -> Markdown Projection
Markdown Edit -> Parsed Patch -> Canonical Model -> Canvas Refresh
```

### 20.2 Example Domain Tool Style

```text
create_object(type, title, summary)
update_object(id, fields)
connect_objects(from_id, relation_type, to_id)
generate_explanation(selection)
generate_mockup(selection)
export_markdown(scope)
apply_markdown_patch(document)
```

This pseudocode illustrates intent only. It does not prescribe implementation syntax.

---

## 21. Information Architecture and Content Model

### 21.1 Core Entity Groups

A minimal initial content model should include:

**Intent Entities**

- goals
- constraints
- questions
- assumptions

**System Entities**

- actors
- screens
- components
- data objects

**Flow Entities**

- steps
- decisions
- transitions
- outputs

**Support Entities**

- notes
- examples
- risks
- open issues

### 21.2 Extensibility

The model should be extensible without requiring a total redesign. New semantic types should be addable over time as long as they follow the same core rules:

- stable identity,
- structured metadata,
- clear semantics,
- and support for projection into canvas and markdown.

---

## 22. Interaction Design Patterns

### 22.1 Recommended Patterns

- Create from semantic templates rather than blank arbitrary shapes.
- Offer AI actions on current selection.
- Show uncertainty visually.
- Let the AI create explanation overlays in a clearly distinct visual style.
- Support side-by-side human content and AI interpretation where helpful.
- Allow one-click conversion from rough notes into structured objects.
- Allow one-click export from selection to markdown summary.

### 22.2 Selection-Centric AI

The AI should be able to operate on:

- selected object,
- selected group,
- selected flow,
- current page,
- or entire workspace.

Selection-based operations reduce ambiguity and make AI actions easier for users to predict.

---

## 23. Tailwind and Nuxt.js Role in the Product

### 23.1 Nuxt.js Role

Nuxt.js will provide the application shell and product structure around the vue-flow canvas.

Likely responsibilities include:

- routing,
- layout organization,
- panels and application shell,
- state coordination,
- command surfaces,
- persistence and integration boundaries,
- and any server/client interaction patterns needed by the product.

### 23.2 Tailwind Role

Tailwind will provide the styling system for:

- application shell,
- panels,
- controls,
- metadata views,
- markdown previews,
- chat surfaces,
- and responsive behavior.

The visual design should support clarity, hierarchy, and low-friction interpretation rather than ornamental complexity.

---

## 24. Persistence and Handoff Requirements

The product must support durable handoff.

### 24.1 What Must Be Persisted

At a conceptual level, the system should preserve:

- semantic model state,
- canvas state,
- markdown projections,
- and enough provenance to understand what was user-created vs AI-created vs AI-inferred.

### 24.2 Why Handoff Matters

A future developer, PM, or AI agent should be able to understand:

- the current intent,
- the structure behind it,
- the documented explanation,
- and the open issues,
without requiring access to a past live conversation.

---

## 25. Acceptance Criteria

The product should be considered successful at an MVP level if the following are possible:

1. A user can create a structured intent board visually.
2. The system can convert that board into a semantic model.
3. The AI can explain the board back to the user visually and in text.
4. The AI can generate a rough mockup from selected semantic content.
5. The system can export markdown artifacts that are understandable on their own.
6. The user can revise the canvas and see those changes reflected in the semantic understanding.
7. The user can revise markdown and have relevant changes reconciled back into the model.
8. A future human or AI agent can continue work from the saved artifacts without relying on prior chat context.

---

## 26. Success Metrics

Success metrics should focus on clarity, usability, and reduction of ambiguity.

Examples:

- time required for a user to express an idea to the AI,
- reduction in clarification loops compared to chat-only workflows,
- percentage of AI interpretations accepted without major correction,
- usefulness rating of AI-generated explanations,
- usefulness rating of generated markdown handoffs,
- and ability of a new contributor to understand the project state from saved artifacts.

---

## 27. Risks and Challenges

### 27.1 Semantic Drift

Risk: canvas, markdown, and AI understanding diverge.

Mitigation: maintain a canonical semantic model and reconcile all changes through it.

### 27.2 Over-Freedom on the Canvas

Risk: users create content too loosely for the AI to interpret reliably.

Mitigation: constrain the visual language, use templates, and support AI-assisted normalization.

### 27.3 Over-Structuring the User Experience

Risk: the interface becomes too rigid and intimidating.

Mitigation: keep creation flows simple, progressive, and forgiving.

### 27.4 AI Over-Inference

Risk: the AI invents structure or requirements not actually intended.

Mitigation: visually distinguish inferred content and require traceable updates.

### 27.5 Markdown Lossiness

Risk: markdown cannot represent all canvas nuance.

Mitigation: treat markdown as a projection, not the sole source of truth.

### 27.6 Mockup Misinterpretation

Risk: users interpret AI-generated mockups as final design commitments.

Mitigation: label mockups by fidelity and purpose.

---

## 28. Open Design Questions

These questions should be resolved during product design and implementation planning:

1. What is the exact initial semantic object taxonomy?
2. Which relations are supported in MVP vs later phases?
3. How much freeform drawing is allowed before prompting for normalization?
4. How should provenance and confidence be shown visually?
5. What markdown structure is best for downstream implementation workflows?
6. How should conflict resolution work when markdown and canvas edits happen close together?
7. What is the exact scope of mockup generation in MVP?
8. How should multi-page or multi-board workspaces be represented?

---

## 29. Recommended Delivery Phases

### Phase 1: Semantic Canvas Foundation

Focus:

- constrained semantic object creation,
- relation support,
- object editing,
- semantic model persistence,
- basic chat integration,
- and markdown export.

### Phase 2: AI Interpretation and Explanation

Focus:

- AI normalization,
- ambiguity detection,
- visual explanation overlays,
- alternative interpretation proposals,
- and selection-based AI actions.

### Phase 3: Mockup Generation

Focus:

- generation of low-to-medium fidelity mockups,
- screen/state representation,
- and richer explanation visuals.

### Phase 4: Reconciliation and Handoff Maturity

Focus:

- markdown patch import,
- provenance tracking,
- artifact refinement,
- and stronger handoff workflows for future humans and AI agents.

---

## 30. Final Product Statement

This product is a structured collaboration layer between human thinking and AI reasoning.

It uses:

- **vue-flow** as the visual interaction and explanation surface,
- **Nuxt.js** as the application shell and orchestration layer,
- and **Tailwind** as the UI styling system.

Its purpose is not just to draw diagrams and not just to chat with AI.
Its purpose is to make intent:

- easier for humans to express,
- easier for AI to understand,
- easier for AI to explain back,
- and easier to preserve as durable implementation-ready artifacts.

That is the core requirement this PRD defines.

---

## 31. One-Page Summary for Handoff

### What is being built?

A visual-semantic collaboration product where users express intent on a vue-flow canvas, AI interprets and explains it, and the result is projected into markdown artifacts for durable handoff.

### What problem does it solve?

It reduces ambiguity between what a human means and what an AI understands, while giving both a shared surface for refinement.

### What are the key representations?

- Canvas
- Semantic intent model
- Markdown artifacts

### Which one is the source of truth?

The semantic intent model.

### What are the major product capabilities?

- Visual intent modeling
- AI interpretation
- AI explanation
- Mockup generation
- Markdown export and reconciliation
- Tool-driven semantic actions

### What is the implementation mindset?

Build a constrained, semantically meaningful human/AI interaction layer rather than a generic whiteboard or chat app.
