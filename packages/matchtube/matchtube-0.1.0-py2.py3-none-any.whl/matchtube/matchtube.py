import pafy

term = 'everybody'
api_key = 'AIzaSyDHTKjtUchUxUOzCtYW4V_h1zzcyd0P6c0'

# CONTENT_TYPE:
# channel, playlist, video

# DURATION:
# any, long, medium, short

# ORDER:
# date, rating, relevance, title, videocount, viewcount


def search_results(term, api_key, content, results, category, duration, order):
    query = {
        'part'            : 'id',
        'safeSearch'      : 'none',
        'maxResults'      : results,
        'type'            : content,
        'key'             : api_key,
        'videoCategoryId' : category,
        'videoDuration'   : duration,
        'q'               : term,
        'order'           : order
    }

    search = pafy.call_gdata('search', query)
    return search


def video_results(video_ids, api_key):
    query = {
        'id'   : ','.join(video_ids),
        'part' : 'snippet,statistics,contentDetails',
        'key'  : api_key,
    }

    videos = pafy.call_gdata('videos', query)
    return videos


def fetch(term, content='video', results=50, category=10, duration='any', order='relevance', api_key=api_key):
    search = search_results(term, api_key, content, results, category, duration, order)
    video_ids = [video['id']['videoId'] for video in search['items']]
    results = video_results(video_ids, api_key)
    return results['items']


# results = fetch(term)
# [print('{0}{1}'.format(x, '\n')) for x in results]
