{{ config(materialized="table") }}

select
    track_id,
    title,
    artist,
    album,
    ytm_url,
    main_genre,
    sub_genre,
    all_genres,
    duration_ms,
    extraction_date
from {{ ref('int_library') }}
