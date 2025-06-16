resume_prompts = """You are an expert HR professional. Your task is to extract information from the given resume text and format it into a structured JSON object matching the following schema:
                    Resume Text:{text}
                    Domain:{domain}
                    Job Title: {job_title}
                    Job Description : {job_description}
                    User Data : {user_data}

                    Instructions:
                    1. Extract relevant information and map it to the appropriate fields in the schema.
                    2. If a field cannot be filled directly from the text, infer its value based on context or leave it blank.
                    3. Make sure that everything is written perfectly in english.
                    4. Add sufficient project according to job title and job description.
                    5. Make it ATS Friendly.
                    6. make sure to return something with validation of it's type so that i don't get error
                    7. if job title and job description is none then use user_data and make an resume based on that. 
                    """

enhance_resume_prompts = """You are an expert resume writer. Enhance the following text to be more professional and ATS-friendly.
            Consider the job title and description while making improvements.
            
            Original Text: {text}
            Job Title: {job_title}
            Job Description: {job_description}
            
            Instructions:
            1. Use strong action verbs
            2. Quantify achievements where possible
            3. Remove any informal language
            4. Ensure proper grammar and punctuation
            5. Make it concise and impactful
            6. Use industry-specific keywords from the job description
            """

grammar_resume_prompts = """You are an expert grammar checker. Analyze the following text and provide grammar suggestions.
            
            Text: {text}
            
            Instructions:
            1. Identify grammar errors
            2. Suggest corrections
            3. Explain why each correction is needed
            4. Format the response as a list of errors and their corrections
            """

adjust_resume_prompts = """You are an expert in professional writing. Adjust the tone of the following text to be more {tone}.
            
            Text: {text}
            Desired Tone: {tone}
            
            Instructions:
            1. Maintain the original meaning
            2. Adjust word choice to match the desired tone
            3. Ensure consistency throughout the text
            4. Keep it concise and clear
            """

extract_keyword_prompts = """You are an expert in resume optimization. Extract relevant keywords from the text that match the job description.
            
            Text: {text}
            Job Description: {job_description}
            
            Instructions:
            1. Identify technical skills
            2. Identify soft skills
            3. Identify industry-specific terms
            4. Prioritize keywords that appear in the job description
            5. Return a list of unique keywords
            """

bullet_format_prompts = """You are an expert in resume optimization. Extract relevant keywords from the text that match the job description.
            
            Text: {text}
            Job Description: {job_description}
            
            Instructions:
            1. Identify technical skills
            2. Identify soft skills
            3. Identify industry-specific terms
            4. Prioritize keywords that appear in the job description
            5. Return a list of unique keywords
            """