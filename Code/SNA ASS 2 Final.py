#!/usr/bin/env python
# coding: utf-8

# In[34]:


from stackapi import StackAPI, StackAPIError
SITE = StackAPI('stackoverflow',key='1m2D1EmsS*nKHGMwKBEAgQ((')
SITE.max_pages=100
SITE.page_size=100
questions = SITE.fetch('questions', sort='votes',tagged='javascript;jquery;html;css;animation')
print("Number of questions fetched: ",len(questions['items']))


# In[108]:


qid = []
for i in (questions['items']):
    qid.append(i['question_id'])
print(len(qid))


# In[109]:


answer = []
for q in qid:
    print(q)
    ans = SITE.fetch('questions/{0}/answers/'.format(q))
    answer.append(ans)
print("Number of Answers fetched: ",len(answer))
# # print((answer[1]))


# In[4]:


def header(file):
    result = []
    if (file == 'allposts'):
        result.append('Tags'); result.append('Asker Reputation'); result.append('Asker Id');result.append('User type')
        result.append('Profile Image');result.append('Asker Name');result.append('Link to Asker')
        result.append('Is Answered'); result.append('View Count'); result.append('Answer Count')
        result.append('Score'); result.append('last_activity_date'); result.append('creation_date');
        result.append('last_edit_date');result.append('Question Id'); result.append('link'); result.append('Title')

        result.append('Answerer reputation'); result.append('Answerer Id'); result.append('Answerer user_type')
        result.append('Answerer accept rate'); result.append('Answerer profile_image'); result.append('Answerer Name')
        result.append('Answerer link'); result.append('Is Accepted'); result.append('Answerer score')
        result.append('last_activity_date'); result.append('last_edit_date'); result.append('creation_date')
        result.append('Answer_id'); result.append('Question_id')
    elif (file == 'meta_data'):
        result.append('User Id');result.append('Post ID');result.append('Post Type');
    #header for ask_ans file
    elif (file == 'ask_ans'):
            result.append('Asker Id');result.append('Answerer Id')
    return(result)


# In[5]:


def extract(file,tsvout):
    final = []
    for i in range(len(questions['items'])):
        for j in range(len(answer[i]['items'])):
            qown = questions['items'][i]['owner']
            aown = answer[i]['items'][j]['owner']
            if qown['user_type'] == 'does_not_exist' or aown['user_type'] == 'does_not_exist':
                continue
            else:    
                out = []
                if (file == 'allposts'):
                    out.append(questions['items'][i]['tags']);out.append(qown['reputation'])
                    out.append(qown['user_id']); out.append(qown['user_type'])
                    if 'profile_image' not in qown:
                        out.append('N/A')
                    else:
                        out.append(qown['profile_image']); 
                    out.append(qown['display_name'])
                    out.append(qown['link']); out.append(questions['items'][i]['is_answered'])
                    out.append(questions['items'][i]['view_count']);
                    out.append(questions['items'][i]['answer_count']);out.append(questions['items'][i]['score'])
                    out.append(questions['items'][i]['last_activity_date']); 
                    out.append(questions['items'][i]['creation_date'])
                    if 'last_edit_date' not in questions['items'][i]:
                        out.append('N/A')
                    else:
                        out.append(questions['items'][i]['last_edit_date'])
                    out.append(questions['items'][i]['question_id']); out.append(questions['items'][i]['link'])
                    out.append(questions['items'][i]['title'])

                    out.append(aown['reputation']); out.append(aown['user_id'])
                    out.append(aown['user_type']); 
                    if 'accept_rate' not in aown:
                        out.append('N/A')
                    else:
                        out.append(aown['accept_rate'])
                    out.append(aown['profile_image']); out.append(aown['display_name'])
                    out.append(aown['link']); out.append(answer[i]['items'][j]['is_accepted'])
                    out.append(answer[i]['items'][j]['score'])
                    out.append(answer[i]['items'][j]['last_activity_date']);
                    if 'last_edit_date' not in answer[i]['items'][j]:
                        out.append('N/A')
                    else:
                        out.append(answer[i]['items'][j]['last_edit_date'])
                    out.append(answer[i]['items'][j]['creation_date']);out.append(answer[i]['items'][j]['answer_id'])
                    out.append(answer[i]['items'][j]['question_id'])
                elif (file == 'ask_ans'):
                    out.append(qown['user_id']); out.append(aown['user_id'])
                elif (file == 'meta_data'):
                    if j == 0:
                        out.append(qown['user_id']); out.append(questions['items'][i]['question_id']);out.append('question')
                        final.append(out)
                    out = []
                    out.append(aown['user_id']); out.append(answer[i]['items'][j]['question_id']);out.append('answer')
                final.append(out)
    return(final)
