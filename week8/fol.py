import re
from typing import Set, List, Dict, Tuple, Optional, Generator
from graphviz import Digraph
from IPython.display import display, Image

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
        return fact_string, []  # Handles facts with no arguments

    predicate = match.group(1)
    args_str = match.group(2)

    if not args_str:
        return predicate, [] # Handles Predicate()

    args = [arg.strip() for arg in args_str.split(',')]
    return predicate, args

def is_variable(term: str) -> bool:
    """A term is a variable if it's a lowercase string."""
    return term[0].islower()

def apply_substitution(conclusion: Fact, sub: Substitution) -> Fact:
    """Applies a substitution to a conclusion string to generate a new fact."""
    pred, args = parse_fact(conclusion)
    if not args:
        return pred
    new_args = [sub.get(arg, arg) for arg in args]
    return f"{pred}({','.join(new_args)})"

def unify(pattern: Fact, fact: Fact, sub: Substitution) -> Optional[Substitution]:
    """
    Unifies a pattern (from a rule premise) with a fact (from KB).
    Facts are assumed to have no variables.
    Returns a new substitution on success, None on failure.
    """
    p_pred, p_args = parse_fact(pattern)
    f_pred, f_args = parse_fact(fact)

    if p_pred != f_pred or len(p_args) != len(f_args):
        return None

    new_sub = sub.copy()
    for p_arg, f_arg in zip(p_args, f_args):
        # Resolve variable from pattern using existing substitution if available
        p_arg_resolved = new_sub.get(p_arg, p_arg)

        if is_variable(p_arg_resolved):
            # If the variable is not yet bound, bind it to the fact's argument.
            new_sub[p_arg_resolved] = f_arg
        elif p_arg_resolved != f_arg:
            # If it's a constant or a bound variable, it must match the fact's argument.
            return None

    return new_sub

def find_substitutions(premises: List[Fact], kb: Set[Fact], initial_sub: Substitution) -> Generator[Substitution, None, None]:
    """
    A recursive generator that finds all valid substitutions for a list of premises.
    It yields each valid substitution dictionary.
    """
    if not premises:
        yield initial_sub
        return

    current_premise = premises[0]
    remaining_premises = premises[1:]

    for fact in kb:
        # Try to unify the current premise with a fact from the KB
        sub_for_premise = unify(current_premise, fact, initial_sub)

        if sub_for_premise is not None:
            # If unification succeeds, recurse for the remaining premises
            for final_sub in find_substitutions(remaining_premises, kb, sub_for_premise):
                yield final_sub

