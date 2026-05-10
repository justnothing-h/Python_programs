"""
generator.py
Generates random C++ (and optionally other language) source files.
Uses multiple code templates with randomized content to ensure unique commits.
"""

import os
import random
import string
import time
import json
from datetime import datetime
from typing import Optional
from utils.logger import get_logger
from utils.config_loader import load_config, get

logger = get_logger("generator")


# ─── C++ Template Library ────────────────────────────────────────────────────

CPP_TEMPLATES = [

    # Template 1: Sorting algorithms
    lambda ctx: f"""\
// Auto-generated: {ctx['timestamp']}
// Module: Sorting Utility — {ctx['uid']}
#include <iostream>
#include <vector>
#include <algorithm>
#include <chrono>

namespace sort_util_{ctx['tag']} {{

    void bubble_sort(std::vector<int>& arr) {{
        int n = arr.size();
        for (int i = 0; i < n - 1; ++i)
            for (int j = 0; j < n - i - 1; ++j)
                if (arr[j] > arr[j + 1])
                    std::swap(arr[j], arr[j + 1]);
    }}

    void selection_sort(std::vector<int>& arr) {{
        int n = arr.size();
        for (int i = 0; i < n - 1; ++i) {{
            int min_idx = i;
            for (int j = i + 1; j < n; ++j)
                if (arr[j] < arr[min_idx])
                    min_idx = j;
            std::swap(arr[i], arr[min_idx]);
        }}
    }}

    void print_array(const std::vector<int>& arr) {{
        for (int x : arr) std::cout << x << " ";
        std::cout << "\\n";
    }}

}} // namespace sort_util_{ctx['tag']}

int main() {{
    std::vector<int> data = {{ {ctx['nums']} }};
    std::cout << "Before: ";
    sort_util_{ctx['tag']}::print_array(data);
    sort_util_{ctx['tag']}::bubble_sort(data);
    std::cout << "After:  ";
    sort_util_{ctx['tag']}::print_array(data);
    return 0;
}}
""",

    # Template 2: Math utilities
    lambda ctx: f"""\
// Auto-generated: {ctx['timestamp']}
// Module: Math Utils — {ctx['uid']}
#include <iostream>
#include <cmath>
#include <vector>
#include <numeric>

namespace math_{ctx['tag']} {{

    double factorial(int n) {{
        if (n <= 1) return 1.0;
        return n * factorial(n - 1);
    }}

    bool is_prime(int n) {{
        if (n < 2) return false;
        for (int i = 2; i <= static_cast<int>(std::sqrt(n)); ++i)
            if (n % i == 0) return false;
        return true;
    }}

    std::vector<int> sieve(int limit) {{
        std::vector<bool> is_p(limit + 1, true);
        std::vector<int> primes;
        is_p[0] = is_p[1] = false;
        for (int i = 2; i <= limit; ++i) {{
            if (is_p[i]) {{
                primes.push_back(i);
                for (int j = 2 * i; j <= limit; j += i)
                    is_p[j] = false;
            }}
        }}
        return primes;
    }}

    double mean(const std::vector<double>& v) {{
        return std::accumulate(v.begin(), v.end(), 0.0) / v.size();
    }}

}} // namespace math_{ctx['tag']}

int main() {{
    std::cout << "Factorial({ctx['n1']}) = " << math_{ctx['tag']}::factorial({ctx['n1']}) << "\\n";
    auto primes = math_{ctx['tag']}::sieve({ctx['n2']});
    std::cout << "Primes up to {ctx['n2']}: ";
    for (int p : primes) std::cout << p << " ";
    std::cout << "\\n";
    return 0;
}}
""",

    # Template 3: Linked List
    lambda ctx: f"""\
// Auto-generated: {ctx['timestamp']}
// Module: Linked List — {ctx['uid']}
#include <iostream>
#include <memory>
#include <stdexcept>

namespace ds_{ctx['tag']} {{

    template<typename T>
    struct Node {{
        T data;
        std::shared_ptr<Node<T>> next;
        explicit Node(T val) : data(val), next(nullptr) {{}}
    }};

    template<typename T>
    class LinkedList {{
        std::shared_ptr<Node<T>> head;
        int size_ = 0;
    public:
        void push_front(T val) {{
            auto node = std::make_shared<Node<T>>(val);
            node->next = head;
            head = node;
            ++size_;
        }}
        void push_back(T val) {{
            auto node = std::make_shared<Node<T>>(val);
            if (!head) {{ head = node; ++size_; return; }}
            auto cur = head;
            while (cur->next) cur = cur->next;
            cur->next = node;
            ++size_;
        }}
        int size() const {{ return size_; }}
        void print() const {{
            auto cur = head;
            while (cur) {{ std::cout << cur->data << " -> "; cur = cur->next; }}
            std::cout << "NULL\\n";
        }}
        void reverse() {{
            std::shared_ptr<Node<T>> prev = nullptr, cur = head, next;
            while (cur) {{ next = cur->next; cur->next = prev; prev = cur; cur = next; }}
            head = prev;
        }}
    }};

}} // namespace ds_{ctx['tag']}

int main() {{
    ds_{ctx['tag']}::LinkedList<int> list;
    for (int x : {{ {ctx['nums']} }}) list.push_back(x);
    std::cout << "List: "; list.print();
    list.reverse();
    std::cout << "Reversed: "; list.print();
    std::cout << "Size: " << list.size() << "\\n";
    return 0;
}}
""",

    # Template 4: File I/O + string processing
    lambda ctx: f"""\
// Auto-generated: {ctx['timestamp']}
// Module: String Processor — {ctx['uid']}
#include <iostream>
#include <string>
#include <sstream>
#include <vector>
#include <algorithm>
#include <cctype>

namespace str_{ctx['tag']} {{

    std::string to_upper(std::string s) {{
        std::transform(s.begin(), s.end(), s.begin(), ::toupper);
        return s;
    }}

    std::string to_lower(std::string s) {{
        std::transform(s.begin(), s.end(), s.begin(), ::tolower);
        return s;
    }}

    std::vector<std::string> split(const std::string& s, char delim) {{
        std::vector<std::string> tokens;
        std::stringstream ss(s);
        std::string token;
        while (std::getline(ss, token, delim)) tokens.push_back(token);
        return tokens;
    }}

    std::string trim(const std::string& s) {{
        auto start = s.find_first_not_of(" \\t\\n\\r");
        auto end   = s.find_last_not_of(" \\t\\n\\r");
        return (start == std::string::npos) ? "" : s.substr(start, end - start + 1);
    }}

    bool is_palindrome(const std::string& s) {{
        std::string clean;
        for (char c : s) if (std::isalnum(c)) clean += std::tolower(c);
        return clean == std::string(clean.rbegin(), clean.rend());
    }}

    int count_words(const std::string& s) {{
        auto tokens = split(trim(s), ' ');
        return static_cast<int>(tokens.size());
    }}

}} // namespace str_{ctx['tag']}

int main() {{
    std::string sample = "{ctx['sample_str']}";
    std::cout << "Original: " << sample << "\\n";
    std::cout << "Upper:    " << str_{ctx['tag']}::to_upper(sample) << "\\n";
    std::cout << "Words:    " << str_{ctx['tag']}::count_words(sample) << "\\n";
    std::cout << "Palindrome check 'racecar': "
              << (str_{ctx['tag']}::is_palindrome("racecar") ? "yes" : "no") << "\\n";
    return 0;
}}
""",

    # Template 5: Stack + Queue
    lambda ctx: f"""\
// Auto-generated: {ctx['timestamp']}
// Module: Stack & Queue — {ctx['uid']}
#include <iostream>
#include <stdexcept>
#include <vector>

namespace ds_{ctx['tag']} {{

    template<typename T>
    class Stack {{
        std::vector<T> data;
    public:
        void push(T val) {{ data.push_back(val); }}
        T pop() {{
            if (data.empty()) throw std::underflow_error("Stack underflow");
            T top = data.back(); data.pop_back(); return top;
        }}
        T peek() const {{
            if (data.empty()) throw std::underflow_error("Stack empty");
            return data.back();
        }}
        bool empty() const {{ return data.empty(); }}
        int size() const {{ return static_cast<int>(data.size()); }}
    }};

    template<typename T>
    class CircularQueue {{
        std::vector<T> buf;
        int head = 0, tail = 0, count = 0;
        int cap;
    public:
        explicit CircularQueue(int cap) : buf(cap), cap(cap) {{}}
        void enqueue(T val) {{
            if (count == cap) throw std::overflow_error("Queue full");
            buf[tail] = val; tail = (tail + 1) % cap; ++count;
        }}
        T dequeue() {{
            if (count == 0) throw std::underflow_error("Queue empty");
            T val = buf[head]; head = (head + 1) % cap; --count; return val;
        }}
        int size() const {{ return count; }}
    }};

}} // namespace ds_{ctx['tag']}

int main() {{
    ds_{ctx['tag']}::Stack<int> stk;
    for (int x : {{ {ctx['nums']} }}) stk.push(x);
    std::cout << "Stack peek: " << stk.peek() << "  size: " << stk.size() << "\\n";

    ds_{ctx['tag']}::CircularQueue<int> q(10);
    for (int x : {{ {ctx['nums']} }}) q.enqueue(x);
    std::cout << "Queue size: " << q.size() << "\\n";
    std::cout << "Dequeued:   " << q.dequeue() << "\\n";
    return 0;
}}
""",

    # Template 6: Matrix operations
    lambda ctx: f"""\
// Auto-generated: {ctx['timestamp']}
// Module: Matrix Math — {ctx['uid']}
#include <iostream>
#include <vector>
#include <iomanip>
#include <stdexcept>

using Matrix = std::vector<std::vector<double>>;

namespace matrix_{ctx['tag']} {{

    Matrix create(int rows, int cols, double fill = 0.0) {{
        return Matrix(rows, std::vector<double>(cols, fill));
    }}

    Matrix multiply(const Matrix& A, const Matrix& B) {{
        int m = A.size(), n = B[0].size(), k = B.size();
        if (A[0].size() != static_cast<size_t>(k))
            throw std::invalid_argument("Dimension mismatch");
        Matrix C = create(m, n);
        for (int i = 0; i < m; ++i)
            for (int j = 0; j < n; ++j)
                for (int p = 0; p < k; ++p)
                    C[i][j] += A[i][p] * B[p][j];
        return C;
    }}

    Matrix transpose(const Matrix& A) {{
        int m = A.size(), n = A[0].size();
        Matrix T = create(n, m);
        for (int i = 0; i < m; ++i)
            for (int j = 0; j < n; ++j)
                T[j][i] = A[i][j];
        return T;
    }}

    void print(const Matrix& M) {{
        for (auto& row : M) {{
            for (double v : row) std::cout << std::setw(8) << std::fixed << std::setprecision(2) << v;
            std::cout << "\\n";
        }}
    }}

}} // namespace matrix_{ctx['tag']}

int main() {{
    Matrix A = {{{ctx['mat_row1']}}};
    Matrix B = matrix_{ctx['tag']}::transpose(A);
    std::cout << "A:\\n"; matrix_{ctx['tag']}::print(A);
    std::cout << "A^T:\\n"; matrix_{ctx['tag']}::print(B);
    Matrix C = matrix_{ctx['tag']}::multiply(A, B);
    std::cout << "A * A^T:\\n"; matrix_{ctx['tag']}::print(C);
    return 0;
}}
"""
]


