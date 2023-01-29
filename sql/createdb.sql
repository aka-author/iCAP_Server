create table log_records (
    uuid                uuid default gen_random_uuid() not null primary key,
    session_id          varchar,
    writer_name         varchar not null,
    record_type         varchar,
    wording             varchar,
    details             varchar,
    created_at          timestamp not null default now(),
    updated_at          timestamp not null default now(),
    deleted_at          timestamp
);

create index log_records__writer_name__idx on log_records (writer_name);
create index log_records__created_at__idx on log_records (created_at);


create table users (
    uuid                uuid not null primary key,
    username            varchar not null,
    password_hash       varchar,
    auth_required       boolean not null default true, 
    configuring_system  boolean not null default false,
    saving_measurements boolean not null default false,
    fetching_reports    boolean not null default false,
    details             varchar,
    created_at          timestamp not null default now(),
    updated_at          timestamp not null default now(),
    deleted_at          timestamp
);


create table user_sessions
(
    uuid                uuid not null primary key,
    user_uuid           uuid references users,
    username_deb        varchar,
    host                varchar,
    opened_at           timestamp not null default now(),
    expire_at           timestamp not null default now(),
    closed_at           timestamp
)

create index user_sessions__expire_at__idx on user_sessions (expire_at);
create index user_sessions__closed_at__idx on user_sessions (closed_at);


create table touchpoints (
    uuid                uuid default gen_random_uuid() not null primary key,
    tpoint_name         varchar not null,
    details             varchar,
    created_at          timestamp not null default now(),
    updated_at          timestamp not null default now(),
    deleted_at          timestamp
);

create unique index touchpoints__tpoint_name__idx on touchpoints (tpoint_name);


create table shops (
    uuid                uuid default gen_random_uuid() not null primary key, 
    shop_name           varchar not null,
    details             varchar,
    created_at          timestamp not null default now(),
    updated_at          timestamp not null default now(),
    deleted_at          timestamp
);


create table sensors (
    uuid                uuid default gen_random_uuid() not null primary key,
    sensor_id           varchar not null,
    touchpoint_uuid     uuid references touchpoints,
    tpoint_name_deb     varchar,
    details             varchar,
    created_at          timestamp not null default now(),
    updated_at          timestamp not null default now(),
    deleted_at          timestamp
); 

create unique index sensors__sensor_id__idx on sensors (sensor_id);


create type datatype_name as enum ('STRING', 'BIGINT', 'DOUBLE', 'TIMESTAMP', 'TIMESTAMP_TZ', 'BOOLEAN', 'JSON');

create table variables (
    uuid                uuid default gen_random_uuid() not null primary key,
    varname             varchar not null,
    shortcut            varchar,
    shop_uuid           uuid references shops,
    datatype_name       datatype_name not null,
    validate_pattern    varchar,
    parse_format        varchar,
    serialize_format    varchar,
    details             varchar,
    created_at          timestamp not null default now(),
    updated_at          timestamp not null default now(),
    deleted_at          timestamp
);

create unique index variables__varname__idx on variables (varname);


create table measurements (
    uuid                uuid not null primary key,
    accepted_at         timestamp with time zone,
    sensor_uuid         uuid references sensors,
    sensor_id_deb       varchar,
    hashkey             varchar,
    created_at          timestamp not null default now(),
    updated_at          timestamp not null default now(),
    deleted_at          timestamp
);

create unique index measurements__accepted_at__idx on measurements (accepted_at);
create unique index measurements__hashkey__idx on measurements (hashkey);


create type value_subset_code as enum ('ARG', 'OUT');

create table varvalues (
    uuid                uuid default gen_random_uuid() not null primary key,
    measurement_uuid    uuid references measurements,
    variable_uuid       uuid references variables,
    varname_deb         varchar,
    value_subset        value_subset_code not null,       
    serialized_value    varchar,
    created_at          timestamp not null default now(),
    updated_at          timestamp not null default now(),
    deleted_at          timestamp
);


create table models (
    uuid                uuid not null primary key,
    model_name          varchar,
    shop_uuid           uuid references shops,
    shop_name_deb       varchar,
    details             varchar,
    created_at          timestamp not null default now(),
    updated_at          timestamp not null default now(),
    deleted_at          timestamp
);


create table model_params (
    uuid                uuid default gen_random_uuid() not null primary key,
    parname             varchar not null,
    model_uuid          uuid references models,
    base_datatype       base_datatype_code not null,
    mandatory           boolean,
    default_value_str   varchar,
    default_value_bgi   bigint,
    default_value_dbl   double precision,
    default_value_tms   timestamp,
    default_value_boo   boolean,
    default_value_jsn   json,
    details             varchar,
    created_at          timestamp not null default now(),
    updated_at          timestamp not null default now(),
    deleted_at          timestamp
);


create table parvalues (
    uuid                uuid default gen_random_uuid() not null primary key,
    model_uuid          uuid references models,
    model_name_deb      varchar,
    model_param_uuid    uuid references model_params,
    parname_deb         varchar,       
    parsable_value_str  varchar,
    parsable_value_bgi  bigint,
    parsable_value_dbl  double precision,
    parsable_value_tms  timestamp,
    parsable_value_boo  boolean,
    parsable_value_jsn  json,
    created_at          timestamp not null default now(),
    updated_at          timestamp not null default now(),
    deleted_at          timestamp
);

create unique index mmm on parvalues ()