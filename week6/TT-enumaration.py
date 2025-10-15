import re
from itertools import product

def tt_entails(kb_str: str, alpha_str: str) -> bool:
    """
    Checks if a knowledge base (KB) entails a query (alpha) using truth-table enumeration.
    
    Args:
        kb_str: A string representing the knowledge base, with sentences joined by '&'.
                Use '=>' for implication, '<=>' for biconditional, '~' for not.
        alpha_str: A string representing the query sentence.
        
    Returns:
        True if kb entails alpha, False otherwise.
    """
    # Replace logical operators with Python-compatible ones for eval()
    def format_expression(expr):
        return expr.replace('&', ' and ').replace('|', ' or ').replace('=>', '<=').replace('<=>', '==').replace('~', ' not ')

    kb = format_expression(kb_str)
    alpha = format_expression(alpha_str)

    # 1. Get all unique symbols from the KB and alpha
    symbols = sorted(list(set(re.findall(r'[A-Za-z]+', kb + ' ' + alpha))))
    
    print(f"KB: {kb_str}")
    print(f"Query (Alpha): {alpha_str}")
    print(f"Symbols: {symbols}\n")
    
    print("--- Truth Table Enumeration ---")
    header = " | ".join(symbols) + f" | {'KB':^15} | {'Alpha':^10} | Entails?"
    print(header)
    print("-" * len(header))

    # 2. Iterate through all possible models (all 2^n combinations of True/False)
    for values in product([True, False], repeat=len(symbols)):
        # A model is a dictionary mapping symbols to True/False
        model = dict(zip(symbols, values))
        
        # 3. Evaluate KB and alpha in the current model
        try:
            kb_is_true = eval(kb, {}, model)
            alpha_is_true = eval(alpha, {}, model)
        except Exception as e:
            print(f"Error evaluating expressions: {e}")
            return False

        # Print the current row of the truth table
        row_str = " | ".join(f"{str(v):^5}" for v in values)
        row_str += f" | {str(kb_is_true):^15} | {str(alpha_is_true):^10} |"
        
        # 4. Check for the condition that breaks entailment
        # If we find a model where the KB is true but alpha is false, entailment is disproven.
        if kb_is_true and not alpha_is_true:
            print(f"{row_str}   ❌ (CONTRADICTION)")
            print("\nConclusion: KB does NOT entail Alpha.")
            return False
        
        print(f"{row_str}   ✅")

    # 5. If the loop completes without finding a contradiction, entailment holds.
    print("\nConclusion: KB ENTAILS Alpha (no contradictions found).")
    return True

# --- Example Usage ---
if __name__ == "__main__":
    # Example 1: Simple Modus Ponens (Should be True)
    # KB: If P is true, then Q is true. P is true.
    # Query: Is Q true?
    print("--- Example 1: Modus Ponens ---")
    kb_1 = "(P => Q) & P"
    alpha_1 = "Q"
    tt_entails(kb_1, alpha_1)
    print("\n" + "="*50 + "\n")
    
    # Example 2: False Entailment (Should be False)
    # KB: It is raining or it is sunny.
    # Query: Is it both raining AND sunny?
    print("--- Example 2: False Entailment ---")
    kb_2 = "Raining | Sunny"
    alpha_2 = "Raining & Sunny"
    tt_entails(kb_2, alpha_2)
    print("\n" + "="*50 + "\n")

    # Example 3: A more complex case (Should be True)
    # KB: If a creature is mythical, it's immortal. If it's not mythical, it's a mammal.
    #     If it's either immortal or a mammal, then it is horned.
    # Query: Is the creature horned?
    print("--- Example 3: Mythical Creature ---")
    kb_3 = "(Mythical => Immortal) & (~Mythical => Mammal) & ((Immortal | Mammal) => Horned)"
    alpha_3 = "Horned"
    tt_entails(kb_3, alpha_3)