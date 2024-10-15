import pandas as pd
import re
from auth import authenticate
from photo import get_albums, filter_albums_by_name, get_photo_count
from googleapiclient.discovery import build_from_document


def extract_year(album_name):
    """Extracts the year from an album name that follows the 'ChyllaXXXX' or 'Chylla XXXX' pattern."""
    match = re.search(r'\d{4}', album_name)
    if match:
        return match.group(0)
    return None


def load_photos_service(creds):
    """Loads the Google Photos API service using the discovery document."""
    with open("photoslibrary_v1.json", "r") as f:
        photos_library_doc = f.read()

    service = build_from_document(photos_library_doc, credentials=creds)
    return service


def main():
    # Authenticate and load Google Photos API service
    creds = authenticate()
    service = load_photos_service(creds)
    print('Service ', service)

    # Retrieve and filter albums
    albums = get_albums(service)
    print('Albums: ', len(albums))
    filtered_albums = filter_albums_by_name(albums)
    print('Filtered Albums: ', len(filtered_albums))

    # Prepare data for DataFrame
    data = []
    for album in filtered_albums:
        album_name = album['title']
        album_id = album['id']
        year = extract_year(album_name)
        photo_count = get_photo_count(service, album_id)
        data.append([year, photo_count])
        print(album_name)

    # Create a DataFrame with 'Year' and 'Photo Count' columns
    df = pd.DataFrame(data, columns=['Year', 'Photo Count'])
    df.to_csv('albums_photo_count.csv', index=False)
    print("Data written to albums_photo_count.csv")


if __name__ == '__main__':
    main()
