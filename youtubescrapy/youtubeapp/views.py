from django.shortcuts import render

from django.http import HttpResponse
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from googleapiclient.discovery import build
from youtubeapp import views
from django.test import TestCase
from googleapiclient.discovery import build
from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

# api_key = 'AIzaSyAF94fhY3-ulWP3f2HdGvHXGyw9qHXV_Fs'
# channel_ids = ['UCmyKnNRH0wH-r8I-ceP-dsg','UCxD03AhBg9LWQuJfijnzhhQ','UC-JFyL0zDFOsPMpuWu39rPA','UC16niRr50-MSBwiO3YDb3RA']
# youtube = build('youtube','v3',developerKey=api_key)

# def get_channel_stats(youtube,channel_ids):
#     all_data=[]
#     request = youtube.channels().list(part = 'snippet,contentDetails,statistics',id =','.join(channel_ids))
#     response = request.execute()
#     for i in range(len(response['items'])):
#         data = dict(CHANNEL_NAME = response['items'][i]['snippet']['title'],
#                     SUBSCRIBERS=response['items'][i]['statistics']['subscriberCount'],
#                     VIEWS=response['items'][i]['statistics']['viewCount'],
#                     TOTAL_VIDEOS=response['items'][i]['statistics']['videoCount'],
#                  PLAYLIST=response['items'][i]['contentDetails']['relatedPlaylists']['uploads'])
#         all_data.append(data)
#     return all_data

# channel_statistics=get_channel_stats(youtube,channel_ids)
# channel_data=pd.DataFrame(channel_statistics)
# # print(channel_data)

# playlist_id= channel_data.loc[channel_data['CHANNEL_NAME']=='BBC News','PLAYLIST'].iloc[0]
# # print("-------------PlayList_ID-------------------------")
# # print(playlist_id)

# def get_video_ids(youtube , playlist_id):
#   request =  youtube.playlistItems().list(part='contentDetails',playlistId=playlist_id,maxResults=50)
#   response = request.execute()
#   video_ids=[]
#   for i in range(len(response['items'])):
#     video_ids.append(response['items'][i]['contentDetails']['videoId'])

#   next_page_token=response.get('nextPageToken')
#   more_pages=True

#   while more_pages:
#     if next_page_token is None:
#       more_pages = False
#     else:
#       request =  youtube.playlistItems().list(part='contentDetails',playlistId=playlist_id,maxResults=50,pageToken=next_page_token)
#       response=request.execute()
#       for i in range(len(response['items'])):
#         video_ids.append(response['items'][i]['contentDetails']['videoId'])

#       next_page_token=response.get('nextPageToken')
      
#   return video_ids

# video_ids=get_video_ids(youtube,playlist_id)

# def get_video_details(youtube,video_ids):
#   all_video_stats=[]
#   for i in range(0,len(video_ids),50):
#     request = youtube.videos().list(part="snippet,statistics",id=','.join(video_ids[i:i+50]))
#     response = request.execute()

#     for video in response['items']:
#       video_stats = dict(Title=video['snippet']['title'],
#                          Published_date=video['snippet']['publishedAt'],
#                          Views = video['statistics'].get('viewCount'),
#                          #  Views=video['statistics']['viewCount'],
#                          #Likes=video['statistics']['likeCount'],
#                          Likes = video['statistics'].get('likeCount'),
#                          Favorite=video['statistics']['favoriteCount'],
#                          #Comments=video['statistics']['commentCount'],
#                          Comments = video['statistics'].get('commentCount')
#                          )
#       all_video_stats.append(video_stats)

#   return all_video_stats

# video_details=get_video_details(youtube, video_ids)
# video_data=pd.DataFrame(video_details)
# # print(video_data)

# video_data['Published_date']=pd.to_datetime(video_data['Published_date']).dt.date
# video_data['Views']=pd.to_numeric(video_data['Views'])
# video_data['Likes']=pd.to_numeric(video_data['Likes'])
# video_data['Favorite']=pd.to_numeric(video_data['Favorite'])
# video_data['Comments']=pd.to_numeric(video_data['Comments'])
# top10_videos=video_data.sort_values(by='Views',ascending=False).head(10)
# # print(top10_videos)


# tamil_font = FontProperties(fname='D:\Dhanu\youtubeproject\Lohit_Tamil.ttf')
# ax = sns.barplot(x='Views', y='Title', data=top10_videos)
# ax.set_xticklabels(ax.get_xticklabels(), rotation=20, ha='right', fontproperties=tamil_font)
# plt.tight_layout()
# plt.show()


# def youtube_stats(request):
#     return render(request,'home.html')

