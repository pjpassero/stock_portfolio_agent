<h1>Context - FinLab</h1>

Stock Portfolio Agent, now named FinLab started as a project in linear algebra. I wanted a way to quantify portfolio health into one number, that was supported
with already established portfolio statistics. <br>

The project was initially designed off my portfolio and I built up the fundamentals in C++ over the course of the semester I did it. As a CS / Math 
student, I understood the console outputs and the raw data, but I realized not everyone could. That's where I got the idea to process this data and 
present it on a nice frontend for any user, of any level to understand. <br>

The biggest problem I ran into was analysis - every portfolio is different and designing an engine to produce outputs would have been difficult. Enter the
LLM. Here is where adding an AI layer was perfect for producing analysis of the data rather than calculating the data itself. <br>

My basic model was simple: Portfolio Input from the User --> Calculate Deterministic Statistics --> Feed along with a prompt to an LLM --> Deliver it all to the user <br>

Now FinLab exists with a full authentication system, analysis system, it gives reallocation advice, and it has a built in Agentic chat tool called "Fin." <br>

<h1>Backend</h1>

The backend for this project was done with FastAPI in Python. FastAPI handles the API portion while Lang Graph handles the workflow orchestration and agentic
capabilities. <br>

All dependencies can be found in <strong> Requirements.txt </strong>

<h1><Frontend/h1>

The frontend for this project was built on React with Bootstrap styling and formatting. There are many React packages used, like a package that renders
latex for mathematical functions and markdown for LLM responses.


<h1>Running the application</h1>

There are a few ways you can run this application locally. The backend and frontend are separate.  <br>

For the frontend, navigate to the frontend folder then run <strong> npm dev start </strong> <br>

The backend has two options. You can either build the Docker file OR run from the command line using: 
<strong> uvicorn main:app --reload </strong> <br>

Docker was used to practice containerization and to give me an alternative to launch the product on various online hosting platforms.




