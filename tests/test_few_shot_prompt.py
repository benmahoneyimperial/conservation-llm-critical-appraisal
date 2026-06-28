from domain_shot.build_few_shot_prompt import (
    SYSTEM_PROMPT_INSTRUCTIONS,
    build_prompt,
    build_prompt_messages,
    load_domain_examples,
    load_domain_questions,
)


def test_build_few_shot_prompt_sections_in_order():
    prompt = build_prompt(
        domain_name="domain_1",
        domain_guidance_text="Domain guidance",
        domain_questions_text="Q1\nQ2",
        worked_examples_text="Example A",
        paper_text="Paper text",
        intro_text="Guidance intro",
    )

    assert "--- GUIDANCE INTRO ---" in prompt
    assert "--- DOMAIN GUIDANCE (domain_1) ---" in prompt
    assert "--- DOMAIN QUESTIONS (domain_1) ---" in prompt
    assert "--- WORKED EXAMPLES (domain_1) ---" in prompt
    assert "--- TARGET PAPER ---" in prompt

    assert prompt.index("Guidance intro") < prompt.index("Domain guidance")
    assert prompt.index("Domain guidance") < prompt.index("Q1")
    assert prompt.index("Q1") < prompt.index("Example A")
    assert prompt.index("Example A") < prompt.index("Paper text")


def test_build_few_shot_prompt_messages_include_system_prompt():
    messages = build_prompt_messages(
        domain_name="domain_1",
        domain_guidance_text="Domain guidance",
        domain_questions_text="Q1",
        worked_examples_text="Example A",
        paper_text="Paper text",
        intro_text="Guidance intro",
    )

    assert messages[0]["role"] == "system"
    assert messages[0]["content"] == SYSTEM_PROMPT_INSTRUCTIONS
    assert messages[1]["role"] == "user"


def test_missing_questions_and_examples_return_placeholders(tmp_path):
    questions_text = load_domain_questions("domain_9", questions_dir=str(tmp_path))
    examples_text = load_domain_examples("domain_9", examples_dir=str(tmp_path))

    assert "[PLACEHOLDER]" in questions_text
    assert "domain_9_questions.md" in questions_text
    assert "[PLACEHOLDER]" in examples_text
    assert "domain_9_examples.md" in examples_text
