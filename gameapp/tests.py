import base64

with open("/Users/Davlet/Downloads/team1.py", "rb") as f:
    encoded_file = base64.b64encode(f.read()).decode('utf-8')
print(encoded_file)

with open("/Users/Davlet/Downloads/team2.py", "rb") as f:
    encoded_file = base64.b64encode(f.read()).decode('utf-8')
print(encoded_file)

with open("/Users/Davlet/Downloads/team3.py", "rb") as f:
    encoded_file = base64.b64encode(f.read()).decode('utf-8')
print(encoded_file)



