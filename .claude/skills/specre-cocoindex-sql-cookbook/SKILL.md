---
name: specre-cocoindex-sql-cookbook
description: "SQL patterns and cookbook for querying the cocoindex PostgreSQL database during specre domain discovery. Use this skill when executing Phase 1 (Discovery) of the specre-generate-cocoindex workflow. Covers domain isolation patterns, exclusion techniques, sub-domain breakdown, large domain handling, layer classification, tag extraction, complexity ranking, and semantic similarity search."
---

# CocoIndex SQL Cookbook for Domain Discovery

This skill provides SQL patterns and ready-to-use queries for discovering and analyzing domain files in the cocoindex-indexed codebase. All queries target the `codebaseindex__code_embeddings` table.

**Execution method:** All SQL queries use:
```bash
docker exec cocoindex_postgres psql -U cocoindex -d cocoindex_db -c "..."
```

## SQL Pattern Techniques for Domain Isolation

Choose the right pattern operator depending on the precision needed:

| Technique | SQL | Use case |
|---|---|---|
| Simple substring | `filename ILIKE '%tag%'` | Broad match — catches `tag`, `tags`, `tagging`, `tag_adjustment` |
| Word-boundary regex | `filename ~* '(^|/)tags?[_/.]'` | Precise — matches `tag.rb`, `tags_controller.rb` but not `liquid_tag` |
| Multi-keyword AND | `filename ~* 'tag' AND filename ~* 'moderator'` | Intersection — files that involve both concepts |
| Compound exclusion | `AND filename NOT ILIKE '%liquid_tag%'` | Filter out a known sub-domain |
| Directory scoping | `AND (filename LIKE 'app/%' OR filename LIKE 'spec/%')` | Restrict to specific source directories |
| Extension filtering | `AND filename ~ '\.(rb|js|jsx)$'` | Limit to specific file types |

## Common Exclusion Patterns for Large Domains

When a domain keyword appears in multiple qualitatively different sub-domains (e.g., `tag` appears in `tags`, `liquid_tags`, `tag_adjustments`, `tag_moderators`), build exclusions systematically:

```sql
-- Step 1: Identify all sub-domain patterns first
SELECT
  CASE
    WHEN filename ~* 'liquid_tag' THEN 'liquid_tags'
    WHEN filename ~* 'tag_adjustment' THEN 'tag_adjustments'
    WHEN filename ~* 'tag_moderator' THEN 'tag_moderators'
    WHEN filename ~* 'tag_subforem' THEN 'tag_subforem'
    ELSE 'tag_core'
  END AS subdomain,
  COUNT(DISTINCT filename) AS file_count
FROM codebaseindex__code_embeddings
WHERE filename ~* 'tag'
GROUP BY subdomain
ORDER BY file_count DESC;

-- Step 2: Target only the desired sub-domain
SELECT DISTINCT filename
FROM codebaseindex__code_embeddings
WHERE filename ~* '(^|/)tags?[_/.]'
  AND filename NOT ILIKE '%liquid_tag%'
ORDER BY filename;
```

## Handling Very Large Domains (>300 files)

If the initial query returns more than 300 distinct files, do NOT attempt to process the full domain. Instead:

1. Run the sub-domain breakdown query (the Step 1 CASE query above) to identify natural splits.
2. Present the sub-domain split to the user with file counts.
3. Stop execution. The user will run `/specre-generate-cocoindex <sub-domain>` for each independently.

## Ready-to-Use Queries

### A. Domain Discovery with Complex Exclusions

```sql
-- Discover "comment" domain, excluding comments_admin, comment_scoring, etc.
SELECT DISTINCT filename
FROM codebaseindex__code_embeddings
WHERE filename ~* '(^|/)comments?[_/.]'
  AND filename NOT ILIKE '%comments_admin%'
  AND filename NOT ILIKE '%comment_scor%'
  AND filename NOT ILIKE '%comment_subscription%'
ORDER BY filename;
```

### B. Sub-Domain Breakdown for Split Decisions

