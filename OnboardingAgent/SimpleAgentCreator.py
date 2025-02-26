import autogen
def create_user_info_agent(company_name, config_list):
    ONBOARDING_USER_INFO_AGENT_SYSTEM_MESSAGE = f'''
        You are helpful customer agent.
        You work for {company_name}. You are part of workflow that is  helping customer to get started using the product they bought. 
        Your specific role is to get first name, last name and customer location,address of the customer
        Donot ask for any other information.
        After customer describes the issue repeat the information and ask "Please answer with 'TERMINATE' if I have noted down your details correctly
       
        '''
    onboarding_user_info_agent = autogen.ConversableAgent(name="UserInfoAgent",
                                                        llm_config={"config_list":config_list},
                                                        system_message = ONBOARDING_USER_INFO_AGENT_SYSTEM_MESSAGE,
                                                        human_input_mode="NEVER",
                                                        is_termination_msg = lambda msg: "TERMINATE" in msg.get("content").lower(),
                                                       

                                                        )
    return onboarding_user_info_agent


def create_product_agent(company_name,config_list ):
    
    ONBOARDIND_PRODUCT_AGENT_SYSTEM_MESSAGE = f'''
    you are a helpful customer agent.
    Your work for {company_name}. Your role is to help customer to get started using the product they bought.
    Gather the details about the product the customer trying to use
    and ask about the pain point or the issues that are faced by customer in using the product or start using the product
    Donot ask for any other information other than product name and the issue. Restrict yourself with {company_name} related responses. Donot ask about customer information
    After customer describes the issue repeat it and add "Please anser with 'TERMINATE' if i have understood your question
    
    '''
    onboarding_product_agent = autogen.ConversableAgent(name="OnboardingProductAgent",
                                        llm_config={"config_list":config_list},
                                        system_message=ONBOARDIND_PRODUCT_AGENT_SYSTEM_MESSAGE,
                                        human_input_mode= 'NEVER',
                                        is_termination_msg=lambda msg:'TERMINATE' in msg.get("content").lower())
    return onboarding_product_agent
    
def create_uesr_proxy_agent():
    user_agent  = autogen.ConversableAgent(name="CustomerProxyAgent",human_input_mode="ALWAYS", code_execution_config= False, llm_config=False)
    return user_agent

def create_engagement_agent(company_name,config_list ):
    
    ONBOARDIND_CUSTOMER_ENGAGEMENT_SYSTEM_MESSAGE = f'''
    you are a helpful customer Service agent.
    Your work for {company_name}. The customer is waiting online to converse to human agent.
    Till then Your role is to engage and entertain user based on user preferences set.
    This could be current news, jokes, funny memes.
    You should not ask customer for any other information. You should not hallucinate. Make sure the content is engaging and fun

    '''
    onboarding_product_agent = autogen.ConversableAgent(name="CustomerEngagementAgent",
                                        llm_config={"config_list":config_list},
                                        system_message=ONBOARDIND_CUSTOMER_ENGAGEMENT_SYSTEM_MESSAGE,
                                        human_input_mode= 'NEVER',
                                        is_termination_msg=lambda msg:'TERMINATE' in msg.get("content").lower())
    return onboarding_product_agent