from openai import OpenAI
import fitz  

def read_pdf(pdf_path):
    doc = fitz.open(pdf_path)

    text_content = ""
    for page_number in range(doc.page_count):
        page = doc[page_number]
        text_content += page.get_text()

    doc.close()
    return text_content

def patient_flag(patient_details, medical_report):
    api_key = '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'
    client = OpenAI(api_key=api_key)
    instructions = """I want u to act like a simple flagging bot. Lets keep it simple. I will share with you a medical report or a patient's condition, and I need u to give me the following thing: True if the patient is fit for the medical trials, false if the patient is not fit for the medical trials.
    Here is a reference of Vital Data: Patient ID,Age,Sex,Temperature,Heart Beat,Respiratory Rate,Systolic BP,Diastolic BP,Oxygen Saturation\n1,29,M,98.6,72,16,120,80,98\n2,34,F,96.9,75,14,115,75,99\n3,45,M,98.4,70,18,110,70,97\n4,26,F,97.8,78,16,118,76,98\n5,37,M,97.1,72,15,120,80,96\n6,50,F,98.6,74,16,122,82,97\n7,32,M,97.7,68,14,115,78,99\n8,28,F,98.5,76,18,117,75,98\n9,41,M,98.6,70,17,119,79,96\n10,28,M,97.06,72,16,120,80,98\n
        These are considered baseline data. If I give u a medical report/patient's health vitals. For it being true, the input values should be within the range of the baseline data. If the input values are not within the range, then it should be flagged as FALSE(if false, tell me why false- KEEP IT SHORT). If the input values are within the range, but not exactly the same, then it should be flagged as NEUTRAL."""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": instructions
            },
            {
                "role": "user",
                "content": ""
            },
            {
                "role": "assistant",
                "content": "Okay, I will give u True or False"
            },
            {
                "role": "user",
                "content": f"{patient_details}\n{medical_report}"
            },
        ],
        temperature=1,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    response_message = response.choices[0].message.content
    return response_message

if __name__ == "__main__":
    pdf_path = input('Enter the path of the medical report: ')
    medical_report = read_pdf(pdf_path)

    patient_details = input('Enter Patient Details: ')
    print(patient_flag(patient_details, medical_report))
