import re

def get_albums(service):
    """Returns a list of albums from Google Photos."""
    albums = []
    next_page_token = ''

    while next_page_token is not None:
        results = service.albums().list(pageSize=50, pageToken=next_page_token).execute()
        albums.extend(results.get('albums', []))
        next_page_token = results.get('nextPageToken')

    return albums


def filter_albums_by_name(albums):
    """Filters albums whose name matches 'ChyllaXXXX' or 'Chylla XXXX' pattern."""
    pattern = re.compile(r'Chylla\s?\d{4}')
    filtered_albums = [album for album in albums if pattern.match(album['title'])]
    return filtered_albums


def get_photo_count(service, album_id):
    """Returns the number of photos in a given album."""
    photo_count = 0
    next_page_token = ''

    while next_page_token is not None:
        results = service.mediaItems().search(
            body={'albumId': album_id, 'pageSize': 100, 'pageToken': next_page_token}).execute()
        photo_count += len(results.get('mediaItems', []))
        next_page_token = results.get('nextPageToken')

    return photo_count