#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 18:17:51 2018

@author: yuhe
"""

from pandas import DataFrame
import pandas as pd
from numpy.random import randn
import numpy as np
from time import strftime
from datetime import datetime

#read file: artists.dat, user_artists.dat, user_friends.dat, tags.dat, user_taggedartists.dat
artists_df = pd.read_table('artists.dat', sep = '\t')
user_artists_df = pd.read_table('user_artists.dat', sep = '\t')
user_friends_df = pd.read_table('user_friends.dat', sep = '\t')
tags_df = pd.read_table('tags.dat', sep = '\t', encoding = 'Latin1')
taggedartists_df = pd.read_table('user_taggedartists.dat', sep = '\t')

#question 1：
q1 = '1. Who are the top artists in terms of play counts?'
#merge two tables on artistID
user_artists_merge = pd.merge(user_artists_df, artists_df, left_on = 'artistID', right_on = 'id')
artists_weight = user_artists_merge['weight'].groupby(user_artists_merge['artistID']).sum()
# sort and then slice to find the top 10
artists_weight = artists_weight.sort_values(ascending = False)
top_10a_weight = DataFrame(artists_weight[:10])
top_10a_weight = pd.merge(top_10a_weight, artists_df, left_index = True, right_on = 'id')
top_artists_pc = top_10a_weight[['name','weight','id']]
top_artists_pc.index = range(len(top_artists_pc))
print()
print('!'*40)
print()
print(q1)
for i in range(10):
    record = top_artists_pc.loc[i]
    print('%s(%d) %d'%(record['name'], record['id'],record['weight']))


#question 2:
q2 = '2. What artists have the most listeners?'
user_count = user_artists_df.groupby(user_artists_df['artistID'])['userID'].count()
top_10_count = DataFrame(user_count.sort_values(ascending = False)[:10])
top_artists_uc = pd.merge(top_10_count, artists_df, left_index = True, right_on = 'id')[['name','id','userID']]
top_artists_uc = top_artists_uc.rename(columns = {'userID':'userID_count'})
top_artists_uc.index = range(len(top_artists_uc))
print()
print('!'*40)
print()
print(q2)
for i in range(10):
    record = top_artists_uc.loc[i]
    print('%s(%d) %d'%(record['name'], record['id'],record['userID_count']))


#question 3:
q3 = '3. Who are the top users?'
users_weight = user_artists_merge['weight'].groupby(user_artists_merge['userID']).sum()
users_weight = users_weight.reset_index()
top_10u_weight = users_weight.sort_values(by = 'weight', ascending = False)[:10]
top_10u_weight.index = range(len(top_10u_weight))
print()
print('!'*40)
print()
print(q3)
for i in range(10):
    record = top_10u_weight.loc[i]
    print('%d %d'%(record['userID'],record['weight']))


#question 4:
q4 = '4. What artists have the highest average number of plays per listener?'
#total plays for each artist
total_plays = user_artists_df.groupby(user_artists_df['artistID'])['weight'].sum()
#the average is the number of total plays for that artist divided by the number of listenter for that artist
per_user = total_plays/user_count
#round the float number
per_user = np.rint(per_user)
per_user = DataFrame(per_user)
user_count = DataFrame(user_count)
total_plays = DataFrame(total_plays)
#combine total plays, user_count, average
per_artist = pd.merge(total_plays, user_count, left_index = True, right_index = True)
per_artist = pd.merge(per_artist, per_user, left_index = True, right_index = True)
labels = ['total_plays','user_count','plays_per_user']
per_artist.columns = labels
top_10_average = per_artist.sort_values(by='plays_per_user', ascending = False)[:10]
top_10_average = top_10_average.reset_index()
#combine with artist information
top_artists_ua = pd.merge(top_10_average, artists_df, left_on = 'artistID', right_on = 'id')
top_artists_ua = top_artists_ua[['name', 'id', 'total_plays', 'user_count', 'plays_per_user']]
print()
print('!'*40)
print()
print(q4)
for i in range(10):
    record = top_artists_ua.loc[i]
    print('%s(%d) %d %d %d'%(record['name'], record['id'], record['total_plays'], record['user_count'], record['plays_per_user'] ))
    


#question 5:
q5 = '5. What artists with at least 50 listeners have the highest average number of plays per listener?'
#filter out user_count less than 50
per_artist_atleast50 = per_artist[per_artist['user_count'] > 49 ]
top_10_average_50 = per_artist_atleast50.sort_values(by='plays_per_user', ascending = False)[:10]
top_10_average_50 = top_10_average_50.reset_index()
#combine with artist information
top_artists_ua_50 = pd.merge(top_10_average_50, artists_df, left_on = 'artistID', right_on = 'id')
top_artists_ua_50 = top_artists_ua_50[['name', 'id', 'total_plays', 'user_count', 'plays_per_user']]
print()
print('!'*40)
print()
print(q5)
for i in range(10):
    record = top_artists_ua_50.loc[i]
    #record['plays_per_user'] = np.rint(record['plays_per_user'])
    print('%s(%d) %d %d %d'%(record['name'], record['id'], record['total_plays'], record['user_count'], record['plays_per_user'] ))


#question 6:
q6 = '6. Do users with five or more friends listen to more songs?'
friend_count = user_friends_df.groupby(user_friends_df['userID']).count()
friend_count.columns = ['friend_count']
friend_count = friend_count.reset_index()
user_friends_plays = pd.merge(friend_count, users_weight, on = 'userID')

#filter users with more than 5 friends
user_friends_plays_ge5 = user_friends_plays[user_friends_plays['friend_count'] > 4]
#count total plays of users with five or more friends
total_plays_ge5 = user_friends_plays_ge5['weight'].sum()
#count total number of users who have got five or more friends
total_users_ge5 = user_friends_plays_ge5['userID'].count()
#divide total plays by the total number of users
average_plays_ge5 = np.rint(total_plays_ge5/total_users_ge5)

user_friends_plays_lt5 = user_friends_plays[user_friends_plays['friend_count'] < 5]
total_plays_lt5 = user_friends_plays_lt5['weight'].sum()
total_users_lt5 = user_friends_plays_lt5['userID'].count()
average_plays_lt5 = np.rint(total_plays_lt5/total_users_lt5)
print()
print('!'*40)
print()
print(q6)
print('average plays of users with five or more friends: %d'% average_plays_ge5)
print('average plays of users with less than five friends: %d'% average_plays_lt5)


#question 7:
q7 = '7. How similar are two artists?'

def artist_sim(aid1, aid2):
    #find out the name of two artist
    temp = artists_df.set_index('id')
    name_aid1 = temp['name'][aid1]
    name_aid2 = temp['name'][aid2]
    #find out listeners of the two artist
    record_aid1 = user_artists_df[user_artists_df['artistID'] == aid1]
    record_aid2 = user_artists_df[user_artists_df['artistID'] == aid2]
    lis_aid1 = set(record_aid1['userID'])
    lis_aid2 = set(record_aid2['userID'])
    #find out the number of items in the intersection of the two sets
    lis_intersect = len(lis_aid1.intersection(lis_aid2))
    #find out the number of items in the union of the two sets
    lis_union = len(lis_aid1.union(lis_aid2))
    #calculate the Jaccard index
    jaccard_index = float(round((lis_intersect / lis_union),2))
    print('%s, %s, jaccard_index = %.2f'%(name_aid1, name_aid2, jaccard_index))

print()
print('!'*40)
print()
print(q7)
print()
#aid1 = int(input('Please input first artist id: '))
#aid2 = int(input('Please input second artist id: '))

artist_sim(735,562)
artist_sim(735,89)
artist_sim(735,289)
artist_sim(89,289)
artist_sim(89,67)
artist_sim(67,735)



#question 8:
q8 = '8. Analysis of top tagged artists.'
#find out top 10 tagged artists
tag_count = taggedartists_df['tagID'].groupby(taggedartists_df['artistID']).count()
top_10_tag = tag_count.sort_values(ascending = False)[:10]
#find out distint date
date_tag = taggedartists_df['tagID'].groupby([taggedartists_df['year'],taggedartists_df['month']]).count()
result = dict()
for index, item in date_tag.iteritems():
    curr_year = index[0]
    curr_month = index[1]
    tmp = taggedartists_df[taggedartists_df['year'] == curr_year]
    curr = tmp[tmp['month'] == curr_month]
    curr_tag = curr['tagID'].groupby(curr['artistID']).count()
    curr_top10 = curr_tag.sort_values(ascending = False)[:10]
    curr_top10 = set(curr_top10.index)
    result[index] = curr_top10

print()
print('!'*40)
print()
print(q8)
print()

for artist_id, tag_num in top_10_tag.iteritems():
    #find out artist name of certain artistID
    month_in_top10 = 0
    artist_name = artists_df[artists_df.id == artist_id]['name'].values[0]
    #find out the first month in top10
    for date in result:
        if artist_id in result[date]:
            tag_date = date
            break
    #find out the num of months in top10
    for date in result:
        if artist_id in result[date]:
            month_in_top10 += 1    
    
    #convert month number to name
    month_num = list(tag_date)[1]
    year_num = list(tag_date)[0]
    formated_month = datetime(year_num,int(month_num),1)
    selected_month = formated_month.strftime('%b')
    #print out the result
    
    print('%s(%d): num tags = %d'%(artist_name,artist_id, tag_num))
    print('{:<2}'.format(' '), end = '')
    print('first month in top10 = %s %d'%(selected_month, year_num))
    print('{:<2}'.format(' '), end = '')
    print('months in top10 = %d'% month_in_top10)
    print()
