from autogen import AssistantAgent
import autogen,pprint
OAI_CONFIG_LIST = "autogen\AiAgents\OAI_CONFIG_LIST.json"

company_name = 'Servicenow'
task = f'''
Write a concise 2 blog post about recent developments of {company_name} development. 
The post can be of any area in Servicenow. But it should be done within 5 days. 
What are acceptable content.
Explaining various New releases about {company_name}


The target audience is mix of Servicenow new developers, architects, ITSM, ITOM, HR or someone who is tryingt to understand what is servicenow

'''

WRITER_SYSTEM_MESSAGE = '''
You are a writer. You are writing engaging and concise articles with titles on given topics.
you must polish your post based on the feedback you receieve and give a refined version
only return your final work without additional comments
'''

CRITIC_SYSTEM_MESSAGE = '''
You are critic. You review work of  the writer and provide constructive feedback to improve quality of content
'''

SEO_REVIEWER_MESSAGE  ='''
You are SEO reviewer. You review the work of a writer and provide constructive feedback to improve SEO ranking of the content. 
Give feedback in three bullet points, first point being most impactful and third point is relatively less impactful
All feedback should be related to SEO engines only and for improving the provided message alone. 
Donot apologize if there is none foud and return  'Content Looks good from SEO perpesctive' 
'''

LEGAL_REVIEWER_MESSAGE = '''
You are SEO reviewer. You review the work of a writer and provide constructive feedback to make the content 
Legally and political compliant. 
Give feedback in three bullet points, first point being most impactful and third point is relatively less impactful.
All feedback should be related to legal point of view only and for improving the provided message alone. 
Donot apologize if there is none foud and return  'Content Looks good from LEGAL perpesctive' 
'''

ETHICS_REVIEWER_MESSAGE = '''
You are SEO reviewer. You review the work of a writer and provide constructive feedback to make the content 
ethical and business practice compliant. 
Give feedback in three bullet points, first point being most impactful and third point is relatively less impactful.
All feedback should be related to ethical point of view only and for improving the provided message alone. 
Donot apologize if there is none foud and return  'Content Looks good from ethical perpesctive' 
'''

META_REVIEWER_MESSAGE = ''' 
    You are meta reviewer. You aggregate and review the work of other reviewers and give a final suggestion on the content
'''

config_list = autogen.config_list_from_json(OAI_CONFIG_LIST)

seo_reviewer = AssistantAgent(
        name='SEO_REVIEWER',
        llm_config = {'config_list':config_list},
        system_message= SEO_REVIEWER_MESSAGE
        )
legal_reviewer = AssistantAgent(
    name = 'LEGAL_REVIEWER',
    llm_config= {'config_list':config_list},
    system_message = LEGAL_REVIEWER_MESSAGE
)

ethical_reviewer = AssistantAgent(
    name = 'ETHICAL_REVIEWER',
    llm_config= {'config_list':config_list},
    system_message = ETHICS_REVIEWER_MESSAGE
)



meta_reviewer = AssistantAgent(name = "meta_reviewer", llm_config={'config_list':config_list}, system_message = META_REVIEWER_MESSAGE)

writer = AssistantAgent(name ='Writer',
                        llm_config={'config_list': config_list},
                        system_message= WRITER_SYSTEM_MESSAGE
                        )

critic = AssistantAgent(name ='Critic',
                        llm_config={'config_list': config_list},
                        system_message= CRITIC_SYSTEM_MESSAGE
                        )


def reflecton_message(recipient, message, sender, config):
    print("called")
    return f''' Review the following content.
    \n\n    {recipient.chat_messages_for_summary(sender)[-1]['content']}
'''

review_chats = [{

    "recipient": seo_reviewer,
    'message' : reflecton_message,
    'summary_method': 'reflection_with_llm',
    'summary_args' :{
        "summary_prompt":" Return review as JSON object only: {'Reviewer':'', 'Reviewer:''} Here reviewer is your role"
    },
    'max_turns':1

},
{

    "recipient": legal_reviewer,
    'message' : reflecton_message,
    'summary_method': 'reflection_with_llm',
    'summary_args' :{
        "summary_prompt":" return review as JSON object only: {'Reviewer':'', 'Reviewer:''} Here reviewer is your role"
    },
    'max_turns':1

},{

    "recipient": ethical_reviewer,
    'message' : reflecton_message,
    'summary_method': 'reflection_with_llm',
    'summary_args' :{
        "summary_prompt":" return review as JSON object only: {'Reviewer':'', 'Reviewer:''} "
    },
    'max_turns':1

},
{

    "recipient": meta_reviewer,
    'message' : 'Aggregate feedback from all reviewers and give final suggestions on the writing',
    'max_turns':1

},
]

# Trigger mentions only when Writer agent contacts critic, the nested chat is to be triggered

critic.register_nested_chats(review_chats, trigger=writer)
chat_result = critic.initiate_chat(recipient= writer,
                                   message= task,
                                   max_turns=2,
                                   summary_method='last_msg')
print(chat_result)