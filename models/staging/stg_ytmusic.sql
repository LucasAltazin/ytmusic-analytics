with source as (
    select *
    from {{ source('ytmusic_raw', 'raw_library') }}
),

renamed as (
    select
        track_id,
        title as track_title,
        artist,
        album,
        duration_seconds,
        liked,
        ytm_url,
        extraction_date,
        source
    from source
)

select * from renamed
