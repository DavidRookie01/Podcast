from django.http import JsonResponse, HttpResponse
from django.shortcuts  import render
import modules.database_utils as du
import ast
import re

def loadmain(request):
    return render(request, "myapp/podcast.html")

def load_podcast(request):
    con, cursor = du.db_connect('postgres')
    cursor.execute("select twgt.title, twgt.series_name from public.keywords_bert kb join public.transcripts_w_grouping_temp twgt using (podcast_id)")
    podcasts = cursor.fetchall()
    con.close()
    return JsonResponse({'podcasts': podcasts})

def searchPodcasts(request):
    query = request.GET.get('query')
    mode = request.GET.get('mode')
    print(mode)
    print(query)
    if query == None or query == '':
        mode = 'Podcast Name'
    con, cursor = du.db_connect('postgres')
    query = '%' + query + '%'
    if mode == 'Podcast Name':
        cursor.execute("select twgt.title, twgt.series_name from public.keywords_bert kb join public.transcripts_w_grouping_temp twgt using (podcast_id) where twgt.title ilike %s", [query])
    if mode == 'Keywords':
        cursor.execute("select twgt.title, twgt.series_name from public.keywords_bert kb join public.transcripts_w_grouping_temp twgt using (podcast_id) where twgt.keywords ilike %s", [query])
    if mode == 'Transcipts':
        cursor.execute("select twgt.title, twgt.series_name from public.keywords_bert kb join public.transcripts_w_grouping_temp twgt using (podcast_id) where twgt.machine_summary ilike %s", [query])
    podcasts = cursor.fetchall()
    print(podcasts)
    con.close()
    return JsonResponse({'podcasts': podcasts})

def load_result(request):
    podcast_name = request.GET.get("podcast_name")
    episode_name = request.GET.get("episode_name")
    con, cursor = du.db_connect('postgres')
    cursor.execute("select twgt.title, twgt.series_name, twgt.machine_summary, kb.keywords_bert from public.keywords_bert kb join public.transcripts_w_grouping_temp twgt using (podcast_id) where twgt.title = %s and twgt.series_name = %s", [podcast_name, episode_name])
    result = cursor.fetchone()
    query = """
        WITH OverlapCounts AS (
            SELECT 
                t2.podcast_id AS recommended_podcast_id,
                t2.title AS recommended_title,
                t2.series_name AS recommended_series_name,
                t2.date AS recommended_date,
                (
                    (t1.feature_group_1 = 1 AND t2.feature_group_1 = 1)::int +
                    (t1.feature_group_2 = 1 AND t2.feature_group_2 = 1)::int +
                    (t1.feature_group_3 = 1 AND t2.feature_group_3 = 1)::int +
                    (t1.feature_group_4 = 1 AND t2.feature_group_4 = 1)::int +
                    (t1.feature_group_5 = 1 AND t2.feature_group_5 = 1)::int +
                    (t1.feature_group_6 = 1 AND t2.feature_group_6 = 1)::int +
                    (t1.feature_group_7 = 1 AND t2.feature_group_7 = 1)::int +
                    (t1.feature_group_8 = 1 AND t2.feature_group_8 = 1)::int +
                    (t1.feature_group_9 = 1 AND t2.feature_group_9 = 1)::int +
                    (t1.feature_group_10 = 1 AND t2.feature_group_10 = 1)::int
                ) AS overlap_count
            FROM 
                public.keywords_bert kb1
            JOIN 
                public.transcripts_w_grouping_temp t1 
            ON kb1.podcast_id = t1.podcast_id
            CROSS JOIN 
                public.keywords_bert kb2
            JOIN 
                public.transcripts_w_grouping_temp t2 
            ON kb2.podcast_id = t2.podcast_id
            WHERE 
                t1.title = %s 
                AND t1.series_name = %s 
                AND t1.podcast_id != t2.podcast_id
        ),
        FilteredRecommendations AS (
            SELECT recommended_title as podcast_name, recommended_series_name as series_name, recommended_date as date, overlap_count as overlap_count
            FROM OverlapCounts
            WHERE overlap_count > 0
            ORDER BY overlap_count DESC, recommended_date DESC
            LIMIT 10
        )
        SELECT *
        FROM FilteredRecommendations;
    """

    cursor.execute(query, [podcast_name, episode_name])
    recommendations = cursor.fetchall()
    print(recommendations)
    # human_summary, human_sentiment, human_keywords, machine_summaries, sentiments_summary, keywords_data_Tf_IDF, keywords_data_Bertopic = result[2], result[3], result[4], result[5], result[6], result[7], result[8]
    # human_keywords = human_keywords[10:]
    # human_sentiment = human_sentiment[10:]
    # sentiments = re.findall(r"'Keywords_Sentiments_raw':\s*array\(\[(.*?)\], dtype=object\)", keywords_data_Tf_IDF)
    # keywords = re.findall(r"'Keywords_raw':\s*array\(\[(.*?)\], dtype=object\)", keywords_data_Tf_IDF)
    # print(keywords)
    # sentiments_list = [s.strip(" '") for s in sentiments[0].split(',')]
    # keywords_list = [k.strip(" '") for k in keywords[0].split(',')]
    # keywords_data_Tf_IDF = ', '.join(f"{keyword}:{sentiment}" for keyword, sentiment in zip(keywords_list, sentiments_list))
    
    # sentiments = re.findall(r"'Keywords_Sentiments_raw':\s*array\(\[(.*?)\], dtype=object\)", keywords_data_Bertopic)
    # keywords = re.findall(r"'Keywords_raw':\s*array\(\[(.*?)\], dtype=object\)", keywords_data_Bertopic)
    # sentiments_list = [s.strip(" '") for s in sentiments[0].split(',')]
    # keywords_list = [k.strip(" '") for k in keywords[0].split(',')]
    # keywords_data_Bertopic = ', '.join(f"{keyword}:{sentiment}" for keyword, sentiment in zip(keywords_list, sentiments_list))
    # keywords_data_Tf_IDF = ast.literal_eval(keywords_data_Tf_IDF)
    # keywords_data_Bertopic = ast.literal_eval(keywords_data_Bertopic)
    # keywords_data_Tf_IDF = ', '.join(f"{keyword}:{sentiment}" for keyword, sentiment in zip(keywords_data_Tf_IDF['Keywords_raw'], keywords_data_Tf_IDF['Keywords_Sentiments_raw']))
    # keywords_data_Bertopic = ', '.join(f"{keyword}:{sentiment}" for keyword, sentiment in zip(keywords_data_Bertopic['Keywords_raw'], keywords_data_Bertopic['Keywords_Sentiments_raw']))
    print(result)
    con.close()
    return JsonResponse({'result': result, 'recommendations': recommendations})


    
    