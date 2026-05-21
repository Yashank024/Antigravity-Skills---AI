# Advanced Analysis Systems

To avoid the pitfalls of shallow static analysis, the engine must use deep structural comprehension.

## 1. Dependency Graph Analysis
Before removing elements or consolidating, build a mental (or CLI-based) module map.
- **Circular Dependency Detection**: Find paths like `A imports B, B imports C, C imports A`. Actively break these loops by extracting the shared interface or state into an independent module `D`.
- **Import Graphs**: Map which files are terminal (leaves) and which are roots. Terminal files with 0 incoming dependencies are candidates for deletion if they aren't entry points.

## 2. Semantic Code Understanding
Simple regex or AST unused-variable detection is dangerous in dynamic languages.
- **Dynamic Usage Prevention**: A function might look unused by static analysis but be invoked dynamically via metaprogramming, computed properties (`obj[methodName]()`), or global window bindings.
- **Rule**: If an object or class uses reflection, proxy objects, or dynamic strings for access, downgrade the Confidence Score of deleting its members to **Low (<40%)**, and aggressively flag it in the Change Impact Analysis.

## 3. Learning Memory (Optimization Memory)
(Optional but powerful layer): The agent should maintain a persistent memory log (usually in a `.optimization-memory` file or via the internal framework state) of recurrent bad patterns in the specific project.
- *Example*: "In previous passes, deleting `utils/math.js` broke the dynamic report generator. Never flag `math.js` for deletion again."
