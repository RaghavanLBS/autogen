from autogen import  initiate_chats
import autogen
import json, pprint
import SimpleAgentCreator 

OAI_CONFIG_LIST = "autogen\OnboardingAgent\OAI_CONFIG_LIST.json"
with open('autogen\OnboardingAgent\config.json') as f:
    config = json.load(f)

with open('autogen\OnboardingAgent\company_details.json') as f:
    company = json.load(f)

#llm_config = {"model":"gpt-4o","api_key":config["openai_api_key"]}
#print(config["openai_api_key"])

config_list = autogen.config_list_from_json( env_or_file = OAI_CONFIG_LIST)
print(config_list)
def main():
    company_name =company["company_name"]
    print(company_name)
    user_info_agent = SimpleAgentCreator.create_user_info_agent(company_name=company_name, config_list=config_list)
    onboarding_product_agent = SimpleAgentCreator.create_product_agent(company_name=company_name, config_list=config_list)
    engagament_agent = SimpleAgentCreator.create_engagement_agent(company_name=company_name, config_list=config_list)
    customer_proxy_agent =  SimpleAgentCreator.create_uesr_proxy_agent()
    chats = []

    chats.append({
        'sender':user_info_agent,
        'recipient': customer_proxy_agent,
        'message' : 'Hello!  I am here to help you solve any issue with our product. Could you tell your name',
        'summary_method': 'reflection_with_llm',
        'summary_args':{
            "summary_prompt": "Return the customer information in JSON object format only , {'name','location'}"
        },
        'clear_history':True
        })
    
    chats.append ({
        'sender':onboarding_product_agent,
        'recipient':customer_proxy_agent,
        'message':'Great! Could you tell me more about your issue that are you are facing and the product which you are using',
        'summary_method':'reflection_with_llm',
        
        'clear_history':False
    })

    chats.append({
        'sender':engagament_agent,
        'recipient':customer_proxy_agent,
        'message':'While we wait for human agent to take over and help you solve your issue, can you tell me how you use our products ',
        'max_turns':4,
        'summary_method':'reflection_with_llm',
    
        
    })
    print(chats)
    chat_results = initiate_chats(chats)
    pprint(chat_results.summary)

if __name__ == "__main__":
    main()