#                 tsvout.writerow(out)


# In[6]:


def fetch(file,tsvout):
    import csv
    result = header(file);
    tsvout = csv.writer(tsvout, delimiter = '\t')
    #writing header
    tsvout.writerow(result)
    fin_out = extract(file,tsvout)
    for i in fin_out:
        tsvout.writerow(i)
#     print(file)


# In[7]:


def main(file):
    import csv
    #opening and writing the fetched data into out.tsv file
    if file == 'allposts':
        with open('C:/Users/Ravali/Desktop/allposts.tsv', 'w',encoding='utf-8',newline="") as tsvout:
            fetch(file,tsvout)
    elif (file == 'meta_data'):
        with open('C:/Users/Ravali/Desktop/allposts_metadata.tsv', 'w',encoding='utf-8',newline="") as tsvout:
            fetch(file,tsvout)
    elif (file == 'ask_ans'):
        with open('C:/Users/Ravali/Desktop/asker_answerer.tsv', 'w',encoding='utf-8',newline="") as tsvout:
            fetch(file,tsvout)
    
    print('{0}.tsv file generated'.format(file))


# In[8]:


main('allposts')
main('meta_data')
main('ask_ans')


# In[41]:


import pandas as pd
import numpy as np
import copy


# In[76]:


data = pd.read_csv('allposts.tsv',sep='\t')
data = pd.DataFrame(data)
data.head()


# In[77]:


q_id, q_ind = np.unique(data['Question_id'], return_index=True) #unique questions
print(len(q_id))


# In[78]:


data=data.to_dict(orient='list')
dict_temp = {}
for key in data.keys():
    dict_temp[key] = []
#print(dict_temp)


# In[80]:


ABAN={'Asker_Id': [],'Answerer_Id':[]} # 2nd network
CBEN = {'Non_Best_Answerer_Id': [],'Best_Answerer_Id':[]} # 3rd network
# VBEN = {'Low_Vote_Answerer_Id':[],'Top_Vote_Answerer_Id':[],'Weight':[]}

Q_id = np.array(data['Question_id'])

for i in q_id:
    ind_i = np.where(Q_id  == i)
    
    for key in data.keys():
        dict_temp[key]=[]
        for ind_i_j in range(len(ind_i[0])):
            dict_temp[key].append(data[key][ind_i[0][ind_i_j]]) 
            
    #print(len(dict_temp['Answerer Id']) == len(dict_temp['Answerer score']))
    
    #ans_sco_highest = np.argmax(dict_temp['Answerer score']) 
    
    num_max = np.argwhere(dict_temp['Answerer score']==np.amax(dict_temp['Answerer score']))
    for num in range(len(num_max)):

        ans_sco_highest=num_max[num][0]
    
        asker_temp = dict_temp['Asker Id'][ans_sco_highest]

        answerer_temp = dict_temp['Answerer Id'][ans_sco_highest]

        ABAN['Asker_Id'].append(asker_temp)

        ABAN['Answerer_Id'].append(answerer_temp)
    
        if len(dict_temp['Answerer Id']) > 1:#262 questions with more than 1 answer, 240 question with only 1 answer
            
            lower_answer = copy.deepcopy(dict_temp['Answerer Id'])
            
            del lower_answer[ans_sco_highest]
        
            length_non_best = len(lower_answer)
            CBEN['Best_Answerer_Id'].extend([answerer_temp]*length_non_best)
            CBEN['Non_Best_Answerer_Id'].extend(lower_answer)

# print(len(ABAN['Asker_Id'])) 
# print(len(CBEN['Best_Answerer_Id']))
# print(len(CBEN['Non_Best_Answerer_Id']))


# In[112]:


def prune(Asker,Answerer,th):
    all_id =  Asker + Answerer
    length=len(Asker)
    unique_id=np.unique(all_id)
    num_less=[]
    list1=[]
    list2=[]
    for find in unique_id:
        len_temp = [i for i,v in enumerate(all_id) if v==find]
        num_find = len(len_temp)
        if num_find < th:
            num_less.append(find)
    for j in range(length):
        if Asker[j] not in num_less and Answerer[j] not in num_less:
            list1.append(Asker[j])
            list2.append(Answerer[j])
    return list1,list2
def prune2(Asker,Answerer,weight,th):
    all_id =  Asker + Answerer
    length=len(Asker)
    unique_id=np.unique(all_id)
    num_less=[]
    list1=[]
    list2=[]
    list3=[]
    for find in unique_id:
        len_temp = [i for i,v in enumerate(all_id) if v==find]
        num_find = len(len_temp)
        if num_find < th:
            num_less.append(find)
    for j in range(length):
        if Asker[j] not in num_less and Answerer[j] not in num_less:
            list1.append(Asker[j])
            list2.append(Answerer[j])
            list3.append(weight[j])
    return list1,list2,list3


