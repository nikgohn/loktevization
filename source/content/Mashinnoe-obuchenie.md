# Задача классификации

Исходные данные


| Номер объекта | Признаки |     |     |       | Метка класса |
| ------------- | -------- | --- | --- | ----- | ------------ |
|               | x1       | x2  | ... | $x_m$ |              |
| 1             |          |     |     |       | y1           |
| 2             |          |     |     |       | y2           |
| ...           |          |     |     |       | ...          |
| N             |          |     |     |       | ym           |
Бинарная классификация
$y_i\in \{0:1\}$
$y_i\in \{-1:1\}$

Многоклассовая классификация
$y_i\in\{0,1,2,...,k\}$


$$X = \begin{pmatrix} x_{1} \\ x_{2} \\ \vdots \\ x_{m} \end{pmatrix}, \quad x_i = \begin{pmatrix} x_{i1} \\ x_{i2} \\ \vdots \\ x_{im} \end{pmatrix}$$
$x_i$ - признаки объекта с номером i

$y_i$ - метка класса объекта i

## Бинарная линейная классификация

$$y_i \in \{-1, 1\}$$
$$w = \begin{pmatrix} w_1 \\ w_2 \\ w_m \end{pmatrix} \rightarrow \text{Настраиваемое мир параматри}
$$$$w_0$$
$$f(x) = \langle w, x \rangle + w_0$$

ОПР Функция знак
$$
\text{sign}(x)=
\begin{cases}
1, & x>0 \\
0, & x=0 \\
-1, & x<0
\end{cases}
$$
предсказание класса
$f(x_i)=\text{sign}(\langle\omega, x_i\rangle + b)$


Найдем $\omega, \omega_0$
$$
\begin{cases}
y_i=1, & \langle\omega, x_i\rangle + \omega_0 > 0 \\
y_i=-1, & \langle\omega, x_i\rangle + \omega_0 < 0
\end{cases}
$$
$y_i(\langle\omega, x_i\rangle + \omega_0) > 0$ - условие верней Класси
Опр Отступ (Margin) - это
$M_i = y_i (\langle\omega, x_i\rangle + \omega_0)$

ОПР логическая скобка
$$
I[a] =
\begin{cases}
1, & a - верн\text{o} \\
0, & a - ложн\text{o}
\end{cases}
$$
$M_i < 0$ - не верно классифицировано

$$
\text{loss}(\omega) = \sum_{i=1}^{N} I[M_i<0] \rightarrow \underset{\omega,\omega_0}{\text{min}}
$$
$$
\text{loss}(\omega) = \sum_{i=1}^{N} I[y_i(\langle\omega, x_i\rangle + \omega_0) < 0] \rightarrow \underset{\omega,\omega_0}{\text{min}}
$$
Проблемы метода
1) $I[M_i<0]$ - Ступенчатая

![[Pasted image 20250915104129.png]]

2) $\nabla L$ - не существует при $M_i = 0$.
$\nabla L = 0$ при $M_i \neq 0$
Не решить град. мет.
3) $\omega, \omega_0$ - определены не однозначно

## Метод опорных векторов

линейно разделяемая Класса {-1; 1}
$\langle w,x \rangle + w_0 = 0$
$\langle w,x \rangle + w_0 = -1$
$\rho \rightarrow max$

![[Pasted image 20250915105041.png]]

$\langle w, x \rangle + w_0 = 1$


