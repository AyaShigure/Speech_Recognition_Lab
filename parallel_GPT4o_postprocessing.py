import openai
import os
import datetime
from bcolors import bcolors

# Upgrade note (2024-7-5):
#   0. transcription.txtにせずに、発表者の名前にする
#   1. 開始前にtranscription.txtを削除 
#  bug fix, ./segements dir

# Utilities
def PrintGPTHeader():
    print('[' +  bcolors.color256(fg=154) + 'OpenAI GPT4o' + bcolors.ENDC + ' | '+ f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}' + ']' + ' Initiallizing')
    headerString = '[' +  bcolors.color256(fg=154) + 'OpenAI GPT4o' + bcolors.ENDC + ' | '+ f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}' + ']'
    return headerString
def PrintUserHeader():
    print('[' +  bcolors.color256(fg=214) + f'{userName}' + bcolors.ENDC + ' | '+ f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}' + ']' + ' Initiallizing')
    headerString = '[' +  bcolors.color256(fg=214) + f'{userName}' + bcolors.ENDC + ' | '+ f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}' + ']'
    return headerString
def PrintSystemHeader():
    print('[' +  bcolors.FAIL + 'System' + bcolors.ENDC + ' | '+ f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}' + ']' + ' Initiallizing')
    headerString = '[' +  bcolors.FAIL + 'System' + bcolors.ENDC + ' | '+ f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}' + ']'
    return headerString

def save_string_to_file(string, filename, mode='w'):
    with open(filename, mode) as file:
        file.write(string)
    
    print(headerString + ' ' +  f"Transcription is saved to {filename}")

def OpenAI_initilizations():
    # OpenAI 
    api_key = os.getenv("OPENAI_API_KEY")
    openai.api_key = api_key
    # print(api_key)
    if api_key == None:
        # print(bcolors.BOLD + '===================================' + bcolors.ENDC)
        print(headerString + ' ' + bcolors.FAIL + '\nOpenAI API key error! Exiting..\n' + bcolors.ENDC)
        # print(bcolors.BOLD + '===================================' + bcolors.ENDC)
        os._exit(0)
    else:
        # print(bcolors.BOLD + '===================================' + bcolors.ENDC)
        print(headerString + ' ' + bcolors.OKGREEN + 'OpenAI API Key is loaded!' + bcolors.ENDC)
        # print(bcolors.BOLD + '===================================' + bcolors.ENDC)
        print(headerString + ' ' + bcolors.OKCYAN + 'Loading OpenAI client..' + bcolors.ENDC)
        client = openai.OpenAI(
        api_key = api_key,
        )
        print(headerString + ' ' + bcolors.OKGREEN + 'Client is loaded!' + bcolors.ENDC)
        # print(bcolors.BOLD + '===================================' + bcolors.ENDC)
    try:
        os.mkdir('./processed_transcriptions')
    except:
        print(systemHeaderString + ' ' + bcolors.WARNING + ' ./processed_transcriptions already exists' + bcolors.ENDC)

    return client

def call_GPT_for_postprocessing(GPT_Prompt):

    try:
        completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"{GPT_Prompt}"}
        ]
        )
        print(headerString + ' ' + bcolors.OKCYAN + 'Uploading to OpenAI...' + bcolors.ENDC)
        print(headerString + ' ' + bcolors.OKCYAN + completion.choices[0].message.content + bcolors.ENDC)
        # print(completion.choices[0].message.content)
        return completion.choices[0].message.content

    except:
        print('error')
        # Print the response from the GPT-4 API
    #     print(response.choices[0].message['content'])
    # except openai.error.InvalidRequestError as e:
    #     print(f"InvalidRequestError: {e}")
    # except openai.error.AuthenticationError as e:
    #     print(f"AuthenticationError: {e}")
    # except openai.error.RateLimitError as e:
    #     print(f"RateLimitError: {e}")
    # except Exception as e:
    #     print(f"An unexpected error occurred: {e}")


    post_processed_string = None
    return post_processed_string

def read_text_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(systemHeaderString + ' ' + bcolors.FAIL + f"Error: The file at {file_path} was not found." + bcolors.ENDC)
        print(systemHeaderString + ' ' + bcolors.FAIL + f"Please check if the file name is set up correctly." + bcolors.ENDC)
        print(systemHeaderString + ' ' + bcolors.FAIL + f"Exiting.." + bcolors.ENDC)
        os._exit(0)
    except IOError:
        print(systemHeaderString + ' ' + bcolors.FAIL + f"Error: An error occurred while reading the file at {file_path}." + bcolors.ENDC)
        print(systemHeaderString + ' ' + bcolors.FAIL + f"Exiting.." + bcolors.ENDC)
        os._exit(0)

