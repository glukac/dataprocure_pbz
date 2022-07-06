CREATE TABLE pbz.raw (
	id uuid NOT NULL,
	raw_type varchar NOT NULL,
	pbz_id int8 NOT NULL,
	"domain" varchar NOT NULL,
	body jsonb NOT NULL,
	created_at timestamp NOT NULL,
	updated_at timestamp NULL,
	CONSTRAINT raw_pk PRIMARY KEY (id)
);

-- pbz.newest_raw_clients source

CREATE OR REPLACE VIEW pbz.newest_raw_clients
AS SELECT DISTINCT ON (r.domain, r.pbz_id) r.id AS raw_id,
    r.raw_type,
    md5(concat(r.domain, '_', r.pbz_id)) AS ipo,
    r.pbz_id,
    r.domain,
    r.body,
    r.created_at
   FROM pbz.raw r
  WHERE r.raw_type::text = 'client'::text
  ORDER BY r.domain, r.pbz_id, r.created_at DESC;


-- pbz.newest_raw_participants source

CREATE OR REPLACE VIEW pbz.newest_raw_participants
AS SELECT DISTINCT ON (r.domain, r.pbz_id) r.id AS raw_id,
    r.raw_type,
    r.body ->> 'organizationId'::text AS ipo,
    r.pbz_id,
    r.domain,
    r.body,
    r.created_at
   FROM pbz.raw r
  WHERE r.raw_type::text = 'participant'::text
  ORDER BY r.domain, r.pbz_id, r.created_at DESC;


-- pbz.newest_raw_client_participant source

CREATE OR REPLACE VIEW pbz.newest_raw_client_participant
AS SELECT DISTINCT ON (r.domain, r.pbz_id) r.id AS raw_id,
    r.domain,
    (r.body ->> 'id'::text)::integer AS participant_pbz_id,
    (r.body ->> 'clientId'::text)::integer AS client_pbz_id,
    r.created_at
   FROM pbz.raw r
  WHERE r.raw_type::text = 'client_participant'::text
  ORDER BY r.domain, r.pbz_id, r.created_at DESC;


-- pbz.newest_raw_auctions source

CREATE OR REPLACE VIEW pbz.newest_raw_auctions
AS SELECT DISTINCT ON (r.domain, r.pbz_id) r.id AS raw_id,
    r.raw_type,
    r.pbz_id,
    r.domain,
    r.body,
    r.created_at
   FROM pbz.raw r
  WHERE r.raw_type::text = 'auction'::text
  ORDER BY r.domain, r.pbz_id, r.created_at DESC;


-- pbz.newest_raw_client_auction source

CREATE OR REPLACE VIEW pbz.newest_raw_client_auction
AS SELECT DISTINCT ON (r.domain, ((r.body -> 'id'::text)::integer)) r.id AS raw_id,
    r.domain,
    r.pbz_id AS client_pbz_id,
    (r.body -> 'id'::text)::integer AS auction_pbz_id,
    r.created_at
   FROM pbz.raw r
  WHERE r.raw_type::text = 'client_auction'::text
  ORDER BY r.domain, ((r.body -> 'id'::text)::integer), r.created_at DESC;


-- pbz.client source

CREATE MATERIALIZED VIEW pbz.client
TABLESPACE pg_default
AS SELECT uuid_generate_v4() AS id,
    nrc.raw_id,
    nrc.ipo,
    nrc.pbz_id AS client_pbz_id,
    nrc.domain,
    nrc.body ->> 'name'::text AS name,
    nrc.body ->> 'street'::text AS street,
    nrc.body ->> 'city'::text AS city,
    nrc.body ->> 'postalCode'::text AS postal_code,
    nrc.body ->> 'phone'::text AS phone,
    nrc.body ->> 'fax'::text AS fax,
    nrc.body ->> 'email'::text AS email,
    nrc.body ->> 'person'::text AS person,
    nrc.body ->> 'timezone'::text AS timezone,
    nrc.body ->> 'countryCode'::text AS country_code,
    nrc.body AS raw_data
   FROM pbz.newest_raw_clients nrc
WITH DATA;


-- pbz.participant source

CREATE MATERIALIZED VIEW pbz.participant
TABLESPACE pg_default
AS SELECT uuid_generate_v4() AS id,
    nrp.raw_id,
    nrp.ipo,
    nrp.pbz_id AS participant_pbz_id,
    nrp.domain,
    nrp.body ->> 'name'::text AS name,
    nrp.body ->> 'language'::text AS language,
    nrp.body ->> 'accessTime'::text AS access_time,
    nrp.body ->> 'person'::text AS person,
    nrp.body ->> 'job'::text AS job,
    nrp.body ->> 'street'::text AS street,
    nrp.body ->> 'city'::text AS city,
    nrp.body ->> 'postalCode'::text AS postal_code,
    nrp.body ->> 'region'::text AS region,
    nrp.body ->> 'countryCode'::text AS country_code,
    nrp.body ->> 'www'::text AS www,
    nrp.body ->> 'taxId'::text AS tax_number,
    nrp.body ->> 'statutoryAuthority'::text AS statutory_authority,
    nrp.body ->> 'email'::text AS email,
    nrp.body AS raw_data
   FROM pbz.newest_raw_participants nrp
WITH DATA;


-- pbz.client_participant source

CREATE MATERIALIZED VIEW pbz.client_participant
TABLESPACE pg_default
AS SELECT DISTINCT nrcp.domain,
    c.client_pbz_id,
    c.ipo AS client_ipo,
    p.participant_pbz_id,
    p.ipo AS participant_ipo
   FROM pbz.newest_raw_client_participant nrcp
     JOIN pbz.client c ON nrcp.domain::text = c.domain::text AND nrcp.client_pbz_id = c.client_pbz_id
     JOIN pbz.participant p ON nrcp.domain::text = p.domain::text AND nrcp.participant_pbz_id = p.participant_pbz_id
