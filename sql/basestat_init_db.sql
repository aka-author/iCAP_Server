/*
    Performer Basestat
*/

create table icap.basestat__actions (
    uuid                        uuid primary key,
    accepted_at                 timestamptz,
    icap__pagereadId            varchar,
    icap__cms__doc__uid         varchar,
    icap__cms__doc__localCode   varchar,
    icap__cms__doc__verno       varchar,
    icap__cms__topic__uid       varchar,
    icap__cms__topic__verno     varchar,
    icap__page__title           varchar,
    icap__page__url             varchar,
    icap__action__code          varchar,
    icap__action__timeOffset    bigint,
    icap__action__message       varchar,
    icap__countryCode           varchar,
    userLangCode                varchar,
    userAgentInfo               varchar,
    userOs                      varchar,
    userBrowser                 varchar
);

create index basestat__actions__accepted_at__idx
    on icap.basestat__actions (accepted_at);

create index basestat__actions__icap_pagereadId__idx
    on icap.basestat__actions (icap__pagereadI);

create index basestat__actions__icap_cms_doc_uid__idx
    on icap.basestat__actions (icap__cms__doc__uid);

create index basestat__actions__icap_cms_doc_localCode__idx
    on icap.basestat__actions (icap__cms__doc__localCode);

create index basestat__actions__icap_cms_doc_verno__idx
    on icap.basestat__actions (icap__cms__doc__verno);

create index basestat__actions__icap_cms_topic_uid__idx
    on icap.basestat__actions (icap__cms__topic__uid);

create index basestat__actions__icap_cms_topic_verno__idx
    on icap.basestat__actions (icap__cms__topic__verno);

create index basestat__actions__icap_action_code__idx
    on icap.basestat__actions (icap__action__code);

create index basestat__actions__icap_countryCode__idx
    on icap.basestat__actions (icap__countryCode);

create index basestat__actions__userLangCode__idx
    on icap.basestat__actions (userLangCode);

create index basestat__actions__userAgentInfo__idx
    on icap.basestat__actions (userAgentInfo);

create index basestat__actions__userOs__idx
    on icap.basestat__actions (userOs);

create index basestat__actions__userBrowser__idx
    on icap.basestat__actions (userBrowser);


create table icap.basestat__topics (
    measurement_uuid            uuid primary key,
    accepted_at                 timestamptz,
    icap__cms__doc__uid         varchar,
    icap__cms__doc__localCode   varchar,
    icap__cms__doc__verno       varchar,
    icap__cms__topic__uid       varchar,
    icap__cms__topic__verno     varchar,
    icap__page__title           varchar,
    icap__page__url             varchar
);

create index basestat__actions__accepted_at__idx
    on icap.basestat__actions (accepted_at);
    
create index basestat__actions__icap_cms_doc_uid__idx
    on basestat__actions (icap__cms__doc__uid);

create index basestat__actions__icap_cms_doc_localCode__idx
    on basestat__actions (icap__cms__doc__localCode);

create index basestat__actions__icap_cms_doc_verno__idx
    on basestat__actions (icap__cms__doc__verno);

create index basestat__actions__icap_cms_topic_uid__idx
    on basestat__actions (icap__cms__topic__uid);

create index basestat__actions__icap_cms_topic_verno__idx
    on basestat__actions (icap__cms__topic__verno);