# In[82]:


ARN_df=pd.read_csv('asker_answerer.tsv',sep='\t')
# print(ARN_df['Asker Id'])


# In[118]:


def vben(answerer_id,a_score):
    vben1 = []
    for i in range(len(answerer_id)):
        for j in range(len(a_score)):
            vben_tem = []
            if a_score[i] < a_score[j]:
                vben_tem.append(answerer_id[i])
                vben_tem.append(answerer_id[j])
                vben_tem.append(a_score[j]-a_score[i])
                vben1.append(vben_tem)
            else:
                continue
    return(vben1)
def vben2(answerer_id,asker_id,a_score,q_score):
    for i in range(len(answerer_id)):
        if a_score[i]>q_score:
            vben2=[(asker_id),answerer_id[i],a_score[i]-q_score]
            tsvout.writerow(vben2)
        for j in range(len(a_score)):
            if a_score[i] < a_score[j]:
                vben2=[answerer_id[i],answerer_id[j],a_score[j]-a_score[i]]
                tsvout.writerow(vben2)
            else:
                continue     


# In[119]:


import csv
vben2 =[]
for i in range(len(questions['items'])):
    answerer_id = []
    a_score = []
#     print('length',len(answer[i]['items']))
    for j in range(len(answer[i]['items'])):
        qown = questions['items'][i]['owner']
        aown = answer[i]['items'][j]['owner']
        if qown['user_type'] == 'does_not_exist' or aown['user_type'] == 'does_not_exist':
            continue
        if questions['items'][i]['question_id'] == answer[i]['items'][j]['question_id']:
            q_score = questions['items'][i]['score']
            a_score.append(answer[i]['items'][j]['score'])
            answerer_id.append(aown['user_id'])
    vben2.append(vben(answerer_id,a_score))

output2 = []
for i in vben2:
    for j in i:
        output2.append(j)
# print(output2)
import pandas as pd
vben_df = pd.DataFrame(output2, columns = ['Low Answerer Id','Top Answerer','Weight'])
vben_df.to_csv('4-VBEN.tsv', sep = '\t', index = False)
print('file generated') 


# In[120]:


with open('C:/Users/Ravali/Desktop/vben2.tsv', 'w',encoding='utf-8',newline='') as tsvout:
    tsvout = csv.writer(tsvout, delimiter = '\t')
    header = ['Low voted user','Top Voted user','Weight']
    tsvout.writerow(header)
    for i in range(len(questions['items'])):
            answerer_id = []
            a_score = []
            for j in range(len(answer[i]['items'])):
                qown = questions['items'][i]['owner']
                aown = answer[i]['items'][j]['owner']
                if qown['user_type'] == 'does_not_exist' or aown['user_type'] == 'does_not_exist':
                    continue
                if questions['items'][i]['question_id'] == answer[i]['items'][j]['question_id']:
                    q_score = questions['items'][i]['score']
                    a_score.append(answer[i]['items'][j]['score'])
                answerer_id.append(aown['user_id'])
                asker_id = qown['user_id']
            vben2(answerer_id,asker_id,a_score,q_score)
print('file generated')      
#         break
# print(q_score,a_score)
# print(a_score.index(max(a_score)))
# print(answerer_id)


# In[88]:


vben_df = pd.read_csv('vben.tsv',sep='\t')
vben2_df = pd.read_csv('vben2.tsv',sep='\t')


# In[83]:


ARN_pruned={}
ABAN_pruned={}
CBEN_pruned={}
VBEN_pruned={}
VBEN2_pruned={}

ARN_pruned['Asker_Id'],ARN_pruned['Answerer_Id']=prune(ARN_df['Asker Id'],ARN_df['Answerer Id'],1)
ABAN_pruned['Asker_Id'],ABAN_pruned['Answerer_Id']=prune(ABAN['Asker_Id'],ABAN['Answerer_Id'],3)
CBEN_pruned['Non_Best_Answerer_Id'],CBEN_pruned['Best_Answerer_Id']=prune(CBEN['Non_Best_Answerer_Id'],CBEN['Best_Answerer_Id'],3)
VBEN_pruned['Low Answerer Id'],VBEN_pruned['Top Answerer'],VBEN_pruned['Weight']=prune2(vben_df['Low Answerer Id'],vben_df['Top Answerer'],vben_df['Weight'],3)
VBEN2_pruned['Low voted user'],VBEN2_pruned['Top Voted user'],VBEN2_pruned['Weight']=prune2(vben2_df['Low voted user'],vben2_df['Top Voted user'],vben2_df['Weight'],3)


# In[84]:


