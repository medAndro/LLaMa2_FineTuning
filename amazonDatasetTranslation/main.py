from papagopy import Papagopy
#pip install papagopy -i http://ftp.daumkakao.com/pypi/simple --trusted-host ftp.daumkakao.com
from datasets import load_dataset, Dataset, DatasetDict
import pandas as pd
import time
translator = Papagopy() # use web api

#번역할 데이터의 총 길이
train_len = 21000 # 21000
validation_len = 6000 # 6000
test_len = 3000 # 3000

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



def translator_except_ctrl(original_sentence):
    while True:
        try:
            result = translator.translate(original_sentence, targetCode='ko', sourceCode='en')
            return result
        except Exception as e:
            print(f"오류 발생: {e}")
            print("15초 대기 후 다시 시도합니다.")
            time.sleep(15)  # 15초 대기

## 파파고 번역기 실행을 위한 코드
"""
#df_train 번역
for i in range(df_train.shape[0], train_len):
    label = train_data['label'][i]
    try:
        translated_title = translator_except_ctrl(train_data['title'][i])
        translated_content = translator_except_ctrl(train_data['content'][i])
    except:
        time.sleep(5)

    print(label)
    print(translated_title)
    print(translated_content)
    df_train.loc[i] = [label, translated_title, translated_content]
    if i % 10 == 0:
        df_train.to_excel("df_train.xlsx", index=False)
        print("df_train.xlsx 중간 저장됨")
        print(f"{i} / {train_len}번역됨")
df_train.to_excel("df_train.xlsx", index=False)

#df_validation 번역
for i in range(df_validation.shape[0], validation_len):
    label = validation_data['label'][i]
    translated_title = translator_except_ctrl(validation_data['title'][i])
    translated_content = translator_except_ctrl(validation_data['content'][i])
    print(label)
    print(translated_title)
    print(translated_content)
    df_validation.loc[i] = [label, translated_title, translated_content]
    if i % 10 == 0:
        df_validation.to_excel("df_validation.xlsx", index=False)
        print("df_validation.xlsx 중간 저장됨")
        print(f"{i} / {validation_len}번역됨")
df_validation.to_excel("df_validation.xlsx", index=False)

#df_test 번역
for i in range(df_test.shape[0], test_len):
    label = test_data['label'][i]
    translated_title = translator_except_ctrl(test_data['title'][i])
    translated_content = translator_except_ctrl(test_data['content'][i])
    print(label)
    print(translated_title)
    print(translated_content)
    df_test.loc[i] = [label, translated_title, translated_content]
    if i % 10 == 0:
        df_test.to_excel("df_test.xlsx", index=False)
        print("df_test.xlsx 중간 저장됨")
        print(f"{i} / {test_len}번역됨")
df_test.to_excel("df_test.xlsx", index=False)

"""

translated_dataset = DatasetDict({
  "train": Dataset.from_pandas(df_train),
  "valid": Dataset.from_pandas(df_validation),
  "test": Dataset.from_pandas(df_test)
})

train_data_translated = translated_dataset['train']
validation_data_translated = translated_dataset['valid']
test_data_translated = translated_dataset['test']




id_to_label = {0:'부정', 1:'긍정'}
question_template = "### Human: 다음 문장의 긍정, 부정 여부를 판단하세요"

## 리뷰의 Title과 콘텐츠를 가지고 학습
train_instructions = [f'{question_template}\n제목: {x}\n내용: {y}\n\n### 판단: {id_to_label[z]}' for x,y,z in zip(train_data['title'],train_data['content'],train_data['label'])]
validation_instructions = [f'{question_template}\n제목: {x}\n내용: {y}\n\n### 판단: {id_to_label[z]}' for x,y,z in zip(validation_data['title'],validation_data['content'],validation_data['label'])]

ds_train = Dataset.from_dict({"text": train_instructions})
ds_validation = Dataset.from_dict({"text": validation_instructions})
instructions_ds_dict = DatasetDict({"train": ds_train, "eval": ds_validation})
#원본 데이터셋 0번 데이터 출력
print(instructions_ds_dict['train']['text'][0])
#원본 데이터셋 구조 출력
print(subset_dataset)




question_template = "### Human: 다음 문장의 긍정, 부정 여부를 판단하세요"

## 리뷰의 Title과 콘텐츠를 가지고 학습
train_instructions = [f'{question_template}\n제목: {x}\n내용: {y}\n\n### 판단: {id_to_label[z]}' for x,y,z in zip(train_data_translated['title'],train_data_translated['content'],train_data_translated['label'])]
validation_instructions = [f'{question_template}\n제목: {x}\n내용: {y}\n\n### 판단: {id_to_label[z]}' for x,y,z in zip(validation_data_translated['title'],validation_data_translated['content'],validation_data_translated['label'])]

## 리뷰의 Title만 가지고 학습
##train_instructions = [f'{question_template}\ntitle: {x}\n\n### Assistant: {id_to_label[z]}' for x,z in zip(train_data['title'],train_data['label'])]
##validation_instructions = [f'{question_template}\ntitle: {x}\n\n### Assistant: {id_to_label[z]}' for x,z in zip(validation_data['title'],validation_data['label'])]

ds_train = Dataset.from_dict({"text": train_instructions})
ds_validation = Dataset.from_dict({"text": validation_instructions})
instructions_ds_dict = DatasetDict({"train": ds_train, "eval": ds_validation})
#번역 데이터셋 0번 데이터 출력
print(instructions_ds_dict['train']['text'][0])
#번역 데이터셋 구조 출력
print(translated_dataset)
#번역 데이터셋 파일로 저장
translated_dataset.save_to_disk("translated_dataset")