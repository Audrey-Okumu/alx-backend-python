# 0x03. Unittests and Integration Tests

## 📌 Project Overview
This project introduces **unit testing** and **integration testing** in Python using the `unittest` framework.  
The main focus is to understand how to:
- Test small, isolated functions (unit tests).
- Test code end-to-end (integration tests).
- Use advanced patterns such as **mocking, patching, parameterization, and fixtures**.

I will practice writing tests for utility functions (`utils.py`) and API clients (`client.py`).

---

## 🧪 Concepts

### 🔹 Unit Tests
Unit tests check if a specific function works as expected.  
- They focus only on the function itself.  
- Any external dependencies (DB, network, files) should be **mocked**.  
- Example: Testing `utils.access_nested_map`.

**Key question:** If everything outside this function works correctly, does this function behave correctly?

---

### 🔹 Integration Tests
Integration tests check whether multiple components work **together** correctly.  
- They test a whole flow (end-to-end).  
- Only external calls (HTTP, DB, file I/O) are mocked.  
- Example: Testing `GithubOrgClient.public_repos`.

**Key question:** Do all the pieces of this application work together as expected?

---

## 🛠️ Resources
- [unittest — Unit testing framework](https://docs.python.org/3/library/unittest.html)  
- [unittest.mock — mock object library](https://docs.python.org/3/library/unittest.mock.html)  
- [parameterized](https://pypi.org/project/parameterized/)  
- [Memoization](https://en.wikipedia.org/wiki/Memoization)  

---

## 🎯 Learning Objectives
By the end of this project, I should be able to explain:
- ✅ The difference between **unit tests** and **integration tests**.  
- ✅ Common testing patterns: **mocking, parameterization, and fixtures**.  
- ✅ How to structure tests for Python modules.  