def split_list_into_chunks(input_list, chunk_size):
    """Splits a list into smaller lists of a fixed size."""
    chunks = [input_list[i:i + chunk_size] for i in range(0, len(input_list), chunk_size)]
    return chunks

def save_string_to_file(string, filename, mode='w'):
    with open(filename, mode) as file:
        file.write(string)
    
    print(headerString + ' ' +  f"Transcription is saved to {filename}")

if __name__ == '__main__':
    userName = 'Aya'
    DEBUG_MODE = False
    headerString = PrintGPTHeader()
    userHeaderString = PrintUserHeader()
    systemHeaderString = PrintSystemHeader()
    print(systemHeaderString + ' ' + bcolors.WARNING + 'Debug mode is at ' + bcolors.FAIL+'{}'.format(DEBUG_MODE) + bcolors.ENDC)
    print(systemHeaderString + ' ' + bcolors.WARNING + 'If debug mode is on, system will not call GPT'.format(DEBUG_MODE) + bcolors.ENDC)

    client = OpenAI_initilizations()

    ###################################################################
    ####################### USER INPUT SECTION: #######################

    # Note: Raw transcript must be {presentation_info_object['name']}.txt

    presentation_info_object = {
        'name': '',
        'research_title': '',
        'research_abstract': '',
    }

    ####################### USER INPUT SECTION #######################
    ##################################################################

    raw_transcription = read_text_file('{}.txt'.format(presentation_info_object['name']))
    if presentation_info_object['name'] == '' or presentation_info_object['research_title'] == '' or presentation_info_object['research_abstract'] == '':
        print(systemHeaderString + ' ' + bcolors.FAIL + 'Please input information to the \'presentation_info_object\'')
        os._exit(0)

    print(systemHeaderString + ' ' + bcolors.OKBLUE + '***************************************************************************************' + bcolors.ENDC)
    print(systemHeaderString + ' ' + bcolors.WARNING + 'Double check below information before calling the GPT' + bcolors.ENDC)
    print(systemHeaderString + ' ' + bcolors.WARNING + 'Name: {}'.format(presentation_info_object['name']) + bcolors.ENDC)
    print(systemHeaderString + ' ' + bcolors.WARNING + 'Research title: {}'.format(presentation_info_object['research_title']) + bcolors.ENDC)
    print(systemHeaderString + ' ' + bcolors.WARNING + 'Research abstract: {}'.format(presentation_info_object['research_abstract']) + bcolors.ENDC)
    print(systemHeaderString + ' ' + bcolors.OKBLUE + '***************************************************************************************' + bcolors.ENDC)

    # Input raw script will be chopped to 1000 charactor per chunck.
    chunk_size = 1000
    chunks = split_list_into_chunks(raw_transcription, chunk_size)
    chunk_num = len(chunks)

    for i in range(chunk_num):
        GPT_Prompt = '研究のタイトル：{}'.format(presentation_info_object['research_title']) + '\n' + '研究の概要：{}'.format(presentation_info_object['research_abstract'])
        GPT_Prompt = GPT_Prompt + f'このは発表の発表を録音してスクリプトをwhisperで取り出したもので、第{i+1}部分である。スクリプトに聞き間違いがあり、研究のタイトルと概要に基づいて修正するとともに句読点をつけてください。特に、「以下は修正したスクリプト」など修正したスクリプトと関係しないものは一切示さないでください。'
        GPT_Prompt = GPT_Prompt + 'また、翻訳は一切しないで、与えられたスクリプトの言語に従いなさい'
        GPT_Prompt = GPT_Prompt + '\n\n' + '発表のスクリプト：\n{}'.format(chunks[i])

        if not DEBUG_MODE:
            print(userHeaderString + ' ' + bcolors.color256(fg=223) + f'{GPT_Prompt}' + bcolors.ENDC)
            output_string = call_GPT_for_postprocessing(GPT_Prompt)
            save_string_to_file(output_string, './processed_transcriptions/{}_out.txt'.format(presentation_info_object['name']), mode='a')
        else:
            print(systemHeaderString + ' ' + bcolors.WARNING + 'DEBUG MODE, GPT is not called.'.format(DEBUG_MODE) + bcolors.ENDC)

