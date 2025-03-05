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
config_list = autogen.config_list_from_json( env_or_file = OAI_CONFIG_LIST)
writer_agent = AssistantAgent(name ='BlogWriter',
                              system_message=WRITER_SYSTEM_MESSAGE,
                              llm_config= {'config_list':config_list}
                              )

critic_agent = AssistantAgent(name='critic',
                              system_message = CRITIC_SYSTEM_MESSAGE,
                              llm_config = {'config_list':config_list})

#writer_agent.generate_reply(messages =[{'content':task, 'role':'user' }])
chat_result = critic_agent.initiate_chat(recipient=writer_agent,
                           message=task,
                           max_turns =2,
                           summary_method='last_msg'
                           )

pprint(chat_result.summary)
