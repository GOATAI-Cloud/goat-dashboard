# goat_console.py

def execute_command(cmd):
    if "buy" in cmd:
        return f"[GOAT] Executing market buy: {cmd}"
    elif "sell" in cmd:
        return f"[GOAT] Executing market sell: {cmd}"
    elif "override" in cmd:
        return f"[GOAT] Strategy override applied: {cmd}"
    elif "pulse" in cmd:
        return f"[GOAT] Fetching pulse for: {cmd.split(' ')[1]}"
    else:
        return f"[GOAT] Unknown command: '{cmd}' — no divine interpretation available."
