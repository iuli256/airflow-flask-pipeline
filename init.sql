DROP TABLE IF EXISTS public.data_feed;

CREATE TABLE public.data_feed (
    id             bigserial     NOT NULL,
    url            varchar(256)  NULL,
    process_start  timestamp     NULL,
    process_end    timestamp     NULL,
    status         varchar(256)  NULL,
    CONSTRAINT data_feed_pkey PRIMARY KEY (id)
);

INSERT INTO public.data_feed

(url, status)

VALUES

('https://data.openaddresses.io/runs/1026530/es/25829.zip', '0'),
('https://data.openaddresses.io/runs/1026274/es/25830.zip', '0'),
('https://data.openaddresses.io/runs/1026594/es/25831.zip', '0'),
('https://data.openaddresses.io/runs/1024515/es/32628.zip', '0');
