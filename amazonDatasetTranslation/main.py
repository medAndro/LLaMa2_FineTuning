from papagopy import Papagopy
from datasets import load_dataset, Dataset, DatasetDict
import pandas as pd
translator = Papagopy() # use web api

#번역할 데이터의 총 길이
train_len = 2000 # 21000
validation_len = 2000 # 6000
test_len = 2000 # 3000

#데이터셋 로드
subset_dataset = DatasetDict.load_from_disk("subset_dataset_30000")
train_data = subset_dataset['train']
validation_data = subset_dataset['valid']
test_data = subset_dataset['test']

#빈 데이터프레임 생성
#df_train = pd.DataFrame({  "label": [],  "title": [],  "content": []})
#df_validation = pd.DataFrame({  "label": [],  "title": [],  "content": []})
#df_test = pd.DataFrame({  "label": [],  "title": [],  "content": []})

#엑셀에서 판다스 데이터프레임 로드
df_train = pd.read_excel("df_train.xlsx")
df_validation = pd.read_excel("df_validation.xlsx")
df_test = pd.read_excel("df_test.xlsx")


#df_train 번역
for i in range(df_train.shape[0], train_len):
    label = train_data['label'][i]
    translated_title = translator.translate(train_data['title'][i], targetCode='ko', sourceCode='en')
    translated_content = translator.translate(train_data['content'][i], targetCode='ko', sourceCode='en')
    print(label)
    print(translated_title)
    print(translated_content)
    df_train.loc[i] = [label, translated_title, translated_content]
    if i % 10 == 0:
        df_train.to_excel("df_train.xlsx", index=False)
        print("df_train.xlsx 중간 저장됨")
df_train.to_excel("df_train.xlsx", index=False)

#df_validation 번역
for i in range(df_validation.shape[0], validation_len):
    label = validation_data['label'][i]
    translated_title = translator.translate(validation_data['title'][i], targetCode='ko', sourceCode='en')
    translated_content = translator.translate(validation_data['content'][i], targetCode='ko', sourceCode='en')
    print(label)
    print(translated_title)
    print(translated_content)
    df_validation.loc[i] = [label, translated_title, translated_content]
    if i % 10 == 0:
        df_validation.to_excel("df_validation.xlsx", index=False)
        print("df_validation.xlsx 중간 저장됨")
df_validation.to_excel("df_validation.xlsx", index=False)

#df_test 번역
for i in range(df_test.shape[0], test_len):
    label = test_data['label'][i]
    translated_title = translator.translate(test_data['title'][i], targetCode='ko', sourceCode='en')
    translated_content = translator.translate(test_data['content'][i], targetCode='ko', sourceCode='en')
    print(label)
    print(translated_title)
    print(translated_content)
    df_test.loc[i] = [label, translated_title, translated_content]
    if i % 10 == 0:
        df_test.to_excel("df_test.xlsx", index=False)
        print("df_test.xlsx 중간 저장됨")
df_test.to_excel("df_test.xlsx", index=False)


"""

id_to_label = {0:'부정', 1:'긍정'}

question_template = "### Human: 다음 문장의 긍정, 부정 여부를 판단하세요"

## 리뷰의 Title과 콘텐츠를 가지고 학습
train_instructions = [f'{question_template}\n제목: {x}\n내용: {y}\n\n### 판단: {id_to_label[z]}' for x,y,z in zip(train_data['title'],train_data['content'],train_data['label'])]
validation_instructions = [f'{question_template}\n제목: {x}\n내용: {y}\n\n### 판단: {id_to_label[z]}' for x,y,z in zip(validation_data['title'],validation_data['content'],validation_data['label'])]

## 리뷰의 Title만 가지고 학습
##train_instructions = [f'{question_template}\ntitle: {x}\n\n### Assistant: {id_to_label[z]}' for x,z in zip(train_data['title'],train_data['label'])]
##validation_instructions = [f'{question_template}\ntitle: {x}\n\n### Assistant: {id_to_label[z]}' for x,z in zip(validation_data['title'],validation_data['label'])]

ds_train = Dataset.from_dict({"text": train_instructions})
ds_validation = Dataset.from_dict({"text": validation_instructions})
instructions_ds_dict = DatasetDict({"train": ds_train, "eval": ds_validation})
print(instructions_ds_dict['train']['text'][0])
print(subset_dataset)

"""

"""


text = "Classify this sentence as either negative, positive\ntitle: Anyone who likes this better than the Pekinpah is a moron.\ncontent: All the pretty people in this film. Even the Rudy character played by Michael Madsen. This is adapted from a Jim Thompson novel for cryin' out loud! These are supposed to be marginal characters, not fashion models. Though McQueen and McGraw were attractive (but check out McQueen's crummy prison haircut) they were believable in the role. Baldwin and Bassinger seem like movie stars trying to act like hard cases. Action wise, the robbery scene in the Pekinpah version was about 100 times more exciting and suspenseful than anything in this re-make.\n\n### Assistant: negative"

print(translated_text)"""