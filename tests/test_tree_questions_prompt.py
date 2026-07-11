import pytest

from domain_shot.build_tree_guided_prompt import (
    SYSTEM_PROMPT_INSTRUCTIONS,
    build_prompt,
    build_prompt_messages,
    load_default_guidance_intro,
    load_domain_decision_tree,
    load_domain_questions,
)


def test_build_tree_guided_prompt_sections_in_order():
    prompt = build_prompt(
        domain_name="domain_1",
        intro_text="Guidance intro",
        decision_tree_text="Tree step A",
        domain_questions_text="Q1\nQ2",
        paper_text="Paper text",
    )

    assert "--- GUIDANCE INTRO ---" in prompt
    assert "--- DECISION TREE (domain_1) ---" in prompt
    assert "--- DOMAIN QUESTIONS (domain_1) ---" in prompt
    assert "--- TARGET PAPER ---" in prompt

    assert prompt.index("Guidance intro") < prompt.index("Q1")
    assert prompt.index("Q1") < prompt.index("Tree step A")
    assert prompt.index("Tree step A") < prompt.index("Paper text")


def test_build_tree_guided_prompt_messages_include_system_prompt():
    messages = build_prompt_messages(
        domain_name="domain_1",
        intro_text="Guidance intro",
        decision_tree_text="Tree step A",
        domain_questions_text="Q1",
        paper_text="Paper text",
    )

    assert messages[0]["role"] == "system"
    assert messages[0]["content"] == SYSTEM_PROMPT_INSTRUCTIONS
    assert messages[1]["role"] == "user"


def test_load_default_guidance_intro_returns_text():
    intro_text = load_default_guidance_intro()
    assert isinstance(intro_text, str)
    assert intro_text.strip()


def test_missing_questions_and_decision_tree_raise_file_not_found(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_domain_questions("domain_9", questions_dir=str(tmp_path))
    with pytest.raises(FileNotFoundError):
        load_domain_decision_tree("domain_9", decision_trees_dir=str(tmp_path))
