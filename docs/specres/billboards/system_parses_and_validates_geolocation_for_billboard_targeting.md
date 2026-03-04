---
id: "01KJVM3FKT43WXVQCRJFZ2V12N"
name: "system_parses_and_validates_geolocation_for_billboard_targeting"
status: "stable"
last_verified: "2026-03-04"
---

## Related Files

- `app/models/geolocation.rb`
- `app/validators/enabled_countries_hash_validator.rb`
- `spec/models/geolocation_spec.rb` (Test)

## Functional Overview

The `Geolocation` model represents a geographic location as a country code optionally paired with a region code, and enforces that billboard targeting only uses administrator-configured enabled countries and their valid subdivisions. It supports two string formats: ISO 3166-2 (hyphen-separated, e.g., `US-WA`) and PostgreSQL ltree (dot-separated, e.g., `US.WA`), with class-level factory methods to parse each format and gracefully handle nil, blank, or already-parsed inputs. Validation checks that the country appears in the `billboard_enabled_countries` settings hash and that the region, when provided, belongs to that country according to ISO 3166 data. A separate targeting validation context additionally rejects region codes when the country's settings entry is `:without_regions`. The companion `EnabledCountriesHashValidator` validates the shape of that settings hash itself, requiring it to be a non-empty Hash whose keys are valid ISO 3166 country codes and whose values are either `:with_regions` or `:without_regions`.

## Design Intent

Two validation contexts are used deliberately: the default context allows region codes on any enabled country (needed to support querying stored ltree values), while the `:targeting` context applies the stricter `:with_regions` / `:without_regions` gate so that ad authors cannot target sub-national regions in countries where that capability is disabled. The ltree format is chosen for PostgreSQL's native `ltree` extension, enabling efficient prefix matching queries against stored targeting arrays.

## Key Members

- `country_code` — ISO 3166-1 alpha-2 string, required; validated against `Settings::General.billboard_enabled_countries` keys.
- `region_code` — ISO 3166-2 subdivision string, optional; validated as belonging to `country_code` when present.
- `DEFAULT_ENABLED_COUNTRIES` — fallback hash enabling the United States and Canada with `:with_regions`.
- `ArrayType` — `ActiveRecord::Type::Value` subclass that casts, serializes, and deserializes arrays of `Geolocation` objects to/from PostgreSQL ltree arrays.
- `VALID_HASH_VALUES` (`EnabledCountriesHashValidator`) — the two permitted symbol values (`:with_regions`, `:without_regions`) for the enabled countries settings hash.

## Scenarios

### Parsing a geolocation from ISO 3166-2 format

1. Caller passes a hyphen-separated string such as `"US-WA"` to `Geolocation.from_iso3166`.
2. The system splits the string on the hyphen and constructs a `Geolocation` with the country code and region code.
3. Blank or nil input returns nil; an already-parsed `Geolocation` object is returned as-is.

### Parsing a geolocation from PostgreSQL ltree format

1. Caller passes a dot-separated string such as `"CA.NL"` to `Geolocation.from_ltree`.
2. The system splits on the dot and constructs a `Geolocation` with the country code and region code.
3. The same edge cases (nil, blank, existing instance) are handled identically to ISO 3166 parsing.

### Validating that a country is enabled for billboard targeting

1. A `Geolocation` is constructed with a country code.
2. On validation, the system checks whether the country code appears as a key in `Settings::General.billboard_enabled_countries`.
3. Country codes absent from that hash (including unrecognised codes) cause the geolocation to be invalid.

### Validating that a region belongs to its country

1. A `Geolocation` is constructed with both a country code and a region code.
2. On validation, the system verifies the region code is a recognised subdivision of the given country via ISO 3166 data.
3. A region code from a different country (e.g., a Canadian province on a US country code) makes the geolocation invalid.
4. Omitting the region code is always permitted.

### Rejecting region targeting when the country disallows it

1. A `Geolocation` with a region code is validated under the `:targeting` context.
2. If the country's entry in `billboard_enabled_countries` is `:without_regions`, the system adds a validation error on `region_code`.
3. If the entry is `:with_regions`, the geolocation remains valid in the targeting context.

## Failures / Exceptions

- Country code not in `billboard_enabled_countries` keys: adds an inclusion error on `country_code`.
- Region code not a valid subdivision of the given country: adds an inclusion error on `region_code`.
- Region code provided on a `:without_regions` country in the `:targeting` context: adds a descriptive error on `region_code`.
- `EnabledCountriesHashValidator` — blank or non-Hash value: adds the `is_blank` i18n error; invalid country code key: adds `invalid_key` error; invalid value symbol: adds `invalid_value` error.
