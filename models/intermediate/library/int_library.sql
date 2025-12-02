with sp as (
    select *
    from {{ ref('int_spotify') }}
),

yt as (
    select *
    from {{ ref('int_ytmusic') }}
),

-- EXPLODE GENRES INTO ROWS (ROBUST VERSION)
exploded as (
    select
        sp.*,
        split_genre as raw_genre
    from sp,
    unnest(split(coalesce(genres, ''), ',')) as split_genre
),

-- JOIN GENRE LOOKUP
genre_join as (
    select
        e.*,
        gl.main_genre,
        gl.sub_genre
    from exploded e
    left join {{ source('ytmusic_raw', 'genre_lookup') }} gl
        on trim(lower(e.raw_genre)) = trim(lower(gl.spotify_raw_genre))
),

-- GROUP BY TRACK
grouped as (
    select
        track_id,
        title_clean,
        artist_clean,
        album_clean,
        title_original,
        artist_original,
        album_original,
        duration_ms,
        popularity,
        extraction_date,
        array_agg(distinct main_genre ignore nulls)[safe_offset(0)] as main_genre,
        array_agg(distinct sub_genre ignore nulls)[safe_offset(0)] as sub_genre,
        array_agg(distinct raw_genre ignore nulls) as raw_genres
    from genre_join
    group by
        track_id,
        title_clean,
        artist_clean,
        album_clean,
        title_original,
        artist_original,
        album_original,
        duration_ms,
        popularity,
        extraction_date
),

-- JOIN WITH YT MUSIC METADATA
final_join as (
    select
        g.*,
        yt.ytm_url
    from grouped g
    left join yt
        on g.track_id = yt.track_id
)

select
    track_id,
    title_clean  as title,
    artist_clean as artist,
    album_clean  as album,
    duration_ms,
    popularity,
    extraction_date,
    ytm_url,
    main_genre,
    sub_genre,
    array_to_string(raw_genres, ', ') as all_genres
from final_join
