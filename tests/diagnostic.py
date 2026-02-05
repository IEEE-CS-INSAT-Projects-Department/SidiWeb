import sys
import os
from fastapi import FastAPI
from fastapi.testclient import TestClient
    
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("Checking routers/me.py...")
with open("routers/me.py", "r") as f:
    content = f.read()
    print(content)
    
    # Check if it has Depends(get_current_user)
    if "Depends(get_current_user)" in content:
        print("✓ Has Depends(get_current_user)")
    else:
        print("✗ Missing Depends(get_current_user)")
    
    # Check the actual function
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if "@router.get" in line and "/me" in line:
            print(f"Found /me endpoint at line {i+1}: {line.strip()}")
            # Print the function definition
            for j in range(i, min(i+10, len(lines))):
                if "async def me" in lines[j]:
                    print(f"Function: {lines[j].strip()}")
                    # Print next few lines
                    for k in range(j, min(j+5, len(lines))):
                        print(f"  {lines[k].rstrip()}")
                    break

print("\n" + "="*50 + "\n")

# Try to import and test
try:
    app = FastAPI()
    # Try to import your router
    try:
        from routers.me import router as me_router
        app.include_router(me_router)
        print("✓ Successfully imported and included me router")
        
        client = TestClient(app)
        
        print("\nTesting endpoint:")
        response = client.get("/api/auth/me")
        print(f"Status: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        print(f"Body: {response.json()}")
        
    except Exception as e:
        print(f"✗ Error importing me router: {e}")
        
except Exception as e:
    print(f"✗ Error: {e}")

