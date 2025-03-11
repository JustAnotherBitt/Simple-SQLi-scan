# SQL Injection Vulnerability Scanner

This Python script tests URL parameters for potential SQL injection vulnerabilities by checking server responses for known database error messages (which can be improved).


## 🛠️ How It Works

1. Analyzes the parameters in the provided URL.
2. Injects common SQL attack characters (`'` and `"`) into each parameter.
3. Checks server responses for known SQL error messages.


## 🚀 How to Use

   Run the script with the target URL:
   
   ```bash
   python main.py "http://example.com/page.php?id=1&name=test"
   ```
   On Linux (with `python3`):
   
   ```bash
   python3 main.py "http://example.com/page.php?id=1&name=test"
   ```

### Output:
- If vulnerable:
  
  ```
  [ + ] id parameter is vulnerable
  ```
- If no vulnerability is found:
  
  ```
  NOT VULNERABLE
  ```

## ⚠️ Disclaimer

This script is for educational and ethical security purposes only. Use it **only on systems you have explicit authorization to test**. Misuse may violate local or international laws.
