# LangGraph Parallel-Workflow Assignment

## Overview

You have been given a working LangGraph project - **Mental Wellness Practice
Suggester** - as your reference implementation. Your task is to build your own
unique use case using the same framework and graph pattern.

Study `mental_wellness_graph.py` carefully. Your graph must follow a similar
structure:

```text
[User Input] -> [Understand / Classify Input]
                     |
                     +-> [Specialist Node 1] --+
                     +-> [Specialist Node 2] --+-> [Decision Node] -> [Conditional Final Output]
                     +-> [Specialist Node 3] --+
```

---

## What You Must Build

Using the same LangGraph patterns from the reference code:

- `StateGraph` - to create the graph
- A Pydantic state model - to define data fields
- Node functions - each node must do one clear job
- At least 3 parallel specialist nodes
- One decision node that reads all specialist outputs
- One conditional routing function
- At least 2 possible final output nodes
- `ChatOpenAI` - for LLM-based reasoning
- A `run_<your_project>()` function - as the main entry point

Your graph should not copy the mental wellness use case. Use the same pattern,
but build your assigned project.

---

## Submission Steps

1. Fork or clone this repo to your local machine.
2. Create your own Python file, for example `resume_review_graph.py`.
3. Do not modify `mental_wellness_graph.py`.
4. Build your assigned use case using the same LangGraph structure.
5. Test it end-to-end with your OpenAI key.
6. Push your code to a new public GitHub repository under your own account.
7. Share the GitHub link in the Excel sheet shared on WhatsApp.

Your repo must contain:

- Your LangGraph `.py` file
- A `requirements.txt`
- A `.env.example` file
- A `.gitignore`
- A `README.md` explaining what your graph does and how to run it

Never commit your real `.env` file or API key.

---

## Individual Assignments

---

### 1. nisargkadam23@gmail.com - Resume Reviewer Graph

**Use Case:** A user pastes resume text and a job description. The graph reviews
the resume and recommends improvements.

**Specialist Node 1 - `check_skills_match`**
- Identify matching and missing skills.

**Specialist Node 2 - `check_experience_alignment`**
- Compare work experience with job requirements.

**Specialist Node 3 - `check_resume_keywords`**
- Suggest important keywords missing from the resume.

**Decision Node:** Decide whether the resume needs minor edits or major rewrite.

**Final Nodes:** `minor_resume_edits` and `major_resume_rewrite_plan`.

---

### 2. vasentsethia@gmail.com - Recipe Planner Graph

**Use Case:** A user provides ingredients available at home. The graph suggests
what to cook.

**Specialist Node 1 - `suggest_main_dish`**
- Suggest a dish using the available ingredients.

**Specialist Node 2 - `suggest_side_or_drink`**
- Suggest a simple side dish or drink.

**Specialist Node 3 - `check_missing_staples`**
- Identify 1-2 common pantry items that may be needed.

**Decision Node:** Decide whether the recipe is quick or detailed.

**Final Nodes:** `quick_recipe_card` and `detailed_cooking_plan`.

---

### 3. Korde.sachin@gmail.com - Code Explainer Graph

**Use Case:** A user pastes code. The graph explains, reviews, and comments it.

**Specialist Node 1 - `explain_code_plain_english`**
- Explain what the code does.

**Specialist Node 2 - `identify_code_risks`**
- Identify bugs, edge cases, or unclear parts.

**Specialist Node 3 - `add_code_comments`**
- Return the code with helpful inline comments.

**Decision Node:** Decide whether the code needs simple explanation or deeper review.

**Final Nodes:** `simple_code_explanation` and `deep_code_review`.

---

### 4. Lokeshmargana9@Gmail.com - Story Writer Graph

**Use Case:** A user provides a story idea. The graph develops it into a story.

**Specialist Node 1 - `create_characters`**
- Create main characters.

**Specialist Node 2 - `create_plot_outline`**
- Create beginning, middle, and ending.

**Specialist Node 3 - `create_setting_and_tone`**
- Define setting, mood, and genre.

**Decision Node:** Decide whether to write a short story or expanded story.

**Final Nodes:** `write_short_story` and `write_expanded_story`.

---

### 5. tadikondavishnu1@gmail.com - SQL Helper Graph

**Use Case:** A user describes the data they need. The graph generates SQL and
explains it.

**Specialist Node 1 - `identify_tables`**
- Infer likely tables and fields.

**Specialist Node 2 - `generate_sql_query`**
- Write a clean SQL query.

**Specialist Node 3 - `check_sql_risks`**
- Check for missing filters, joins, or assumptions.

**Decision Node:** Decide whether the query is simple or advanced.