```sql
-- Identify natural sub-domains within a large domain
SELECT
  CASE
    WHEN filename ~* 'liquid_tag' THEN 'liquid_tags'
    WHEN filename ~* 'tag_adjustment' THEN 'tag_adjustments'
    WHEN filename ~* 'tag_moderator' THEN 'tag_moderators'
    WHEN filename ~* 'tag_subforem' THEN 'tag_subforem'
    ELSE 'tag_core'
  END AS subdomain,
  COUNT(DISTINCT filename) AS file_count,
  COUNT(DISTINCT CASE WHEN filename LIKE 'spec/%' THEN filename END) AS spec_count,
  COUNT(DISTINCT CASE WHEN filename NOT LIKE 'spec/%' THEN filename END) AS src_count
FROM codebaseindex__code_embeddings
WHERE filename ~* 'tag'
GROUP BY subdomain
ORDER BY file_count DESC;
```

### C. Layer Distribution Analysis

```sql
SELECT
  CASE
    WHEN filename LIKE 'app/models/%' THEN 'Models'
    WHEN filename LIKE 'app/controllers/admin/%' THEN 'Admin Controllers'
    WHEN filename LIKE 'app/controllers/api/%' THEN 'API Controllers'
    WHEN filename LIKE 'app/controllers/concerns/%' THEN 'Controller Concerns'
    WHEN filename LIKE 'app/controllers/%' THEN 'Controllers'
    WHEN filename LIKE 'app/services/%' THEN 'Services'
    WHEN filename LIKE 'app/policies/%' THEN 'Policies'
    WHEN filename LIKE 'app/views/%' THEN 'Views'
    WHEN filename LIKE 'app/workers/%' THEN 'Workers'
    WHEN filename LIKE 'app/lib/%' THEN 'Lib'
    WHEN filename LIKE 'app/decorators/%' THEN 'Decorators'
    WHEN filename LIKE 'app/queries/%' THEN 'Queries'
    WHEN filename LIKE 'app/sanitizers/%' THEN 'Sanitizers'
    WHEN filename LIKE 'app/serializers/%' THEN 'Serializers'
    WHEN filename LIKE 'app/uploaders/%' THEN 'Uploaders'
    WHEN filename LIKE 'app/assets/%' OR filename LIKE 'app/javascript/%' THEN 'Frontend (JS/JSX)'
    WHEN filename LIKE 'spec/%' THEN 'Specs'
    ELSE 'Other'
  END AS layer,
  COUNT(DISTINCT filename) AS file_count
FROM codebaseindex__code_embeddings
WHERE <domain_filter>
GROUP BY layer
ORDER BY file_count DESC;
```

### D. Existing @specre Tag Extraction

```sql
SELECT DISTINCT filename,
  (regexp_matches(text, '@specre\s+([A-Z0-9]{26})', 'g'))[1] AS ulid
FROM codebaseindex__code_embeddings
WHERE <domain_filter>
  AND text ~ '@specre\s+[A-Z0-9]{26}';
```

### E. Complexity Ranking by Chunk Count

```sql
SELECT filename, COUNT(*) AS chunks,
  string_agg(DISTINCT language, ', ') AS lang
FROM codebaseindex__code_embeddings
WHERE <domain_filter>
  AND filename NOT LIKE 'spec/%'
GROUP BY filename
ORDER BY chunks DESC
LIMIT 20;
```

### F. Semantic Similarity Search

```sql
-- Find code semantically similar to a given file's first chunk
SELECT filename, LEFT(text, 100) AS preview,
  1 - (embedding <=> (
    SELECT embedding FROM codebaseindex__code_embeddings
    WHERE filename = '<reference_file>'
    ORDER BY location LIMIT 1
  )) AS similarity
FROM codebaseindex__code_embeddings
WHERE filename NOT LIKE 'spec/%'
  AND filename != '<reference_file>'
ORDER BY embedding <=> (
  SELECT embedding FROM codebaseindex__code_embeddings
  WHERE filename = '<reference_file>'
  ORDER BY location LIMIT 1
)
LIMIT 20;
```

**Evaluate relevance:** Not all semantically similar files belong to the target domain. Files with similarity < 0.5 are unlikely to be relevant. Files from clearly different domains (e.g., a user model appearing similar to an article model because both use `acts_as_followable`) should be excluded.

### G. Full Code Text Retrieval for Subagent Context

```sql
SELECT filename, text
FROM codebaseindex__code_embeddings
WHERE filename IN ('<file1>', '<file2>', '<file3>')
ORDER BY filename, location;
```