WITH DATA;


-- pbz.auction source

CREATE MATERIALIZED VIEW pbz.auction
TABLESPACE pg_default
AS SELECT uuid_generate_v4() AS id,
    nra.raw_id,
    nra.domain,
    nra.pbz_id AS auction_pbz_id,
    nrc.ipo AS client_ipo,
    nrca.client_pbz_id,
    nra.body -> 'name'::text AS name,
    (nra.body ->> 'categoryId'::text)::integer AS category_id,
    (nra.body ->> 'template'::text)::integer AS template_id,
    nra.body ->> 'templateName'::text AS template_name,
    (nra.body -> 'isTemplate'::text)::boolean AS is_template,
    (nra.body -> 'isTesting'::text)::boolean AS is_testing,
    (nra.body -> 'isPublic'::text)::boolean AS is_public,
    (nra.body -> 'isSignatureEnabled'::text)::boolean AS is_signature_enabled,
    nra.body ->> 'type'::text AS type,
    nra.body ->> 'typeSpecification'::text AS type_specification,
    jsonb_array_elements_text(nra.body -> 'languages'::text) AS languages,
    nra.body ->> 'currency'::text AS currency,
    (nra.body ->> 'announcmentTime'::text)::timestamp without time zone AS announcment_time,
    (nra.body ->> 'endTime'::text)::timestamp without time zone AS endtime,
    (nra.body -> 'evaluationMethod'::text)::integer AS evaluation_method,
    (nra.body -> 'precision'::text)::integer AS "precision",
    (nra.body -> 'isSealed'::text)::boolean AS is_sealed,
    nra.body ->> 'commision'::text AS commision,
    nra.body ->> 'person'::text AS person,
    nra.body ->> 'street'::text AS street,
    nra.body ->> 'city'::text AS city,
    nra.body ->> 'postalCode'::text AS postal_code,
    nra.body ->> 'countryCode'::text AS country_code,
    nra.body ->> 'email'::text AS email,
    nra.body ->> 'phone'::text AS phone,
    nra.body ->> 'executor'::text AS executor,
    nra.body ->> 'announcerName'::text AS announcer_name,
    nra.body ->> 'announcerStreet'::text AS announcer_street,
    nra.body ->> 'announcerCity'::text AS announcer_city,
    nra.body ->> 'announcerPostalCode'::text AS announcer_postal_code,
    nra.body ->> 'announcerCountryCode'::text AS announcer_country_code,
    nra.body ->> 'announcerPerson'::text AS announcer_person,
    nra.body ->> 'announcerEmail'::text AS announcer_email,
    nra.body ->> 'announcerPhone'::text AS announcer_phone,
    (nra.body ->> 'comparativePrice'::text)::numeric AS comparative_price,
    (nra.body ->> 'winnerPrice'::text)::numeric AS winner_price,
    (nra.body ->> 'winnerPrice2'::text)::numeric AS winner_price_2,
    (nra.body ->> 'saving'::text)::numeric AS saving,
    (nra.body ->> 'savingPercent'::text)::numeric AS saving_percent,
    (nra.body ->> 'saving2'::text)::numeric AS saving_2,
    (nra.body ->> 'saving2Percent'::text)::numeric AS saving_2_percent,
    (nra.body ->> 'numChanges'::text)::integer AS num_changes,
    (nra.body ->> 'bestPossibleBid'::text)::numeric AS best_possible_bid,
        CASE
            WHEN (nra.body ->> 'bestTotalBid'::text) <> '-'::text THEN nra.body ->> 'bestTotalBid'::text
            ELSE NULL::text
        END::numeric AS best_total_bid,
    (nra.body ->> 'worstTotalBid'::text)::numeric AS worst_total_bid,
    (nra.body ->> 'timeInvitationToEndRound'::text)::numeric AS time_invitation_to_end_round,
    (nra.body ->> 'changeTime'::text)::timestamp without time zone AS change_time,
    nra.body -> 'currencies'::text AS currencies,
    nra.body -> 'items'::text AS items,
    nra.body -> 'rounds'::text AS rounds,
    nra.body -> 'specifications'::text AS specifications
   FROM pbz.newest_raw_auctions nra
     JOIN pbz.newest_raw_client_auction nrca ON nra.domain::text = nrca.domain::text AND nra.pbz_id = nrca.auction_pbz_id
     JOIN pbz.newest_raw_clients nrc ON nrca.domain::text = nrc.domain::text AND nrca.client_pbz_id = nrc.pbz_id
WITH DATA;


-- pbz.auction_participant source

CREATE MATERIALIZED VIEW pbz.auction_participant
TABLESPACE pg_default
AS WITH auction_participants AS (
         SELECT jsonb_array_elements(nra2.body -> 'participants'::text) AS participant,
            nra2.domain,
            nra2.pbz_id AS auction_pbz_id
           FROM pbz.newest_raw_auctions nra2
        )
 SELECT ap.domain,
    (ap.participant -> 'participantId'::text)::numeric AS participant_pbz_id,
    p.ipo AS participant_ipo,
    (ap.participant -> 'isWinner'::text)::boolean AS is_winner,
    ap.auction_pbz_id
   FROM auction_participants ap
     JOIN pbz.participant p ON ap.domain::text = p.domain::text AND (ap.participant -> 'participantId'::text)::numeric = p.participant_pbz_id::numeric
WITH DATA;