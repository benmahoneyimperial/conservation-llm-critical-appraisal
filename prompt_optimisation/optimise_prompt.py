import os
import sys
import gepa.optimize_anything as oa

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from appraisal.llm_client import set_instructions, DEFAULT_INSTRUCTIONS, API_KEY
from benchmarking.evaluate import run_benchmark

def evaluate(candidate: str) -> float:
    """
    Evaluator function for optimize_anything.
    1. Sets the global LLM instructions to the candidate string.
    2. Runs the benchmark.
    3. Logs failures as Actionable Side Information (ASI) for the optimizer.
    4. Returns the accuracy score.
    """
    # Update the prompt instructions with the candidate from the optimizer
    set_instructions(candidate)
    
    # Run the benchmark silently
    # Ensure these paths are correct relative to where you run the script
    accuracy, failures = run_benchmark(
        "data/benchmark.csv", 
        "data/processed_text", 
        verbose=False
    )
    
    # Log diagnostic feedback (ASI) so the optimizer knows *why* it got this score
    if failures:
        oa.log(f"Accuracy: {accuracy:.2%}. Sample Failures:")
        for fail in failures[:3]: # Log first 3 failures
            oa.log(f" - {fail}")
            
    return accuracy

if __name__ == "__main__":
    print("Starting prompt optimization...")
    
    # Ensure litellm can find your OpenRouter API key
    os.environ["OPENROUTER_API_KEY"] = API_KEY

    result = oa.optimize_anything(
        seed_candidate=DEFAULT_INSTRUCTIONS,
        evaluator=evaluate,
        objective="Generate instructions that ensure the LLM follows the decision tree strictly and outputs the final result in double brackets (e.g. [[Low Risk]]).",
        config=oa.GEPAConfig(
            engine=oa.EngineConfig(max_metric_calls=10),
            reflection=oa.ReflectionConfig(reflection_lm="openrouter/meta-llama/llama-3.3-70b-instruct:free")
        )
    )
    
    print(f"\nOptimization Complete.\nBest Score: {result.best_score}\nBest Prompt:\n{result.best_candidate}")
