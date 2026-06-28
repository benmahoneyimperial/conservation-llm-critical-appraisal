from domain_shot.build_domain_shot_prompt import SYSTEM_PROMPT_INSTRUCTIONS, build_prompt, build_prompt_messages


def test_build_prompt_concatenates_parts_in_order():
    prompt = build_prompt(
        domain_name="domain_1",
        domain_guidance_text="Domain guidance",
        paper_text="Paper text",
        intro_text="Guidance intro",
    )

    assert "--- GUIDANCE INTRO ---" in prompt
    assert "--- GUIDANCE FOR domain_1 ---" in prompt
    assert "--- RESEARCH PAPER ---" in prompt
    assert prompt.index("Guidance intro") < prompt.index("Domain guidance")
    assert prompt.index("Domain guidance") < prompt.index("Paper text")


def test_build_prompt_messages_uses_system_instructions():
    messages = build_prompt_messages(
        domain_name="domain_1",
        domain_text="Domain guidance",
        paper_text="Paper text",
        intro_text="Guidance intro",
    )

    assert messages[0]["role"] == "system"
    assert messages[0]["content"] == SYSTEM_PROMPT_INSTRUCTIONS