$$\rho = hpr\omega(x^+ - x^-)$$
$$
\rho = \frac{\langle x^+ - x^-, \omega \rangle}{\|\omega\|}
$$
$$
\rho = \frac{\langle x^+, \omega \rangle - \langle x^-, \omega \rangle}{\|\omega\|}
$$
$$
\rho = \frac{1 - \omega_0 - (-1 - \omega_0)}{\|\omega\|}
$$
$$
\rho = \frac{2}{\|\omega\|} \rightarrow \underset{\omega}{\text{max}}
$$
$$
\frac{\|\omega\|^2}{2} - \underset{\omega}{\text{min}}
$$
$$
\begin{cases}
y=1, & \langle\omega, x\rangle + \omega_0 \ge 1 \\
y=-1, & \langle\omega, x\rangle + \omega_0 \le -1
\end{cases}
$$
$$
\left\{ \begin{array}{l}
\delta(\langle\omega, x\rangle+\omega_0) \ge 1 \\
-1(\langle\omega, x\rangle+\omega_0) \ge 1
\end{array} \right.
$$
$$
y_i(\langle\omega, x_i\rangle+\omega_0) \ge 1
$$
$$M_i \ge 1$$


$$
\begin{cases}
\frac{\langle \omega, \omega \rangle}{2} - \underset{\omega}{\text{min}} \\
1 - y_i(\langle \omega, x_i \rangle + \omega_0) \le 0, i=1, \ldots, N
\end{cases}
$$
Условия для поиска $\omega, \omega_0$
$1 - M_i \le 0, M_i \ge 1$ - условие верной Классификации

Метод решения системы для $w_1,\ w_0$ - это линейный метод лагранжа

$$
\begin{cases}
\frac{\langle \omega, \omega \rangle}{2} - \underset{\omega}{\min} \\
1 - y_i(\langle \omega, x_i \rangle + \omega_0) \le 0, \quad i = 1, \ldots, N
\end{cases}
$$
Функция Лагранжа
$$
L(\omega, \omega_0, \lambda_i) = \frac{\langle \omega, \omega \rangle}{2} + \sum_{i=1}^N \lambda_i (1 - y_i(\langle \omega, x_i \rangle + \omega_0))\rightarrow \underset{\omega,\omega_0}{\min} \underset{\lambda_i}{\max}
$$
$$ \lambda_i \ge 0
$$
Я понимаю, вы хотите, чтобы все четыре уравнения были представлены как единая система. Вот как это можно записать:

$$
\begin{cases}
\omega - \sum_{i=1}^N \lambda_i y_i x_i = 0 \\
- \sum_{i=1}^N \lambda_i y_i = 0 \\
\lambda_i > 0 \quad \\
y_i(\langle \omega, x_i \rangle + \omega_0) \ge 1 \quad
\end{cases}
$$

$$
\begin{cases}
\omega = \sum_{i=1}^N \lambda_i y_i x_i \\
\sum_{i=1}^N \lambda_i y_i = 0 \\
\lambda_i > 0 \\
\lambda_i(1 - M_i) = 0\ \quad i=1, 2, \ldots, N
\end{cases}
$$
Типы объектов:
1) $\lambda_i = 0, M_i > 1$
Верно классиф. объект
$\omega = 0$ (не участвует в расчетах)
2) $M_i = 1$, $\lambda_i > 0$, $\omega \neq 0$.
Опорный объект
(Участвуют в расчетах)

![[Pasted image 20250915111235.png]]

2) Линейно неразделяемый объекты
$$
\begin{cases}
\frac{\langle \omega, \omega \rangle}{2} + c \cdot \sum_{i=1}^N \varepsilon_i \\
y_i(\langle \omega, x_i \rangle + \omega_0) \ge 1 - \varepsilon_i
\end{cases}
$$
$\varepsilon_i$ – отступ, $\varepsilon_i > 0$.

Классификадция
1) $M_i > 1$, $\lambda_i = 0$, $\varepsilon_i = 0$
верно классиф. объект
$\omega = 0$

2) $M_i = 1$, $\lambda_i > 0$, $\omega \neq 0$.
Опорний объект

3) $M_i < 0$, $\varepsilon_i > 1$
не верно классиф

![[Pasted image 20250915111845.png]]

$$
\begin{cases}
-L(\omega) = -\sum_{i=1}^{N} d_i + \frac{1}{2} \sum_{i,j=1}^{N} d_i d_j y_i y_j \underbrace{\langle x_i, x_j \rangle}_{\text{скалярное произв}} \rightarrow \min_{d_i} \\
0 \le d_i \le C \\
d_i(1 - \varepsilon_i - y_i(\langle \omega, x_i \rangle + \omega_0)) = 0
\end{cases}
$$
Ядерный SVM
Идея $\langle x_i, x_j \rangle \rightarrow K(x_i, x_j)$ - ядро.

![[Pasted image 20250915112704.png]]

![[IMG_20250915_112653822.jpg]]

Конструктивный подход к ядрам
1) $\langle x, x' \rangle$ - это ядро
2) $1$ - это ядро
3) Произведение двух ядер - это ядро
4) Если $\psi(x)$ - функция, то $K(x, x') = \psi(x) \cdot \psi(x')$ - ядро
5) Линейная комбинация $\alpha_1 K_1 + \alpha_2 K_2$ - ядро, $\alpha_1 > 0, \alpha_2 > 0$

# Многоклассовое обучение