network1_pruned= pd.DataFrame(ARN_pruned)
network2_pruned= pd.DataFrame(ABAN_pruned)
network3_pruned= pd.DataFrame(CBEN_pruned)
network4_pruned= pd.DataFrame(VBEN_pruned)
network5_pruned= pd.DataFrame(VBEN2_pruned)

network1_pruned.to_csv('1-ARN_pruned.tsv',sep='\t',index=False)
network2_pruned.to_csv('2-ABAN_pruned.tsv',sep='\t',index=False)
network3_pruned.to_csv('3-CBEN_pruned.tsv',sep='\t',index=False)
network4_pruned.to_csv('4-VBEN_pruned.tsv',sep='\t',index=False)
network5_pruned.to_csv('5-VBEN2_pruned.tsv',sep='\t',index=False)


# In[85]:


# Network without pruning
network2= pd.DataFrame(ABAN)
network3= pd.DataFrame(CBEN)
network2.to_csv('2-ABAN.tsv',sep='\t')
network3.to_csv('3-CBEN.tsv',sep='\t')


# In[121]:


arn_rank = pd.read_csv('ARN_rank.tsv',sep='\t')
aban_rank = pd.read_csv('ABAN_rank.tsv',sep='\t')
cben_rank = pd.read_csv('CBEN_rank.tsv',sep='\t')
vben_rank = pd.read_csv('VBEN_rank.tsv',sep='\t')
vben2_rank = pd.read_csv('VBEN2_rank.tsv',sep='\t')


# In[122]:


arn_rank.columns = arn_rank.columns.str.replace('Unnamed.*', 'Answerer')
aban_rank.columns = arn_rank.columns.str.replace('Unnamed.*', 'Answerer')
cben_rank.columns = arn_rank.columns.str.replace('Unnamed.*', 'Answerer')
vben_rank.columns = arn_rank.columns.str.replace('Unnamed.*', 'Answerer')
vben2_rank.columns = arn_rank.columns.str.replace('Unnamed.*', 'Answerer')


# In[124]:


all_rank = []
for i in range(10):
    all_rank.append(arn_rank['Answerer'][i])
    all_rank.append(aban_rank['Answerer'][i])
    all_rank.append(cben_rank['Answerer'][i])
    all_rank.append(vben_rank['Answerer'][i])
    all_rank.append(vben2_rank['Answerer'][i])
fin_rank = np.unique(all_rank)
print(len(fin_rank))


# In[125]:


data1 = pd.read_csv('allposts.tsv',sep='\t')
data1 = pd.DataFrame(data)
# data1.head()


# In[126]:


five = []
for i in range(len(data['Tags'])):
    for j in range(len(fin_rank)):
        temp_five = []
        if fin_rank[j] == data['Answerer Id'][i]:
            temp_five.append(fin_rank[j])
            temp_five.append(data['Answerer Name'][i])
            temp_five.append(data['Answerer link'][i])
            five.append(temp_five)
        if temp_five == []: 
            if fin_rank[j] == data['Asker Id'][i]:
                temp_five.append(fin_rank[j])
                temp_five.append(data['Asker Name'][i])
                temp_five.append(data['Link to Asker'][i])
                five.append(temp_five)


# In[127]:


unique_five = [list(x) for x in set(tuple(x) for x in five)]


# In[128]:


print(len(unique_five))


# In[129]:


rank_out = []
for i in unique_five:
    temp = []
    temp.append(i[0])
    temp.append(i[1])
    temp.append(i[2])
    arn_r = arn_rank.index[arn_rank['Answerer'] == i[0]].tolist()
    if arn_r == []:
        temp.append('NA')
    else:
        temp.append(arn_r[0]+1)
    aban_r = aban_rank.index[aban_rank['Answerer'] == i[0]].tolist()
    if aban_r == []:
        temp.append('NA')
    else:
        temp.append(aban_r[0]+1)
    cben_r = cben_rank.index[cben_rank['Answerer'] == i[0]].tolist()
    if cben_r == []:
        temp.append('NA')
    else:
        temp.append(cben_r[0]+1)
    vben_r = vben_rank.index[vben_rank['Answerer'] == i[0]].tolist()
    if vben_r == []:
        temp.append('NA')
    else:
        temp.append(vben_r[0]+1)
    vben2_r = vben2_rank.index[vben2_rank['Answerer'] == i[0]].tolist()
    if vben2_r == []:
        temp.append('NA')
    else:
        temp.append(vben2_r[0]+1)
    rank_out.append(temp)
print(len(rank_out))


# In[131]:


final_output = pd.DataFrame(rank_out, columns = ['UserId','Display Name','Profile Link','Rank1ARN','Rank2ABAN','Rank3CBEN','Rank4VBEN','Rank5VBEN2'])
final_output.to_csv('Ranks.tsv', sep = '\t', index = False)

