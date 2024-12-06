from django.http import JsonResponse, HttpResponse
from django.shortcuts  import render
import modules.database_utils as du
import ast
import re

def loadmain(request):
    return render(request, "myapp/podcast.html")

def load_podcast(request):
    con, cursor = du.db_connect('postgres')
    cursor.execute("select title, series_name from public.final_data fd order by feedback DESC NULLs Last")
    podcasts = cursor.fetchall()
    con.close()
    return JsonResponse({'podcasts': podcasts})

def searchPodcasts(request):
    query = request.GET.get('query')
    mode = request.GET.get('mode')
    if query == None or query == '':
        mode = 'Episode Name'
    con, cursor = du.db_connect('postgres')
    query = '%' + query + '%'
    print(query)
    if mode == 'Episode Name':
        cursor.execute("select title, series_name from public.final_data where title ilike %s", [query])
    if mode == 'Keywords':
        cursor.execute("select title, series_name from public.final_data where keywords ilike %s", [query])
    if mode == 'Transcripts':
        cursor.execute("select title, series_name from public.final_data where transcript ilike %s", [query])
    podcasts = cursor.fetchall()
    con.close()
    return JsonResponse({'podcasts': podcasts})

def load_result(request):
    podcast_name = request.GET.get("podcast_name")
    episode_name = request.GET.get("episode_name")
    con, cursor = du.db_connect('postgres')
    cursor.execute("select title, series_name, machine_summary, keywords, sentiments from public.final_data where title = %s and series_name = %s", [podcast_name, episode_name])
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
                    (t1.feature_group_10 = 1 AND t2.feature_group_10 = 1)::int +
                    (t1.feature_group_11 = 1 AND t2.feature_group_11 = 1)::int +
                    (t1.feature_group_12 = 1 AND t2.feature_group_12 = 1)::int +
                    (t1.feature_group_13 = 1 AND t2.feature_group_13 = 1)::int +
                    (t1.feature_group_14 = 1 AND t2.feature_group_14 = 1)::int +
                    (t1.feature_group_15 = 1 AND t2.feature_group_15 = 1)::int +
                    (t1.feature_group_16 = 1 AND t2.feature_group_16 = 1)::int +
                    (t1.feature_group_17 = 1 AND t2.feature_group_17 = 1)::int +
                    (t1.feature_group_18 = 1 AND t2.feature_group_18 = 1)::int +
                    (t1.feature_group_19 = 1 AND t2.feature_group_19 = 1)::int +
                    (t1.feature_group_20 = 1 AND t2.feature_group_20 = 1)::int +
                    (t1.feature_group_21 = 1 AND t2.feature_group_21 = 1)::int
                ) AS overlap_count,
                CONCAT(
					IF((t1.feature_group_1 = 1 AND t2.feature_group_1 = 1) ? t2.feature_word_1+', ' : NULL),
					IF((t1.feature_group_2 = 1 AND t2.feature_group_2 = 1) ? t2.feature_word_2+', ' : NULL),
					IF((t1.feature_group_3 = 1 AND t2.feature_group_3 = 1) ? t2.feature_word_3+', ' : NULL),
					IF((t1.feature_group_4 = 1 AND t2.feature_group_4 = 1) ? t2.feature_word_4+', ' : NULL),
					IF((t1.feature_group_5 = 1 AND t2.feature_group_5 = 1) ? t2.feature_word_5+', ' : NULL),
					IF((t1.feature_group_6 = 1 AND t2.feature_group_6 = 1) ? t2.feature_word_6+', ' : NULL),
					IF((t1.feature_group_7 = 1 AND t2.feature_group_7 = 1) ? t2.feature_word_7+', ' : NULL),
					IF((t1.feature_group_8 = 1 AND t2.feature_group_8 = 1) ? t2.feature_word_8+', ' : NULL),
					IF((t1.feature_group_9 = 1 AND t2.feature_group_9 = 1) ? t2.feature_word_9+', ' : NULL),
					IF((t1.feature_group_10 = 1 AND t2.feature_group_10 = 1) ? t2.feature_word_10+', ' : NULL),
					IF((t1.feature_group_11 = 1 AND t2.feature_group_11 = 1) ? t2.feature_word_11+', ' : NULL),
					IF((t1.feature_group_12 = 1 AND t2.feature_group_12 = 1) ? t2.feature_word_12+', ' : NULL),
					IF((t1.feature_group_13 = 1 AND t2.feature_group_13 = 1) ? t2.feature_word_13+', ' : NULL),
					IF((t1.feature_group_14 = 1 AND t2.feature_group_14 = 1) ? t2.feature_word_14+', ' : NULL),
					IF((t1.feature_group_15 = 1 AND t2.feature_group_15 = 1) ? t2.feature_word_15+', ' : NULL),
					IF((t1.feature_group_16 = 1 AND t2.feature_group_16 = 1) ? t2.feature_word_16+', ' : NULL),
					IF((t1.feature_group_17 = 1 AND t2.feature_group_17 = 1) ? t2.feature_word_17+', ' : NULL),
					IF((t1.feature_group_18 = 1 AND t2.feature_group_18 = 1) ? t2.feature_word_18+', ' : NULL),
					IF((t1.feature_group_19 = 1 AND t2.feature_group_19 = 1) ? t2.feature_word_19+', ' : NULL),
					IF((t1.feature_group_20 = 1 AND t2.feature_group_20 = 1) ? t2.feature_word_20+', ' : NULL),
					IF((t1.feature_group_21 = 1 AND t2.feature_group_21 = 1) ? t2.feature_word_21+', ' : NULL)
                ) AS overlapping_keywords
            FROM public.final_data t1 
            CROSS JOIN 
                public.final_data t2 
            WHERE 
                t1.title = %s
                AND t1.series_name = %s
                AND t1.podcast_id != t2.podcast_id
        ),
        FilteredRecommendations AS (
            SELECT 
                recommended_title AS podcast_name, 
                recommended_series_name AS series_name, 
                recommended_date AS date, 
                overlap_count AS overlap_count, 
                overlapping_keywords
            FROM OverlapCounts
            WHERE overlap_count > 0
            ORDER BY overlap_count DESC, recommended_date DESC
            LIMIT 5
        )
        SELECT *
        FROM FilteredRecommendations;
    """
    cursor.execute(query, [podcast_name, episode_name])
    recommendations = cursor.fetchall()
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
    con.close()
    return JsonResponse({'result': result, 'recommendations': recommendations})

def update_feedback_positive(request):
    podcast_name = request.GET.get("podcast_name")
    episode_name = request.GET.get("episode_name")
    print(episode_name)
    con, cursor = du.db_connect("postgres")
    cursor.execute("update public.final_data set feedback = coalesce(feedback, 0) + 1 where title = %s and series_name = %s", [podcast_name, episode_name])
    con.close()
    return JsonResponse({'msg': 'Thank you for your feedback'})
    
def update_feedback_negative(request):
    podcast_name = request.GET.get("podcast_name")
    episode_name = request.GET.get("episode_name")
    con, cursor = du.db_connect("postgres")
    cursor.execute("update public.final_data set feedback = coalesce(feedback, 0) - 1 where title = %s and series_name = %s", [podcast_name, episode_name])
    cursor.execute("""
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
                ) AS overlap_count,
                ARRAY_REMOVE(
                    ARRAY[
                        CASE WHEN t1.feature_group_1 = 1 AND t2.feature_group_1 = 1 THEN t2.feature_word_1 ELSE NULL END,
                        CASE WHEN t1.feature_group_2 = 1 AND t2.feature_group_2 = 1 THEN t2.feature_word_2 ELSE NULL END,
                        CASE WHEN t1.feature_group_3 = 1 AND t2.feature_group_3 = 1 THEN t2.feature_word_3 ELSE NULL END,
                        CASE WHEN t1.feature_group_4 = 1 AND t2.feature_group_4 = 1 THEN t2.feature_word_4 ELSE NULL END,
                        CASE WHEN t1.feature_group_5 = 1 AND t2.feature_group_5 = 1 THEN t2.feature_word_5 ELSE NULL END,
                        CASE WHEN t1.feature_group_6 = 1 AND t2.feature_group_6 = 1 THEN t2.feature_word_6 ELSE NULL END,
                        CASE WHEN t1.feature_group_7 = 1 AND t2.feature_group_7 = 1 THEN t2.feature_word_7 ELSE NULL END,
                        CASE WHEN t1.feature_group_8 = 1 AND t2.feature_group_8 = 1 THEN t2.feature_word_8 ELSE NULL END,
                        CASE WHEN t1.feature_group_9 = 1 AND t2.feature_group_9 = 1 THEN t2.feature_word_9 ELSE NULL END,
                        CASE WHEN t1.feature_group_10 = 1 AND t2.feature_group_10 = 1 THEN t2.feature_word_10 ELSE NULL END
                    ], NULL
                ) AS overlapping_keywords
            FROM public.final_data t1 
            CROSS JOIN 
                public.final_data t2 
            WHERE 
                t1.title = %s
                AND t1.series_name = %s
                AND t1.podcast_id != t2.podcast_id
        ),
        FilteredRecommendations AS (
            SELECT 
                recommended_title AS podcast_name, 
                recommended_series_name AS series_name, 
                recommended_date AS date, 
                overlap_count AS overlap_count, 
                overlapping_keywords
            FROM OverlapCounts
            WHERE overlap_count > 0
            ORDER BY overlap_count DESC, recommended_date DESC
            LIMIT 10
        )
        SELECT *
        FROM FilteredRecommendations
        OFFSET 5;
        """, [podcast_name, episode_name])
    recommendations = cursor.fetchall()
    return JsonResponse({'msg': 'Thank you for your feedback', 'recommendations': recommendations})


    


    
    