SAMPLE_STRINGS = [
    "hello world from github bot",
    "automated commit system running",
    "code generation complete",
    "continuous integration pipeline",
    "open source contribution",
]

MATRIX_ROWS = [
    "{{1.0, 2.0, 3.0}}, {{4.0, 5.0, 6.0}}",
    "{{2.0, 0.0, 1.0}}, {{1.0, 3.0, 2.0}}",
    "{{5.0, 1.0, 0.0}}, {{2.0, 4.0, 1.0}}",
]


def _make_context(uid: str) -> dict:
    tag = uid[:8]
    nums = ", ".join(str(random.randint(1, 99)) for _ in range(random.randint(6, 10)))
    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "uid": uid,
        "tag": tag,
        "nums": nums,
        "n1": random.randint(5, 12),
        "n2": random.randint(30, 80),
        "sample_str": random.choice(SAMPLE_STRINGS),
        "mat_row1": random.choice(MATRIX_ROWS),
    }


def _random_uid() -> str:
    ts = str(int(time.time() * 1000))
    rand = "".join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return f"{ts}_{rand}"


def generate_cpp_file(output_dir: str, cfg: dict) -> Optional[str]:
    """
    Generate a random C++ source file in output_dir.
    Returns the full path of the generated file, or None on failure.
    """
    os.makedirs(output_dir, exist_ok=True)
    uid = _random_uid()
    template_fn = random.choice(CPP_TEMPLATES)
    ctx = _make_context(uid)

    try:
        code = template_fn(ctx)
    except Exception as e:
        logger.error(f"Template rendering failed: {e}")
        return None

    filename = f"gen_{uid}.cpp"
    filepath = os.path.join(output_dir, filename)

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(code)
        logger.info(f"Generated file: {filename} ({len(code)} chars)")
        return filepath
    except Exception as e:
        logger.error(f"Failed to write file {filepath}: {e}")
        return None


