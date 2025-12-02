with source as (
    select *
    from {{ source('ytmusic_raw', 'raw_spotify_library') }}
),

renamed as (
    select
        spotify_track_id,
        source_track_id as track_id,
        title_original,
        artist_original,
        album_original,
        lower(trim(title_original))  as title_clean,
        lower(trim(artist_original)) as artist_clean,
        lower(trim(album_original))  as album_clean,
        duration_ms,
        popularity,
        genres,
        extraction_date,
        release_year
    from source
)

select * from renamed