**Final Nodes:** `simple_sql_response` and `advanced_sql_response`.

---

### 6. rohanjs94blr@gmail.com - Product Copywriter Graph

**Use Case:** A user gives a product name and features. The graph creates
product copy.

**Specialist Node 1 - `write_feature_summary`**
- Summarize product features.

**Specialist Node 2 - `write_benefit_summary`**
- Convert features into customer benefits.

**Specialist Node 3 - `identify_target_customer`**
- Identify the likely buyer persona.

**Decision Node:** Decide whether the output should be formal or marketing-heavy.

**Final Nodes:** `formal_product_description` and `marketing_product_copy`.

---

### 7. thumati.ragavendrachary@gmail.com - Meeting Notes Graph

**Use Case:** A user pastes messy meeting notes. The graph organizes them.

**Specialist Node 1 - `extract_discussion_points`**
- Extract important discussion topics.

**Specialist Node 2 - `extract_decisions`**
- Extract decisions made.

**Specialist Node 3 - `extract_action_items`**
- Extract owners, tasks, and deadlines.

**Decision Node:** Decide whether notes are complete or missing key details.

**Final Nodes:** `complete_meeting_summary` and `meeting_summary_with_gaps`.

---

### 8. kedarpuja.239@gmail.com - Travel Planner Graph

**Use Case:** A user provides a destination and trip length. The graph creates a
travel plan.

**Specialist Node 1 - `suggest_sightseeing`**
- Suggest attractions.

**Specialist Node 2 - `suggest_food_experiences`**
- Suggest food and restaurant experiences.

**Specialist Node 3 - `suggest_culture_or_adventure`**
- Suggest cultural or adventure activities.

**Decision Node:** Decide whether the trip style is relaxed or packed.

**Final Nodes:** `relaxed_itinerary` and `packed_itinerary`.

---

### 9. hemanthhppl@gmail.com - Interview Coach Graph

**Use Case:** A user provides a job role. The graph prepares interview practice.

**Specialist Node 1 - `generate_technical_questions`**
- Generate technical questions.

**Specialist Node 2 - `generate_behavioral_questions`**
- Generate behavioral questions.

**Specialist Node 3 - `generate_role_specific_questions`**
- Generate questions specific to the role.

**Decision Node:** Decide whether the candidate needs beginner or advanced prep.

**Final Nodes:** `beginner_interview_pack` and `advanced_interview_pack`.

---

### 10. vishalghume.ai@gmail.com - Social Media Post Graph

**Use Case:** A user provides an announcement. The graph converts it into social
content.

**Specialist Node 1 - `write_formal_announcement`**
- Write a professional announcement.

**Specialist Node 2 - `create_social_hook`**
- Write hook options.

**Specialist Node 3 - `suggest_hashtags`**
- Suggest relevant hashtags.

**Decision Node:** Decide whether the tone should be professional or playful.

**Final Nodes:** `linkedin_style_post` and `instagram_style_post`.

---

### 11. firdos.cs028@gmail.com - Bug Report Analyzer Graph

**Use Case:** A user pastes a bug report or error message. The graph analyzes
the issue.

**Specialist Node 1 - `identify_possible_causes`**
- List likely causes.

**Specialist Node 2 - `suggest_logs_to_check`**
- Suggest logs, files, or commands to inspect.

**Specialist Node 3 - `estimate_severity`**
- Classify severity and user impact.

**Decision Node:** Decide whether the issue is low priority or urgent.

**Final Nodes:** `standard_debug_plan` and `urgent_debug_plan`.

---

## Evaluation Criteria

| Criteria | Points |
|---|---:|
| Code follows the same LangGraph structure as `mental_wellness_graph.py` | 20 |
| Uses Pydantic state, `StateGraph`, nodes, edges, and conditional routing correctly | 20 |
| Includes at least 3 parallel specialist nodes | 15 |
| Decision node reads all specialist outputs before routing | 15 |
| Graph runs end-to-end without errors | 10 |
| `README.md` clearly explains the use case and how to run it | 10 |
| GitHub repo is public, clean, and has `.env.example` with no real API key | 10 |
| **Total** | **100** |

---

## Tips

- Run `mental_wellness_graph.py` first before building your own graph.
- Keep every node focused on one responsibility.
- Add one state field for each important output.
- Use `messages: Annotated[list, operator.add]` if you want to track node logs.
- Make your decision node return structured JSON when possible.
- Test simple inputs before testing complex examples.
- Do not push `.env`, `venv`, or `__pycache__` to GitHub.

---

*Deadline and submission link: shared on WhatsApp. Post your GitHub URL in the Excel sheet.*