def generate_file(output_dir: str, cfg: dict) -> Optional[str]:
    """
    Entry point: generate a file based on config['file_type'].
    Currently supports: cpp
    """
    lang = get(cfg, "generator.language", "cpp").lower()
    if lang == "cpp":
        return generate_cpp_file(output_dir, cfg)
    else:
        logger.warning(f"Unsupported language '{lang}', falling back to cpp.")
        return generate_cpp_file(output_dir, cfg)


# ─── AI Code Generator (optional) ────────────────────────────────────────────

def generate_ai_file(output_dir: str, cfg: dict) -> Optional[str]:
    """
    Uses the Anthropic API to generate a unique C++ program.
    Requires ANTHROPIC_API_KEY in environment.
    """
    try:
        import anthropic
        client = anthropic.Anthropic()
        model = get(cfg, "generator.ai_model", "claude-sonnet-4-20250514")
        topics = ["graph traversal", "dynamic programming", "binary search tree",
                  "hash map implementation", "priority queue", "Dijkstra's algorithm",
                  "merge sort", "red-black tree", "trie data structure", "LRU cache"]
        topic = random.choice(topics)
        prompt = (
            f"Write a complete, compilable C++ program implementing {topic}. "
            "Include comments, a main() that demonstrates it with sample data, "
            "and use modern C++17. Output ONLY the raw C++ code, no markdown fences."
        )
        msg = client.messages.create(
            model=model,
            max_tokens=1200,
            messages=[{"role": "user", "content": prompt}]
        )
        code = msg.content[0].text
        uid = _random_uid()
        filename = f"ai_{uid}.cpp"
        filepath = os.path.join(output_dir, filename)
        os.makedirs(output_dir, exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"// AI-generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"// Topic: {topic}\n\n")
            f.write(code)
        logger.info(f"AI-generated file: {filename}")
        return filepath
    except Exception as e:
        logger.error(f"AI generation failed: {e}")
        return None


if __name__ == "__main__":
    from utils.config_loader import load_config
    cfg = load_config()
    repo_path = os.path.abspath(cfg.get("repo_path", "./repo"))
    path = generate_file(repo_path, cfg)
    if path:
        print(f"Generated: {path}")