def forward_chaining(kb: Set[Fact], rules: List[Rule], query: Fact):
    """
    Implements the forward chaining algorithm and generates a proof graph matching the example.
    """
    print("🚀 Starting Forward Chaining Proof...")
    print("=====================================")
    print(f"Initial Knowledge Base: {kb}")
    print(f"Query to Prove: {query}\n")

    # --- Visualization Setup ---
    dot = Digraph('ForwardChainingProof', comment='Forward Chaining Proof Visualization')
    dot.attr(rankdir='TB', splines='polyline', nodesep='0.6', ranksep='0.8') # Adjust layout for cleaner connections
    dot.attr(bgcolor="white") # Set background to white

    # Add initial facts to the graph in a conceptual "layer"
    for fact in kb:
        dot.node(fact, fact, shape='box', style='filled', fillcolor='white') # All facts are white boxes

    # Keep track of inferred facts and the rules that generated them
    inferred_facts_rules: Dict[Fact, Tuple[List[Fact], Rule]] = {}

    iteration = 1
    while True:
        new_facts = set()
        print(f"--- Iteration {iteration} ---")

        # Iterate over rules and try to apply them
        for rule_idx, (premises_template, conclusion_template) in enumerate(rules):
            # Find all possible substitutions that satisfy the rule's premises
            for sub in find_substitutions(premises_template, kb, {}):
                inferred_fact = apply_substitution(conclusion_template, sub)

                if inferred_fact not in kb and inferred_fact not in new_facts:
                    new_facts.add(inferred_fact)
                    premise_str = ' & '.join([apply_substitution(p, sub) for p in premises_template])
                    print(f"✅ Applied rule: {' & '.join(premises_template)} => {conclusion_template}")
                    print(f"   - With facts: {premise_str}")
                    print(f"   - Using substitution: {sub}")
                    print(f"   ==> Inferred: {inferred_fact}\n")

                    # Store for visualization
                    inferred_facts_rules[inferred_fact] = ([apply_substitution(p, sub) for p in premises_template], (premises_template, conclusion_template))

                    # Add new fact node to graph
                    dot.node(inferred_fact, inferred_fact, shape='box', style='filled', fillcolor='white')

        if not new_facts:
            print("No new facts can be inferred. Halting.")
            break

        kb.update(new_facts)
        print(f"📚 Updated KB with new facts: {new_facts}")
        print(f"   Current KB size: {len(kb)}\n")

        if query in kb:
            print(f"🎉 Goal '{query}' found in the Knowledge Base!")
            break # Goal achieved

        iteration += 1

    # Now, add edges and labels based on the inference chain
    for inferred_fact, (source_facts, (premises_template, conclusion_template)) in inferred_facts_rules.items():
        # Identify which rule was used. This is a simplified labeling.
        # For the final rule, we can add the full text like in the image.
        is_final_rule_to_query = (inferred_fact == query)

        rule_label = ""
        if is_final_rule_to_query:
            # Format the label similar to the example image for the final step
            rule_label = f"{' & '.join(premises_template)} \n⇒ {conclusion_template}"

        for sf in source_facts:
            # Ensure the source fact node exists (it should, as it was either initial or previously inferred)
            # Add an edge from the source fact to the inferred fact
            dot.edge(sf, inferred_fact, label=rule_label if is_final_rule_to_query else "", fontsize="10", labelfontcolor="black", fontcolor="blue", penwidth='2')

        # If it's the final query, make its box stand out
        if inferred_fact == query:
            dot.node(query, query, shape='box', style='filled', fillcolor='white', penwidth='3', color='black') # Thick black border for query

    # Ensure initial facts also get a standard box if they weren't inferred
    for fact in knowledge_base:
        if fact not in inferred_facts_rules: # If not an inferred fact
             dot.node(fact, fact, shape='box', style='filled', fillcolor='white')


    # Final result and rendering the graph
    print("=====================================")
    if query in kb:
        print(f"Conclusion: The query '{query}' is proven to be TRUE.")
    else:
        print(f"Conclusion: The query '{query}' cannot be proven.")
    print("=====================================")

    # Render and save the graph
    try:
        graph_image = dot.render('forward_chaining_proof', format='png', view=False, cleanup=True)
        print("\n📊 Visualization of the explanation proof has been saved to 'forward_chaining_proof.png'")
        display(Image('forward_chaining_proof.png'))
    except Exception as e:
        print(f"\nCould not generate visualization. Please ensure you have Graphviz installed. Error: {e}")


if __name__ == '__main__':
    # 1. Define the initial Knowledge Base
    knowledge_base: Set[Fact] = {
        "American(Robert)",
        "Owns(A, T1)",
        "Missile(T1)",
        "Enemy(A, America)"
    }

    # 2. Define the rules
    rules: List[Rule] = [
        (["Missile(x)"], "Weapon(x)"),
        (["Enemy(x, America)"], "Hostile(x)"),
        (["Missile(x)", "Owns(A, x)"], "Sells(Robert, x, A)"),
        (["American(p)", "Weapon(q)", "Sells(p, q, r)", "Hostile(r)"], "Criminal(p)")
    ]

    # 3. Define the query
    query: Fact = "Criminal(Robert)"

    # 4. Run the algorithm
    forward_chaining(knowledge_base, rules, query)