from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
from matplotlib.font_manager import FontProperties
import seaborn as sns
import matplotlib.pyplot as plt
from googleapiclient.discovery import build



api_key = 'AIzaSyCijXDCfWL1uJWmmJK_-JANBLUNl-Uone4'
channel_ids =['UC16niRr50-MSBwiO3YDb3RA','UCyn1QFyonOr-NKVtX3gw0vw','UC7cs8q-gJRlGwj4A8OmCmXg','UCWv7vMbMWH4-V0ZXdmDpPBA']
youtube = build('youtube', 'v3', developerKey=api_key)


def youtube_stats(request):
    
    channel_data = get_channel_stats(youtube, channel_ids)

    selected_channel = None
    videos = None
    playlist_id = None  # Initialize playlist_id

    if request.method == 'POST':
        selected_channel = request.POST.get('channel')
        # selected_channel_row = channel_data[channel_data['CHANNEL_NAME'] == selected_channel]
        selected_channel_row = [channel for channel in channel_data if channel['CHANNEL_NAME'] == selected_channel]

        if not selected_channel_row:
            # Handle the case where the selected channel doesn't exist
            playlist_id = None
            video_ids = []
            video_details = []
            videos = []
        else:
            # If the channel exists, get the playlist_id
            playlist_id = selected_channel_row[0]['PLAYLIST']  # Access the first dictionary in the list
            # Rest of your code remains the same
            video_ids = get_video_ids(youtube, playlist_id)
            video_details = get_video_details(youtube, video_ids)
            video_data = pd.DataFrame(video_details)
            video_data['Published_date'] = pd.to_datetime(video_data['Published_date']).dt.date
            video_data['Views'] = pd.to_numeric(video_data['Views'])
            video_data['Likes'] = pd.to_numeric(video_data['Likes'])
            video_data['Favorite'] = pd.to_numeric(video_data['Favorite'])
            video_data['Comments'] = pd.to_numeric(video_data['Comments'])
            videos = video_data.sort_values(by='Views', ascending=False).head(10).to_dict(orient='records')

    return render(request, 'home.html', {
        'channel_data': channel_data,
        'selected_channel': selected_channel,
        'videos': videos,
    })


def get_channel_stats(youtube, channel_ids):
    all_data=[]
    request = youtube.channels().list(part = 'snippet,contentDetails,statistics', id=','.join(channel_ids))
    response = request.execute()
    for i in range(len(response['items'])):
        data = dict(CHANNEL_NAME = response['items'][i]['snippet']['title'],
                    SUBSCRIBERS=response['items'][i]['statistics']['subscriberCount'],
                    VIEWS=response['items'][i]['statistics']['viewCount'],
                    TOTAL_VIDEOS=response['items'][i]['statistics']['videoCount'],
                    PLAYLIST=response['items'][i]['contentDetails']['relatedPlaylists']['uploads'])
        all_data.append(data)
    return all_data

channel_statistics=get_channel_stats(youtube,channel_ids)
channel_data=pd.DataFrame(channel_statistics)
# print(channel_data)

def get_video_details(youtube,video_ids):
  all_video_stats=[]
  for i in range(0,len(video_ids),50):
    request = youtube.videos().list(part="snippet,statistics",id=','.join(video_ids[i:i+50]))
    response = request.execute()

    for video in response['items']:
      video_stats = dict( Title=video['snippet']['title'],
                          Published_date=video['snippet']['publishedAt'],
                          Views = video['statistics'].get('viewCount'),
                          #Views=video['statistics']['viewCount'],
                          #Likes=video['statistics']['likeCount'],
                          Likes = video['statistics'].get('likeCount'),
                          Favorite=video['statistics']['favoriteCount'],
                          #Comments=video['statistics']['commentCount'],
                          Comments = video['statistics'].get('commentCount')
                         )
      test=all_video_stats.append(video_stats)

  return all_video_stats

def get_video_ids(youtube,playlist_id):
    request =  youtube.playlistItems().list(part='contentDetails',playlistId=playlist_id,maxResults=50)
    response = request.execute()
    video_ids=[]
    for i in range(len(response['items'])):
        video_ids.append(response['items'][i]['contentDetails']['videoId'])

    next_page_token=response.get('nextPageToken')
    more_pages=True

    while more_pages:
        if next_page_token is None:
            more_pages = False
        else:
            request =  youtube.playlistItems().list(part='contentDetails',playlistId=playlist_id,maxResults=50,pageToken=next_page_token)
            response=request.execute()
        for i in range(len(response['items'])):
            video_ids.append(response['items'][i]['contentDetails']['videoId'])

        next_page_token=response.get('nextPageToken')
        
    return video_ids







