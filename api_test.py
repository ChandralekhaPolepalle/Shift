from fastapi import FastAPI, Form
import httpx

app = FastAPI()

HUBSPOT_API_KEY = "your_hubspot_api_key"


@app.post("/submit-form/")
async def submit_form(name: str = Form(...), email: str = Form(...), phone: str = Form(...)):
    url = "https://api.hubapi.com/crm/v3/objects/contacts"

    data = {
        "properties": {
            "firstname": name,
            "email": email,
            "phone": phone
        }
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {HUBSPOT_API_KEY}"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=data, headers=headers)

    if response.status_code == 201:
        return {"message": "Contact added successfully"}
    else:
        return {"message": "Failed to add contact", "error": response.json()}


# Example form submission data
@app.get("/")
async def main():
    content = """
    <form action="/submit-form/" method="post">
        <label for="name">Name:</label><br>
        <input type="text" id="name" name="name"><br>
        <label for="email">Email:</label><br>
        <input type="email" id="email" name="email"><br>
        <label for="phone">Phone:</label><br>
        <input type="tel" id="phone" name="phone"><br><br>
        <input type="submit" value="Submit">
    </form> 
    """
    return content
