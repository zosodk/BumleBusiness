import shlex

log_line = '2026-03-01T08:01:17 level=INFO event=LOGIN_SUCCESS user=eve src_ip=10.0.0.5 dest_host=db01 dest_port=53 status=OK msg="User authenticated successfully"'

parts = shlex.split(log_line)
print(parts)

data = {"timestamp": parts[0]}
for item in parts[1:]:
    key, value = item.split("=", 1)
    data[key] = value

print(data)