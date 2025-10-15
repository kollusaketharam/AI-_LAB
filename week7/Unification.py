import re
from typing import Set, List, Dict, Tuple, Optional, Generator

# Define types for clarity
Fact = str
Substitution = Dict[str, str]
Rule = Tuple[List[Fact], Fact]

def parse_fact(fact_string: Fact) -> Tuple[str, List[str]]:
    """
    Parses a string like 'Predicate(Arg1,Arg2)' into a predicate and its arguments.
    Example: 'Sells(Robert, T1, A)' -> ('Sells', ['Robert', 'T1', 'A'])
    """
    match = re.match(r"(\w+)\((.*?)\)", fact_string)
    if not match:
        return fact_string, []  # Handles facts with no arguments, e.g., 'Goal'

    predicate = match.group(1)
    args_str = match.group(2)
    
    if not args_str:
        return predicate, [] # Handles Predicate()
        
    args = [arg.strip() for arg in args_str.split(',')]
    return predicate, args

def is_variable(term: str) -> bool:
    """A term is a variable if it's a single lowercase letter or starts with one."""
    return term[0].islower()

def apply_substitution(fact_template: Fact, sub: Substitution) -> Fact:
    """Applies a substitution to a fact template to generate a concrete fact."""
    pred, args = parse_fact(fact_template)
    if not args:
        return pred # No arguments to substitute
    
    new_args = [sub.get(arg, arg) for arg in args]
    return f"{pred}({','.join(new_args)})"

def unify(pattern: Fact, fact: Fact, existing_sub: Substitution) -> Optional[Substitution]:
    """
    Unifies a pattern (from a rule premise) with a fact (from the KB).
    Returns a new substitution on success, None on failure.
    """
    p_pred, p_args = parse_fact(pattern)
    f_pred, f_args = parse_fact(fact)

    if p_pred != f_pred or len(p_args) != len(f_args):
        return None

    new_sub = existing_sub.copy()
    for p_arg, f_arg in zip(p_args, f_args):
        # Resolve the pattern's argument using any existing substitutions
        p_arg_resolved = new_sub.get(p_arg, p_arg)
        
        if is_variable(p_arg):
            if is_variable(p_arg_resolved):
                # If the variable is unbound, bind it to the fact's argument.
                new_sub[p_arg] = f_arg
            elif p_arg_resolved != f_arg:
                # If the variable is already bound to something else, fail.
                return None
        elif p_arg_resolved != f_arg:
            # If the pattern has a constant, it must match the fact's constant.
            return None
            
    return new_sub

def find_substitutions_for_premises(premises: List[Fact], kb: Set[Fact], initial_sub: Substitution) -> Generator[Substitution, None, None]:
    """
    A recursive generator that finds all valid substitutions for a list of premises.
    It yields each valid substitution dictionary.
    """
    if not premises:
        yield initial_sub
        return

    current_premise = premises[0]
    remaining_premises = premises[1:]

    # For the current premise, find a fact in the KB that unifies with it
    for fact in kb:
        sub_for_premise = unify(current_premise, fact, initial_sub)
        
        if sub_for_premise is not None:
            # If unification succeeds, recurse to find matches for the rest of the premises
            for final_sub in find_substitutions_for_premises(remaining_premises, kb, sub_for_premise):
                yield final_sub

def forward_chaining(kb: Set[Fact], rules: List[Rule], query: Fact):
    """
    Implements the forward chaining algorithm to prove a query.
    """
    print("🚀 Starting Forward Chaining Proof...")
    print("=====================================")
    print(f"Initial Knowledge Base: {kb}")
    print(f"Query to Prove: {query}\n")

    iteration = 1
    while True:
        new_facts = set()
        print(f"--- Iteration {iteration} ---")
        
        for premises, conclusion in rules:
            # Find all possible substitutions that satisfy the rule's premises
            for sub in find_substitutions_for_premises(premises, kb, {}):
                inferred_fact = apply_substitution(conclusion, sub)
                
                # Add the fact only if it's genuinely new
                if inferred_fact not in kb and inferred_fact not in new_facts:
                    new_facts.add(inferred_fact)
                    premise_str = ' & '.join([apply_substitution(p, sub) for p in premises])
                    print(f"✅ Applied rule: {' & '.join(premises)} => {conclusion}")
                    print(f"   - With facts: {premise_str}")
                    print(f"   - Using substitution: {sub}")
                    print(f"   ==> Inferred: {inferred_fact}\n")

        # If no new facts were inferred in a full pass, the process stops
        if not new_facts:
            print("No new facts can be inferred. Halting.")
            break
        
        # Add the newly inferred facts to the main knowledge base
        kb.update(new_facts)
        print(f"📚 Updated KB with new facts: {new_facts}")
        print(f"   Current KB size: {len(kb)}\n")
        
        # Check if the query has been proven
        if query in kb:
            print(f"🎉 Goal '{query}' found in the Knowledge Base!")
            break
            
        iteration += 1

    # Final result
    print("=====================================")
    if query in kb:
        print(f"Conclusion: The query '{query}' is proven to be TRUE.")
    else:
        print(f"Conclusion: The query '{query}' cannot be proven.")
    print("=====================================")


if __name__ == '__main__':
    # 1. Define the initial Knowledge Base (facts) from the problem description
    # T1 is a Skolem constant representing "some missiles".
    knowledge_base: Set[Fact] = {
        "American(Robert)",
        "Owns(A, T1)",
        "Missile(T1)",
        "Enemy(A, America)"
    }

    # 2. Define the rules (implications) based on the FOL representation
    rules: List[Rule] = [
        # Rule: It is a crime for an American to sell weapons to hostile nations.
        (["American(p)", "Weapon(q)", "Sells(p, q, r)", "Hostile(r)"], "Criminal(p)"),
        
        # Rule: All missiles were sold to country A by Robert.
        (["Missile(x)", "Owns(A, x)"], "Sells(Robert, x, A)"),
        
        # Implicit Rule: If something is a missile, it is a weapon.
        (["Missile(x)"], "Weapon(x)"),
        
        # Rule: An enemy of America is hostile.
        (["Enemy(x, America)"], "Hostile(x)"),
    ]

    # 3. Define the query to be proven
    query: Fact = "Criminal(Robert)"

    # 4. Run the forward chaining algorithm
    forward_chaining(knowledge_base, rules, query)