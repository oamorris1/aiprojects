

from langchain_openai import AzureChatOpenAI
from langchain_openai import AzureOpenAIEmbeddings


 

from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv('.env'))

text = """
The Denver Zoological Foundation provides information on the African lion (Panthera leo melanochaita), a vulnerable species primarily found
 in sub-Saharan Africa's savannas, grasslands, and woodlands. Classified as a mammal within the order Carnivora and the family Felidae, lions 
 are the second-largest big cat species, with males larger than females and possessing distinctive manes. They are social animals, living in 
 prides and exhibiting communal hunting and parenting behaviors. Lions are carnivorous, preying on various ungulates and scavenging when necessary.
In captivity, their diet is carefully managed with nutrient-fortified meat and occasional fasting.Lions have several adaptations for survival,
including group behavior, night vision, and powerful bodies with retractable claws for hunting.
They are apex and keystone predators, with roars that can be heard up to 5 miles away. 
The Denver Zoo houses a coalition of four male lions born in 2015 and a pride with several females and a male cub born in 2019.
The lions' conservation status is vulnerable due to habitat loss and human conflict, with an estimated 43% population reduction over 21 years,
leaving around 20,000 lions in the wild. Conservation efforts focus on creating safe habitats and national parks to ensure their survival.
Additional information can be found through resources like National Geographic and the Lion Recovery Fund.

"""

text2 = """
This systematic review by Daniel Martinez-Marquez and colleagues examines the application of eye tracking technology in high-risk industries such as aviation, maritime, and construction. The review highlights that most accidents in these sectors are due to human error, often linked to impaired mental performance and attention failure. Eye tracking research, dating back 150 years, captures a variety of eye movements that reflect human cognitive, emotional, and physiological states, providing insights into the human mind in different scenarios.

The review identifies the demographic distribution and applications of eye tracking research, revealing that the aviation industry has the highest number of studies, followed by maritime and construction. The USA leads in eye tracking studies, with significant contributions from Germany, Norway, China, and the UK. The research uncovers different applications of eye tracking, such as studying visual attention, mental workload, human-machine interfaces, situation awareness, training improvement, and hazard identification.

Eye tracking technologies are often integrated with simulators, video and audio recording, head trackers, EEG, ECG, and other technologies to study various human aspects in detail. The review identifies gaps in the literature, suggesting the need for further research on topics like mental workload in construction, hazard detection in aviation and maritime, and the integration of additional technologies to support eye tracking research. The study concludes that eye tracking has a promising future in enhancing understanding and training in high-risk industries.
"""

text3 = """
The study, published in Transportation Engineering 13 (2023), examines the role of human factors in aviation ground operation-related accidents and incidents using a human error analysis approach. The research analyzed 87 accident and incident reports from 2000 to 2020, employing the Human Factors Dirty Dozen (HF DD) Model and the Human Factors Analysis and Classification Scheme (HFACS) for systematic thematic analysis. The findings highlight that the main causes of ground operation-related accidents and incidents are lack of situational awareness and failure to follow prescribed procedures. Critical operational actions identified include aircraft pushback/towing, aircraft arrival and departure, and aircraft weight and balance. The study proposes an agenda for future research and recommendations for industry corrective action, emphasizing the need for a comprehensive Ramp Resource Management (RRM) framework to address the identified safety issues. The research also suggests that current human error analysis models may need to be extended to consider the broader organization and aviation system context.

"""
from langchain.evaluation import load_evaluator
embeddings = AzureOpenAIEmbeddings(deployment="text-embedding-ada-002", model="text-embedding-ada-002", chunk_size=10)

evaluator = load_evaluator("pairwise_embedding_distance", embeddings=embeddings)


eval_result = evaluator.evaluate_string_pairs(
    prediction="What are some common variables used in studies regarding human error-based aviation accidents", prediction_b=text3
)
print(eval_result)



def handle_file_upload(event):
    uploaded_file = file_input.value
    file_name = file_input.filename 
    save_folder_path = "C:/Users/Admin/Desktop/erdcDBFunc/analysis_crew/test"
    save_path = Path(save_folder_path, file_name)
    if uploaded_file:
        with open(save_path, mode='wb') as w:
            w.write(uploaded_file)
        # Here you can process the uploaded file
        if save_path.exists():
            chat_interface.send(f"File '{file_name}' uploaded successfully!", user="System", respond=False)
