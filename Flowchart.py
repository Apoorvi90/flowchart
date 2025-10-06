import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from sympy import symbols, Eq, solve, sympify, sstr
import re

# Utility to standardize user input for sympy

def standardize_equation_input(equation: str) -> str:
    equation = equation.replace('^', '**')
    equation = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', equation)
    equation = re.sub(r'([a-zA-Z])([a-zA-Z])', r'\1*\2', equation)
    equation = equation.replace(' ', '')
    return equation

# Utility to format equation for display with superscripts

def format_equation_for_display(equation: str) -> str:
    def repl_power(match):
        num = match.group(1)
        sup_map = str.maketrans('0123456789-', '⁰¹²³⁴⁵⁶⁷⁸⁹⁻')
        return f"^{num.translate(sup_map)}"
    eq = re.sub(r'\*\*([\d-]+)', repl_power, equation)
    eq = eq.replace('*', '')
    return eq

# Utility to format roots for display

def format_roots_for_display(roots) -> list:
    import re as _re
    def sqrt_bracket_fix(s):
        # Replace √expr with √(expr) if not already in brackets
        return _re.sub(r'√([a-zA-Z0-9^+\-*/]+)', r'√(\1)', s)
    def format_root(r):
        s = sstr(r)
        s = s.replace('sqrt', '√').replace('**', '^').replace('*', '').replace('I', 'i')
        s = sqrt_bracket_fix(s)
        return s
    return [format_root(r) for r in roots]

# Draw a labeled box

def draw_box(ax: Axes, text: str, x: float, y: float, color: str = 'lightyellow', edge: str = 'black') -> None:
    ax.text(x, y, text, ha='center', va='center', fontsize=11, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.6', facecolor=color, edgecolor=edge, linewidth=2))

def generate_flowchart(equation: str, roots=None) -> None:
    fig, ax = plt.subplots(figsize=(7, 10))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 14)
    ax.axis('off')

    colors = ['#FFEB3B', '#B2FF59', '#40C4FF', '#FF8A65', '#D1C4E9', '#FFD54F', '#FFCDD2']
    arrow_colors = ['#FBC02D', '#388E3C', '#0288D1', '#D84315', '#7E57C2', '#FFA000', '#E57373']

    # Calculate number of boxes (steps) dynamically
    base_boxes = [
        'Start',
        'Input equation',
        None,  # Placeholder for equation
        'Find roots (symbolic/numerical)'
    ]
    root_boxes = []
    if roots is not None and len(roots) > 0:
        formatted_roots = format_roots_for_display(roots)
        for idx, root in enumerate(formatted_roots, 1):
            root_boxes.append(f'Root {idx}: {root}')
    else:
        root_boxes.append('No real roots')
    base_boxes.append('End')

    # Insert the equation at the right place
    display_eq = format_equation_for_display(equation)
    base_boxes[2] = f'Solve: {display_eq} = 0'

    # Combine all boxes
    all_boxes = base_boxes[:4] + root_boxes + [base_boxes[-1]]
    num_boxes = len(all_boxes)

    # Calculate vertical positions for equal spacing
    y_top = 13
    y_bottom = 1.5
    y_positions = [y_top - i * (y_top - y_bottom) / (num_boxes - 1) for i in range(num_boxes)]

    # Draw all boxes
    for i, (box, y) in enumerate(zip(all_boxes, y_positions)):
        color_idx = min(i, len(colors)-1)
        edge_idx = min(i, len(arrow_colors)-1)
        draw_box(ax, box, 5, y, color=colors[color_idx], edge=arrow_colors[edge_idx])

    # Draw arrows between boxes
    cm_space = 0.39
    box_height = 1.2
    for i in range(num_boxes - 1):
        start_y = y_positions[i] - (box_height / 2)
        end_y = y_positions[i+1] + (box_height / 2)
        ax.annotate(
            '',
            xy=(5, end_y - cm_space),
            xytext=(5, start_y - cm_space),
            arrowprops=dict(
                arrowstyle='->',
                lw=2,
                color=arrow_colors[i % len(arrow_colors)],
                shrinkA=0,
                shrinkB=0,
                connectionstyle="arc3,rad=0.0"
            )
        )
    plt.title('Equation Solution Flowchart', fontsize=16, fontweight='bold', color='#1976D2', pad=20)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    user_input = input("Enter a quadratic equation (e.g., 2x^2 + 3x + 1): ")
    equation = standardize_equation_input(user_input)
    x = symbols('x')
    try:
        expr = sympify(equation)
        roots = solve(Eq(expr, 0), x)
        print("Roots of the equation:")
        formatted_roots = format_roots_for_display(roots)
        for idx, r in enumerate(formatted_roots, 1):
            print(f"Root {idx}: {r}")
        generate_flowchart(equation, roots=roots)
    except Exception as e:
        print("Could not compute roots:", e)
        generate_flowchart(equation, roots=None)
