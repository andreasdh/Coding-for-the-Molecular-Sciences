import json
import textwrap
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "numerical_methods"
IMG = BASE / "images"
IMG.mkdir(parents=True, exist_ok=True)


def clean(text):
    return textwrap.dedent(text).strip("\n") + "\n"


def md(text):
    return {"cell_type": "markdown", "metadata": {}, "source": clean(text).splitlines(True)}


def code(text):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": clean(text).splitlines(True),
    }


def load(name):
    path = BASE / name
    return path, json.loads(path.read_text(encoding="utf-8"))


def save(path, nb, cells):
    nb["cells"] = cells
    path.write_text(json.dumps(nb, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def download_image(source_name, target_name):
    target = IMG / target_name
    if target.exists():
        return
    quoted = urllib.parse.quote(source_name)
    urls = [
        f"https://raw.githubusercontent.com/andreasdh/programmering-i-kjemi/master/docs/bilder/{quoted}",
    ]
    if source_name.endswith(".png"):
        urls.append(
            f"https://raw.githubusercontent.com/andreasdh/programmering-i-kjemi/master/docs/bilder/{urllib.parse.quote(source_name + '.png')}"
        )
    last_error = None
    for url in urls:
        try:
            urllib.request.urlretrieve(url, target)
            return
        except Exception as exc:
            last_error = exc
    raise RuntimeError(f"Could not download {source_name}: {last_error}")


# Figures restored in the Norwegian pedagogical revision.
for source, target in [
    ("brute_force_likninger.png", "root_scan.png"),
    ("halveringsmetoden.png", "bisection.png"),
    ("newtonsmetode.png", "newton_method.png"),
    ("numerisk_derivasjon.png", "numerical_differentiation.png"),
    ("rektangel10_utentall.png", "rectangles_10.png"),
    ("rektangel_n=50.png", "rectangles_50.png"),
    ("rektangel_venstre_n=10.png", "rectangles_left_10.png"),
    ("rektangel_høyre_n=10.png", "rectangles_right_10.png"),
    ("rektangel_midt_n=10.png", "rectangles_midpoint_10.png"),
    ("trapes_n=1.png", "trapezoid_1.png"),
    ("trapes10.png", "trapezoids_10.png"),
]:
    download_image(source, target)


# ---------------------------------------------------------------------------
# Equations and root finding
# ---------------------------------------------------------------------------
path, nb = load("equations.ipynb")
old = nb["cells"]

cells = [
    md(r'''
    # Equations and root finding

    ```{admonition} Learning outcomes
    After working through this chapter, you should be able to:

    1. explain what a root-finding problem is and formulate equations as $f(x)=0$
    2. explain the theoretical basis of the bisection method and Newton's method
    3. implement the methods using simple Python code
    4. use a tolerance to control a numerical calculation
    5. discuss strengths, weaknesses and convergence of the methods
    6. use ready-made root solvers in SciPy for chemical problems
    ```

    ## Equations as root-finding problems

    Solving an equation and finding a root are really the same problem written in two different ways. If we have

    $$g(x)=h(x),$$

    we can move everything to one side:

    $$f(x)=g(x)-h(x)=0.$$

    A **root** is a value of $x$ for which the function value is zero. Solving $g(x)=h(x)$ therefore means finding the value of $x$ that makes $f(x)=0$. This is what we mean when we say that we **formulate the equation as a root-finding problem**.

    For quadratic equations we know a dedicated formula. For more complicated equations there is not always a practical analytical expression for the solution. Numerical methods are more general: instead, they approach the solution step by step.
    '''),
    md(r'''
    ## A chemical example: pH of a weak acid

    We use a 0.010 M solution of acetic acid as an example. For a monoprotic weak acid, we can combine the mass balance for the protonated and deprotonated forms, $C=[\mathrm{HA}]+[\mathrm{A^-}]$, with the acid dissociation constant to write

    $$[\mathrm{A^-}]=C\frac{K_a}{[\mathrm{H_3O^+}]+K_a}.$$

    ```{admonition} Where does the expression for $[\mathrm{A^-}]$ come from?
    :class: tip, dropdown

    $C$ is the total analytical concentration. The acid does not disappear; it is distributed between two forms:

    $$C=[\mathrm{HA}]+[\mathrm{A^-}].$$

    This is the mass balance. Note that $C\neq[\mathrm{HA}]$ unless almost none of the acid has dissociated.

    The acid dissociation constant gives $[\mathrm{HA}]=\dfrac{[\mathrm{H_3O^+}][\mathrm{A^-}]}{K_a}$. Substituting this into the mass balance and factoring out $[\mathrm{A^-}]$ gives

    $$C=[\mathrm{A^-}]\left(\frac{[\mathrm{H_3O^+}]}{K_a}+1\right)=[\mathrm{A^-}]\,\frac{[\mathrm{H_3O^+}]+K_a}{K_a},$$

    which gives the expression above when solved for $[\mathrm{A^-}]$. The fraction is the proportion of the acid present in the deprotonated form at a given pH. At $\mathrm{pH}=\mathrm{p}K_a$, it is $1/2$.
    ```

    The charge balance is

    $$[\mathrm{H_3O^+}]=[\mathrm{A^-}]+[\mathrm{OH^-}],$$

    and the ion product of water gives

    $$[\mathrm{OH^-}]=\frac{K_w}{[\mathrm{H_3O^+}]}.$$

    If we set $h=[\mathrm{H_3O^+}]$, the whole problem can be collected in one function:

    $$f(h)=h-C\frac{K_a}{h+K_a}-\frac{K_w}{h}.$$

    The pH is found when the charge balance is satisfied, that is, when $f(h)=0$. In other words, we do not have to isolate $h$ algebraically. It is enough to evaluate $f(h)$ and search for its root.

    Before solving an equation numerically, it is often useful to **visualise the function**. A graph can show us approximately where the root is, whether several roots exist, and which starting values might be sensible:
    '''),
    old[2],
    md(r'''
    ## From graph to algorithm

    To locate the root more precisely, we need an algorithm. A very simple idea is to start at a value $x$ and move along the graph with a fixed step size $dx$. At each step, we compare the signs of $f(x)$ and $f(x+dx)$. If the sign changes, a root must lie between the points as long as the function is continuous.

    ```{image} images/root_scan.png
    :width: 500px
    :align: center
    ```

    In the figure, $f(x_7)$ and $f(x_8)$ have opposite signs. The root must therefore lie somewhere between $x_7$ and $x_8$, and we can use the midpoint as a first estimate.

    This approach is intuitive, but not very efficient. If $dx$ is large, the answer is coarse. If $dx$ is small, we must examine many points. The idea of a **sign change** is nevertheless important because it leads directly to a more robust and efficient method: the *bisection method*.
    '''),
    code(r'''
    def f(x):
        return x**2 - x - 2

    x = -5
    x_end = 5
    dx = 0.5

    while x < x_end and f(x)*f(x + dx) > 0:
        x = x + dx

    root = (x + (x + dx))/2
    print("A first estimate is x =", root)
    '''),
    md(r'''
    ## The bisection method

    Instead of moving through the whole interval with equally sized steps, we can be smarter. We start with an interval $[a,b]$ where $f(a)$ and $f(b)$ have opposite signs. We then divide the interval in two and **discard the half that cannot contain the root**.

    We begin with the simplest possible code. Here we deliberately choose a function with a root that the algorithm can hit exactly, so that the idea is easy to follow.
    '''),
    code(r'''
    def f(x):
        return 2*x - 2

    a = -5
    b = 5
    m = (a + b)/2

    while f(m) != 0:
        if f(a)*f(m) < 0:
            b = m
        elif f(b)*f(m) < 0:
            a = m
        m = (a + b)/2

    print("The root is x =", m)
    '''),
    md(r'''
    Study the code line by line. Each iteration makes the interval half as wide. This is why the method is called the **bisection method**.

    More generally, the method works as follows:

    1. Choose an interval $[a,b]$ where $f(a)$ and $f(b)$ have opposite signs.
    2. Find the midpoint

    $$m=\frac{a+b}{2}.$$

    3. Determine which half, $[a,m]$ or $[m,b]$, still contains a sign change.
    4. Keep that half and repeat.

    ```{image} images/bisection.png
    :width: 500px
    :align: center
    ```

    The figure shows two iterations. The point is not that we know the root beforehand, but that we always know **which half it must lie in**.

    ### From exact equality to a tolerance

    In real numerical problems, we should not wait for `f(m) == 0`. Floating-point arithmetic and complicated functions mean that we may never hit zero exactly. Instead, we decide how close to zero is good enough. This is called a **tolerance**.
    '''),
    code(r'''
    def f(x):
        return x**2 - x - 2

    a = 0
    b = 5
    tolerance = 1E-8
    m = (a + b)/2

    while abs(f(m)) > tolerance:
        if f(a)*f(m) < 0:
            b = m
        elif f(b)*f(m) < 0:
            a = m
        m = (a + b)/2

    print("The root is x =", m)
    print("f(x) =", f(m))
    '''),
    md(r'''
    Now that we understand the algorithm as a concrete loop, it is natural to wrap it in a function so that we can use it on many problems without rewriting the code.
    '''),
    code(r'''
    def bisection(f, a, b, tol=1E-10, max_iterations=100):
        i = 0
        m = (a + b)/2

        while i < max_iterations and abs(f(m)) > tol:
            if f(a)*f(m) < 0:
                b = m
            elif f(b)*f(m) < 0:
                a = m
            m = (a + b)/2
            i = i + 1

        if i == max_iterations:
            print("The maximum number of iterations has been reached.")

        return m, i
    '''),
    md("We can now use the same function for our pH problem:"),
    code(r'''
    h_root, iterations = bisection(charge_balance, 1e-7, 1e-2)
    pH = -np.log10(h_root)

    print(f"[H3O+] = {h_root:.6e} mol/L")
    print(f"pH = {pH:.3f}")
    print("Iterations:", iterations)
    '''),
    md(r'''
    ### Try it yourself

    Complete the bisection method in the editor and use it to find the pH of the weak acid.

    <iframe src="../../basthon/?from=examples/equations_bisection.py" width="100%" height="600" frameborder="0" title="Try it yourself: the bisection method" loading="lazy" allowfullscreen></iframe>

    ## Newton's method

    The bisection method makes use of the fact that a root lies **between** two points. Newton's method uses a different idea: the tangent at one point can be used to predict where the root lies.

    1. Choose a starting guess $x_0$.
    2. Draw, or imagine, the tangent at $(x_0,f(x_0))$.
    3. Find where the tangent crosses the x-axis. This becomes the next guess, $x_1$.
    4. Repeat the process from the new point.

    ```{image} images/newton_method.png
    :width: 500px
    :align: center
    ```

    The figure shows why the method can approach a root much faster than bisection.

    Let us derive the formula. The tangent through $(x_n,f(x_n))$ has slope $f'(x_n)$:

    $$y=f(x_n)+f'(x_n)(x-x_n).$$

    We want the root of the tangent, so we set $y=0$:

    $$0=f(x_n)+f'(x_n)(x-x_n).$$

    Solving for $x$ gives the next estimate:

    $$x_{n+1}=x_n-\frac{f(x_n)}{f'(x_n)}.$$

    Again, we start with the simplest possible implementation before making a general function.
    '''),
    code(r'''
    def f(x):
        return x**2 - x - 2

    def f_derivative(x):
        return 2*x - 1

    x = 5
    tolerance = 1E-8

    while abs(f(x)) > tolerance:
        x = x - f(x)/f_derivative(x)

    print("The root is x =", x)
    '''),
    md("Once the algorithm is clear as a simple loop, we can wrap it in a function:"),
    code(r'''
    def newton_method(f, f_derivative, x, tol=1E-10):
        while abs(f(x)) > tol:
            x = x - f(x)/f_derivative(x)
        return x
    '''),
    md(r'''
    Newton's method needs only one starting guess and often converges quickly. The disadvantage is that we need the derivative, and an unfortunate starting guess can lead us to the wrong root or prevent the method from converging. At this stage, it is more important to **understand the limitation** than to build extensive error handling into the first implementation.

    Later, when we use ready-made library functions, we get more robustness and information about whether the method actually converged.

    ```{admonition} Exercise along the way
    :class: tip
    Try several different starting values for a function with more than one root. Do all starting guesses lead to the same root? What does this tell you about the difference between bisection and Newton's method?
    ```

    ## Ready-made solvers in SciPy

    Once we understand the principle, it is common to use tested algorithms from numerical libraries. `scipy.optimize.root_scalar` provides several methods for one-dimensional root-finding problems.
    '''),
    old[12],
    old[13],
    old[14],
]
save(path, nb, cells)


# ---------------------------------------------------------------------------
# Numerical differentiation
# ---------------------------------------------------------------------------
path, nb = load("numerical_differentiation.ipynb")
old = nb["cells"]

cells = [
    md(r'''
    # Numerical differentiation

    ```{admonition} Learning outcomes
    After working through this chapter, you should be able to:

    1. explain the difference between analytical and numerical differentiation
    2. implement forward, backward and central differences
    3. investigate how step size and round-off error affect the result
    4. differentiate experimental data and interpret what the numerical derivative means chemically
    ```

    ## The derivative

    Differentiation is about change. You may know the derivative as $f'(x)$. In science, Leibniz notation is also common,

    $$\frac{df}{dx},$$

    which means “the change in $f$ with respect to $x$”. The two notations describe the same quantity when $f$ is a function of $x$:

    $$f'(x)=\frac{df}{dx}.$$

    In chemistry, this notation is useful because the variables have a physical meaning. For example,

    $$\frac{dc}{dt}$$

    describes how a concentration changes with time, whereas

    $$\frac{d\mathrm{pH}}{dV}$$

    describes how pH changes as volume is added during a titration.

    The derivative is defined as the limit

    $$f'(x)=\lim_{\Delta x\rightarrow0}\frac{f(x+\Delta x)-f(x)}{\Delta x}.$$

    On a computer, we cannot use an infinitely small $\Delta x$. We therefore replace the limit with a small, finite step size $h$:

    $$f'(x)\approx\frac{f(x+h)-f(x)}{h}.$$

    This is called the **forward difference**.
    '''),
    old[2],
    code(r'''
    import numpy as np
    import matplotlib.pyplot as plt

    def f(x):
        return 2*x + 2

    x = 1.0
    h = 1E-8
    fder = (f(x + h) - f(x))/h

    print("Numerical:", fder)
    print("Analytical:", 2.0)
    '''),
    md(r'''
    This is the simplest implementation: we calculate the derivative at **one particular point**. Numerical differentiation does not automatically produce a new symbolic function in the way that differentiation by hand does. It gives values of the derivative at the points we choose.

    Once the principle is clear, we can wrap it in a Python function:
    '''),
    code(r'''
    def derivative_forward(f, x, h=1E-8):
        dy = f(x + h) - f(x)
        return dy/h
    '''),
    md("If we want to draw the derivative as a curve, we simply evaluate the derivative at many x values."),
    old[6],
    old[7],
    md(r'''
    ## Other approximations

    The forward difference uses the points $x$ and $x+h$. But this is not the only possible choice. We can just as well use the point **behind** $x$. This gives the backward difference:

    $$\frac{df}{dx}\approx\frac{f(x)-f(x-h)}{h}.$$

    The backward difference is not introduced because it is necessarily better than the forward difference. Rather, it shows that the same derivative can be approximated by choosing data points in different ways.

    Once we have one approximation that looks forward and one that looks backward, a natural idea appears: why not use information from **both sides** of the point? This gives the central difference:

    $$\frac{df}{dx}\approx\frac{f(x+h)-f(x-h)}{2h}.$$

    Here, the point $x$ lies halfway between the two points used to calculate the slope. For the same step size, this usually gives a better approximation than the forward or backward difference.

    ```{image} images/numerical_differentiation.png
    :width: 500px
    :align: center
    ```

    The figure illustrates the geometrical difference between the approximations.
    '''),
    code(r'''
    def derivative_backward(f, x, h=1E-8):
        return (f(x) - f(x - h))/h

    def derivative_central(f, x, h=1E-5):
        return (f(x + h) - f(x - h))/(2*h)

    x = 1.0
    print("Forward:", derivative_forward(np.sin, x, 1E-5))
    print("Backward:", derivative_backward(np.sin, x, 1E-5))
    print("Central:", derivative_central(np.sin, x, 1E-5))
    print("Analytical:", np.cos(x))
    '''),
    md(r'''
    ```{admonition} Exercise along the way
    :class: tip
    Perform an error analysis of the three approximations for several values of $h$. Use $f(x)=\sin x$ and compare with $f'(x)=\cos x$.
    ```
    '''),
] + old[10:]
save(path, nb, cells)


# ---------------------------------------------------------------------------
# Numerical integration
# ---------------------------------------------------------------------------
path, nb = load("numerical_integration.ipynb")
old = nb["cells"]

cells = [
    md(r'''
    # Numerical integration

    ```{admonition} Learning outcomes
    After working through this chapter, you should be able to:

    1. explain how a definite integral can be approximated as a sum of small areas
    2. implement and explain the difference between left, right and midpoint approximations
    3. explain and implement the trapezoidal method
    4. compare numerical methods using error and convergence
    5. integrate functions and experimental data with SciPy
    6. interpret integrals in a chemical context
    ```

    ## Integration

    You may know integration both as a method for finding the area under a graph and as the inverse operation of differentiation. In this chapter, we are mainly concerned with **definite integrals**, that is, integrals between two limits $a$ and $b$.

    A computer works with finite numbers and discrete points. We therefore do not ask it to “find an antiderivative” in the same way as we do symbolically. Instead, we approximate the area under the graph by dividing it into many small pieces.

    ## Integrals in chemistry

    Numerical integration appears in many areas of chemistry, for example when we calculate

    - the area under a chromatographic peak
    - the area under an NMR signal
    - accumulated heat or electrical charge over time
    - integrals that occur in numerical solutions of differential equations

    A major advantage of numerical integration is that we can also integrate **experimental data**, for which we do not necessarily have an analytical function.
    '''),
    md(r'''
    ## The rectangle method: from integral to Riemann sum

    A definite integral can be understood as the limit of a **Riemann sum**: we divide the area under the graph into narrow strips and approximate each strip with a simple geometrical shape. The simplest shape is a rectangle.

    ```{image} images/rectangles_10.png
    :width: 500px
    :align: center
    ```

    Here, the interval is divided into 10 rectangles. If the interval is $[a,b]$ and we use $n$ rectangles, their width is

    $$h=\frac{b-a}{n}.$$

    In the figure, the height is determined by the function value at the **left edge** of each rectangle. This gives the left approximation.

    If we increase the number of rectangles, they follow the graph more closely:

    ```{image} images/rectangles_50.png
    :width: 500px
    :align: center
    ```

    This is the basic idea behind numerical integration: more, narrower geometrical shapes usually give a better approximation.

    ### Left approximation

    We begin with the code without making a function. This makes the algorithm easier to understand:
    '''),
    code(r'''
    import numpy as np
    import matplotlib.pyplot as plt

    def f(x):
        return np.cos(x) + 2

    a = 2
    b = 12
    n = 10

    h = (b - a) / n
    area = 0.0
    x = a

    for k in range(n):
        area = area + f(x) * h
        x = x + h

    print("Numerical area:", area)
    '''),
    md(r'''
    The loop does exactly what the figure shows: calculate the area of one rectangle, add it to the total, move $x$ one rectangle width, and repeat.

    Once the algorithm is clear, we wrap it in a function:
    '''),
    code(r'''
    def rectangle_left(f, a, b, n):
        h = (b - a) / n
        area = 0.0
        x = a

        for k in range(n):
            area = area + f(x) * h
            x = x + h

        return area
    '''),
    md(r'''
    ### Where should we measure the height?

    The left edge is only one possible choice. For an increasing function, the left approximation will systematically lie **below** the graph:

    ```{image} images/rectangles_left_10.png
    :width: 500px
    :align: center
    ```

    If we instead measure the height at the **right edge**, we obtain a corresponding overestimate:

    ```{image} images/rectangles_right_10.png
    :width: 500px
    :align: center
    ```

    This is an important point: there are several ways to approximate the same area. The right approximation requires only one small change to the algorithm – we start at $a+h$ instead of $a$.
    '''),
    code(r'''
    def rectangle_right(f, a, b, n):
        h = (b - a) / n
        area = 0.0
        x = a + h

        for k in range(n):
            area = area + f(x) * h
            x = x + h

        return area
    '''),
    md(r'''
    ### Midpoint approximation

    When the left edge gives too little area and the right edge gives too much, it is natural to ask whether we can choose a point **between them**. We then use the function value at the midpoint of each subinterval:

    ```{image} images/rectangles_midpoint_10.png
    :width: 500px
    :align: center
    ```

    For a linear function, the error areas above and below the graph cancel exactly, so the midpoint approximation is exact. For many curved functions, it is also considerably better than the left and right approximations.
    '''),
    code(r'''
    def rectangle_midpoint(f, a, b, n):
        h = (b - a) / n
        area = 0.0
        x = a + h/2

        for k in range(n):
            area = area + f(x) * h
            x = x + h

        return area

    exact = (np.sin(12) + 2*12) - (np.sin(2) + 2*2)

    print("Left:", rectangle_left(f, 2, 12, 10))
    print("Right:", rectangle_right(f, 2, 12, 10))
    print("Midpoint:", rectangle_midpoint(f, 2, 12, 10))
    print("Exact:", exact)
    '''),
    old[5],
    old[6],
    md(r'''
    ## The trapezoidal method

    The rectangle methods assume that the top of each small shape is **horizontal**. In other words, we replace the function locally with a constant value. This works, but if the function changes noticeably through the interval, we are throwing away information.

    A natural improvement is to draw a **straight line between the two endpoints**. This gives a trapezoid instead of a rectangle:

    ```{image} images/trapezoid_1.png
    :width: 500px
    :align: center
    ```

    For one subinterval of width $h$, the two parallel sides are $f(x_i)$ and $f(x_{i+1})$. The area is therefore

    $$A_i=\frac{f(x_i)+f(x_{i+1})}{2}h.$$

    For the complete interval, we add one such trapezoid for each subinterval. We can write this as

    $$\int_a^b f(x)\,dx\approx h\left[\frac{f(a)+f(b)}{2}+\sum_{i=1}^{n-1}f(x_i)\right].$$

    Again, we first implement the algorithm directly:
    '''),
    code(r'''
    def f(x):
        return x**3

    a = 0
    b = 5
    n = 100

    h = (b - a) / n
    area = 0.0
    x = a

    for k in range(n):
        area = area + (f(x) + f(x + h))/2 * h
        x = x + h

    print("Trapezoidal:", area)
    '''),
    md("We can then wrap exactly the same loop in a function:"),
    code(r'''
    def trapezoidal_method(f, a, b, n):
        h = (b - a) / n
        area = 0.0
        x = a

        for k in range(n):
            area = area + (f(x) + f(x + h))/2 * h
            x = x + h

        return area

    print("Trapezoidal:", trapezoidal_method(f, 0, 5, 100))
    print("Exact:", 156.25)
    '''),
    md(r'''
    As the number of trapezoids increases, the straight line segments follow the graph more closely:

    ```{image} images/trapezoids_10.png
    :width: 500px
    :align: center
    ```

    ## Simpson's method

    We can view the rectangle and trapezoidal methods as a small progression:

    - rectangle: the function is approximated locally by a **constant**
    - trapezoid: the function is approximated locally by a **straight line**

    The next step is to use a curved top. Simpson's method uses quadratic polynomials over pairs of subintervals, and is often very accurate for smooth functions.

    For an even number $n$, the method can be written

    $$\int_a^b f(x)\,dx\approx\frac{h}{3}\left[f(a)+f(b)+4\sum_{\text{odd }k}f(x_k)+2\sum_{\text{even }k}f(x_k)\right].$$

    The code is a little less intuitive than the rectangle and trapezoidal methods, so the main goal is to recognise the structure of the formula.
    '''),
    code(r'''
    def simpsons_method(f, a, b, n):
        if n % 2 != 0:
            print("n must be even.")
            return None

        h = (b - a) / n
        area = f(a) + f(b)
        x = a + h

        for k in range(1, n):
            if k % 2 == 0:
                area = area + 2*f(x)
            else:
                area = area + 4*f(x)
            x = x + h

        return area * h/3

    print("Simpson:", simpsons_method(f, 0, 5, 100))
    '''),
    md(r'''
    The rectangle methods, the trapezoidal method and Simpson's method belong to the same family of integration methods, **Newton–Cotes methods**. We do not need to learn the whole family; the important idea is to see how better approximations can be constructed by using more information about the shape of the function.
    '''),
] + old[11:]
save(path, nb, cells)


# ---------------------------------------------------------------------------
# Differential equations and rate laws
# ---------------------------------------------------------------------------
path, nb = load("differential_equations.ipynb")
old = nb["cells"]

cells = [
    md(r'''
    # Differential equations and rate laws

    ```{admonition} Learning outcomes
    After working through this chapter, you should be able to:

    1. explain how a differential equation describes change in a dynamic system
    2. derive and implement the Forward Euler method
    3. model simple and coupled chemical rate laws
    4. investigate how the time step affects numerical error and stability
    5. use `solve_ivp` to solve initial-value problems
    6. validate a simulation using analytical solutions, mass balance and chemical plausibility
    ```

    ## Motivation

    Experiments are central to chemistry, but simulations have become an important supplement. A simulation can help us investigate how a chemical system evolves when we change a parameter, test a model against experimental data, or study systems that are difficult to follow directly.

    Often, we do not know a ready-made expression for the evolution, but we do know the **change**. A classic example is a rate law. For a first-order reaction

    $$\mathrm{A\rightarrow products}$$

    we have

    $$\frac{d[A]}{dt}=-k[A].$$

    The equation tells us how the concentration changes right now. Our task is to use this information to find the complete evolution, $[A](t)$.

    ## What is a differential equation?

    A differential equation is an equation containing an unknown function and one or more derivatives of that function. You may encounter many forms:

    $$y'=y$$

    $$y'=t-y$$

    $$u'(t)=u(t)$$

    or, more generally,

    $$y'(t)=\frac{dy}{dt}=f(t,y).$$

    What they have in common is that the left-hand side describes the **change**, while the right-hand side tells us what the change depends on.

    When we solve an ordinary algebraic equation, we search for a number. When we solve a differential equation, we search for a **function** or, numerically, a sequence of function values.

    ### Why do we need an initial value?

    Consider the very simple differential equation

    $$y'=1.$$

    Integrating gives

    $$y=t+C.$$

    There are therefore infinitely many solutions – one for each value of the constant $C$. If we also know that

    $$y(0)=2,$$

    then $C=2$, and we obtain one particular solution. Such information is called an **initial condition**.

    In chemistry, an initial condition may for example be the starting concentration $[A](0)$.

    ## From the derivative to Euler's method

    From numerical differentiation, we know the forward difference:

    $$\frac{dy}{dt}\approx\frac{y(t+\Delta t)-y(t)}{\Delta t}.$$

    We now use it in a slightly different way. We know $y(t)$ and the expression for the derivative $dy/dt$, and we want to find the **next value**, $y(t+\Delta t)$.

    First, multiply by $\Delta t$:

    $$\frac{dy}{dt}\Delta t\approx y(t+\Delta t)-y(t).$$

    Then move $y(t)$ to the other side:

    $$y(t+\Delta t)\approx y(t)+\frac{dy}{dt}\Delta t.$$

    If we write the differential equation as $dy/dt=f(t,y)$ and use indices, we obtain

    $$y_{n+1}=y_n+f(t_n,y_n)\Delta t.$$

    This is **Forward Euler**. Notice the connection to the previous numerical ideas: we have turned a continuous differential equation into a **difference equation** that the computer can repeat step by step.
    '''),
    md(r'''
    ## First-order reaction with Euler

    We use

    $$\frac{d[A]}{dt}=-k[A].$$

    Before writing a general Euler function, we spell out the algorithm directly. This makes the connection between the rate law and the code as clear as possible.
    '''),
    code(r'''
    import numpy as np
    import matplotlib.pyplot as plt

    k = 0.03
    A0 = 1.0
    dt = 1.0
    t_end = 150

    time = np.arange(0, t_end + dt, dt)
    A = np.zeros(len(time))
    A[0] = A0

    for n in range(len(time) - 1):
        rate_of_change = -k*A[n]
        A[n + 1] = A[n] + rate_of_change*dt

    plt.plot(time, A)
    plt.xlabel("Time (s)")
    plt.ylabel("[A] (mol/L)")
    plt.show()
    '''),
    md(r'''
    The loop follows Euler's formula directly: calculate the rate of change from the current concentration, multiply by the time step, and use that change to obtain the next concentration.

    Once this update rule is clear, we can write a general Euler function. The function receives the differential equation itself as the function `f`.
    '''),
    code(r'''
    def first_order(t, A):
        return -k*A

    def euler(f, y0, t_start, t_end, dt):
        time = np.arange(t_start, t_end + dt, dt)
        y = np.zeros(len(time))
        y[0] = y0

        for n in range(len(time) - 1):
            y[n + 1] = y[n] + f(time[n], y[n])*dt

        return time, y

    time, A_euler = euler(first_order, A0, 0, 150, 1.0)
    A_analytical = A0*np.exp(-k*time)

    plt.plot(time, A_euler, label="Euler")
    plt.plot(time, A_analytical, "--", label="Analytical")
    plt.xlabel("Time (s)")
    plt.ylabel("[A] (mol/L)")
    plt.legend()
    plt.show()

    print("Largest absolute error:", np.max(np.abs(A_euler - A_analytical)))
    '''),
    md(r'''
    ## How large should the time step be?

    Euler assumes that the slope we have **now** is a good approximation throughout the next time step. If the time step is large and the system changes rapidly, that assumption becomes poor.

    We should therefore not investigate only one value of $\Delta t$. An important numerical check is:

    > Does the solution change substantially if we reduce the time step?

    Forward Euler is a **first-order method**, meaning that its global error decreases approximately in proportion to $\Delta t$ for a sufficiently smooth problem.
    '''),
    code(r'''
    for dt_test in [10.0, 5.0, 1.0, 0.2]:
        t_test, A_test = euler(first_order, A0, 0, 150, dt_test)
        A_exact = A0*np.exp(-k*t_test[-1])
        error = abs(A_test[-1] - A_exact)
        print(f"dt = {dt_test:4.1f} s   final error = {error:.3e}")
    '''),
] + old[6:]
save(path, nb, cells)


# Update the Euler Basthon activity to use the same first-order example.
basthon = ROOT / "docs" / "_static" / "basthon_examples" / "differential_equation_euler_reaction.py"
basthon.write_text(clean(r'''
import numpy as np
import matplotlib.pyplot as plt

k = 0.03
A0 = 1.0
dt = 1.0
t_end = 150

time = np.arange(0, t_end + dt, dt)
A = np.zeros(len(time))
A[0] = A0

for n in range(len(time) - 1):
    # Complete the Euler update:
    # A[n + 1] = ...
    A[n + 1] = A[n]

analytical = A0*np.exp(-k*time)

plt.plot(time, A, "o-", label="Euler")
plt.plot(time, analytical, label="Analytical")
plt.xlabel("Time (s)")
plt.ylabel("[A] (mol/L)")
plt.legend()
plt.show()
'''), encoding="utf-8")

# Keep a readable, temporary inspection file for the next CI pass.
lines = []
for name in [
    "equations.ipynb",
    "numerical_differentiation.ipynb",
    "numerical_integration.ipynb",
    "differential_equations.ipynb",
]:
    p = BASE / name
    notebook = json.loads(p.read_text(encoding="utf-8"))
    lines.append(f"===== {p.relative_to(ROOT)} | {len(notebook['cells'])} cells =====")
    for i, cell in enumerate(notebook["cells"]):
        lines.append(f"--- CELL {i:02d} [{cell['cell_type']}] ---")
        lines.append("".join(cell.get("source", [])))
    lines.append("")
(ROOT / "numerical_inspection_after.txt").write_text("\n".join(lines), encoding="utf-8")
